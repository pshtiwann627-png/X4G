# telegram_bot.py
# ══════════════════════════════════════════════════════════════════════════════
# ربات مدیریت تلگرام — نسخه پیشرفته با قابلیت‌های جدید
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import os
import re
import json
import secrets
import gzip
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Any, Optional, Tuple
from io import BytesIO
import hashlib

import httpx
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

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
    stats,
    hourly_traffic,
    connections,
    LINKS_LOCK,
    save_state,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
_admin_ids_raw = os.environ.get("TELEGRAM_ADMIN_IDS", "").strip()
ADMIN_IDS = {int(x) for x in _admin_ids_raw.replace(" ", "").split(",") if x.isdigit()} if _admin_ids_raw else set()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
PAGE_SIZE = 6

_client: httpx.AsyncClient | None = None
_poll_task: asyncio.Task | None = None
_running = False
_pending: dict = {}   # chat_id -> {"action": "wizard", "step": "...", "data": {...}}

# ── سیستم‌های پیشرفته ─────────────────────────────────────────────────────────

class TwoFactorAuth:
    """سیستم احراز هویت دو مرحله‌ای"""
    def __init__(self):
        self.user_secrets: Dict[int, str] = {}
        self.user_2fa_enabled: Dict[int, bool] = {}
    
    def enable_2fa(self, chat_id: int) -> str:
        import pyotp
        secret = pyotp.random_base32()
        self.user_secrets[chat_id] = secret
        self.user_2fa_enabled[chat_id] = True
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=f"X4G_{chat_id}", issuer_name="X4G VPN")
    
    def verify_2fa(self, chat_id: int, code: str) -> bool:
        if not self.user_2fa_enabled.get(chat_id, False):
            return True
        secret = self.user_secrets.get(chat_id)
        if not secret:
            return False
        import pyotp
        totp = pyotp.TOTP(secret)
        return totp.verify(code)

class ReferralSystem:
    """سیستم ارجاع و پاداش"""
    def __init__(self):
        self.referral_codes: Dict[int, str] = {}
        self.referral_rewards: Dict[int, Dict] = {}
        self.referral_used: Dict[str, int] = {}
    
    def generate_referral_code(self, user_id: int) -> str:
        code = secrets.token_urlsafe(6)
        self.referral_codes[user_id] = code
        return code
    
    async def process_referral(self, referrer_id: int, new_user_id: int) -> bool:
        if referrer_id == new_user_id:
            return False
        # 1GB پاداش
        reward_bytes = 1024 * 1024 * 1024
        self.referral_rewards[new_user_id] = {
            "referred_by": referrer_id,
            "time": datetime.now().isoformat(),
            "reward": reward_bytes
        }
        return True

class NotificationSystem:
    """سیستم هشدار هوشمند"""
    def __init__(self):
        self.alert_history: Dict[int, List[str]] = defaultdict(list)
        self.last_alert: Dict[str, datetime] = {}
    
    async def check_alerts(self) -> List[Dict]:
        alerts = []
        for uid, link in LINKS.items():
            # بررسی حجم مصرفی
            if link.get('limit_bytes', 0) > 0:
                usage = link.get('used_bytes', 0)
                limit = link['limit_bytes']
                usage_percent = (usage / limit) * 100
                
                if usage_percent >= 90 and usage_percent < 100:
                    if f"{uid}_90" not in self.last_alert:
                        alerts.append({
                            "uid": uid,
                            "label": link.get('label', '?'),
                            "type": "volume_warning",
                            "message": f"⚠️ حجم مصرفی {link['label']} به {usage_percent:.0f}% رسید!",
                            "percent": usage_percent
                        })
                        self.last_alert[f"{uid}_90"] = datetime.now()
                
                elif usage_percent >= 100:
                    if f"{uid}_100" not in self.last_alert:
                        alerts.append({
                            "uid": uid,
                            "label": link.get('label', '?'),
                            "type": "volume_exceeded",
                            "message": f"❌ حجم مصرفی {link['label']} تمام شد!",
                            "percent": usage_percent
                        })
                        self.last_alert[f"{uid}_100"] = datetime.now()
            
            # بررسی تاریخ انقضا
            if link.get('expires_at'):
                try:
                    exp_date = datetime.fromisoformat(link['expires_at'])
                    days_left = (exp_date - datetime.now()).days
                    if 1 <= days_left <= 3:
                        if f"{uid}_exp_{days_left}" not in self.last_alert:
                            alerts.append({
                                "uid": uid,
                                "label": link.get('label', '?'),
                                "type": "expiry_warning",
                                "message": f"⚠️ کانفیگ {link['label']} تا {days_left} روز دیگر منقضی می‌شود!",
                                "days_left": days_left
                            })
                            self.last_alert[f"{uid}_exp_{days_left}"] = datetime.now()
                except:
                    pass
        
        return alerts

class BackupSystem:
    """سیستم پشتیبان‌گیری خودکار"""
    BACKUP_DIR = "backups"
    
    @classmethod
    async def create_backup(cls) -> Optional[str]:
        try:
            os.makedirs(cls.BACKUP_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{cls.BACKUP_DIR}/backup_{timestamp}.json"
            
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "stats": dict(stats),
                "version": "2.0"
            }
            
            with open(filename, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            # فشرده‌سازی
            with open(filename, 'rb') as f_in:
                with gzip.open(f"{filename}.gz", 'wb') as f_out:
                    f_out.writelines(f_in)
            
            return f"{filename}.gz"
        except Exception as e:
            logger.error(f"Backup error: {e}")
            return None
    
    @classmethod
    async def list_backups(cls) -> List[Dict]:
        backups = []
        try:
            for f in os.listdir(cls.BACKUP_DIR):
                if f.endswith('.gz'):
                    path = os.path.join(cls.BACKUP_DIR, f)
                    stat = os.stat(path)
                    backups.append({
                        "name": f,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        except:
            pass
        return sorted(backups, key=lambda x: x['modified'], reverse=True)

class CouponSystem:
    """سیستم تخفیف و کوپن"""
    def __init__(self):
        self.coupons: Dict[str, Dict] = {}
    
    async def create_coupon(self, discount_percent: int, max_uses: int = 1, expires_in_days: int = 30) -> str:
        code = secrets.token_urlsafe(8)
        self.coupons[code] = {
            "discount": discount_percent,
            "uses": 0,
            "max_uses": max_uses,
            "expires_at": (datetime.now() + timedelta(days=expires_in_days)).isoformat(),
            "used_by": []
        }
        return code
    
    async def apply_coupon(self, code: str, user_id: int) -> Tuple[bool, str, int]:
        coupon = self.coupons.get(code)
        if not coupon:
            return False, "کوپن نامعتبر است", 0
        
        if coupon['uses'] >= coupon['max_uses']:
            return False, "تعداد استفاده از این کوپن به پایان رسیده", 0
        
        if datetime.now() > datetime.fromisoformat(coupon['expires_at']):
            return False, "این کوپن منقضی شده است", 0
        
        coupon['uses'] += 1
        coupon['used_by'].append(user_id)
        return True, f"تخفیف {coupon['discount']}% اعمال شد", coupon['discount']

class StatsDashboard:
    """داشبورد آماری پیشرفته"""
    
    @staticmethod
    async def generate_traffic_chart(days: int = 7) -> BytesIO:
        """تولید نمودار مصرف ترافیک"""
        dates = []
        traffic = []
        
        now = datetime.now()
        for i in range(days - 1, -1, -1):
            date = now - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            dates.append(date_str)
            
            # جمع‌آوری ترافیک روزانه
            daily_traffic = 0
            for hour_key, bytes_count in hourly_traffic.items():
                if hour_key.startswith(date_str):
                    daily_traffic += bytes_count
            traffic.append(daily_traffic / (1024 * 1024 * 1024))  # تبدیل به GB
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(dates, traffic, color='skyblue', edgecolor='navy')
        ax.set_xlabel('تاریخ', fontsize=12)
        ax.set_ylabel('ترافیک (GB)', fontsize=12)
        ax.set_title('مصرف ترافیک روزانه', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        plt.close()
        buffer.seek(0)
        return buffer
    
    @staticmethod
    async def generate_pdf_report() -> BytesIO:
        """تولید گزارش PDF"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # عنوان
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, 10*inch, "گزارش آماری X4G")
        
        # اطلاعات
        y = 9*inch
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, y, f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        y -= 0.5*inch
        
        c.drawString(1*inch, y, f"تعداد کانفیگ‌ها: {len(LINKS)}")
        y -= 0.3*inch
        
        active = len([l for l in LINKS.values() if is_link_allowed(l)])
        c.drawString(1*inch, y, f"کانفیگ‌های فعال: {active}")
        y -= 0.3*inch
        
        total_traffic = stats.get("total_bytes", 0)
        c.drawString(1*inch, y, f"کل ترافیک مصرفی: {fmt_bytes(total_traffic)}")
        y -= 0.3*inch
        
        total_requests = stats.get("total_requests", 0)
        c.drawString(1*inch, y, f"تعداد درخواست‌ها: {total_requests}")
        y -= 0.3*inch
        
        errors = stats.get("total_errors", 0)
        c.drawString(1*inch, y, f"خطاها: {errors}")
        
        c.save()
        buffer.seek(0)
        return buffer

# ── Config creation wizard ────────────────────────────────────────────────────
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

async def _send_photo(chat_id: int, photo: BytesIO, caption: str = "", kb: dict | None = None):
    """ارسال عکس با captcha"""
    if _client is None:
        return None
    files = {"photo": ("chart.png", photo, "image/png")}
    payload = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
    if kb:
        payload["reply_markup"] = json.dumps(kb)
    try:
        r = await _client.post(f"{API_BASE}/sendPhoto", data=payload, files=files, timeout=40)
        data = r.json()
        if not data.get("ok"):
            logger.warning(f"Telegram sendPhoto failed: {data}")
        return data
    except Exception as e:
        logger.warning(f"Telegram sendPhoto error: {e}")
        return None

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

# ── سیستم‌های پیشرفته (نمونه‌های کلاس) ──────────────────────────────────────

# نمونه‌سازی سیستم‌ها
tfa_system = TwoFactorAuth()
referral_system = ReferralSystem()
notification_system = NotificationSystem()
backup_system = BackupSystem()
coupon_system = CouponSystem()
stats_dashboard = StatsDashboard()

# ── Keyboards ────────────────────────────────────────────────────────────────
def _main_menu_kb():
    return {"inline_keyboard": [
        [{"text": "📋 لیست کانفیگ‌ها", "callback_data": "list:0"}],
        [{"text": "➕ ساخت کانفیگ جدید", "callback_data": "newcfg"}],
        [{"text": "🗂 گروه‌های ساب", "callback_data": "subs:0"}],
        [{"text": "📊 آمار و گزارش‌ها", "callback_data": "stats_menu"}],
        [{"text": "🎁 سیستم ارجاع", "callback_data": "referral"}],
        [{"text": "🔄 پشتیبان‌گیری", "callback_data": "backup_menu"}],
        [{"text": "🔐 احراز هویت ۲ مرحله‌ای", "callback_data": "2fa"}],
        [{"text": "🔄 رفرش", "callback_data": "menu"}],
    ]}

def _stats_menu_kb():
    return {"inline_keyboard": [
        [{"text": "📈 نمودار ترافیک", "callback_data": "chart:7"}],
        [{"text": "📊 گزارش PDF", "callback_data": "report_pdf"}],
        [{"text": "📋 خلاصه آمار", "callback_data": "stats_summary"}],
        [{"text": "⬅ منوی اصلی", "callback_data": "menu"}],
    ]}

def _backup_menu_kb():
    return {"inline_keyboard": [
        [{"text": "📤 ایجاد پشتیبان جدید", "callback_data": "backup_create"}],
        [{"text": "📥 لیست پشتیبان‌ها", "callback_data": "backup_list"}],
        [{"text": "⬅ منوی اصلی", "callback_data": "menu"}],
    ]}

def _links_list_kb(page: int):
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

def _link_detail_kb(uid: str, active: bool):
    return {"inline_keyboard": [
        [{"text": "🔗 نمایش لینک اتصال", "callback_data": f"link:{uid}"}],
        [{"text": "🗂 گروه ساب", "callback_data": f"cfggroup:{uid}"}],
        [{"text": ("⛔ غیرفعال‌سازی" if active else "✅ فعال‌سازی"), "callback_data": f"toggle:{uid}"}],
        [{"text": "🗑 حذف کانفیگ", "callback_data": f"del:{uid}"}],
        [{"text": "⬅ بازگشت به لیست", "callback_data": "list:0"}],
    ]}

def _confirm_delete_kb(uid: str):
    return {"inline_keyboard": [
        [{"text": "✅ بله، حذف کن", "callback_data": f"delok:{uid}"},
         {"text": "❌ انصراف", "callback_data": f"view:{uid}"}],
    ]}

# ── Wizard keyboards ─────────────────────────────────────────────────────────
def _wizard_cancel_kb():
    return {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "w:cancel"}]]}

def _wizard_protocol_kb():
    rows = [[{"text": _protocol_label(p), "callback_data": f"w:proto:{p}"}] for p in PROTOCOLS]
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_fp_kb():
    rows, row = [], []
    for fp in FINGERPRINTS:
        row.append({"text": _fp_label(fp), "callback_data": f"w:fp:{fp}"})
        if len(row) == 3:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_skip_kb(step_key: str, label: str):
    return {"inline_keyboard": [
        [{"text": label, "callback_data": f"w:skip:{step_key}"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

ALPN_PRESET_MAP = {"p1": "http/1.1", "p2": "h2,http/1.1", "p3": "h2"}

def _wizard_alpn_kb():
    return {"inline_keyboard": [
        [{"text": "🔤 http/1.1 (پیشنهادی)", "callback_data": "w:alpnpreset:p1"}],
        [{"text": "🔤 h2,http/1.1", "callback_data": "w:alpnpreset:p2"}],
        [{"text": "🔤 h2", "callback_data": "w:alpnpreset:p3"}],
        [{"text": "⏭ پیش‌فرض پروتکل", "callback_data": "w:skip:alpn"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

def _wizard_unlimited_kb(step_key: str):
    return _wizard_skip_kb(step_key, "♾ نامحدود")

def _wizard_confirm_kb():
    return {"inline_keyboard": [
        [{"text": "✅ ساخت کانفیگ", "callback_data": "w:confirm"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

def _wizard_prompt(step: str, data: dict) -> str:
    n = WIZARD_STEPS.index(step) + 1 if step in WIZARD_STEPS else len(WIZARD_STEPS)
    head = f"🧩 ساخت کانفیگ جدید — مرحله {n}/{len(WIZARD_STEPS)}\n\n"
    if step == "label":
        return head + "✏️ اسم/برچسب کانفیگ رو بفرست:"
    if step == "protocol":
        return head + "🌐 پروتکل رو از دکمه‌های زیر انتخاب کن:"
    if step == "fingerprint":
        return head + "🖐 Fingerprint (uTLS) رو انتخاب کن:"
    if step == "alpn":
        return head + ("🔤 ALPN رو از دکمه‌های زیر انتخاب کن (پیشنهادی: <code>http/1.1</code>)\n"
                        "یا خودت هر مقدار دلخواهی رو تایپ و ارسال کن (مثلاً h2,http/1.1):")
    if step == "port":
        return head + f"🔌 شماره پورت (بین {MIN_PORT} تا {MAX_PORT}) رو بفرست\nیا پیش‌فرض ({DEFAULT_PORT}) رو انتخاب کن:"
    if step == "volume":
        return head + "📦 محدودیت حجم مصرفی رو بفرست، مثلاً:\n<code>10GB</code> یا <code>500MB</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "speed":
        return head + "🚀 محدودیت سرعت رو به مگابیت‌بر‌ثانیه بفرست، مثلاً <code>20</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "iplimit":
        return head + "👥 حداکثر تعداد آی‌پی/کاربر هم‌زمان مجاز رو بفرست\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "days":
        return head + "📅 تعداد روزهای اعتبار کانفیگ رو بفرست\nیا دکمه‌ی نامحدود (بدون انقضا) رو بزن:"
    return head

def _wizard_summary(data: dict) -> str:
    limit = "نامحدود" if not data.get("limit_bytes") else fmt_bytes(data["limit_bytes"])
    speed = "نامحدود" if not data.get("speed_limit_bytes") else f"{data['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    iplim = data.get("ip_limit", 0) or "نامحدود"
    days = data.get("expires_days", 0)
    days_txt = "بدون انقضا" if not days else f"{days} روز"
    proto = data.get("protocol", DEFAULT_PROTOCOL)
    alpn = data.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    return (
        "🧩 خلاصه‌ی کانفیگ جدید — تایید کن:\n\n"
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

# ── View builders ────────────────────────────────────────────────────────────
def _format_detail(uid: str, l: dict) -> str:
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

# ── Sub-group view builders ──────────────────────────────────────────────────
def _group_public_url(s: dict) -> str:
    host = get_host()
    return f"https://{host}/p/{s.get('uuid_key','')}"

def _subs_list_kb(page: int):
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

def _format_sub_detail(sid: str, s: dict) -> str:
    cnt = len(s.get("link_ids", []))
    pw = "🔒 دارد" if s.get("password_hash") else "بدون رمز"
    desc = s.get("desc") or "—"
    return (
        f"🗂 <b>{s.get('name','?')}</b>\n"
        f"توضیحات: {desc}\n"
        f"تعداد کانفیگ‌های داخل گروه: {cnt}\n"
        f"رمز عبور: {pw}\n\n"
        f"🔗 لینک ساب حرفه‌ای این گروه:\n<code>{_group_public_url(s)}</code>"
    )

def _sub_detail_kb(sid: str):
    return {"inline_keyboard": [
        [{"text": "➕ افزودن کانفیگ به این گروه", "callback_data": f"subaddlink:{sid}:0"}],
        [{"text": "🗑 حذف گروه", "callback_data": f"subdel:{sid}"}],
        [{"text": "⬅ بازگشت به لیست گروه‌ها", "callback_data": "subs:0"}],
    ]}

def _confirm_subdel_kb(sid: str):
    return {"inline_keyboard": [
        [{"text": "✅ بله، حذف کن", "callback_data": f"subdelok:{sid}"},
         {"text": "❌ انصراف", "callback_data": f"subview:{sid}"}],
    ]}

def _pick_link_for_group_kb(sid: str, page: int):
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

def _cfg_group_kb(uid: str):
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        return {"inline_keyboard": [
            [{"text": "➖ خارج کردن از گروه", "callback_data": f"cfgungroup:{uid}"}],
            [{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}],
        ]}
    rows = []
    for sid2, s in sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)[:8]:
        rows.append([{"text": f"➕ افزودن به «{s.get('name','?')[:24]}»", "callback_data": f"cfgaddgroup:{sid2}"}])
    rows.append([{"text": "🆕 ساخت گروه جدید و افزودن", "callback_data": f"cfgnewgroup:{uid}"}])
    rows.append([{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}])
    return {"inline_keyboard": rows}

def _format_cfg_group(uid: str) -> str:
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        s = SUBS[sid]
        return (
            f"🗂 کانفیگ «{link.get('label','?')}» توی گروه «{s.get('name','?')}» هست.\n\n"
            f"🔗 لینک ساب حرفه‌ای این گروه:\n<code>{_group_public_url(s)}</code>"
        )
    return (
        f"کانفیگ «{link.get('label','?')}» توی هیچ گروهی نیست، یعنی فقط لینک ساب ساده داره.\n\n"
        "برای گرفتن لینک ساب حرفه‌ای (صفحه‌ی زیبا)، این کانفیگ رو به یک گروه اضافه کن یا یه گروه جدید بساز:"
    )

# ── Update handling ──────────────────────────────────────────────────────────
async def _handle_message(msg: dict):
    chat_id = msg.get("chat", {}).get("id")
    text = (msg.get("text") or "").strip()
    if chat_id is None:
        return
    if not _is_admin(chat_id):
        await _send(chat_id, "⛔ شما اجازه‌ی دسترسی به این ربات رو ندارید.")
        return

    if text in ("/start", "/menu"):
        _pending.pop(chat_id, None)
        await _send(chat_id, "👋 به ربات مدیریت X4G خوش اومدی.\nاز دکمه‌های زیر برای مدیریت کانفیگ‌ها استفاده کن:", _main_menu_kb())
        return

    if text == "/cancel":
        _pending.pop(chat_id, None)
        await _send(chat_id, "لغو شد.", _main_menu_kb())
        return

    pending = _pending.get(chat_id)

    if pending and pending.get("action") == "newsub" and pending.get("step") == "name" and text:
        name = text[:60]
        sid, s = await create_sub_group(name=name)
        link_uid = pending.get("link_uid")
        _pending.pop(chat_id, None)
        if link_uid and link_uid in LINKS:
            await set_link_sub(link_uid, sid)
            await _send(chat_id, f"✅ گروه ساخته شد و کانفیگ به اون اضافه شد.\n\n{_format_cfg_group(link_uid)}", _cfg_group_kb(link_uid))
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

    # ── منوی اصلی ──────────────────────────────────────────────────────────────
    if data == "menu":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "منوی مدیریت X4G:", _main_menu_kb())
        return

    if data.startswith("list:"):
        page = int(data.split(":", 1)[1] or 0)
        if not LINKS:
            await _edit(chat_id, message_id, "هنوز هیچ کانفیگی ساخته نشده.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"📋 لیست کانفیگ‌ها ({len(LINKS)} مورد):", _links_list_kb(page))
        return

    # ── آمار و گزارش ──────────────────────────────────────────────────────────
    if data == "stats_menu":
        await _edit(chat_id, message_id, "📊 منوی آمار و گزارش:", _stats_menu_kb())
        return

    if data.startswith("chart:"):
        days = int(data.split(":", 1)[1])
        try:
            chart = await stats_dashboard.generate_traffic_chart(days)
            await _send_photo(chat_id, chart, f"📈 نمودار مصرف ترافیک {days} روز اخیر", _stats_menu_kb())
        except Exception as e:
            logger.error(f"Chart error: {e}")
            await _send(chat_id, "❌ خطا در تولید نمودار", _stats_menu_kb())
        return

    if data == "report_pdf":
        try:
            pdf = await stats_dashboard.generate_pdf_report()
            if _client is not None:
                files = {"document": ("report.pdf", pdf, "application/pdf")}
                await _client.post(f"{API_BASE}/sendDocument", data={"chat_id": chat_id}, files=files)
        except Exception as e:
            logger.error(f"PDF report error: {e}")
            await _send(chat_id, "❌ خطا در تولید گزارش", _stats_menu_kb())
        return

    if data == "stats_summary":
        active = len([l for l in LINKS.values() if is_link_allowed(l)])
        total_traffic = stats.get("total_bytes", 0)
        total_requests = stats.get("total_requests", 0)
        errors = stats.get("total_errors", 0)
        
        summary = (
            "📋 خلاصه آمار:\n\n"
            f"📌 تعداد کل کانفیگ‌ها: {len(LINKS)}\n"
            f"🟢 کانفیگ‌های فعال: {active}\n"
            f"📊 کل ترافیک مصرفی: {fmt_bytes(total_traffic)}\n"
            f"🔄 تعداد درخواست‌ها: {total_requests}\n"
            f"❌ خطاها: {errors}\n"
            f"🔗 اتصالات همزمان: {len(connections)}\n"
            f"📅 زمان: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        await _edit(chat_id, message_id, summary, _stats_menu_kb())
        return

    # ── سیستم ارجاع ─────────────────────────────────────────────────────────────
    if data == "referral":
        code = referral_system.generate_referral_code(chat_id)
        host = get_host()
        referral_link = f"https://{host}/ref/{code}"
        msg = (
            "🎁 سیستم ارجاع X4G\n\n"
            "هر کاربر جدیدی که با لینک ارجاع شما ثبت‌نام کنه، به شما ۱GB ترافیک هدیه داده می‌شه!\n\n"
            f"🔗 لینک ارجاع شما:\n<code>{referral_link}</code>\n\n"
            "این لینک رو با دوستانتون به اشتراک بذارید 🚀"
        )
        await _edit(chat_id, message_id, msg, _main_menu_kb())
        return

    # ── پشتیبان‌گیری ───────────────────────────────────────────────────────────
    if data == "backup_menu":
        await _edit(chat_id, message_id, "🔄 منوی پشتیبان‌گیری:", _backup_menu_kb())
        return

    if data == "backup_create":
        await _edit(chat_id, message_id, "⏳ در حال ایجاد پشتیبان...")
        backup_file = await backup_system.create_backup()
        if backup_file:
            if _client is not None:
                with open(backup_file, 'rb') as f:
                    files = {"document": (os.path.basename(backup_file), f, "application/gzip")}
                    await _client.post(f"{API_BASE}/sendDocument", data={"chat_id": chat_id}, files=files)
                await _send(chat_id, "✅ پشتیبان با موفقیت ایجاد و ارسال شد.", _backup_menu_kb())
        else:
            await _send(chat_id, "❌ خطا در ایجاد پشتیبان.", _backup_menu_kb())
        return

    if data == "backup_list":
        backups = await backup_system.list_backups()
        if not backups:
            await _send(chat_id, "هیچ پشتیبان‌ی یافت نشد.", _backup_menu_kb())
            return
        
        msg = "📋 لیست پشتیبان‌ها:\n\n"
        for b in backups[:10]:
            size_mb = b['size'] / (1024 * 1024)
            msg += f"📄 {b['name']} ({size_mb:.1f} MB)\n"
            msg += f"   🕐 {b['modified'][:16]}\n\n"
        
        await _send(chat_id, msg, _backup_menu_kb())
        return

    # ── احراز هویت دو مرحله‌ای ──────────────────────────────────────────────────
    if data == "2fa":
        try:
            import pyotp
            secret_uri = tfa_system.enable_2fa(chat_id)
            import qrcode
            img = qrcode.make(secret_uri)
            buffer = BytesIO()
            img.save(buffer, 'PNG')
            buffer.seek(0)
            
            await _send_photo(chat_id, buffer, 
                "🔐 احراز هویت دو مرحله‌ای\n\n"
                "QR Code رو با Google Authenticator یا هر اپ مشابه اسکن کن.\n"
                "برای تایید، کد ۶ رقمی رو ارسال کن.",
                _main_menu_kb())
        except ImportError:
            await _send(chat_id, "❌ کتابخانه pyotp نصب نیست. لطفاً نصب کنید: pip install pyotp qrcode")
        return

    # ── گروه‌های ساب ──────────────────────────────────────────────────────────
    if data.startswith("subs:"):
        page = int(data.split(":", 1)[1] or 0)
        if not SUBS:
            await _edit(chat_id, message_id, "هنوز هیچ گروهی ساخته نشده.", _subs_list_kb(0))
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
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_sub_detail(sid, s), _sub_detail_kb(sid))
        return

    if data.startswith("subaddlink:"):
        _, sid, page_s = data.split(":", 2)
        if sid not in SUBS:
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        if not LINKS:
            await _edit(chat_id, message_id, "هنوز هیچ کانفیگی نداری.", _sub_detail_kb(sid))
            return
        _pending[chat_id] = {"action": "subaddlink_ctx", "sid": sid}
        await _edit(chat_id, message_id, "کدوم کانفیگ رو به این گروه اضافه کنم؟", _pick_link_for_group_kb(sid, int(page_s or 0)))
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
            await _answer_cb(cb_id, "این کانفیگ دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        s = SUBS.get(sid)
        await _edit(chat_id, message_id, f"✅ کانفیگ به گروه اضافه شد.\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if data.startswith("subdel:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف گروه «{s.get('name')}» مطمئنی؟", _confirm_subdel_kb(sid))
        return

    if data.startswith("subdelok:"):
        sid = data.split(":", 1)[1]
        name = await remove_sub_group(sid)
        if name is None:
            await _edit(chat_id, message_id, "این گروه قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 گروه «{name}» حذف شد.", _main_menu_kb())
        return

    # ── گروه یک کانفیگ خاص ────────────────────────────────────────────────────
    if data.startswith("cfggroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "cfg_group_ctx", "uid": uid}
        await _edit(chat_id, message_id, _format_cfg_group(uid), _cfg_group_kb(uid))
        return

    if data.startswith("cfgungroup:"):
        uid = data.split(":", 1)[1]
        await set_link_sub(uid, None)
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
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
            await _answer_cb(cb_id, "این گروه دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, f"✅ کانفیگ به گروه اضافه شد.\n\n{_format_cfg_group(uid)}", _cfg_group_kb(uid))
        return

    if data.startswith("cfgnewgroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": uid}
        await _edit(chat_id, message_id, "✏️ اسم گروه جدید رو بفرست:", _wizard_cancel_kb())
        return

    # ── ساخت کانفیگ جدید ──────────────────────────────────────────────────────
    if data == "newcfg":
        _pending[chat_id] = {"action": "wizard", "step": "label", "data": {}}
        await _edit(chat_id, message_id, _wizard_prompt("label", {}), _wizard_cancel_kb())
        return

    if data == "w:cancel":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "ساخت کانفیگ لغو شد.", _main_menu_kb())
        return

    if data.startswith("w:"):
        pending = _pending.get(chat_id)
        if not pending or pending.get("action") != "wizard":
            await _edit(chat_id, message_id, "این مرحله دیگه معتبر نیست.", _main_menu_kb())
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
            await _edit(chat_id, message_id, f"✅ کانفیگ ساخته شد.\n\n{_format_detail(uid, link)}", _link_detail_kb(uid, link["active"]))
            return

        await _answer_cb(cb_id, "این دکمه دیگه معتبر نیست.")
        return

    # ── نمایش جزئیات کانفیگ ──────────────────────────────────────────────────
    if data.startswith("view:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("toggle:"):
        uid = data.split(":", 1)[1]
        l = await set_link_active(uid, not LINKS.get(uid, {}).get("active", True))
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("link:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _answer_cb(cb_id, "کانفیگ پیدا نشد")
            return
        host = get_host()
        vless = vless_link_for_link(l, uid, host)
        sub_url = f"https://{host}/sub/{uid}"
        msg = f"🔗 لینک اتصال «{l.get('label')}»:\n\n<code>{vless}</code>\n\nلینک ساب ساده:\n<code>{sub_url}</code>"
        sid = l.get("sub_id")
        if sid and sid in SUBS:
            msg += f"\n\n✨ لینک ساب حرفه‌ای:\n<code>{_group_public_url(SUBS[sid])}</code>"
        await _send(chat_id, msg)
        return

    if data.startswith("del:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف «{l.get('label')}» مطمئنی؟", _confirm_delete_kb(uid))
        return

    if data.startswith("delok:"):
        uid = data.split(":", 1)[1]
        label = await remove_link(uid)
        if label is None:
            await _edit(chat_id, message_id, "این کانفیگ قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 کانفیگ «{label}» حذف شد.", _main_menu_kb())
        return

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
        logger.warning("Telegram bot: TELEGRAM_ADMIN_IDS تنظیم نشده")
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
