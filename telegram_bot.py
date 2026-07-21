# telegram_bot.py
# ══════════════════════════════════════════════════════════════════════════════
# ربات مدیریت تلگرام — نسخه‌ی بازطراحی‌شده با ظاهر حرفه‌ای و جذاب
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import os
import re

import httpx

from datetime import datetime, timedelta

from main import (
    LINKS,
    make_link,
    remove_link,
    set_link_active,
    vless_link_for_link,
    get_host,
    fmt_bytes,
    is_link_allowed,
    logger,
    PROTOCOLS,
    DEFAULT_PROTOCOL,
    FINGERPRINTS,
    DEFAULT_FINGERPRINT,
    DEFAULT_ALPN_BY_PROTOCOL,
    DEFAULT_PORT,
    DEFAULT_SPEED_LIMIT,
    MIN_PORT,
    MAX_PORT,
    parse_size_to_bytes,
    parse_speed_to_bytes,
    SUBS,
    create_sub_group,
    set_link_sub,
    remove_sub_group,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
_admin_ids_raw = os.environ.get("TELEGRAM_ADMIN_IDS", "").strip()
ADMIN_IDS = {int(x) for x in _admin_ids_raw.replace(" ", "").split(",") if x.isdigit()} if _admin_ids_raw else set()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
PAGE_SIZE = 6

_client: httpx.AsyncClient | None = None
_poll_task: asyncio.Task | None = None
_running = False
_pending: dict = {}

WIZARD_STEPS = ["label", "protocol", "fingerprint", "alpn", "port", "volume", "speed", "iplimit", "days"]

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

def _parse_volume_text(text: str):
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

def _parse_speed_text(text: str):
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

def _parse_nonneg_int(text: str):
    try:
        n = int(text.strip())
    except ValueError:
        return None
    return max(0, n)

# ── فرمت‌کننده‌های زیبا ────────────────────────────────────────────────────
def _header(title: str, icon: str = "📌", sub: str = "") -> str:
    """هدر زیبا برای پیام‌ها"""
    line = "▬" * 28
    if sub:
        return f"{icon} <b>{title}</b>\n{sub}\n{line}"
    return f"{icon} <b>{title}</b>\n{line}"

def _format_date(dt_str: str) -> str:
    """نمایش زیبای تاریخ انقضا"""
    if not dt_str:
        return "♾️ بدون انقضا"
    try:
        dt = datetime.fromisoformat(dt_str)
        now = datetime.now()
        diff = (dt - now).days
        if diff < 0:
            return "⏰ منقضی شده ❌"
        elif diff == 0:
            return "⏰ امروز ⚠️"
        elif diff <= 3:
            return f"⏰ {diff} روز مانده ⚠️"
        elif diff <= 7:
            return f"📅 {dt.strftime('%Y/%m/%d')} ({diff} روز)"
        else:
            return f"📅 {dt.strftime('%Y/%m/%d')} ({diff} روز)"
    except:
        return dt_str

def _format_status(l: dict) -> str:
    """وضعیت کانفیگ با ایموجی"""
    if not l.get("active", True):
        return "🔴 غیرفعال"
    if l.get("expired", False):
        return "🟡 منقضی"
    return "🟢 فعال"

def _format_progress(step: str) -> str:
    """نوار پیشرفت ویزارد"""
    if step not in WIZARD_STEPS:
        return ""
    idx = WIZARD_STEPS.index(step) + 1
    total = len(WIZARD_STEPS)
    filled = "█" * idx
    empty = "░" * (total - idx)
    return f"📊 پیشرفت: {idx}/{total}  [{filled}{empty}]"

def _format_bytes(b: int) -> str:
    """فرمت بایت با ایموجی"""
    if b == 0:
        return "♾️ نامحدود"
    return fmt_bytes(b)

def _format_speed(b: int) -> str:
    """فرمت سرعت با ایموجی"""
    if b == 0:
        return "♾️ نامحدود"
    return f"🚀 {b*8/1024/1024:.1f} Mbps"

def _format_iplimit(n: int) -> str:
    """فرمت محدودیت آی‌پی"""
    if n == 0:
        return "♾️ نامحدود"
    return f"👥 {n} کاربر"

# ── Telegram API helpers ────────────────────────────────────────────────────
async def _call(method: str, **params):
    if _client is None:
        return None
    try:
        r = await _client.post(f"{API_BASE}/{method}", json=params, timeout=40)
        data = r.json()
        if not data.get("ok"):
            logger.warning(f"Telegram API {method} failed: {data}")
        return data
    except Exception as e:
        logger.warning(f"Telegram API {method} error: {e}")
        return None

async def _send(chat_id: int, text: str, kb: dict | None = None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if kb:
        payload["reply_markup"] = kb
    return await _call("sendMessage", **payload)

async def _edit(chat_id: int, message_id: int, text: str, kb: dict | None = None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if kb:
        payload["reply_markup"] = kb
    res = await _call("editMessageText", **payload)
    if res is None or not res.get("ok"):
        await _send(chat_id, text, kb)

async def _answer_cb(cb_id: str, text: str = ""):
    await _call("answerCallbackQuery", callback_query_id=cb_id, text=text)

def _is_admin(chat_id: int) -> bool:
    return chat_id in ADMIN_IDS

# ── Keyboards حرفه‌ای ─────────────────────────────────────────────────────
def _main_menu_kb():
    return {"inline_keyboard": [
        [
            {"text": "📋 📊 لیست کانفیگ‌ها", "callback_data": "list:0"},
            {"text": "🆕 ✨ ساخت جدید", "callback_data": "newcfg"}
        ],
        [
            {"text": "🗂 📁 گروه‌های ساب", "callback_data": "subs:0"},
            {"text": "🔄 🔄 رفرش", "callback_data": "menu"}
        ],
        [
            {"text": "❓ 🆘 راهنما", "callback_data": "help"}
        ]
    ]}

def _links_list_kb(page: int):
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total > 0 else 1
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        status = "🟢" if is_link_allowed(l) else "🔴"
        label = l.get('label','?')[:26]
        rows.append([{"text": f"{status} {label}", "callback_data": f"view:{uid}"}])
    
    nav = []
    if start > 0:
        nav.append({"text": "⬅️ صفحه قبل", "callback_data": f"list:{page-1}"})
    nav.append({"text": f"📄 {page+1}/{total_pages}", "callback_data": "dummy"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "صفحه بعد ➡️", "callback_data": f"list:{page+1}"})
    if nav:
        rows.append(nav)
    
    rows.append([
        {"text": "🆕 ✨ ساخت جدید", "callback_data": "newcfg"},
        {"text": "🗂 📁 گروه‌ها", "callback_data": "subs:0"}
    ])
    rows.append([{"text": "🏠 منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}

def _link_detail_kb(uid: str, active: bool):
    return {"inline_keyboard": [
        [{"text": "🔗 📎 نمایش لینک اتصال", "callback_data": f"link:{uid}"}],
        [{"text": "🗂 📁 گروه ساب (لینک حرفه‌ای)", "callback_data": f"cfggroup:{uid}"}],
        [
            {"text": "⛔ غیرفعال‌سازی" if active else "✅ فعال‌سازی", "callback_data": f"toggle:{uid}"},
            {"text": "🗑 حذف کانفیگ", "callback_data": f"del:{uid}"}
        ],
        [{"text": "⬅️ بازگشت به لیست", "callback_data": "list:0"}]
    ]}

def _confirm_delete_kb(uid: str):
    return {"inline_keyboard": [
        [
            {"text": "✅ بله، حذف کن 🗑", "callback_data": f"delok:{uid}"},
            {"text": "❌ انصراف ↩️", "callback_data": f"view:{uid}"}
        ],
    ]}

# ── Wizard keyboards ─────────────────────────────────────────────────────────
def _wizard_cancel_kb():
    return {"inline_keyboard": [[{"text": "❌ انصراف و بازگشت ↩️", "callback_data": "w:cancel"}]]}

def _wizard_protocol_kb():
    rows = [[{"text": _protocol_label(p), "callback_data": f"w:proto:{p}"}] for p in PROTOCOLS]
    rows.append([{"text": "❌ انصراف ↩️", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_fp_kb():
    rows, row = [], []
    for fp in FINGERPRINTS:
        row.append({"text": _fp_label(fp), "callback_data": f"w:fp:{fp}"})
        if len(row) == 3:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([{"text": "❌ انصراف ↩️", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_skip_kb(step_key: str, label: str):
    return {"inline_keyboard": [
        [{"text": label, "callback_data": f"w:skip:{step_key}"}],
        [{"text": "❌ انصراف ↩️", "callback_data": "w:cancel"}]
    ]}

ALPN_PRESET_MAP = {"p1": "http/1.1", "p2": "h2,http/1.1", "p3": "h2"}

def _wizard_alpn_kb():
    return {"inline_keyboard": [
        [{"text": "🔤 http/1.1 (پیشنهادی)", "callback_data": "w:alpnpreset:p1"}],
        [{"text": "🔤 h2,http/1.1", "callback_data": "w:alpnpreset:p2"}],
        [{"text": "🔤 h2", "callback_data": "w:alpnpreset:p3"}],
        [{"text": "⏭ پیش‌فرض پروتکل", "callback_data": "w:skip:alpn"}],
        [{"text": "❌ انصراف ↩️", "callback_data": "w:cancel"}]
    ]}

def _wizard_unlimited_kb(step_key: str):
    return _wizard_skip_kb(step_key, "♾️ نامحدود")

def _wizard_confirm_kb():
    return {"inline_keyboard": [
        [{"text": "✅ ساخت کانفیگ 🚀", "callback_data": "w:confirm"}],
        [{"text": "❌ انصراف ↩️", "callback_data": "w:cancel"}]
    ]}

def _wizard_prompt(step: str, data: dict) -> str:
    head = f"✨ <b>ساخت کانفیگ جدید</b>\n{_format_progress(step)}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    if step == "label":
        return head + "✏️ <b>اسم/برچسب کانفیگ</b> رو بفرست:\n(مثلاً: کاربر علی یا کانال تلگرام)"
    if step == "protocol":
        return head + "🌐 <b>پروتکل</b> رو از دکمه‌های زیر انتخاب کن:"
    if step == "fingerprint":
        return head + "🖐 <b>Fingerprint (uTLS)</b> رو انتخاب کن:"
    if step == "alpn":
        return head + ("🔤 <b>ALPN</b> رو از دکمه‌های زیر انتخاب کن (پیشنهادی: <code>http/1.1</code>)\n"
                        "یا خودت هر مقدار دلخواهی رو تایپ و ارسال کن (مثلاً h2,http/1.1):")
    if step == "port":
        return head + f"🔌 <b>شماره پورت</b> (بین {MIN_PORT} تا {MAX_PORT}) رو بفرست\nیا پیش‌فرض ({DEFAULT_PORT}) رو انتخاب کن:"
    if step == "volume":
        return head + "📦 <b>محدودیت حجم مصرفی</b> رو بفرست، مثلاً:\n<code>10GB</code> یا <code>500MB</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "speed":
        return head + "🚀 <b>محدودیت سرعت</b> رو به مگابیت‌بر‌ثانیه بفرست، مثلاً <code>20</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "iplimit":
        return head + "👥 <b>حداکثر تعداد آی‌پی/کاربر هم‌زمان</b> مجاز رو بفرست\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "days":
        return head + "📅 <b>تعداد روزهای اعتبار</b> کانفیگ رو بفرست\nیا دکمه‌ی نامحدود (بدون انقضا) رو بزن:"
    return head

def _wizard_summary(data: dict) -> str:
    limit = "♾️ نامحدود" if not data.get("limit_bytes") else fmt_bytes(data["limit_bytes"])
    speed = "♾️ نامحدود" if not data.get("speed_limit_bytes") else f"{data['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    iplim = data.get("ip_limit", 0)
    iplim_txt = "♾️ نامحدود" if iplim == 0 else f"{iplim} کاربر"
    days = data.get("expires_days", 0)
    days_txt = "♾️ بدون انقضا" if not days else f"{days} روز"
    proto = data.get("protocol", DEFAULT_PROTOCOL)
    alpn = data.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    
    return (
        "📋 <b>خلاصه‌ی کانفیگ جدید</b>\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"📛 <b>برچسب:</b> {data.get('label','?')}\n"
        f"🌐 <b>پروتکل:</b> {_protocol_label(proto)}\n"
        f"🖐 <b>Fingerprint:</b> {_fp_label(data.get('fingerprint', DEFAULT_FINGERPRINT))}\n"
        f"🔤 <b>ALPN:</b> {alpn}\n"
        f"🔌 <b>پورت:</b> {data.get('port', DEFAULT_PORT)}\n"
        f"📦 <b>محدودیت حجم:</b> {limit}\n"
        f"🚀 <b>محدودیت سرعت:</b> {speed}\n"
        f"👥 <b>محدودیت آی‌پی:</b> {iplim_txt}\n"
        f"📅 <b>انقضا:</b> {days_txt}\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "✅ برای ساخت تایید کن:"
    )

# ── View builders حرفه‌ای ────────────────────────────────────────────────
def _format_detail(uid: str, l: dict) -> str:
    """نمایش جزئیات کانفیگ با استایل کارتی"""
    status = _format_status(l)
    limit = _format_bytes(l.get("limit_bytes", 0))
    speed = _format_speed(l.get("speed_limit_bytes", 0))
    iplim = _format_iplimit(l.get("ip_limit", 0))
    exp = _format_date(l.get("expires_at"))
    proto = _protocol_label(l.get("protocol", DEFAULT_PROTOCOL))
    fp = _fp_label(l.get("fingerprint", DEFAULT_FINGERPRINT))
    alpn = l.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(l.get('protocol', DEFAULT_PROTOCOL), 'http/1.1')})"
    
    return (
        "┌─────────────────────────────\n"
        f"│  📡 <b>کانفیگ</b> {l.get('label','?')}\n"
        "├─────────────────────────────\n"
        f"│  {status}\n"
        f"│  📦 <b>مصرف:</b> {fmt_bytes(l.get('used_bytes',0))} / {limit}\n"
        f"│  {speed}\n"
        f"│  {iplim}\n"
        f"│  {exp}\n"
        "├─────────────────────────────\n"
        f"│  🌐 <b>پروتکل:</b> {proto}\n"
        f"│  🖐 <b>Fingerprint:</b> {fp}\n"
        f"│  🔤 <b>ALPN:</b> {alpn}\n"
        f"│  🔌 <b>پورت:</b> {l.get('port', DEFAULT_PORT)}\n"
        "├─────────────────────────────\n"
        f"│  🆔 <b>UUID:</b> <code>{uid[:8]}...{uid[-4:]}</code>\n"
        f"│  📅 <b>ساخت:</b> {l.get('created_at', '').split('T')[0] if l.get('created_at') else 'نامشخص'}\n"
        "└─────────────────────────────"
    )

def _group_public_url(s: dict) -> str:
    host = get_host()
    return f"https://{host}/p/{s.get('uuid_key','')}"

def _subs_list_kb(page: int):
    items = sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total > 0 else 1
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for sid, s in chunk:
        cnt = len(s.get("link_ids", []))
        lock = "🔒" if s.get("password_hash") else "🔓"
        rows.append([{"text": f"{lock} {s.get('name','?')[:22]} ({cnt})", "callback_data": f"subview:{sid}"}])
    
    nav = []
    if start > 0:
        nav.append({"text": "⬅️ صفحه قبل", "callback_data": f"subs:{page-1}"})
    nav.append({"text": f"📄 {page+1}/{total_pages}", "callback_data": "dummy"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "صفحه بعد ➡️", "callback_data": f"subs:{page+1}"})
    if nav:
        rows.append(nav)
    
    rows.append([
        {"text": "🆕 ✨ ساخت گروه جدید", "callback_data": "newsub"},
        {"text": "🏠 منوی اصلی", "callback_data": "menu"}
    ])
    return {"inline_keyboard": rows}

def _format_sub_detail(sid: str, s: dict) -> str:
    cnt = len(s.get("link_ids", []))
    pw = "🔒 رمز دارد" if s.get("password_hash") else "🔓 بدون رمز"
    desc = s.get("desc") or "—"
    return (
        "┌─────────────────────────────\n"
        f"│  🗂 <b>گروه</b> {s.get('name','?')}\n"
        "├─────────────────────────────\n"
        f"│  📝 <b>توضیحات:</b> {desc}\n"
        f"│  📊 <b>تعداد کانفیگ:</b> {cnt}\n"
        f"│  🔐 <b>امنیت:</b> {pw}\n"
        "├─────────────────────────────\n"
        f"│  🔗 <b>لینک ساب حرفه‌ای:</b>\n"
        f"│  <code>{_group_public_url(s)}</code>\n"
        "└─────────────────────────────"
    )

def _sub_detail_kb(sid: str):
    return {"inline_keyboard": [
        [{"text": "➕ افزودن کانفیگ به این گروه", "callback_data": f"subaddlink:{sid}:0"}],
        [{"text": "🗑 حذف گروه", "callback_data": f"subdel:{sid}"}],
        [{"text": "⬅️ بازگشت به لیست گروه‌ها", "callback_data": "subs:0"}]
    ]}

def _confirm_subdel_kb(sid: str):
    return {"inline_keyboard": [
        [
            {"text": "✅ بله، حذف کن 🗑", "callback_data": f"subdelok:{sid}"},
            {"text": "❌ انصراف ↩️", "callback_data": f"subview:{sid}"}
        ]
    ]}

def _pick_link_for_group_kb(sid: str, page: int):
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total > 0 else 1
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        in_this = "✅ " if l.get("sub_id") == sid else ""
        rows.append([{"text": f"{in_this}{l.get('label','?')[:24]}", "callback_data": f"subaddlinkdo:{uid}"}])
    
    nav = []
    if start > 0:
        nav.append({"text": "⬅️ صفحه قبل", "callback_data": f"subaddlink:{sid}:{page-1}"})
    nav.append({"text": f"📄 {page+1}/{total_pages}", "callback_data": "dummy"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "صفحه بعد ➡️", "callback_data": f"subaddlink:{sid}:{page+1}"})
    if nav:
        rows.append(nav)
    
    rows.append([{"text": "⬅️ بازگشت به گروه", "callback_data": f"subview:{sid}"}])
    return {"inline_keyboard": rows}

def _cfg_group_kb(uid: str):
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        return {"inline_keyboard": [
            [{"text": "➖ خارج کردن از گروه", "callback_data": f"cfgungroup:{uid}"}],
            [{"text": "⬅️ بازگشت", "callback_data": f"view:{uid}"}]
        ]}
    rows = []
    for sid2, s in sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)[:8]:
        rows.append([{"text": f"➕ افزودن به «{s.get('name','?')[:24]}»", "callback_data": f"cfgaddgroup:{sid2}"}])
    rows.append([{"text": "🆕 ساخت گروه جدید و افزودن", "callback_data": f"cfgnewgroup:{uid}"}])
    rows.append([{"text": "⬅️ بازگشت", "callback_data": f"view:{uid}"}])
    return {"inline_keyboard": rows}

def _format_cfg_group(uid: str) -> str:
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        s = SUBS[sid]
        return (
            "┌─────────────────────────────\n"
            f"│  📡 کانفیگ «{link.get('label','?')}»\n"
            "├─────────────────────────────\n"
            f"│  📁 توی گروه «{s.get('name','?')}» هست.\n"
            "├─────────────────────────────\n"
            f"│  🔗 <b>لینک ساب حرفه‌ای:</b>\n"
            f"│  <code>{_group_public_url(s)}</code>\n"
            "└─────────────────────────────"
        )
    return (
        "┌─────────────────────────────\n"
        f"│  📡 کانفیگ «{link.get('label','?')}»\n"
        "├─────────────────────────────\n"
        "│  ℹ️ این کانفیگ توی هیچ گروهی نیست.\n"
        "│  فقط لینک ساب ساده داره.\n"
        "├─────────────────────────────\n"
        "│  💡 برای گرفتن لینک ساب حرفه‌ای\n"
        "│  این کانفیگ رو به یک گروه اضافه کن\n"
        "│  یا یه گروه جدید بساز.\n"
        "└─────────────────────────────"
    )

# ── Update handling ──────────────────────────────────────────────────────────
async def _handle_message(msg: dict):
    chat_id = msg.get("chat", {}).get("id")
    text = (msg.get("text") or "").strip()
    if chat_id is None:
        return
    if not _is_admin(chat_id):
        await _send(chat_id, "⛔ <b>دسترسی ممنوع!</b>\nشما اجازه‌ی استفاده از این ربات رو ندارید.")
        return

    if text in ("/start", "/menu"):
        _pending.pop(chat_id, None)
        welcome = (
            "👋 <b>به ربات مدیریت X4G خوش اومدی!</b>\n\n"
            "🚀 <b>قابلیت‌ها:</b>\n"
            "• 📋 مدیریت کانفیگ‌ها\n"
            "• 🆕 ساخت کانفیگ جدید\n"
            "• 🗂 گروه‌های ساب حرفه‌ای\n"
            "• 🔗 دریافت لینک اتصال و ساب\n\n"
            "از دکمه‌های زیر استفاده کن:"
        )
        await _send(chat_id, welcome, _main_menu_kb())
        return

    if text == "/cancel":
        _pending.pop(chat_id, None)
        await _send(chat_id, "✅ عملیات لغو شد.", _main_menu_kb())
        return

    pending = _pending.get(chat_id)

    if pending and pending.get("action") == "newsub" and pending.get("step") == "name" and text:
        name = text[:60]
        sid, s = await create_sub_group(name=name)
        link_uid = pending.get("link_uid")
        _pending.pop(chat_id, None)
        if link_uid and link_uid in LINKS:
            await set_link_sub(link_uid, sid)
            await _send(chat_id, f"✅ <b>گروه ساخته شد!</b> 🎉\n\n{_format_cfg_group(link_uid)}", _cfg_group_kb(link_uid))
        else:
            await _send(chat_id, f"✅ <b>گروه ساخته شد!</b> 🎉\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
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
            kb = _wizard_protocol_kb() if step == "protocol" else _wizard_fp_kb()
            await _send(chat_id, "لطفاً از دکمه‌های بالا یکی رو انتخاب کن 👆", kb)
            return

        if step == "alpn":
            data["alpn"] = text.strip()[:100]
            pending["step"] = "port"
            await _send(chat_id, _wizard_prompt("port", data), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if step == "port":
            try:
                p = int(text.strip())
            except ValueError:
                p = None
            if p is None or not (MIN_PORT <= p <= MAX_PORT):
                await _send(chat_id, f"❗️ عدد پورت نامعتبره. یه عدد بین {MIN_PORT} تا {MAX_PORT} بفرست:", _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
                return
            data["port"] = p
            pending["step"] = "volume"
            await _send(chat_id, _wizard_prompt("volume", data), _wizard_unlimited_kb("volume"))
            return

        if step == "volume":
            parsed = _parse_volume_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت درست نیست. مثلاً بفرست: <code>10GB</code> یا <code>500MB</code>", _wizard_unlimited_kb("volume"))
                return
            data["limit_bytes"] = parsed
            pending["step"] = "speed"
            await _send(chat_id, _wizard_prompt("speed", data), _wizard_unlimited_kb("speed"))
            return

        if step == "speed":
            parsed = _parse_speed_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت درست نیست. یه عدد بفرست، مثلاً <code>20</code> (Mbps)", _wizard_unlimited_kb("speed"))
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
                await _send(chat_id, "❗️ یه عدد صحیح بفرست (تعداد روز):", _wizard_unlimited_kb("days"))
                return
            data["expires_days"] = n
            pending["step"] = "confirm"
            await _send(chat_id, _wizard_summary(data), _wizard_confirm_kb())
            return

    await _send(chat_id, "از دکمه‌های زیر استفاده کن:", _main_menu_kb())

async def _handle_callback(cb: dict):
    chat_id = cb.get("message", {}).get("chat", {}).get("id")
    message_id = cb.get("message", {}).get("message_id")
    data = cb.get("data", "")
    cb_id = cb.get("id")

    if chat_id is None or not _is_admin(chat_id):
        await _answer_cb(cb_id, "⛔ دسترسی نداری")
        return
    await _answer_cb(cb_id)

    if data == "menu":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "🏠 <b>منوی اصلی</b>\nاز دکمه‌های زیر استفاده کن:", _main_menu_kb())
        return

    if data == "help":
        help_text = (
            "❓ <b>راهنمای ربات X4G</b>\n\n"
            "📋 <b>لیست کانفیگ‌ها:</b>\n"
            "مشاهده و مدیریت همه کانفیگ‌ها\n\n"
            "🆕 <b>ساخت کانفیگ جدید:</b>\n"
            "ساخت کانفیگ با ۹ مرحله\n\n"
            "🗂 <b>گروه‌های ساب:</b>\n"
            "ساخت لینک ساب حرفه‌ای\n\n"
            "🔗 <b>لینک اتصال:</b>\n"
            "دریافت لینک VLESS و ساب\n\n"
            "💡 <b>نکته:</b>\n"
            "هر مرحله قابل لغو هست."
        )
        await _edit(chat_id, message_id, help_text, _main_menu_kb())
        return

    if data.startswith("list:"):
        page = int(data.split(":", 1)[1] or 0)
        if not LINKS:
            await _edit(chat_id, message_id, "📭 <b>هنوز هیچ کانفیگی ساخته نشده.</b>\nاز دکمه‌ی «ساخت جدید» استفاده کن.", _main_menu_kb())
            return
        total = len(LINKS)
        await _edit(chat_id, message_id, f"📋 <b>لیست کانفیگ‌ها</b> ({total} مورد)", _links_list_kb(page))
        return

    # ── گروه‌های ساب ────────────────────────────────────────────────────────────
    if data.startswith("subs:"):
        page = int(data.split(":", 1)[1] or 0)
        if not SUBS:
            await _edit(chat_id, message_id, "📭 <b>هنوز هیچ گروهی ساخته نشده.</b>\n\nبرای گرفتن لینک ساب حرفه‌ای (صفحه‌ی زیبا)، اول یه گروه بساز و کانفیگ مورد نظرت رو داخلش بذار.", _subs_list_kb(0))
            return
        await _edit(chat_id, message_id, f"🗂 <b>گروه‌های ساب</b> ({len(SUBS)} مورد)", _subs_list_kb(page))
        return

    if data == "newsub":
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": None}
        await _edit(chat_id, message_id, "✏️ <b>اسم گروه</b> رو بفرست (این اسم فقط برای خودت توی مدیریت گروه‌هاست):", _wizard_cancel_kb())
        return

    if data.startswith("subview:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "❌ این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_sub_detail(sid, s), _sub_detail_kb(sid))
        return

    if data.startswith("subaddlink:"):
        _, sid, page_s = data.split(":", 2)
        if sid not in SUBS:
            await _edit(chat_id, message_id, "❌ این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        if not LINKS:
            await _edit(chat_id, message_id, "📭 <b>هنوز هیچ کانفیگی نداری</b> که به گروه اضافه کنی.", _sub_detail_kb(sid))
            return
        _pending[chat_id] = {"action": "subaddlink_ctx", "sid": sid}
        await _edit(chat_id, message_id, "🔍 <b>کدوم کانفیگ رو به این گروه اضافه کنم؟</b>\n(کانفیگ‌هایی که علامت ✅ دارن همین الان توی این گروهن)", _pick_link_for_group_kb(sid, int(page_s or 0)))
        return

    if data.startswith("subaddlinkdo:"):
        uid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        sid = ctx.get("sid") if ctx.get("action") == "subaddlink_ctx" else None
        if not sid or sid not in SUBS:
            await _answer_cb(cb_id, "⏰ این عملیات منقضی شده، از منوی گروه‌ها دوباره امتحان کن.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "❌ این کانفیگ دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        s = SUBS.get(sid)
        await _edit(chat_id, message_id, f"✅ <b>کانفیگ به گروه اضافه شد!</b> 🎉\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if data.startswith("subdel:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "❌ این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"⚠️ <b>از حذف گروه «{s.get('name')}» مطمئنی؟</b>\nلینک ساب حرفه‌ای‌اش دیگه کار نمی‌کنه.\n(کانفیگ‌ها حذف نمی‌شن، فقط از گروه خارج می‌شن)", _confirm_subdel_kb(sid))
        return

    if data.startswith("subdelok:"):
        sid = data.split(":", 1)[1]
        name = await remove_sub_group(sid)
        if name is None:
            await _edit(chat_id, message_id, "❌ این گروه قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 <b>گروه «{name}» حذف شد.</b>", _main_menu_kb())
        return

    # ── گروه یک کانفیگ خاص ──────────────────────────────────────────────────────
    if data.startswith("cfggroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "cfg_group_ctx", "uid": uid}
        await _edit(chat_id, message_id, _format_cfg_group(uid), _cfg_group_kb(uid))
        return

    if data.startswith("cfgungroup:"):
        uid = data.split(":", 1)[1]
        await set_link_sub(uid, None)
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("cfgaddgroup:"):
        sid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        uid = ctx.get("uid") if ctx.get("action") == "cfg_group_ctx" else None
        if not uid or uid not in LINKS:
            await _answer_cb(cb_id, "⏰ این عملیات منقضی شده، از روی کانفیگ دوباره وارد این بخش شو.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "❌ این گروه دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, f"✅ <b>کانفیگ به گروه اضافه شد!</b> 🎉\n\n{_format_cfg_group(uid)}", _cfg_group_kb(uid))
        return

    if data.startswith("cfgnewgroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": uid}
        await _edit(chat_id, message_id, "✏️ <b>اسم گروه جدید</b> رو بفرست؛ بعد از ساخته شدن، همین کانفیگ خودکار داخلش قرار می‌گیره:", _wizard_cancel_kb())
        return

    # ── ساخت کانفیگ جدید ──────────────────────────────────────────────────────
    if data == "newcfg":
        _pending[chat_id] = {"action": "wizard", "step": "label", "data": {}}
        await _edit(chat_id, message_id, _wizard_prompt("label", {}), _wizard_cancel_kb())
        return

    if data == "w:cancel":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "❌ ساخت کانفیگ لغو شد.", _main_menu_kb())
        return

    if data.startswith("w:"):
        pending = _pending.get(chat_id)
        if not pending or pending.get("action") != "wizard":
            await _edit(chat_id, message_id, "⏰ این مرحله دیگه معتبر نیست، از منوی زیر دوباره شروع کن.", _main_menu_kb())
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
            await _edit(chat_id, message_id, _wizard_prompt("port", wdata), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if data == "w:skip:alpn" and step == "alpn":
            wdata["alpn"] = ""
            pending["step"] = "port"
            await _edit(chat_id, message_id, _wizard_prompt("port", wdata), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if data == "w:skip:port" and step == "port":
            wdata["port"] = DEFAULT_PORT
            pending["step"] = "volume"
            await _edit(chat_id, message_id, _wizard_prompt("volume", wdata), _wizard_unlimited_kb("volume"))
            return

        if data == "w:skip:volume" and step == "volume":
            wdata["limit_bytes"] = 0
            pending["step"] = "speed"
            await _edit(chat_id, message_id, _wizard_prompt("speed", wdata), _wizard_unlimited_kb("speed"))
            return

        if data == "w:skip:speed" and step == "speed":
            wdata["speed_limit_bytes"] = 0
            pending["step"] = "iplimit"
            await _edit(chat_id, message_id, _wizard_prompt("iplimit", wdata), _wizard_unlimited_kb("iplimit"))
            return

        if data == "w:skip:iplimit" and step == "iplimit":
            wdata["ip_limit"] = 0
            pending["step"] = "days"
            await _edit(chat_id, message_id, _wizard_prompt("days", wdata), _wizard_unlimited_kb("days"))
            return

        if data == "w:skip:days" and step == "days":
            wdata["expires_days"] = 0
            pending["step"] = "confirm"
            await _edit(chat_id, message_id, _wizard_summary(wdata), _wizard_confirm_kb())
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
            await _edit(chat_id, message_id, f"✅ <b>کانفیگ با موفقیت ساخته شد!</b> 🎉\n\n{_format_detail(uid, link)}", _link_detail_kb(uid, link["active"]))
            return

        await _answer_cb(cb_id, "⏰ این دکمه دیگه معتبر نیست.")
        return

    # ── مدیریت کانفیگ ──────────────────────────────────────────────────────────
    if data.startswith("view:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("toggle:"):
        uid = data.split(":", 1)[1]
        l = await set_link_active(uid, not LINKS.get(uid, {}).get("active", True))
        if not l:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        status_emoji = "🟢" if l["active"] else "🔴"
        await _edit(chat_id, message_id, f"{status_emoji} <b>وضعیت کانفیگ تغییر کرد</b>\n\n{_format_detail(uid, l)}", _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("link:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _answer_cb(cb_id, "❌ کانفیگ پیدا نشد")
            return
        host = get_host()
        vless = vless_link_for_link(l, uid, host)
        sub_url = f"https://{host}/sub/{uid}"
        
        msg = (
            f"🔗 <b>لینک اتصال</b> «{l.get('label')}»:\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"<code>{vless}</code>\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"📎 <b>لینک ساب ساده:</b>\n<code>{sub_url}</code>"
        )
        
        sid = l.get("sub_id")
        if sid and sid in SUBS:
            msg += f"\n\n✨ <b>لینک ساب حرفه‌ای گروه «{SUBS[sid].get('name','?')}»:</b>\n<code>{_group_public_url(SUBS[sid])}</code>"
        else:
            msg += "\n\n💡 این کانفیگ توی هیچ گروهی نیست. برای گرفتن لینک ساب حرفه‌ای، از دکمه‌ی «🗂 گروه ساب» استفاده کن."
        
        await _send(chat_id, msg)
        return

    if data.startswith("del:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "❌ این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"⚠️ <b>از حذف «{l.get('label')}» مطمئنی؟</b>\nاین عمل <b>برگشت‌ناپذیر</b> هست!", _confirm_delete_kb(uid))
        return

    if data.startswith("delok:"):
        uid = data.split(":", 1)[1]
        label = await remove_link(uid)
        if label is None:
            await _edit(chat_id, message_id, "❌ این کانفیگ قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 <b>کانفیگ «{label}» حذف شد.</b>", _main_menu_kb())
        return

    # دکمه ناشناخته
    await _answer_cb(cb_id, "❓ دکمه نامعتبر")

# ── Polling loop ─────────────────────────────────────────────────────────────
async def _poll_loop():
    global _running
    offset = 0
    logger.info(f"🤖 Telegram bot polling started (admins: {len(ADMIN_IDS)})")
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
                    logger.warning(f"Telegram update handling error: {e}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"Telegram poll loop error: {e}")
            await asyncio.sleep(3)

# ── Lifecycle ────────────────────────────────────────────────────────────────
async def start_bot():
    global _client, _poll_task, _running
    if not BOT_TOKEN:
        logger.info("Telegram bot: TELEGRAM_BOT_TOKEN تنظیم نشده، ربات غیرفعاله.")
        return
    if not ADMIN_IDS:
        logger.warning("Telegram bot: TELEGRAM_ADMIN_IDS تنظیم نشده، هیچ‌کس اجازه‌ی مدیریت نداره (ربات روشنه ولی همه رد می‌شن).")
    _client = httpx.AsyncClient(timeout=httpx.Timeout(40.0, connect=10.0))
    _running = True
    _poll_task = asyncio.create_task(_poll_loop())

async def stop_bot():
    global _running, _client
    _running = False
    if _poll_task:
        _poll_task.cancel()
    if _client:
        await _client.aclose()
        _client = None
