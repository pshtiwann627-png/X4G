# telegram_bot.py
# ══════════════════════════════════════════════════════════════════════════════
# ربات مدیریت تلگرام — نسخه‌ی جذاب، طنزآمیز و بدون کرش
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import os
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import httpx

from main import (
    LINKS, SUBS, make_link, remove_link, set_link_active, vless_link_for_link,
    get_host, fmt_bytes, is_link_allowed, logger, PROTOCOLS, DEFAULT_PROTOCOL,
    FINGERPRINTS, DEFAULT_FINGERPRINT, DEFAULT_ALPN_BY_PROTOCOL, DEFAULT_PORT,
    parse_size_to_bytes, parse_speed_to_bytes, create_sub_group, set_link_sub,
    remove_sub_group, MIN_PORT, MAX_PORT
)

# ── تنظیمات اولیه ──────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
_admin_ids_raw = os.environ.get("TELEGRAM_ADMIN_IDS", "").strip()
ADMIN_IDS = {int(x) for x in _admin_ids_raw.replace(" ", "").split(",") if x.isdigit()} if _admin_ids_raw else set()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
PAGE_SIZE = 6
TIMEOUT = 45

_client: Optional[httpx.AsyncClient] = None
_poll_task: Optional[asyncio.Task] = None
_running = False
_pending: Dict[int, Dict] = {}

# ── ابزارهای کمکی ──────────────────────────────────────────────────────────────
PROTOCOL_LABELS = {
    "vless-ws": "VLESS + WebSocket",
    "xhttp-packet-up": "XHTTP (packet-up)",
    "xhttp-stream-up": "XHTTP (stream-up)",
    "xhttp-stream-one": "XHTTP (stream-one)",
}

def _protocol_label(p: str) -> str:
    return PROTOCOL_LABELS.get(p, p)

def _fp_label(fp: str) -> str:
    return fp.capitalize()

_VOLUME_RE = re.compile(r"^([\d.]+)\s*(GB|MB|KB)?$", re.IGNORECASE)
_SPEED_RE = re.compile(r"^([\d.]+)\s*(MBIT|MBPS|MB|KB)?$", re.IGNORECASE)

def _parse_volume_text(text: str) -> Optional[int]:
    m = _VOLUME_RE.match(text.strip())
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    if value <= 0:
        return 0
    unit = (m.group(2) or "GB").upper()
    return parse_size_to_bytes(value, unit)

def _parse_speed_text(text: str) -> Optional[int]:
    m = _SPEED_RE.match(text.strip())
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    if value <= 0:
        return 0
    unit_raw = (m.group(2) or "MBIT").upper()
    unit = "MBIT" if unit_raw in ("MBIT", "MBPS") else unit_raw
    return parse_speed_to_bytes(value, unit)

def _parse_nonneg_int(text: str) -> Optional[int]:
    try:
        n = int(text.strip())
    except ValueError:
        return None
    return max(0, n)

# ── ارتباط با API تلگرام ──────────────────────────────────────────────────────
async def _call(method: str, **params) -> Optional[Dict]:
    if _client is None:
        return None
    try:
        r = await _client.post(f"{API_BASE}/{method}", json=params, timeout=TIMEOUT)
        data = r.json()
        if not data.get("ok"):
            logger.warning(f"Telegram API {method} failed: {data}")
        return data
    except Exception as e:
        logger.warning(f"Telegram API {method} error: {e}")
        return None

async def _send(chat_id: int, text: str, kb: Optional[Dict] = None) -> Optional[Dict]:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if kb:
        payload["reply_markup"] = kb
    return await _call("sendMessage", **payload)

async def _edit(chat_id: int, message_id: int, text: str, kb: Optional[Dict] = None) -> None:
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if kb:
        payload["reply_markup"] = kb
    res = await _call("editMessageText", **payload)
    if res is None or not res.get("ok"):
        await _send(chat_id, text, kb)

async def _answer_cb(cb_id: str, text: str = "") -> None:
    await _call("answerCallbackQuery", callback_query_id=cb_id, text=text)

def _is_admin(chat_id: int) -> bool:
    return chat_id in ADMIN_IDS

# ── کیبوردهای جذاب ──────────────────────────────────────────────────────────
def _main_menu_kb() -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "📋 لیست کانفیگ‌ها", "callback_data": "list:0"}],
            [{"text": "➕ ساخت کانفیگ جدید", "callback_data": "newcfg"}],
            [{"text": "🗂 گروه‌های ساب (لینک حرفه‌ای)", "callback_data": "subs:0"}],
            [{"text": "🔄 رفرش", "callback_data": "menu"}],
        ]
    }

def _links_list_kb(page: int) -> Dict:
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        dot = "🟢" if is_link_allowed(l) else "🔴"
        rows.append([{"text": f"{dot} {l.get('label','?')[:28]}", "callback_data": f"view:{uid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"list:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"list:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "➕ ساخت کانفیگ جدید", "callback_data": "newcfg"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}

def _link_detail_kb(uid: str, active: bool) -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "🔗 نمایش لینک اتصال", "callback_data": f"link:{uid}"}],
            [{"text": "🗂 گروه ساب (لینک حرفه‌ای)", "callback_data": f"cfggroup:{uid}"}],
            [{"text": ("⛔ غیرفعال‌سازی" if active else "✅ فعال‌سازی"), "callback_data": f"toggle:{uid}"}],
            [{"text": "🗑 حذف کانفیگ", "callback_data": f"del:{uid}"}],
            [{"text": "⬅ بازگشت به لیست", "callback_data": "list:0"}],
        ]
    }

def _confirm_delete_kb(uid: str) -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "✅ بله، حذف کن", "callback_data": f"delok:{uid}"},
             {"text": "❌ انصراف", "callback_data": f"view:{uid}"}],
        ]
    }

def _subs_list_kb(page: int) -> Dict:
    items = sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for sid, s in chunk:
        cnt = len(s.get("link_ids", []))
        rows.append([{"text": f"🗂 {s.get('name','?')[:26]} ({cnt})", "callback_data": f"subview:{sid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"subs:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"subs:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "➕ ساخت گروه جدید", "callback_data": "newsub"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}

def _sub_detail_kb(sid: str) -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "➕ افزودن کانفیگ به این گروه", "callback_data": f"subaddlink:{sid}:0"}],
            [{"text": "🗑 حذف گروه", "callback_data": f"subdel:{sid}"}],
            [{"text": "⬅ بازگشت به لیست گروه‌ها", "callback_data": "subs:0"}],
        ]
    }

def _confirm_subdel_kb(sid: str) -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "✅ بله، حذف کن", "callback_data": f"subdelok:{sid}"},
             {"text": "❌ انصراف", "callback_data": f"subview:{sid}"}],
        ]
    }

def _pick_link_for_group_kb(sid: str, page: int) -> Dict:
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        in_this = "✅ " if l.get("sub_id") == sid else ""
        rows.append([{"text": f"{in_this}{l.get('label','?')[:28]}", "callback_data": f"subaddlinkdo:{uid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"subaddlink:{sid}:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"subaddlink:{sid}:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "⬅ بازگشت به گروه", "callback_data": f"subview:{sid}"}])
    return {"inline_keyboard": rows}

def _cfg_group_kb(uid: str) -> Dict:
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        return {
            "inline_keyboard": [
                [{"text": "➖ خارج کردن از گروه", "callback_data": f"cfgungroup:{uid}"}],
                [{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}],
            ]
        }
    rows = []
    for sid2, s in sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)[:8]:
        rows.append([{"text": f"➕ افزودن به «{s.get('name','?')[:24]}»", "callback_data": f"cfgaddgroup:{sid2}"}])
    rows.append([{"text": "🆕 ساخت گروه جدید و افزودن", "callback_data": f"cfgnewgroup:{uid}"}])
    rows.append([{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}])
    return {"inline_keyboard": rows}

# ── ویزارت ساخت کانفیگ (نسخه‌ی جذاب) ──────────────────────────────────────
WIZARD_STEPS = ["label", "protocol", "fingerprint", "alpn", "port", "volume", "speed", "iplimit", "days"]

def _wizard_cancel_kb() -> Dict:
    return {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "w:cancel"}]]}

def _wizard_protocol_kb() -> Dict:
    rows = [[{"text": _protocol_label(p), "callback_data": f"w:proto:{p}"}] for p in PROTOCOLS]
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_fp_kb() -> Dict:
    rows, row = [], []
    for fp in FINGERPRINTS:
        row.append({"text": _fp_label(fp), "callback_data": f"w:fp:{fp}"})
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

ALPN_PRESET_MAP = {"p1": "http/1.1", "p2": "h2,http/1.1", "p3": "h2"}

def _wizard_alpn_kb() -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "🔤 http/1.1 (پیشنهادی)", "callback_data": "w:alpnpreset:p1"}],
            [{"text": "🔤 h2,http/1.1", "callback_data": "w:alpnpreset:p2"}],
            [{"text": "🔤 h2", "callback_data": "w:alpnpreset:p3"}],
            [{"text": "⏭ پیش‌فرض پروتکل", "callback_data": "w:skip:alpn"}],
            [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
        ]
    }

def _wizard_unlimited_kb(step_key: str) -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "♾ نامحدود", "callback_data": f"w:skip:{step_key}"}],
            [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
        ]
    }

def _wizard_confirm_kb() -> Dict:
    return {
        "inline_keyboard": [
            [{"text": "✅ ساخت کانفیگ", "callback_data": "w:confirm"}],
            [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
        ]
    }

# ── پیام‌های جذاب و طنزآمیز ──────────────────────────────────────────────
WIZARD_PROMPTS = {
    "label": "✏️ **اسم/برچسب** کانفیگ رو بفرست:\n\n«اگه اسم قشنگی بذاری، کانفیگ هم بهت عشق می‌کنه 😉»",
    "protocol": "🌐 **پروتکل** رو انتخاب کن:\n\n«VLESS مثل تخت‌خواب راحته، XHTTP مثل ماشین اسپورت! کدومو می‌خوای؟ 🏎️»",
    "fingerprint": "🖐 **Fingerprint** (uTLS) رو انتخاب کن:\n\n«مثل انتخاب کلاه نامرئی برای کانفیگته! کدومو بر می‌داری؟ 🎩»",
    "alpn": "🔤 **ALPN** رو تنظیم کن:\n\n«پروتکل ارتباطی رو مثل انتخاب فیلم شب، با سلیقه انتخاب کن! 🎬»",
    "port": f"🔌 **پورت** رو مشخص کن:\n\n«پورت ۴۴۳ مثل خونه‌ی مادربزرگه، امن و آروم. ولی اگه عاشق ماجراجویی هستی، یه پورت جدید انتخاب کن! 🏠»",
    "volume": "📦 **محدودیت حجم** رو بفرست:\n\n«مثلاً ۱۰GB یا ۵۰۰MB. یادت باشه، هرچی بیشتر بدی، کاربر بیشتر خوشحال می‌شه 🎉»",
    "speed": "🚀 **محدودیت سرعت** رو به Mbps بفرست:\n\n«مثلاً ۲۰ یا ۵۰. اگه نتت قوی‌ه، یه عدد بزرگ بده بچه‌ها ذوق کنن 😎»",
    "iplimit": "👥 **تعداد آی‌پی همزمان** رو بفرست:\n\n«چند نفر می‌تونن همزمان از این کانفیگ استفاده کنن؟ اگه می‌خوای همه‌ی فامیل وصل بشن، بذار نامحدود! 👨‍👩‍👧‍👦»",
    "days": "📅 **روزهای اعتبار** کانفیگ رو بفرست:\n\n«چقدر می‌خوای این کانفیگ نفس بکشه؟ ۳۰ روز عالیه، ۹۰ روز عاشقانه‌ست ♥»"
}

def _wizard_prompt(step: str, data: Dict) -> str:
    n = WIZARD_STEPS.index(step) + 1 if step in WIZARD_STEPS else len(WIZARD_STEPS)
    head = f"🧩 **ساخت کانفیگ جدید — مرحله {n}/{len(WIZARD_STEPS)}**\n\n"
    return head + WIZARD_PROMPTS.get(step, "")

def _wizard_summary(data: Dict) -> str:
    limit = "نامحدود" if not data.get("limit_bytes") else fmt_bytes(data["limit_bytes"])
    speed = "نامحدود" if not data.get("speed_limit_bytes") else f"{data['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    iplim = data.get("ip_limit", 0) or "نامحدود"
    days = data.get("expires_days", 0)
    days_txt = "بدون انقضا" if not days else f"{days} روز"
    proto = data.get("protocol", DEFAULT_PROTOCOL)
    alpn = data.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    return (
        "🧩 **خلاصه‌ی کانفیگ جدید — تایید کن:**\n\n"
        f"برچسب: <b>{data.get('label','?')}</b>\n"
        f"پروتکل: {_protocol_label(proto)}\n"
        f"Fingerprint: {_fp_label(data.get('fingerprint', DEFAULT_FINGERPRINT))}\n"
        f"ALPN: {alpn}\n"
        f"پورت: {data.get('port', DEFAULT_PORT)}\n"
        f"محدودیت حجم: {limit}\n"
        f"محدودیت سرعت: {speed}\n"
        f"محدودیت آی‌پی: {iplim}\n"
        f"انقضا: {days_txt}"
    )

def _format_detail(uid: str, l: Dict) -> str:
    status = "🟢 فعال" if is_link_allowed(l) else "🔴 غیرفعال/منقضی"
    limit = "نامحدود" if not l.get("limit_bytes") else fmt_bytes(l["limit_bytes"])
    speed = "نامحدود" if not l.get("speed_limit_bytes") else f"{l['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    exp = l.get("expires_at")
    exp_txt = exp.split("T")[0] if exp else "بدون انقضا"
    proto = l.get("protocol", DEFAULT_PROTOCOL)
    alpn = l.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    return (
        f"<b>{l.get('label','?')}</b>\n"
        f"وضعیت: {status}\n"
        f"مصرف: {fmt_bytes(l.get('used_bytes',0))} / {limit}\n"
        f"محدودیت سرعت: {speed}\n"
        f"محدودیت آی‌پی: {l.get('ip_limit',0) or 'نامحدود'}\n"
        f"پروتکل: {_protocol_label(proto)}\n"
        f"Fingerprint: {_fp_label(l.get('fingerprint', DEFAULT_FINGERPRINT))}\n"
        f"ALPN: {alpn}\n"
        f"پورت: {l.get('port', DEFAULT_PORT)}\n"
        f"انقضا: {exp_txt}\n"
        f"UUID: <code>{uid}</code>"
    )

def _group_public_url(s: Dict) -> str:
    host = get_host()
    return f"https://{host}/p/{s.get('uuid_key','')}"

def _format_sub_detail(sid: str, s: Dict) -> str:
    cnt = len(s.get("link_ids", []))
    pw = "🔒 دارد" if s.get("password_hash") else "بدون رمز"
    desc = s.get("desc") or "—"
    return (
        f"🗂 <b>{s.get('name','?')}</b>\n"
        f"توضیحات: {desc}\n"
        f"تعداد کانفیگ‌ها: {cnt}\n"
        f"رمز عبور: {pw}\n\n"
        f"🔗 لینک ساب حرفه‌ای:\n<code>{_group_public_url(s)}</code>"
    )

def _format_cfg_group(uid: str) -> str:
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        s = SUBS[sid]
        return (
            f"🗂 کانفیگ «{link.get('label','?')}» توی گروه «{s.get('name','?')}» هست.\n\n"
            f"🔗 لینک ساب حرفه‌ای:\n<code>{_group_public_url(s)}</code>"
        )
    return (
        f"کانفیگ «{link.get('label','?')}» توی هیچ گروهی نیست.\n"
        "برای گرفتن لینک ساب حرفه‌ای، این کانفیگ رو به یک گروه اضافه کن."
    )

# ── مدیریت پیام‌ها و کالبک‌ها ──────────────────────────────────────────────
async def _handle_message(msg: Dict) -> None:
    chat_id = msg.get("chat", {}).get("id")
    text = (msg.get("text") or "").strip()
    if chat_id is None or not _is_admin(chat_id):
        await _send(chat_id, "⛔ شما اجازه‌ی دسترسی ندارید.")
        return

    if text in ("/start", "/menu"):
        _pending.pop(chat_id, None)
        await _send(chat_id, "👋 به ربات مدیریت X4G خوش اومدی.\nاز دکمه‌های زیر برای مدیریت کانفیگ‌ها استفاده کن:", _main_menu_kb())
        return

    if text == "/cancel":
        _pending.pop(chat_id, None)
        await _send(chat_id, "😢 آخی، کانفیگ دلش برای تو تنگ می‌شه. ولی هر وقت خواستی، برمی‌گردیم.", _main_menu_kb())
        return

    pending = _pending.get(chat_id)
    if pending and pending.get("action") == "newsub" and pending.get("step") == "name" and text:
        name = text[:60]
        sid, s = await create_sub_group(name=name)
        link_uid = pending.get("link_uid")
        _pending.pop(chat_id, None)
        if link_uid and link_uid in LINKS:
            await set_link_sub(link_uid, sid)
            await _send(chat_id, f"✅ گروه ساخته شد و کانفیگ اضافه شد.\n\n{_format_cfg_group(link_uid)}", _cfg_group_kb(link_uid))
        else:
            await _send(chat_id, f"✅ گروه ساخته شد.\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if pending and pending.get("action") == "wizard" and text:
        step = pending["step"]
        data = pending["data"]

        if step == "label":
            data["label"] = text[:60] or "کانفیگ جدید"
            pending["step"] = "protocol"
            await _send(chat_id, _wizard_prompt("protocol", data), _wizard_protocol_kb())
            return

        if step in ("protocol", "fingerprint"):
            await _send(chat_id, "لطفاً از دکمه‌ها انتخاب کن 👆", _wizard_protocol_kb() if step == "protocol" else _wizard_fp_kb())
            return

        if step == "alpn":
            data["alpn"] = text.strip()[:100]
            pending["step"] = "port"
            await _send(chat_id, _wizard_prompt("port", data), _wizard_unlimited_kb("port"))
            return

        if step == "port":
            try:
                p = int(text.strip())
            except ValueError:
                p = None
            if p is None or not (MIN_PORT <= p <= MAX_PORT):
                await _send(chat_id, f"❗️ پورت نامعتبر. عددی بین {MIN_PORT} تا {MAX_PORT} بفرست:", _wizard_unlimited_kb("port"))
                return
            data["port"] = p
            pending["step"] = "volume"
            await _send(chat_id, _wizard_prompt("volume", data), _wizard_unlimited_kb("volume"))
            return

        if step == "volume":
            parsed = _parse_volume_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت اشتباه. مثلاً: <code>10GB</code> یا <code>500MB</code>", _wizard_unlimited_kb("volume"))
                return
            data["limit_bytes"] = parsed
            pending["step"] = "speed"
            await _send(chat_id, _wizard_prompt("speed", data), _wizard_unlimited_kb("speed"))
            return

        if step == "speed":
            parsed = _parse_speed_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت اشتباه. یه عدد بفرست، مثلاً <code>20</code>", _wizard_unlimited_kb("speed"))
                return
            data["speed_limit_bytes"] = parsed
            pending["step"] = "iplimit"
            await _send(chat_id, _wizard_prompt("iplimit", data), _wizard_unlimited_kb("iplimit"))
            return

        if step == "iplimit":
            n = _parse_nonneg_int(text)
            if n is None:
                await _send(chat_id, "❗️ یه عدد صحیح بفرست:", _wizard_unlimited_kb("iplimit"))
                return
            data["ip_limit"] = n
            pending["step"] = "days"
            await _send(chat_id, _wizard_prompt("days", data), _wizard_unlimited_kb("days"))
            return

        if step == "days":
            n = _parse_nonneg_int(text)
            if n is None:
                await _send(chat_id, "❗️ یه عدد صحیح بفرست:", _wizard_unlimited_kb("days"))
                return
            data["expires_days"] = n
            pending["step"] = "confirm"
            await _send(chat_id, _wizard_summary(data), _wizard_confirm_kb())
            return

    await _send(chat_id, "از دکمه‌ها استفاده کن:", _main_menu_kb())

async def _handle_callback(cb: Dict) -> None:
    chat_id = cb.get("message", {}).get("chat", {}).get("id")
    message_id = cb.get("message", {}).get("message_id")
    data = cb.get("data", "")
    cb_id = cb.get("id")

    if chat_id is None or not _is_admin(chat_id):
        await _answer_cb(cb_id, "⛔ دسترسی ندارید")
        return
    await _answer_cb(cb_id)

    if data == "menu":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "منوی اصلی:", _main_menu_kb())
        return

    if data.startswith("list:"):
        page = int(data.split(":", 1)[1] or 0)
        if not LINKS:
            await _edit(chat_id, message_id, "هنوز کانفیگی وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"📋 لیست کانفیگ‌ها ({len(LINKS)} مورد):", _links_list_kb(page))
        return

    if data.startswith("subs:"):
        page = int(data.split(":", 1)[1] or 0)
        if not SUBS:
            await _edit(chat_id, message_id, "هنوز گروهی وجود ندارد.", _subs_list_kb(0))
            return
        await _edit(chat_id, message_id, f"🗂 گروه‌های ساب ({len(SUBS)} مورد):", _subs_list_kb(page))
        return

    if data == "newsub":
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": None}
        await _edit(chat_id, message_id, "✏️ اسم گروه رو بفرست:", _wizard_cancel_kb())
        return

    if data.startswith("subview:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "این گروه وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_sub_detail(sid, s), _sub_detail_kb(sid))
        return

    if data.startswith("subaddlink:"):
        _, sid, page_s = data.split(":", 2)
        if sid not in SUBS:
            await _edit(chat_id, message_id, "این گروه وجود ندارد.", _main_menu_kb())
            return
        if not LINKS:
            await _edit(chat_id, message_id, "هیچ کانفیگی وجود ندارد.", _sub_detail_kb(sid))
            return
        _pending[chat_id] = {"action": "subaddlink_ctx", "sid": sid}
        await _edit(chat_id, message_id, "کانفیگ مورد نظر رو انتخاب کن:", _pick_link_for_group_kb(sid, int(page_s or 0)))
        return

    if data.startswith("subaddlinkdo:"):
        uid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        sid = ctx.get("sid") if ctx.get("action") == "subaddlink_ctx" else None
        if not sid or sid not in SUBS:
            await _answer_cb(cb_id, "این عملیات منقضی شده.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "کانفیگ وجود ندارد.")
            return
        _pending.pop(chat_id, None)
        s = SUBS.get(sid)
        await _edit(chat_id, message_id, f"✅ کانفیگ اضافه شد.\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if data.startswith("subdel:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "این گروه وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف «{s.get('name')}» مطمئنی؟", _confirm_subdel_kb(sid))
        return

    if data.startswith("subdelok:"):
        sid = data.split(":", 1)[1]
        name = await remove_sub_group(sid)
        if name is None:
            await _edit(chat_id, message_id, "گروه قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 گروه «{name}» حذف شد.", _main_menu_kb())
        return

    if data.startswith("cfggroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "cfg_group_ctx", "uid": uid}
        await _edit(chat_id, message_id, _format_cfg_group(uid), _cfg_group_kb(uid))
        return

    if data.startswith("cfgungroup:"):
        uid = data.split(":", 1)[1]
        await set_link_sub(uid, None)
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("cfgaddgroup:"):
        sid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        uid = ctx.get("uid") if ctx.get("action") == "cfg_group_ctx" else None
        if not uid or uid not in LINKS:
            await _answer_cb(cb_id, "این عملیات منقضی شده.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "گروه وجود ندارد.")
            return
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, f"✅ کانفیگ به گروه اضافه شد.\n\n{_format_cfg_group(uid)}", _cfg_group_kb(uid))
        return

    if data.startswith("cfgnewgroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": uid}
        await _edit(chat_id, message_id, "✏️ اسم گروه جدید رو بفرست:", _wizard_cancel_kb())
        return

    if data == "newcfg":
        _pending[chat_id] = {"action": "wizard", "step": "label", "data": {}}
        await _edit(chat_id, message_id, _wizard_prompt("label", {}), _wizard_cancel_kb())
        return

    if data == "w:cancel":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "😢 آخی، کانفیگ دلش برای تو تنگ می‌شه. ولی هر وقت خواستی، برمی‌گردیم.", _main_menu_kb())
        return

    if data.startswith("w:"):
        pending = _pending.get(chat_id)
        if not pending or pending.get("action") != "wizard":
            await _edit(chat_id, message_id, "این مرحله معتبر نیست.", _main_menu_kb())
            return

        step = pending["step"]
        wdata = pending["data"]

        if data.startswith("w:proto:") and step == "protocol":
            proto = data.split(":", 2)[2]
            wdata["protocol"] = proto if proto in PROTOCOLS else DEFAULT_PROTOCOL
            pending["step"] = "fingerprint"
            await _edit(chat_id, message_id, _wizard_prompt("fingerprint", wdata), _wizard_fp_kb())
            return

        if data.startswith("w:fp:") and step == "fingerprint":
            fp = data.split(":", 2)[2]
            wdata["fingerprint"] = fp if fp in FINGERPRINTS else DEFAULT_FINGERPRINT
            pending["step"] = "alpn"
            await _edit(chat_id, message_id, _wizard_prompt("alpn", wdata), _wizard_alpn_kb())
            return

        if data.startswith("w:alpnpreset:") and step == "alpn":
            code = data.split(":", 2)[2]
            wdata["alpn"] = ALPN_PRESET_MAP.get(code, "")
            pending["step"] = "port"
            await _edit(chat_id, message_id, _wizard_prompt("port", wdata), _wizard_unlimited_kb("port"))
            return

        if data.startswith("w:skip:") and step in ("alpn", "port", "volume", "speed", "iplimit", "days"):
            key = data.split(":", 2)[2]
            defaults = {
                "alpn": "",
                "port": DEFAULT_PORT,
                "volume": 0,
                "speed": 0,
                "iplimit": 0,
                "days": 0
            }
            if key == "alpn":
                wdata["alpn"] = defaults["alpn"]
                pending["step"] = "port"
            elif key == "port":
                wdata["port"] = defaults["port"]
                pending["step"] = "volume"
            elif key == "volume":
                wdata["limit_bytes"] = defaults["volume"]
                pending["step"] = "speed"
            elif key == "speed":
                wdata["speed_limit_bytes"] = defaults["speed"]
                pending["step"] = "iplimit"
            elif key == "iplimit":
                wdata["ip_limit"] = defaults["iplimit"]
                pending["step"] = "days"
            elif key == "days":
                wdata["expires_days"] = defaults["days"]
                pending["step"] = "confirm"
            await _edit(chat_id, message_id, _wizard_prompt(pending["step"], wdata), _wizard_confirm_kb() if pending["step"] == "confirm" else _wizard_unlimited_kb(pending["step"]))
            return

        if data == "w:confirm" and step == "confirm":
            expires_days = wdata.get("expires_days", 0)
            expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None
            uid, link = await make_link(
                label=wdata.get("label") or "کانفیگ جدید",
                limit_bytes=wdata.get("limit_bytes", 0),
                expires_at=expires_at,
                protocol=wdata.get("protocol", DEFAULT_PROTOCOL),
                fingerprint=wdata.get("fingerprint", DEFAULT_FINGERPRINT),
                alpn=wdata.get("alpn", ""),
                port=wdata.get("port", DEFAULT_PORT),
                ip_limit=wdata.get("ip_limit", 0),
                speed_limit_bytes=wdata.get("speed_limit_bytes", 0),
            )
            _pending.pop(chat_id, None)
            await _edit(chat_id, message_id, f"🎉 تبریک! کانفیگ «{link.get('label')}» با موفقیت متولد شد.\n\n{_format_detail(uid, link)}", _link_detail_kb(uid, link["active"]))
            return

        await _answer_cb(cb_id, "این دکمه معتبر نیست.")
        return

    if data.startswith("view:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("toggle:"):
        uid = data.split(":", 1)[1]
        l = await set_link_active(uid, not LINKS.get(uid, {}).get("active", True))
        if not l:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        status = "فعال" if l["active"] else "غیرفعال"
        await _edit(chat_id, message_id, f"🔄 کانفیگ «{l.get('label')}» حالا مثل چراغ راهنمایی، {status} شد!\n\n{_format_detail(uid, l)}", _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("link:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _answer_cb(cb_id, "کانفیگ وجود ندارد.")
            return
        host = get_host()
        vless = vless_link_for_link(l, uid, host)
        sub_url = f"https://{host}/sub/{uid}"
        msg = f"🔗 لینک اتصال «{l.get('label')}»:\n\n<code>{vless}</code>\n\nلینک ساب ساده:\n<code>{sub_url}</code>"
        sid = l.get("sub_id")
        if sid and sid in SUBS:
            msg += f"\n\n✨ لینک ساب حرفه‌ای:\n<code>{_group_public_url(SUBS[sid])}</code>"
        else:
            msg += "\n\nℹ️ این کانفیگ توی هیچ گروهی نیست."
        await _send(chat_id, msg)
        return

    if data.startswith("del:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "کانفیگ وجود ندارد.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف «{l.get('label')}» مطمئنی؟ این کار مثل پاک کردن تاریخچه‌ی مرورگرته! 😱", _confirm_delete_kb(uid))
        return

    if data.startswith("delok:"):
        uid = data.split(":", 1)[1]
        label = await remove_link(uid)
        if label is None:
            await _edit(chat_id, message_id, "کانفیگ قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 کانفیگ «{label}» با احترام کامل خاکسپاری شد. یادش گرامی! 🕊️", _main_menu_kb())
        return

# ── حلقه‌ی اصلی پولینگ ──────────────────────────────────────────────────────
async def _poll_loop() -> None:
    global _running
    offset = 0
    logger.info(f"🤖 ربات تلگرام شروع به کار کرد (ادمین‌ها: {len(ADMIN_IDS)})")
    while _running:
        try:
            res = await _call("getUpdates", offset=offset, timeout=30, allowed_updates=["message", "callback_query"])
            if not res or not res.get("ok"):
                await asyncio.sleep(3)
                continue
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                try:
                    if "message" in upd:
                        await _handle_message(upd["message"])
                    elif "callback_query" in upd:
                        await _handle_callback(upd["callback_query"])
                except Exception as e:
                    logger.warning(f"خطا در پردازش: {e}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"خطا در حلقه: {e}")
            await asyncio.sleep(3)

# ── مدیریت چرخه‌ی عمر ──────────────────────────────────────────────────────
async def start_bot() -> None:
    global _client, _poll_task, _running
    if not BOT_TOKEN:
        logger.info("ربات تلگرام: توکن تنظیم نشده.")
        return
    if not ADMIN_IDS:
        logger.warning("ربات تلگرام: ADMIN_IDS تنظیم نشده.")
    _client = httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT, connect=10.0))
    _running = True
    _poll_task = asyncio.create_task(_poll_loop())

async def stop_bot() -> None:
    global _running, _client
    _running = False
    if _poll_task:
        _poll_task.cancel()
    if _client:
        await _client.aclose()
        _client = None
