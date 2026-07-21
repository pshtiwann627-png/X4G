# pages.py  -  X4G v9.5
# شامل: LOGIN_HTML, DASHBOARD_HTML, get_public_page_html()

# لوگوی X4G (به‌صورت base64 داخلی، بدون نیاز به هاست خارجی)
LOGO_B64 = "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"


LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · X4G</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
/* ========================================
   طراحی شیشه‌ای آیفونی - X4G v9.5
   ======================================== */
*{margin:0;padding:0;box-sizing:border-box}
:root{
  /* ── دارک ── */
  --bg-dark:#0a0a0f;
  --glass-dark:rgba(255,255,255,0.05);
  --glass-border-dark:rgba(255,255,255,0.08);
  --glass-shadow-dark:0 8px 40px rgba(0,0,0,0.6);
  --text-dark:#f0f0f5;
  --text-dim-dark:rgba(255,255,255,0.4);
  --text-mid-dark:rgba(255,255,255,0.7);
  --accent-dark:#5b8def;
  --accent2-dark:#7aa3ff;
  
  /* ── روشن ── */
  --bg-light:#e8ecf2;
  --glass-light:rgba(255,255,255,0.6);
  --glass-border-light:rgba(255,255,255,0.7);
  --glass-shadow-light:0 8px 40px rgba(0,0,0,0.08);
  --text-light:#1a1a2e;
  --text-dim-light:rgba(0,0,0,0.3);
  --text-mid-light:rgba(0,0,0,0.55);
  --accent-light:#3b6fd4;
  --accent2-light:#5a88e8;

  /* ── متغیرهای جاری ── */
  --bg:var(--bg-dark);
  --glass:var(--glass-dark);
  --glass-border:var(--glass-border-dark);
  --glass-shadow:var(--glass-shadow-dark);
  --text:var(--text-dark);
  --text-dim:var(--text-dim-dark);
  --text-mid:var(--text-mid-dark);
  --accent:var(--accent-dark);
  --accent2:var(--accent2-dark);
  --transition:all 0.4s cubic-bezier(0.4,0,0.2,1);
}

[data-theme="light"]{
  --bg:var(--bg-light);
  --glass:var(--glass-light);
  --glass-border:var(--glass-border-light);
  --glass-shadow:var(--glass-shadow-light);
  --text:var(--text-light);
  --text-dim:var(--text-dim-light);
  --text-mid:var(--text-mid-light);
  --accent:var(--accent-light);
  --accent2:var(--accent2-light);
}

html,body{height:100%;overflow:hidden}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px;
  transition:var(--transition);
}

/* ── پس‌زمینه ── */
.bg{
  position:fixed;
  inset:0;
  background:
    radial-gradient(ellipse 70% 50% at 50% -10%, rgba(91,141,239,0.12), transparent 65%),
    var(--bg);
  z-index:0;
  transition:var(--transition);
}

/* ── گرید ظریف ── */
.grid{
  position:fixed;
  inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size:48px 48px;
  z-index:0;
}

/* ── دایره‌های نورانی ── */
.orb{
  position:fixed;
  border-radius:50%;
  filter:blur(100px);
  z-index:0;
  animation:float 14s ease-in-out infinite;
  opacity:0.5;
}
.o1{
  width:400px;height:400px;
  background:rgba(91,141,239,0.08);
  top:-120px;right:-100px;
  animation-delay:0s;
}
.o2{
  width:320px;height:320px;
  background:rgba(139,92,246,0.06);
  bottom:-80px;left:-80px;
  animation-delay:5s;
}
.o3{
  width:200px;height:200px;
  background:rgba(16,185,129,0.04);
  top:50%;left:50%;
  transform:translate(-50%,-50%);
  animation-delay:9s;
  filter:blur(120px);
}
@keyframes float{
  0%,100%{transform:translateY(0) scale(1)}
  33%{transform:translateY(-30px) scale(1.05)}
  66%{transform:translateY(20px) scale(0.95)}
}

/* ── ذرات ── */
.particles{
  position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden
}
.particle{
  position:absolute;
  width:2px;height:2px;
  background:rgba(255,255,255,0.15);
  border-radius:50%;
  animation:twinkle var(--d) ease-in-out infinite alternate;
}
.particle:nth-child(1){top:10%;left:20%;--d:3s;animation-delay:0s}
.particle:nth-child(2){top:30%;right:15%;--d:4s;animation-delay:1s}
.particle:nth-child(3){bottom:25%;left:10%;--d:3.5s;animation-delay:0.5s}
.particle:nth-child(4){top:60%;right:25%;--d:4.5s;animation-delay:2s}
.particle:nth-child(5){bottom:40%;right:5%;--d:3.2s;animation-delay:0.8s}
.particle:nth-child(6){top:15%;left:50%;--d:5s;animation-delay:1.5s}
.particle:nth-child(7){bottom:15%;left:40%;--d:3.8s;animation-delay:0.3s}
.particle:nth-child(8){top:45%;left:5%;--d:4.2s;animation-delay:1.8s}
@keyframes twinkle{
  0%{opacity:0.05;transform:scale(0.3)}
  100%{opacity:0.5;transform:scale(1.2)}
}

/* ── کارت ورود ── */
.wrap{
  position:relative;
  z-index:10;
  width:100%;
  max-width:400px;
  animation:fadeUp 0.9s cubic-bezier(0.16,1,0.3,1);
}
@keyframes fadeUp{
  from{opacity:0;transform:translateY(30px) scale(0.96)}
  to{opacity:1;transform:translateY(0) scale(1)}
}

.card{
  background:var(--glass);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  border:1px solid var(--glass-border);
  border-radius:28px;
  padding:44px 36px 38px;
  box-shadow:var(--glass-shadow);
  position:relative;
  overflow:hidden;
  transition:var(--transition);
}

/* ── درخشش کارت ── */
.card-glow{
  position:absolute;
  top:-60px;right:-60px;
  width:260px;height:260px;
  background:radial-gradient(circle,var(--accent),transparent 70%);
  opacity:0.06;
  pointer-events:none;
  animation:pulseGlow 8s ease-in-out infinite;
}
@keyframes pulseGlow{
  0%,100%{transform:scale(1);opacity:0.04}
  50%{transform:scale(1.2);opacity:0.08}
}

/* ── برند ── */
.brand{
  display:flex;
  align-items:center;
  gap:16px;
  margin-bottom:32px;
  position:relative;
  z-index:1;
}
.brand-img{
  width:56px;height:56px;
  border-radius:50%;
  overflow:hidden;
  border:2px solid var(--glass-border);
  box-shadow:0 0 40px rgba(91,141,239,0.15);
  flex-shrink:0;
  transition:var(--transition);
}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{
  font-size:20px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.02em;
  background:linear-gradient(135deg,var(--text),var(--accent2));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  transition:var(--transition);
}
.brand-sub{
  font-size:11px;
  color:var(--text-dim);
  margin-top:2px;
  font-weight:500;
  letter-spacing:0.04em;
  transition:var(--transition);
}

/* ── عنوان ── */
h1{
  font-size:22px;
  font-weight:800;
  color:var(--text);
  margin-bottom:6px;
  letter-spacing:-0.02em;
  position:relative;
  z-index:1;
  transition:var(--transition);
}
h1 i{color:var(--accent);margin-left:8px}
.sub{
  font-size:12.5px;
  color:var(--text-mid);
  margin-bottom:28px;
  line-height:1.7;
  position:relative;
  z-index:1;
  transition:var(--transition);
}

/* ── باکس رمز ── */
.hint{
  display:flex;
  align-items:center;
  gap:12px;
  background:rgba(91,141,239,0.06);
  border:1px solid rgba(91,141,239,0.1);
  border-radius:14px;
  padding:12px 16px;
  margin-bottom:24px;
  position:relative;
  z-index:1;
  transition:var(--transition);
}
.hint:hover{
  background:rgba(91,141,239,0.08);
  border-color:rgba(91,141,239,0.18);
}
.hint-label{
  font-size:11px;
  color:var(--text-dim);
  flex:1;
  display:flex;
  align-items:center;
  gap:6px;
  transition:var(--transition);
}
.hint-label i{color:var(--accent);font-size:14px}
.hint-val{
  font-family:ui-monospace,monospace;
  font-size:13px;
  font-weight:700;
  color:var(--accent);
  background:rgba(91,141,239,0.08);
  border:1px solid rgba(91,141,239,0.15);
  padding:4px 14px;
  border-radius:10px;
  cursor:pointer;
  transition:all 0.25s;
  letter-spacing:0.06em;
  position:relative;
  overflow:hidden;
}
.hint-val::before{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(90deg,transparent,rgba(91,141,239,0.08),transparent);
  transform:translateX(-100%);
  transition:0.6s;
}
.hint-val:hover::before{transform:translateX(100%)}
.hint-val:hover{
  background:rgba(91,141,239,0.14);
  transform:scale(1.02);
}

/* ── فیلد رمز ── */
.field{
  margin-bottom:20px;
  position:relative;
  z-index:1;
}
.field label{
  display:block;
  font-size:10.5px;
  font-weight:700;
  color:var(--text-mid);
  margin-bottom:8px;
  text-transform:uppercase;
  letter-spacing:0.06em;
  display:flex;
  align-items:center;
  gap:6px;
  transition:var(--transition);
}
.field label i{font-size:13px;color:var(--accent)}
.inp-wrap{
  position:relative;
  border-radius:16px;
  background:rgba(255,255,255,0.03);
  border:1.5px solid var(--glass-border);
  transition:var(--transition);
}
.inp-wrap:focus-within{
  border-color:var(--accent);
  background:rgba(255,255,255,0.05);
  box-shadow:0 0 0 4px rgba(91,141,239,0.05);
}
input[type=password],input[type=text]{
  width:100%;
  padding:14px 48px 14px 18px;
  border:none;
  background:transparent;
  color:var(--text);
  font-family:inherit;
  font-size:14px;
  outline:none;
  letter-spacing:0.02em;
  transition:var(--transition);
}
input[type=password]::placeholder,input[type=text]::placeholder{
  color:var(--text-dim);
  opacity:0.5;
}
.ic{
  position:absolute;
  left:16px;
  top:50%;
  transform:translateY(-50%);
  color:var(--text-dim);
  font-size:17px;
  pointer-events:none;
  transition:var(--transition);
}
.inp-wrap:focus-within .ic{color:var(--accent);transform:translateY(-50%) scale(1.05)}

/* ── دکمه نمایش رمز ── */
.pw-toggle{
  position:absolute;
  left:14px;
  top:50%;
  transform:translateY(-50%);
  background:none;
  border:none;
  color:var(--text-dim);
  cursor:pointer;
  font-size:17px;
  padding:4px;
  transition:var(--transition);
  display:flex;
  align-items:center;
  z-index:2;
}
.pw-toggle:hover{color:var(--accent2);transform:translateY(-50%) scale(1.05)}

/* ── خطا ── */
.err{
  display:none;
  background:rgba(239,68,68,0.06);
  border:1px solid rgba(239,68,68,0.12);
  border-radius:14px;
  padding:12px 16px;
  margin-bottom:16px;
  font-size:12px;
  color:#f87171;
  align-items:center;
  gap:10px;
  animation:shake 0.4s ease;
  position:relative;
  z-index:1;
}
.err.show{display:flex}
@keyframes shake{
  0%,100%{transform:translateX(0)}
  20%{transform:translateX(-6px)}
  40%{transform:translateX(6px)}
  60%{transform:translateX(-4px)}
  80%{transform:translateX(4px)}
}
.err i{font-size:17px}

/* ── دکمه ورود ── */
.btn{
  width:100%;
  padding:15px;
  border-radius:16px;
  border:none;
  cursor:pointer;
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  color:#fff;
  font-family:inherit;
  font-size:14px;
  font-weight:700;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  box-shadow:0 6px 30px rgba(91,141,239,0.25);
  transition:all 0.3s cubic-bezier(0.4,0,0.2,1);
  position:relative;
  overflow:hidden;
  z-index:1;
}
.btn::before{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.1),rgba(255,255,255,0.02));
  opacity:0;
  transition:0.4s;
}
.btn:hover::before{opacity:1}
.btn:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 40px rgba(91,141,239,0.35);
}
.btn:active{transform:translateY(0) scale(0.98)}
.btn:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.btn i{font-size:17px;transition:0.3s}
.btn:hover i{transform:translateX(-4px)}

/* ── بارگذاری ── */
.loading-dots{
  display:inline-flex;
  gap:4px;
  align-items:center;
}
.loading-dots span{
  width:7px;height:7px;
  border-radius:50%;
  background:#fff;
  animation:dotBounce 1.2s ease-in-out infinite;
}
.loading-dots span:nth-child(2){animation-delay:0.2s}
.loading-dots span:nth-child(3){animation-delay:0.4s}
@keyframes dotBounce{
  0%,80%,100%{transform:scale(0.5);opacity:0.3}
  40%{transform:scale(1);opacity:1}
}

/* ── فوتر ── */
.footer{
  margin-top:28px;
  padding-top:20px;
  border-top:1px solid var(--glass-border);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  font-size:11px;
  color:var(--text-dim);
  position:relative;
  z-index:1;
  transition:var(--transition);
}
.footer a{
  color:var(--accent);
  font-weight:600;
  text-decoration:none;
  display:flex;
  align-items:center;
  gap:5px;
  transition:all 0.3s;
  padding:4px 10px;
  border-radius:10px;
}
.footer a:hover{
  background:rgba(91,141,239,0.06);
  color:var(--accent2);
  transform:translateY(-1px);
}
.footer .divider{
  width:1px;
  height:16px;
  background:var(--glass-border);
}

/* ── نسخه ── */
.version-badge{
  position:fixed;
  bottom:24px;right:24px;
  z-index:5;
  font-size:10px;
  color:var(--text-dim);
  background:var(--glass);
  backdrop-filter:blur(12px);
  padding:6px 16px;
  border-radius:24px;
  border:1px solid var(--glass-border);
  display:flex;
  align-items:center;
  gap:6px;
  transition:var(--transition);
}
.version-badge i{font-size:11px;color:var(--accent)}

/* ── دکمه تم ── */
.theme-toggle{
  position:fixed;
  top:24px;right:24px;
  z-index:5;
  width:40px;height:40px;
  border-radius:50%;
  background:var(--glass);
  backdrop-filter:blur(12px);
  border:1px solid var(--glass-border);
  color:var(--text-mid);
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:18px;
  transition:all 0.3s;
}
.theme-toggle:hover{
  transform:scale(1.05);
  background:rgba(255,255,255,0.08);
  color:var(--accent);
}

@keyframes spin{to{transform:rotate(360deg)}}

/* ── ریسپانسیو ── */
@media(max-width:480px){
  .card{padding:32px 22px 28px}
  .brand-img{width:44px;height:44px}
  .brand-name{font-size:17px}
  h1{font-size:19px}
  .version-badge{bottom:16px;right:16px;padding:4px 12px;font-size:9px}
  .theme-toggle{top:16px;right:16px;width:36px;height:36px;font-size:16px}
}
</style>
</head>
<body>
<div class="bg"></div>
<div class="grid"></div>
<div class="orb o1"></div>
<div class="orb o2"></div>
<div class="orb o3"></div>

<div class="particles">
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
  <span class="particle"></span>
</div>

<button class="theme-toggle" onclick="toggleTheme()" title="تغییر تم">
  <i class="ti ti-sun" id="theme-icon"></i>
</button>

<div class="version-badge"><i class="ti ti-rocket"></i> X4G v9.5</div>

<div class="wrap">
  <div class="card">
    <div class="card-glow"></div>
    <div class="brand">
      <div class="brand-img"><img src="data:image/png;base64,__LOGO_B64__" alt="X4G"></div>
      <div>
        <div class="brand-name">X4G</div>
        <div class="brand-sub">⚡ پنل مدیریت پیشرفته</div>
      </div>
    </div>
    <h1><i class="ti ti-shield-lock"></i> ورود به پنل</h1>
    <p class="sub">🔐 رمز عبور را برای دسترسی به داشبورد وارد کنید</p>

    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>

    <div class="hint">
      <span class="hint-label"><i class="ti ti-key"></i> رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="fillPassword('X4GKING')">X4GKING</span>
    </div>

    <form id="form" autocomplete="off">
      <div class="field">
        <label><i class="ti ti-lock"></i> رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="••••••••" autofocus required>
          <button type="button" class="pw-toggle" onclick="togglePassword()" title="نمایش/مخفی کردن رمز">
            <i class="ti ti-eye" id="pw-eye"></i>
          </button>
          <i class="ti ti-key ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn">
        <i class="ti ti-login-2"></i>
        <span id="btn-text">ورود به داشبورد</span>
      </button>
    </form>

    <div class="footer">
      <span>پشتیبانی</span>
      <span class="divider"></span>
      <a href="https://t.me/Farajian2004f" target="_blank">
        <i class="ti ti-brand-telegram"></i> @Farajian2004f
      </a>
    </div>
  </div>
</div>

<script>
// ── تم ──
let isDark = localStorage.getItem('x4g-theme') !== 'light';
function applyTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  document.getElementById('theme-icon').className = 'ti ' + (dark ? 'ti-sun' : 'ti-moon');
}
function toggleTheme() {
  isDark = !isDark;
  localStorage.setItem('x4g-theme', isDark ? 'dark' : 'light');
  applyTheme(isDark);
}
applyTheme(isDark);

// ── پر کردن رمز ──
function fillPassword(pw) {
  const input = document.getElementById('pw');
  input.value = pw;
  input.focus();
  const wrap = input.closest('.inp-wrap');
  wrap.style.borderColor = 'var(--accent)';
  setTimeout(() => { wrap.style.borderColor = ''; }, 800);
}

// ── نمایش/مخفی کردن رمز ──
function togglePassword() {
  const input = document.getElementById('pw');
  const icon = document.getElementById('pw-eye');
  const toText = input.type === 'password';
  input.type = toText ? 'text' : 'password';
  icon.className = 'ti ' + (toText ? 'ti-eye-off' : 'ti-eye');
  input.focus();
}

// ── فوکوس ──
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('pw').focus();
});

// ── ارسال فرم ──
document.getElementById('form').addEventListener('submit', async e => {
  e.preventDefault();
  const btn = document.getElementById('btn');
  const err = document.getElementById('err');
  const et = document.getElementById('err-text');
  const pw = document.getElementById('pw');

  err.classList.remove('show');
  btn.disabled = true;

  btn.innerHTML = `
    <div class="loading-dots">
      <span></span><span></span><span></span>
    </div>
    <span id="btn-text">در حال ورود...</span>
  `;

  try {
    const r = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw.value })
    });

    if (!r.ok) {
      const d = await r.json().catch(() => ({}));
      throw new Error(d.detail || 'رمز عبور اشتباه است');
    }

    btn.innerHTML = '<i class="ti ti-circle-check"></i> <span id="btn-text">ورود موفق ✓</span>';
    btn.style.background = 'linear-gradient(135deg,#10B981,#059669)';
    btn.style.boxShadow = '0 6px 30px rgba(16,185,129,0.4)';

    setTimeout(() => { location.href = '/dashboard'; }, 600);

  } catch (e) {
    et.textContent = e.message;
    err.classList.add('show');

    btn.disabled = false;
    btn.innerHTML = '<i class="ti ti-login-2"></i> <span id="btn-text">ورود به داشبورد</span>';
    btn.style.background = '';
    btn.style.boxShadow = '';

    const wrap = pw.closest('.inp-wrap');
    wrap.style.borderColor = 'rgba(239,68,68,0.4)';
    setTimeout(() => { wrap.style.borderColor = ''; }, 800);
    pw.focus();
    pw.select();
  }
});

document.getElementById('pw').addEventListener('input', () => {
  document.getElementById('err').classList.remove('show');
});

document.getElementById('pw').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    document.getElementById('form').dispatchEvent(new Event('submit'));
  }
});

console.log('⚡ X4G v9.5 — پنل مدیریت پیشرفته');
console.log('🔐 رمز پیش‌فرض: X4GKING');
</script>
</body></html>"""
LOGIN_HTML = LOGIN_HTML.replace("__LOGO_B64__", LOGO_B64)


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>X4G</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
/* ═══════════════════════════════════════════════════════════════════════════════
   طراحی شیشه‌ای آیفونی - داشبورد X4G v9.5
   ═══════════════════════════════════════════════════════════════════════════════ */
*{margin:0;padding:0;box-sizing:border-box}

:root{
  /* ── دارک ── */
  --bg-dark:#0a0a12;
  --bg2-dark:#0f0f1a;
  --bg3-dark:#141420;
  --glass-dark:rgba(255,255,255,0.04);
  --glass-border-dark:rgba(255,255,255,0.06);
  --glass-shadow-dark:0 8px 40px rgba(0,0,0,0.5);
  --text-dark:#eeeff5;
  --text2-dark:rgba(255,255,255,0.7);
  --text3-dark:rgba(255,255,255,0.35);
  --accent-dark:#5b8def;
  --accent2-dark:#7aa3ff;
  --accent-d-dark:rgba(91,141,239,0.08);
  --green-dark:#2dd4a0;
  --green-bg-dark:rgba(45,212,160,0.08);
  --green-t-dark:#5be0b0;
  --red-dark:#f87171;
  --red-bg-dark:rgba(248,113,113,0.08);
  --red-t-dark:#fb9292;
  --amber-dark:#fbbf24;
  --amber-bg-dark:rgba(251,191,36,0.08);
  --amber-t-dark:#fcd34d;
  --purple-dark:#a78bfa;
  --purple-bg-dark:rgba(167,139,250,0.08);

  /* ── روشن ── */
  --bg-light:#eef0f5;
  --bg2-light:#e4e7ef;
  --bg3-light:#d8dce8;
  --glass-light:rgba(255,255,255,0.6);
  --glass-border-light:rgba(255,255,255,0.7);
  --glass-shadow-light:0 8px 40px rgba(0,0,0,0.06);
  --text-light:#12121e;
  --text2-light:rgba(0,0,0,0.65);
  --text3-light:rgba(0,0,0,0.3);
  --accent-light:#3b6fd4;
  --accent2-light:#5a88e8;
  --accent-d-light:rgba(59,111,212,0.06);
  --green-light:#0d9e6e;
  --green-bg-light:rgba(13,158,110,0.06);
  --green-t-light:#0a805a;
  --red-light:#dc2626;
  --red-bg-light:rgba(220,38,38,0.06);
  --red-t-light:#b91c1c;
  --amber-light:#d97706;
  --amber-bg-light:rgba(217,119,6,0.06);
  --amber-t-light:#b45309;
  --purple-light:#7c3aed;
  --purple-bg-light:rgba(124,58,237,0.06);

  /* ── متغیرهای جاری ── */
  --bg:var(--bg-dark);
  --bg2:var(--bg2-dark);
  --bg3:var(--bg3-dark);
  --glass:var(--glass-dark);
  --glass-border:var(--glass-border-dark);
  --glass-shadow:var(--glass-shadow-dark);
  --text:var(--text-dark);
  --text2:var(--text2-dark);
  --text3:var(--text3-dark);
  --accent:var(--accent-dark);
  --accent2:var(--accent2-dark);
  --accent-d:var(--accent-d-dark);
  --green:var(--green-dark);
  --green-bg:var(--green-bg-dark);
  --green-t:var(--green-t-dark);
  --red:var(--red-dark);
  --red-bg:var(--red-bg-dark);
  --red-t:var(--red-t-dark);
  --amber:var(--amber-dark);
  --amber-bg:var(--amber-bg-dark);
  --amber-t:var(--amber-t-dark);
  --purple:var(--purple-dark);
  --purple-bg:var(--purple-bg-dark);
  --sidebar-w:248px;
  --radius:16px;
  --shadow:0 8px 32px rgba(0,0,0,0.25);
  --transition:all 0.35s cubic-bezier(0.4,0,0.2,1);
}

[data-theme="light"]{
  --bg:var(--bg-light);
  --bg2:var(--bg2-light);
  --bg3:var(--bg3-light);
  --glass:var(--glass-light);
  --glass-border:var(--glass-border-light);
  --glass-shadow:var(--glass-shadow-light);
  --text:var(--text-light);
  --text2:var(--text2-light);
  --text3:var(--text3-light);
  --accent:var(--accent-light);
  --accent2:var(--accent2-light);
  --accent-d:var(--accent-d-light);
  --green:var(--green-light);
  --green-bg:var(--green-bg-light);
  --green-t:var(--green-t-light);
  --red:var(--red-light);
  --red-bg:var(--red-bg-light);
  --red-t:var(--red-t-light);
  --amber:var(--amber-light);
  --amber-bg:var(--amber-bg-light);
  --amber-t:var(--amber-t-light);
  --purple:var(--purple-light);
  --purple-bg:var(--purple-bg-light);
}

html,body{height:100%}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  display:flex;
  font-size:14px;
  transition:var(--transition);
}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--text3);border-radius:2px}

a{color:inherit;text-decoration:none}

/* ═══════════════════════════════════════════════════════════════════════════════
   سایدبار شیشه‌ای
   ═══════════════════════════════════════════════════════════════════════════════ */
.sidebar{
  width:var(--sidebar-w);
  min-height:100vh;
  background:var(--glass);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border-left:1px solid var(--glass-border);
  display:flex;
  flex-direction:column;
  flex-shrink:0;
  position:fixed;
  right:0;top:0;bottom:0;
  z-index:200;
  transition:var(--transition);
}

.logo{
  display:flex;
  align-items:center;
  gap:12px;
  padding:20px 16px 16px;
  border-bottom:1px solid var(--glass-border);
}
.logo-img{
  width:38px;height:38px;
  border-radius:50%;
  overflow:hidden;
  border:1px solid var(--glass-border);
  box-shadow:0 0 30px rgba(91,141,239,0.1);
  flex-shrink:0;
}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{
  font-size:14px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.02em;
}
.logo-sub{
  font-size:9.5px;
  color:var(--text3);
  margin-top:1px;
}

.sb-close{
  display:none;
  position:absolute;
  left:12px;top:20px;
  background:var(--glass);
  border:1px solid var(--glass-border);
  color:var(--text3);
  width:30px;height:30px;
  border-radius:10px;
  font-size:16px;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  transition:var(--transition);
}
.sb-close:hover{background:rgba(239,68,68,0.06);color:var(--red)}

.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{
  padding:16px 14px 6px;
  font-size:8.5px;
  letter-spacing:0.12em;
  text-transform:uppercase;
  color:var(--text3);
  font-weight:700;
}
.nav-it{
  display:flex;
  align-items:center;
  gap:10px;
  padding:9px 14px;
  color:var(--text3);
  font-size:12.5px;
  cursor:pointer;
  border-right:2px solid transparent;
  transition:var(--transition);
  margin:2px 6px;
  border-radius:10px;
}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{
  background:var(--accent-d);
  color:var(--text2);
}
.nav-it.on{
  background:var(--accent-d);
  color:var(--text);
  border-right-color:var(--accent);
  font-weight:600;
}
.nav-badge{
  margin-right:auto;
  background:var(--accent-d);
  color:var(--accent2);
  font-size:8.5px;
  padding:1px 8px;
  border-radius:12px;
  font-weight:700;
}

.sb-foot{
  padding:12px 14px;
  border-top:1px solid var(--glass-border);
}
.theme-btn{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  background:var(--accent-d);
  color:var(--text2);
  border-radius:12px;
  padding:9px;
  font-size:11.5px;
  font-weight:600;
  font-family:inherit;
  border:1px solid var(--glass-border);
  cursor:pointer;
  width:100%;
  transition:var(--transition);
  margin-bottom:8px;
}
.theme-btn:hover{background:var(--glass);color:var(--text)}
.logout-btn{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:7px;
  background:var(--red-bg);
  color:var(--red-t);
  border-radius:12px;
  padding:9px;
  font-size:11.5px;
  font-weight:600;
  font-family:inherit;
  border:1px solid rgba(239,68,68,0.08);
  cursor:pointer;
  width:100%;
  transition:var(--transition);
}
.logout-btn:hover{background:rgba(239,68,68,0.12)}

/* ═══════════════════════════════════════════════════════════════════════════════
   هدر موبایل
   ═══════════════════════════════════════════════════════════════════════════════ */
.mob-top{
  display:none;
  position:fixed;
  top:0;right:0;left:0;
  height:54px;
  background:var(--glass);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  border-bottom:1px solid var(--glass-border);
  z-index:150;
  align-items:center;
  justify-content:space-between;
  padding:0 14px;
  transition:var(--transition);
}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{
  width:28px;height:28px;
  border-radius:50%;
  overflow:hidden;
  box-shadow:0 0 20px rgba(91,141,239,0.1);
}
.mob-logo img{width:100%;height:100%;object-fit:cover}
.mob-title{
  color:var(--text);
  font-size:13px;
  font-weight:700;
}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{
  background:var(--glass);
  border:1px solid var(--glass-border);
  color:var(--text3);
  width:34px;height:34px;
  border-radius:10px;
  font-size:16px;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  transition:var(--transition);
}
.menu-btn:hover,.theme-mob:hover{
  background:var(--accent-d);
  color:var(--accent2);
}

.overlay{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.5);
  backdrop-filter:blur(4px);
  z-index:190;
}
.overlay.show{display:block}

/* ═══════════════════════════════════════════════════════════════════════════════
   محتوای اصلی
   ═══════════════════════════════════════════════════════════════════════════════ */
.main{
  margin-right:var(--sidebar-w);
  flex:1;
  padding:28px 28px 60px;
  min-width:0;
  transition:var(--transition);
}

.pg{display:none}
.pg.on{
  display:block;
  animation:fadeIn 0.3s ease;
}
@keyframes fadeIn{
  from{opacity:0;transform:translateY(8px)}
  to{opacity:1;transform:translateY(0)}
}

/* ── هدر ── */
.topbar{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  margin-bottom:24px;
  flex-wrap:wrap;
  gap:12px;
}
.tb-title{
  font-size:18px;
  font-weight:800;
  color:var(--text);
  display:flex;
  align-items:center;
  gap:8px;
  letter-spacing:-0.02em;
}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{
  font-size:11px;
  color:var(--text3);
  margin-top:4px;
}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}

/* ── بج‌ها ── */
.badge{
  font-size:10px;
  padding:3px 12px;
  border-radius:20px;
  font-weight:700;
  display:inline-flex;
  align-items:center;
  gap:5px;
  white-space:nowrap;
  backdrop-filter:blur(8px);
}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:var(--purple)}

.dot{
  width:5px;height:5px;
  border-radius:50%;
  flex-shrink:0;
  display:inline-block;
}
.dg{background:var(--green)}
.dr{background:var(--red)}
.da{background:var(--amber)}
.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}

/* ═══════════════════════════════════════════════════════════════════════════════
   کارت‌های متریک
   ═══════════════════════════════════════════════════════════════════════════════ */
.metrics{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px;
  margin-bottom:20px;
}
.metric{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:18px 18px 15px;
  transition:var(--transition);
  position:relative;
  overflow:hidden;
  cursor:default;
}
.metric::after{
  content:'';
  position:absolute;
  top:0;right:0;
  width:3px;
  height:100%;
  background:var(--accent);
  opacity:0;
  transition:var(--transition);
}
.metric:hover{
  border-color:rgba(255,255,255,0.08);
  transform:translateY(-2px);
  box-shadow:var(--shadow);
}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}

.m-icon{
  width:34px;height:34px;
  border-radius:10px;
  background:var(--accent-d);
  display:flex;
  align-items:center;
  justify-content:center;
  margin-bottom:10px;
  color:var(--accent);
  font-size:16px;
}
.m-icon.suc{background:var(--green-bg);color:var(--green-t)}
.m-icon.dan{background:var(--red-bg);color:var(--red-t)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}

.m-label{
  font-size:10px;
  color:var(--text3);
  margin-bottom:5px;
  font-weight:600;
  text-transform:uppercase;
  letter-spacing:0.05em;
}
.m-val{
  font-size:24px;
  font-weight:800;
  color:var(--text);
  line-height:1;
  letter-spacing:-0.02em;
}
.m-unit{font-size:12px;font-weight:400;color:var(--text3)}
.m-sub{
  font-size:10px;
  color:var(--text3);
  margin-top:6px;
  display:flex;
  align-items:center;
  gap:3px;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   باکس VLESS
   ═══════════════════════════════════════════════════════════════════════════════ */
.vless-box{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:20px 22px;
  margin-bottom:20px;
  box-shadow:var(--shadow);
  position:relative;
  overflow:hidden;
  transition:var(--transition);
}
.vless-box::before{
  content:'';
  position:absolute;
  top:-40px;left:-40px;
  width:160px;height:160px;
  background:radial-gradient(circle,var(--accent-d),transparent 70%);
  pointer-events:none;
}
.vl-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:12px;
  flex-wrap:wrap;
  gap:8px;
}
.vl-title{
  color:var(--text2);
  font-size:11px;
  display:flex;
  align-items:center;
  gap:6px;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{
  background:rgba(0,0,0,0.12);
  border:1px solid var(--glass-border);
  border-radius:12px;
  padding:13px 15px;
  font-size:10.5px;
  font-family:ui-monospace,monospace;
  color:var(--accent2);
  word-break:break-all;
  line-height:1.8;
}
[data-theme="light"] .vl-code{background:rgba(0,0,0,0.04)}
.vl-actions{
  display:flex;
  gap:8px;
  margin-top:12px;
  flex-wrap:wrap;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   دکمه‌ها
   ═══════════════════════════════════════════════════════════════════════════════ */
.btn{
  font-family:inherit;
  font-size:12px;
  font-weight:600;
  border-radius:12px;
  padding:8px 16px;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:5px;
  border:none;
  transition:var(--transition);
  white-space:nowrap;
}
.btn i{font-size:13px}
.btn:disabled{opacity:0.4;cursor:not-allowed}

.btn-p{
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  color:#fff;
  box-shadow:0 4px 16px rgba(91,141,239,0.2);
}
.btn-p:hover{
  transform:translateY(-1px);
  box-shadow:0 6px 24px rgba(91,141,239,0.3);
}

.btn-o{
  background:var(--glass);
  border:1px solid var(--glass-border);
  color:var(--text2);
}
.btn-o:hover{background:var(--accent-d);border-color:rgba(255,255,255,0.08)}

.btn-g{
  background:var(--accent-d);
  color:var(--accent2);
  border:1px solid rgba(91,141,239,0.06);
}
.btn-g:hover{background:rgba(91,141,239,0.12)}

.btn-d{
  background:var(--red-bg);
  color:var(--red-t);
  border:1px solid rgba(248,113,113,0.06);
}
.btn-d:hover{background:rgba(248,113,113,0.12)}

.btn-pur{
  background:var(--purple-bg);
  color:var(--purple);
  border:1px solid rgba(167,139,250,0.06);
}
.btn-pur:hover{background:rgba(167,139,250,0.12)}

.btn-amber{
  background:var(--amber-bg);
  color:var(--amber-t);
  border:1px solid rgba(251,191,36,0.06);
}
.btn-amber:hover{background:rgba(251,191,36,0.12)}

.btn-sm{padding:4px 10px;font-size:10.5px;border-radius:10px}
.btn-icon{width:30px;height:30px;padding:0;justify-content:center}

/* ═══════════════════════════════════════════════════════════════════════════════
   کارت‌ها
   ═══════════════════════════════════════════════════════════════════════════════ */
.card{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:18px 20px;
  transition:var(--transition);
}
.card:hover{border-color:rgba(255,255,255,0.06)}
.card-title{
  font-size:12.5px;
  font-weight:700;
  color:var(--text);
  margin-bottom:14px;
  display:flex;
  align-items:center;
  gap:7px;
}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-right:auto}

.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:18px}
.mb16{margin-bottom:16px}

.sr{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:9px 0;
  border-bottom:1px solid var(--glass-border);
  font-size:12px;
}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--text2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--text3)}
.sr-v{color:var(--text);font-weight:600;font-size:11.5px}

.ch{position:relative;height:230px}
.ch-lg{position:relative;height:330px}
.ch-sm{position:relative;height:185px}

.exp-chip{
  font-size:9px;
  padding:3px 10px;
  border-radius:8px;
  font-weight:700;
  display:inline-flex;
  align-items:center;
  gap:3px;
}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}

.tog{
  width:19px;height:30px;
  border-radius:15px;
  background:var(--text3);
  position:relative;
  cursor:pointer;
  transition:var(--transition);
  flex-shrink:0;
  border:none;
  opacity:0.4;
}
.tog::after{
  content:'';
  position:absolute;
  width:12px;height:12px;
  border-radius:50%;
  background:#fff;
  left:3px;bottom:3px;
  transition:var(--transition);
  box-shadow:0 1px 4px rgba(0,0,0,0.2);
}
.tog.on{opacity:1;background:var(--green)}
.tog.on::after{bottom:14px}

/* ── فرم‌ها ── */
.form-row{
  display:flex;
  gap:9px;
  flex-wrap:wrap;
  align-items:flex-end;
}
.fg{
  display:flex;
  flex-direction:column;
  gap:5px;
}
.fg label{
  font-size:10px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.fi,.fs{
  padding:9px 14px;
  border-radius:12px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.08);
  color:var(--text);
  font-family:inherit;
  font-size:12px;
  outline:none;
  transition:var(--transition);
  min-width:100px;
}
.fi::placeholder{color:var(--text3)}
.fi:focus,.fs:focus{
  border-color:var(--accent);
  background:rgba(0,0,0,0.12);
  box-shadow:0 0 0 3px var(--accent-d);
}
.fs option{background:var(--bg2)}
[data-theme="light"] .fs option{background:#fff}

.cl{
  background:var(--accent-d);
  border:1px solid var(--glass-border);
  border-radius:12px;
  padding:11px 14px;
  font-size:11px;
  color:var(--text2);
  display:flex;
  gap:9px;
  align-items:flex-start;
  line-height:1.8;
  margin-top:12px;
}
.cl i{font-size:15px;color:var(--accent);margin-top:1px;flex-shrink:0}
.cl.amber{
  background:var(--amber-bg);
  border-color:rgba(251,191,36,0.06);
  color:var(--amber-t);
}
.cl.amber i{color:var(--amber)}

.chip-row{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  margin-top:8px;
}
.chip{
  font-size:10.5px;
  font-weight:700;
  padding:5px 14px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--text2);
  border:1px solid var(--glass-border);
  cursor:pointer;
  transition:var(--transition);
  white-space:nowrap;
}
.chip:hover{background:rgba(91,141,239,0.12);color:var(--accent2)}
.chip.active{
  background:var(--accent);
  color:#fff;
  border-color:var(--accent);
  box-shadow:0 4px 16px rgba(91,141,239,0.2);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   پنل ساخت کانفیگ
   ═══════════════════════════════════════════════════════════════════════════════ */
.create-panel{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:22px;
  padding:0;
  overflow:hidden;
  box-shadow:var(--shadow);
  margin-bottom:18px;
  position:relative;
}
.create-panel::before{
  content:'';
  position:absolute;
  top:-60px;left:-60px;
  width:200px;height:200px;
  background:radial-gradient(circle,var(--accent-d),transparent 70%);
  pointer-events:none;
}
.cp-head{
  display:flex;
  align-items:center;
  gap:14px;
  padding:22px 24px 18px;
  position:relative;
  z-index:1;
}
.cp-head-icon{
  width:44px;height:44px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:20px;
  flex-shrink:0;
  box-shadow:0 6px 24px rgba(91,141,239,0.2);
}
.cp-head-text{flex:1;min-width:0}
.cp-head-title{
  font-size:15px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.01em;
}
.cp-head-sub{font-size:11px;color:var(--text3);margin-top:2px}
.cp-body{padding:2px 24px 22px;position:relative;z-index:1}
.cp-row{
  display:grid;
  grid-template-columns:1.3fr 1fr;
  gap:14px;
  margin-bottom:16px;
}
.cp-block{
  background:rgba(0,0,0,0.04);
  border:1px solid var(--glass-border);
  border-radius:14px;
  padding:14px 16px;
}
[data-theme="light"] .cp-block{background:rgba(59,111,212,0.02)}
.cp-block-label{
  font-size:10px;
  font-weight:800;
  color:var(--text2);
  text-transform:uppercase;
  letter-spacing:0.08em;
  display:flex;
  align-items:center;
  gap:6px;
  margin-bottom:10px;
}
.cp-block-label i{color:var(--accent);font-size:14px}
.cp-input-full{
  width:100%;
  padding:10px 14px;
  border-radius:12px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.06);
  color:var(--text);
  font-family:inherit;
  font-size:12.5px;
  outline:none;
  transition:var(--transition);
}
.cp-input-full:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-d);
}
.cp-input-full::placeholder{color:var(--text3)}
.cp-mini-row{display:flex;gap:8px;margin-top:8px}
.cp-quota-inputs{display:flex;gap:8px}
.cp-quota-inputs .cp-input-full{flex:1}
.cp-quota-inputs select.cp-input-full{flex:0 0 76px}

.proto-cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:9px;
}
.proto-card{
  border:1.5px solid var(--glass-border);
  border-radius:14px;
  padding:14px 12px;
  cursor:pointer;
  transition:var(--transition);
  text-align:center;
  position:relative;
  background:rgba(0,0,0,0.02);
}
.proto-card:hover{border-color:rgba(255,255,255,0.08);transform:translateY(-1px)}
.proto-card.active{
  border-color:var(--accent);
  background:var(--accent-d);
  box-shadow:0 0 0 3px var(--accent-d);
}
.proto-card.active .proto-card-check{opacity:1;transform:scale(1)}
.proto-card-check{
  position:absolute;
  top:7px;left:7px;
  width:18px;height:18px;
  border-radius:50%;
  background:var(--accent);
  color:#fff;
  font-size:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  opacity:0;
  transform:scale(0.5);
  transition:var(--transition);
}
.proto-card-icon{
  width:32px;height:32px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--accent);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:16px;
  margin:0 auto 8px;
}
.proto-card.active .proto-card-icon{background:var(--accent);color:#fff}
.proto-card-title{font-size:11px;font-weight:800;color:var(--text)}
.proto-card-desc{font-size:9px;color:var(--text3);margin-top:3px;line-height:1.5}

.cp-footer{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding-top:16px;
  border-top:1px solid var(--glass-border);
  flex-wrap:wrap;
}
.cp-footer-note{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:10.5px;
  color:var(--text3);
  line-height:1.7;
  flex:1;
  min-width:220px;
}
.cp-footer-note i{color:var(--accent);font-size:15px;flex-shrink:0}
.cp-submit-btn{
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  color:#fff;
  border:none;
  border-radius:14px;
  padding:13px 28px;
  font-family:inherit;
  font-size:13px;
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:8px;
  box-shadow:0 6px 24px rgba(91,141,239,0.2);
  transition:var(--transition);
  white-space:nowrap;
}
.cp-submit-btn:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 32px rgba(91,141,239,0.3);
}
.cp-submit-btn:active{transform:translateY(0) scale(0.98)}

/* ═══════════════════════════════════════════════════════════════════════════════
   پنل اطلاعات سرور
   ═══════════════════════════════════════════════════════════════════════════════ */
.srv-panel{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:22px;
  overflow:hidden;
  box-shadow:var(--shadow);
  position:relative;
}
.srv-panel::before{
  content:'';
  position:absolute;
  top:-60px;left:-60px;
  width:200px;height:200px;
  background:radial-gradient(circle,var(--accent-d),transparent 70%);
  pointer-events:none;
}
.srv-hero{
  display:flex;
  align-items:center;
  gap:14px;
  padding:22px 24px;
  position:relative;
  z-index:1;
  border-bottom:1px solid var(--glass-border);
}
.srv-hero-icon{
  width:50px;height:50px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:22px;
  flex-shrink:0;
  box-shadow:0 6px 24px rgba(91,141,239,0.2);
}
.srv-hero-text{flex:1;min-width:0}
.srv-hero-domain{
  font-size:15px;
  font-weight:800;
  color:var(--text);
  word-break:break-all;
}
.srv-hero-sub{
  font-size:10.5px;
  color:var(--text3);
  margin-top:4px;
  display:flex;
  align-items:center;
  gap:6px;
}
.srv-tiles{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:11px;
  padding:20px 22px 22px;
  position:relative;
  z-index:1;
}
.srv-tile{
  display:flex;
  align-items:center;
  gap:11px;
  background:rgba(0,0,0,0.02);
  border:1px solid var(--glass-border);
  border-radius:14px;
  padding:12px 14px;
  transition:var(--transition);
}
.srv-tile:hover{border-color:rgba(255,255,255,0.06);transform:translateY(-1px)}
.srv-tile-icon{
  width:34px;height:34px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--accent);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:16px;
  flex-shrink:0;
}
.srv-tile-text{min-width:0}
.srv-tile-label{
  font-size:9.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.05em;
  margin-bottom:3px;
}
.srv-tile-val{font-size:12px;font-weight:700;color:var(--text);word-break:break-word}

/* ═══════════════════════════════════════════════════════════════════════════════
   پنل تغییر رمز
   ═══════════════════════════════════════════════════════════════════════════════ */
.pw-panel{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:22px;
  overflow:hidden;
  box-shadow:var(--shadow);
  position:relative;
}
.pw-panel::before{
  content:'';
  position:absolute;
  top:-60px;right:-60px;
  width:200px;height:200px;
  background:radial-gradient(circle,var(--purple-bg),transparent 70%);
  pointer-events:none;
}
.pw-hero{
  display:flex;
  align-items:center;
  gap:14px;
  padding:22px 24px 18px;
  position:relative;
  z-index:1;
}
.pw-hero-icon{
  width:50px;height:50px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--purple),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:22px;
  flex-shrink:0;
  box-shadow:0 6px 24px rgba(167,139,250,0.2);
}
.pw-hero-text{flex:1;min-width:0}
.pw-hero-title{font-size:15px;font-weight:800;color:var(--text)}
.pw-hero-sub{font-size:10.5px;color:var(--text3);margin-top:3px}
.pw-body{padding:2px 24px 22px;position:relative;z-index:1}
.pw-field{position:relative;margin-bottom:13px}
.pw-field label{
  display:block;
  font-size:10px;
  font-weight:700;
  color:var(--text2);
  text-transform:uppercase;
  letter-spacing:0.06em;
  margin-bottom:7px;
}
.pw-input{
  width:100%;
  padding:11px 44px 11px 14px;
  border-radius:12px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.06);
  color:var(--text);
  font-family:inherit;
  font-size:12.5px;
  outline:none;
  transition:var(--transition);
}
.pw-input:focus{
  border-color:var(--purple);
  box-shadow:0 0 0 3px var(--purple-bg);
}
.pw-eye{
  position:absolute;
  left:12px;top:34px;
  background:none;
  border:none;
  color:var(--text3);
  cursor:pointer;
  font-size:16px;
  padding:4px;
  display:flex;
  transition:var(--transition);
}
.pw-eye:hover{color:var(--purple)}
.pw-strength{
  height:4px;
  border-radius:4px;
  background:var(--glass-border);
  margin-top:8px;
  overflow:hidden;
  display:flex;
  gap:3px;
}
.pw-strength-seg{
  flex:1;
  height:100%;
  border-radius:4px;
  background:rgba(255,255,255,0.02);
  transition:var(--transition);
}
.pw-strength-label{
  font-size:9.5px;
  color:var(--text3);
  margin-top:5px;
  display:flex;
  align-items:center;
  gap:5px;
}
.pw-reqs{
  display:flex;
  flex-wrap:wrap;
  gap:6px;
  margin-top:10px;
  margin-bottom:16px;
}
.pw-req{
  font-size:9.5px;
  padding:4px 12px;
  border-radius:8px;
  background:var(--accent-d);
  color:var(--text3);
  font-weight:600;
  display:flex;
  align-items:center;
  gap:4px;
  transition:var(--transition);
}
.pw-req.met{background:var(--green-bg);color:var(--green-t)}
.pw-submit{
  width:100%;
  justify-content:center;
  background:linear-gradient(135deg,var(--purple),#7a5cf0);
  color:#fff;
  border:none;
  border-radius:14px;
  padding:12px;
  font-family:inherit;
  font-size:13px;
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:8px;
  box-shadow:0 6px 24px rgba(167,139,250,0.2);
  transition:var(--transition);
}
.pw-submit:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 32px rgba(167,139,250,0.3);
}
.pw-submit:active{transform:translateY(0) scale(0.98)}

/* ═══════════════════════════════════════════════════════════════════════════════
   ادامه... (بقیه بخش‌ها مثل ترافیک، اتصالات، گروه‌های ساب، مودال‌ها...)
   ═══════════════════════════════════════════════════════════════════════════════ */
/* ── ادامه در پاسخ بعدی ── */
</style>
</head>
<body>
...
</body>
</html>"""

/* ═══════════════════════════════════════════════════════════════════════════════
   صفحه ترافیک
   ═══════════════════════════════════════════════════════════════════════════════ */
.traf-hero{
  display:grid;
  grid-template-columns:1.4fr 1fr 1fr 1fr;
  gap:14px;
  margin-bottom:18px;
}
.traf-main-stat{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:22px 24px;
  position:relative;
  overflow:hidden;
}
.traf-main-stat::before{
  content:'';
  position:absolute;
  top:-50px;left:-50px;
  width:200px;height:200px;
  background:radial-gradient(circle,var(--accent-d),transparent 70%);
  pointer-events:none;
}
.traf-main-label{
  font-size:10.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.08em;
  display:flex;
  align-items:center;
  gap:6px;
  margin-bottom:10px;
  position:relative;
  z-index:1;
}
.traf-main-val{
  font-size:34px;
  font-weight:800;
  color:var(--text);
  line-height:1;
  letter-spacing:-0.02em;
  display:flex;
  align-items:baseline;
  gap:6px;
  position:relative;
  z-index:1;
}
.traf-main-val span{font-size:14px;font-weight:500;color:var(--text3)}
.traf-trend{
  display:inline-flex;
  align-items:center;
  gap:4px;
  font-size:11px;
  font-weight:700;
  padding:4px 12px;
  border-radius:20px;
  margin-top:12px;
  position:relative;
  z-index:1;
}
.traf-trend.up{background:var(--green-bg);color:var(--green-t)}
.traf-trend.down{background:var(--red-bg);color:var(--red-t)}
.traf-mini{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:18px 19px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  transition:var(--transition);
}
.traf-mini:hover{border-color:rgba(255,255,255,0.06);transform:translateY(-2px)}
.traf-mini-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:14px;
}
.traf-mini-icon{
  width:32px;height:32px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--accent);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:15px;
}
.traf-mini-icon.pk{background:var(--amber-bg);color:var(--amber)}
.traf-mini-icon.lo{background:var(--purple-bg);color:var(--purple)}
.traf-mini-label{
  font-size:9.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.traf-mini-val{font-size:21px;font-weight:800;color:var(--text);letter-spacing:-0.01em}
.traf-mini-sub{font-size:9.5px;color:var(--text3);margin-top:3px}

.traf-chart-card{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:22px;
  padding:22px 24px 18px;
  box-shadow:var(--shadow);
  margin-bottom:18px;
}
.traf-chart-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:6px;
  flex-wrap:wrap;
  gap:10px;
}
.traf-chart-title{
  font-size:14px;
  font-weight:800;
  color:var(--text);
  display:flex;
  align-items:center;
  gap:8px;
}
.traf-chart-title i{color:var(--accent);font-size:18px}
.traf-chart-sub{font-size:10.5px;color:var(--text3);margin-top:3px}
.traf-legend{display:flex;gap:14px;align-items:center}
.traf-legend-item{
  display:flex;
  align-items:center;
  gap:6px;
  font-size:10.5px;
  color:var(--text2);
  font-weight:600;
}
.traf-legend-dot{width:8px;height:8px;border-radius:4px}
.traf-chart-body{height:320px;margin-top:14px;position:relative}

/* ═══════════════════════════════════════════════════════════════════════════════
   اتصالات فعال
   ═══════════════════════════════════════════════════════════════════════════════ */
.conn-hero{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:12px;
  margin-bottom:18px;
}
.conn-hero-tile{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:18px;
  padding:16px 18px;
  position:relative;
  overflow:hidden;
  transition:var(--transition);
}
.conn-hero-tile:hover{
  border-color:rgba(255,255,255,0.06);
  transform:translateY(-2px);
  box-shadow:var(--shadow);
}
.conn-hero-tile::after{
  content:'';
  position:absolute;
  bottom:0;left:0;right:0;
  height:2px;
  background:linear-gradient(90deg,var(--green),transparent);
}
.conn-hero-icon{
  width:32px;height:32px;
  border-radius:10px;
  background:var(--green-bg);
  color:var(--green-t);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:15px;
  margin-bottom:10px;
}
.conn-hero-tile:nth-child(2) .conn-hero-icon{background:var(--accent-d);color:var(--accent)}
.conn-hero-tile:nth-child(3) .conn-hero-icon{background:var(--purple-bg);color:var(--purple)}
.conn-hero-tile:nth-child(4) .conn-hero-icon{background:var(--amber-bg);color:var(--amber)}
.conn-hero-label{
  font-size:9.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.06em;
  margin-bottom:4px;
}
.conn-hero-val{font-size:21px;font-weight:800;color:var(--text);line-height:1;letter-spacing:-0.02em}
.conn-hero-unit{font-size:11px;color:var(--text3);font-weight:500}

.conn-toolbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  margin-bottom:14px;
  flex-wrap:wrap;
}
.conn-toolbar-title{
  font-size:12px;
  font-weight:800;
  color:var(--text2);
  display:flex;
  align-items:center;
  gap:7px;
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.conn-toolbar-title i{color:var(--green);font-size:15px}
.conn-live-badge{
  display:flex;
  align-items:center;
  gap:6px;
  font-size:10.5px;
  font-weight:700;
  color:var(--green-t);
  background:var(--green-bg);
  padding:5px 14px;
  border-radius:20px;
  border:1px solid rgba(45,212,160,0.06);
}

.conn-grid-v2{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:14px;
}
.conn-card-v2{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  padding:0;
  overflow:hidden;
  transition:var(--transition);
  position:relative;
}
.conn-card-v2:hover{
  border-color:rgba(255,255,255,0.08);
  transform:translateY(-3px);
  box-shadow:var(--shadow);
}
.conn-card-v2-glow{
  position:absolute;
  top:-40px;left:-40px;
  width:140px;height:140px;
  background:radial-gradient(circle,rgba(45,212,160,0.04),transparent 70%);
  pointer-events:none;
}
.conn-card-v2-top{
  display:flex;
  align-items:center;
  gap:12px;
  padding:16px 17px 13px;
  position:relative;
  z-index:1;
}
.conn-avatar{
  width:42px;height:42px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--green),#0d9e6e);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:18px;
  flex-shrink:0;
  position:relative;
  box-shadow:0 4px 16px rgba(45,212,160,0.15);
}
.conn-avatar::after{
  content:'';
  position:absolute;
  inset:-4px;
  border-radius:18px;
  border:1.5px solid var(--green);
  opacity:0.3;
  animation:breathe2 2.4s ease-in-out infinite;
}
@keyframes breathe2{0%,100%{transform:scale(1);opacity:0.3}50%{transform:scale(1.08);opacity:0}}
.conn-card-v2-id{flex:1;min-width:0}
.conn-ip-v2{
  font-family:ui-monospace,monospace;
  font-size:14px;
  font-weight:800;
  color:var(--text);
  display:flex;
  align-items:center;
  gap:6px;
}
.conn-ip-copy{
  background:none;border:none;
  color:var(--text3);
  cursor:pointer;
  font-size:12px;
  padding:2px;
  display:flex;
  transition:var(--transition);
}
.conn-ip-copy:hover{color:var(--accent)}
.conn-label-v2{
  font-size:10.5px;
  color:var(--text3);
  margin-top:2px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.conn-status-pill{
  font-size:9px;
  font-weight:800;
  padding:4px 12px;
  border-radius:20px;
  background:var(--green-bg);
  color:var(--green-t);
  display:flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
  flex-shrink:0;
}
.conn-card-v2-divider{
  height:1px;
  background:linear-gradient(90deg,transparent,var(--glass-border) 15%,var(--glass-border) 85%,transparent);
  margin:0 17px;
}
.conn-card-v2-body{padding:14px 17px 16px}
.conn-proto-row{margin-bottom:12px}
.conn-stat-row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
  margin-bottom:12px;
}
.conn-stat-box{display:flex;align-items:center;gap:8px}
.conn-stat-icon{
  width:26px;height:26px;
  border-radius:9px;
  background:var(--accent-d);
  color:var(--accent);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:12px;
  flex-shrink:0;
}
.conn-stat-icon.time{background:var(--purple-bg);color:var(--purple)}
.conn-stat-text-label{
  font-size:8.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.04em;
}
.conn-stat-text-val{font-size:11.5px;font-weight:700;color:var(--text);margin-top:1px}
.conn-duration-track{
  height:5px;
  border-radius:6px;
  background:var(--glass-border);
  overflow:hidden;
  position:relative;
}
.conn-duration-fill{
  height:100%;
  border-radius:6px;
  background:linear-gradient(90deg,var(--green),#5be0b0);
  position:relative;
  overflow:hidden;
}
.conn-duration-fill::after{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.15),transparent);
  width:40%;
  animation:shimmer 1.8s linear infinite;
}
@keyframes shimmer{0%{transform:translateX(-120%)}100%{transform:translateX(280%)}}

.conn-empty-v2{
  text-align:center;
  padding:70px 20px;
  background:var(--glass);
  border:1px dashed var(--glass-border);
  border-radius:20px;
}
.conn-empty-v2-icon{
  width:64px;height:64px;
  border-radius:18px;
  background:var(--accent-d);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:28px;
  color:var(--text3);
  margin:0 auto 16px;
}
.conn-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--text2);margin-bottom:5px}
.conn-empty-v2-sub{font-size:11px;color:var(--text3)}

/* ═══════════════════════════════════════════════════════════════════════════════
   گروه‌های ساب
   ═══════════════════════════════════════════════════════════════════════════════ */
.subs-toolbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom:16px;
  flex-wrap:wrap;
}
.subs-search{flex:1;min-width:200px;position:relative}
.subs-search input{
  width:100%;
  padding:11px 42px 11px 15px;
  border-radius:14px;
  border:1px solid var(--glass-border);
  background:var(--glass);
  color:var(--text);
  font-family:inherit;
  font-size:12.5px;
  outline:none;
  transition:var(--transition);
}
.subs-search input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-d);
}
.subs-search i{
  position:absolute;
  left:14px;top:50%;
  transform:translateY(-50%);
  color:var(--text3);
  font-size:15px;
}

.sub-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
  gap:16px;
  margin-bottom:18px;
}
.sub-card{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:22px;
  padding:0;
  overflow:hidden;
  transition:var(--transition);
  position:relative;
}
.sub-card:hover{
  border-color:rgba(255,255,255,0.08);
  transform:translateY(-4px);
  box-shadow:var(--shadow);
}
.sub-card-top{
  background:linear-gradient(155deg,var(--purple-bg),transparent 70%);
  padding:20px 20px 16px;
  position:relative;
}
.sub-card-top::before{
  content:'';
  position:absolute;
  top:-30px;left:-30px;
  width:130px;height:130px;
  background:radial-gradient(circle,var(--purple-bg),transparent 70%);
  pointer-events:none;
}
.sub-card-head-v2{
  display:flex;
  align-items:flex-start;
  gap:13px;
  position:relative;
  z-index:1;
}
.sub-card-icon{
  width:46px;height:46px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--purple),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:20px;
  flex-shrink:0;
  box-shadow:0 6px 24px rgba(167,139,250,0.15);
}
.sub-card-titles{flex:1;min-width:0}
.sub-card-name-v2{
  font-size:15.5px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.01em;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.sub-card-desc-v2{
  font-size:11px;
  color:var(--text3);
  margin-top:3px;
  line-height:1.6;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:hidden;
}
.sub-card-lock-badge{
  flex-shrink:0;
  width:26px;height:26px;
  border-radius:9px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:12px;
}
.sub-card-lock-badge.locked{background:var(--amber-bg);color:var(--amber-t)}
.sub-card-lock-badge.open{background:var(--green-bg);color:var(--green-t)}
.sub-card-stats{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:0;
  position:relative;
  z-index:1;
  margin-top:16px;
  background:rgba(0,0,0,0.02);
  border:1px solid var(--glass-border);
  border-radius:12px;
  overflow:hidden;
}
.sub-card-stat{padding:11px 8px;text-align:center;border-left:1px solid var(--glass-border)}
.sub-card-stat:last-child{border-left:none}
.sub-card-stat-val{font-size:15px;font-weight:800;color:var(--text);line-height:1.2}
.sub-card-stat-label{
  font-size:8.5px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.05em;
  margin-top:4px;
}
.sub-card-url-row{
  margin:14px 20px 0;
  background:rgba(167,139,250,0.04);
  border:1px dashed rgba(167,139,250,0.1);
  border-radius:12px;
  padding:9px 12px;
  display:flex;
  align-items:center;
  gap:8px;
}
.sub-card-url-text{
  font-family:ui-monospace,monospace;
  font-size:9.5px;
  color:var(--purple);
  flex:1;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.sub-card-url-copy{
  background:none;border:none;
  color:var(--purple);
  cursor:pointer;
  font-size:13px;
  padding:3px;
  display:flex;
  flex-shrink:0;
  transition:var(--transition);
}
.sub-card-url-copy:hover{color:var(--purple);transform:scale(1.05)}
.sub-card-bottom{
  padding:14px 20px 18px;
  display:flex;
  gap:7px;
  flex-wrap:wrap;
}
.sub-card-bottom .btn{flex:1;justify-content:center;min-width:fit-content}

.subs-empty-v2{
  text-align:center;
  padding:70px 20px;
  background:var(--glass);
  border:1px dashed var(--glass-border);
  border-radius:20px;
  grid-column:1/-1;
}
.subs-empty-v2-icon{
  width:64px;height:64px;
  border-radius:18px;
  background:var(--purple-bg);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:28px;
  color:var(--purple);
  margin:0 auto 16px;
}
.subs-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--text2);margin-bottom:5px}
.subs-empty-v2-sub{font-size:11px;color:var(--text3)}

/* ═══════════════════════════════════════════════════════════════════════════════
   مودال‌ها
   ═══════════════════════════════════════════════════════════════════════════════ */
.modal-bg{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.5);
  backdrop-filter:blur(8px);
  z-index:500;
  align-items:center;
  justify-content:center;
}
.modal-bg.open{display:flex}
.modal{
  background:var(--glass);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--glass-border);
  border-radius:24px;
  padding:28px 26px;
  max-width:520px;
  width:calc(100% - 32px);
  max-height:90vh;
  overflow-y:auto;
  position:relative;
  animation:fadeIn 0.25s ease;
}
.modal-close{
  position:absolute;
  top:14px;left:14px;
  background:var(--glass);
  border:1px solid var(--glass-border);
  color:var(--text3);
  width:30px;height:30px;
  border-radius:10px;
  font-size:16px;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  border:none;
  transition:var(--transition);
}
.modal-close:hover{background:rgba(239,68,68,0.06);color:var(--red)}
.modal-title{
  font-size:16px;
  font-weight:700;
  color:var(--text);
  margin-bottom:18px;
  display:flex;
  align-items:center;
  gap:8px;
}
.modal-title i{color:var(--accent)}

.modal-v2{
  background:var(--glass);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--glass-border);
  border-radius:24px;
  padding:0;
  max-width:430px;
  width:calc(100% - 32px);
  max-height:92vh;
  overflow-y:auto;
  position:relative;
  animation:fadeIn 0.25s ease;
  box-shadow:0 24px 80px rgba(0,0,0,0.3);
}
.modal-v2-head{
  background:linear-gradient(155deg,var(--purple-bg),transparent 70%);
  padding:18px 22px 14px;
  position:relative;
  overflow:hidden;
}
.modal-v2-head::before{
  content:'';
  position:absolute;
  top:-50px;left:-50px;
  width:160px;height:160px;
  background:radial-gradient(circle,var(--purple-bg),transparent 70%);
  pointer-events:none;
}
.modal-v2-close{
  position:absolute;
  top:14px;left:14px;
  background:var(--glass);
  border:1px solid var(--glass-border);
  color:var(--text3);
  width:30px;height:30px;
  border-radius:10px;
  font-size:15px;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  z-index:2;
  transition:var(--transition);
}
.modal-v2-close:hover{background:rgba(239,68,68,0.06);color:var(--red)}
.modal-v2-icon{
  width:42px;height:42px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--purple),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:19px;
  margin-bottom:10px;
  position:relative;
  z-index:1;
  box-shadow:0 6px 24px rgba(167,139,250,0.15);
}
.modal-v2-title{font-size:15.5px;font-weight:800;color:var(--text);position:relative;z-index:1;letter-spacing:-0.01em}
.modal-v2-sub{font-size:10.5px;color:var(--text3);margin-top:3px;position:relative;z-index:1;line-height:1.6}
.modal-v2-body{padding:16px 22px 20px;border-top:1px solid var(--glass-border)}
.modal-v2-field{margin-bottom:11px}
.modal-v2-field label{
  display:flex;
  align-items:center;
  gap:5px;
  font-size:9.5px;
  font-weight:800;
  color:var(--text2);
  text-transform:uppercase;
  letter-spacing:0.06em;
  margin-bottom:6px;
}
.modal-v2-field label i{color:var(--purple);font-size:13px}
.modal-v2-input-wrap{position:relative}
.modal-v2-input-wrap>i{
  position:absolute;
  right:13px;top:50%;
  transform:translateY(-50%);
  color:var(--text3);
  font-size:14px;
  pointer-events:none;
  transition:var(--transition);
  z-index:1;
}
.modal-v2-input{
  width:100%;
  padding:9px 40px 9px 13px;
  border-radius:12px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.04);
  color:var(--text);
  font-family:inherit;
  font-size:12.5px;
  outline:none;
  transition:var(--transition);
}
.modal-v2-input::placeholder{color:var(--text3)}
.modal-v2-input:focus{
  border-color:var(--purple);
  box-shadow:0 0 0 3px var(--purple-bg);
}
.modal-v2-input:focus~i{color:var(--purple)}
.modal-v2-hint{
  background:var(--accent-d);
  border:1px solid var(--glass-border);
  border-radius:12px;
  padding:9px 12px;
  font-size:10px;
  color:var(--text2);
  display:flex;
  gap:7px;
  align-items:flex-start;
  line-height:1.6;
  margin-top:2px;
}
.modal-v2-hint i{font-size:14px;color:var(--accent);margin-top:1px;flex-shrink:0}
.modal-v2-footer{display:flex;gap:8px;margin-top:15px}
.modal-v2-btn-cancel{
  flex:.75;
  justify-content:center;
  padding:10px;
  border-radius:12px;
  background:transparent;
  border:1px solid var(--glass-border);
  color:var(--text2);
  font-family:inherit;
  font-size:12px;
  font-weight:700;
  cursor:pointer;
  transition:var(--transition);
  display:flex;
  align-items:center;
}
.modal-v2-btn-cancel:hover{background:var(--accent-d);color:var(--text)}
.modal-v2-btn-submit{
  flex:1;
  justify-content:center;
  padding:10px;
  border-radius:12px;
  background:linear-gradient(135deg,var(--purple),#7a5cf0);
  color:#fff;
  border:none;
  font-family:inherit;
  font-size:12px;
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:6px;
  box-shadow:0 6px 24px rgba(167,139,250,0.15);
  transition:var(--transition);
}
.modal-v2-btn-submit:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 32px rgba(167,139,250,0.25);
}
.modal-v2-btn-submit:active{transform:translateY(0) scale(0.98)}

.lmodal-head{
  background:linear-gradient(155deg,var(--accent-d),transparent 70%);
  padding:22px 24px 18px;
  position:relative;
  border-bottom:1px solid var(--glass-border);
}
.lmodal-icon-row{
  display:flex;
  align-items:center;
  gap:12px;
  position:relative;
  z-index:1;
}
.lmodal-icon{
  width:44px;height:44px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-size:19px;
  flex-shrink:0;
  box-shadow:0 6px 24px rgba(91,141,239,0.15);
}
.lmodal-title-v2{font-size:14.5px;font-weight:800;color:var(--text)}
.lmodal-sub-v2{font-size:10.5px;color:var(--text3);margin-top:2px}
.lmodal-search{margin-top:14px;position:relative}
.lmodal-search input{
  width:100%;
  padding:10px 40px 10px 13px;
  border-radius:12px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.04);
  color:var(--text);
  font-family:inherit;
  font-size:12px;
  outline:none;
  transition:var(--transition);
}
.lmodal-search input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-d);
}
.lmodal-search i{
  position:absolute;
  left:12px;top:50%;
  transform:translateY(-50%);
  color:var(--text3);
  font-size:14px;
}
.lmodal-quickbar{
  display:flex;
  gap:8px;
  margin-top:11px;
  position:relative;
  z-index:1;
}
.lmodal-qbtn{
  font-size:10px;
  font-weight:700;
  padding:5px 12px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--accent2);
  border:1px solid var(--glass-border);
  cursor:pointer;
  transition:var(--transition);
  font-family:inherit;
}
.lmodal-qbtn:hover{background:rgba(91,141,239,0.12)}
.lmodal-count{margin-right:auto;font-size:10.5px;color:var(--text3);display:flex;align-items:center}

.lmodal-list{padding:10px 14px;max-height:360px;overflow-y:auto}
.lrow-v2{
  display:flex;
  align-items:center;
  gap:11px;
  padding:11px 12px;
  border-radius:14px;
  cursor:pointer;
  transition:var(--transition);
  margin-bottom:4px;
  border:1px solid transparent;
}
.lrow-v2:hover{background:var(--accent-d)}
.lrow-v2.checked{background:var(--accent-d);border-color:rgba(91,141,239,0.1)}
.lrow-v2-check{
  width:20px;height:20px;
  border-radius:8px;
  border:2px solid var(--glass-border);
  flex-shrink:0;
  display:flex;
  align-items:center;
  justify-content:center;
  transition:var(--transition);
}
.lrow-v2.checked .lrow-v2-check{background:var(--accent);border-color:var(--accent)}
.lrow-v2-check i{font-size:12px;color:#fff;opacity:0;transform:scale(0.5);transition:var(--transition)}
.lrow-v2.checked .lrow-v2-check i{opacity:1;transform:scale(1)}
.lrow-v2-avatar{
  width:34px;height:34px;
  border-radius:10px;
  background:var(--accent-d);
  color:var(--accent);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:14px;
  flex-shrink:0;
}
.lrow-v2.checked .lrow-v2-avatar{background:var(--accent);color:#fff}
.lrow-v2-info{flex:1;min-width:0}
.lrow-v2-name{font-size:12.5px;font-weight:700;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lrow-v2-meta{font-size:9.5px;color:var(--text3);margin-top:2px;display:flex;align-items:center;gap:6px}
.lrow-v2-status{
  font-size:9px;
  font-weight:800;
  padding:3px 12px;
  border-radius:20px;
  flex-shrink:0;
  white-space:nowrap;
}
.lrow-v2-status.on{background:var(--green-bg);color:var(--green-t)}
.lrow-v2-status.off{background:var(--red-bg);color:var(--red-t)}

.lmodal-footer{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  padding:16px 24px;
  border-top:1px solid var(--glass-border);
}
.lmodal-footer-info{
  font-size:10.5px;
  color:var(--text3);
  display:flex;
  align-items:center;
  gap:6px;
}
.lmodal-footer-info i{color:var(--accent)}
.lmodal-footer-btns{display:flex;gap:8px}

/* ═══════════════════════════════════════════════════════════════════════════════
   سایر المان‌ها
   ═══════════════════════════════════════════════════════════════════════════════ */
.toast{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%) translateY(40px);
  background:var(--glass);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  border:1px solid var(--glass-border);
  color:var(--text);
  border-radius:14px;
  padding:10px 22px;
  font-size:12.5px;
  font-weight:600;
  opacity:0;
  transition:all 0.3s cubic-bezier(0.4,0,0.2,1);
  z-index:999;
  pointer-events:none;
  display:flex;
  align-items:center;
  gap:8px;
  box-shadow:var(--shadow);
  white-space:nowrap;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(45,212,160,0.1);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(248,113,113,0.1);background:var(--red-bg);color:var(--red-t)}

.dash-footer{
  border-top:1px solid var(--glass-border);
  margin-top:14px;
  padding-top:14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:8px;
}
.df-text{font-size:10px;color:var(--text3)}
.df-link{
  font-size:11.5px;
  color:var(--accent2);
  display:flex;
  align-items:center;
  gap:5px;
  font-weight:600;
}

.sub-box{
  background:var(--accent-d);
  border:1px solid var(--glass-border);
  border-radius:12px;
  padding:14px 16px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
  margin-top:11px;
}
.sub-url{
  font-family:ui-monospace,monospace;
  font-size:10.5px;
  color:var(--purple);
  word-break:break-all;
  flex:1;
}
.spbar{
  height:4px;
  border-radius:6px;
  background:var(--glass-border);
  margin-top:5px;
  overflow:hidden;
}
.spfill{
  height:100%;
  border-radius:6px;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  transition:width 1s ease;
}
.empty{
  text-align:center;
  padding:50px 20px;
  color:var(--text3);
}
.empty i{font-size:40px;opacity:0.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}

/* ═══════════════════════════════════════════════════════════════════════════════
   کانفیگ‌ها (لیست ردیفی)
   ═══════════════════════════════════════════════════════════════════════════════ */
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:16px;
  padding:0;
  transition:var(--transition);
  position:relative;
  overflow:hidden;
}
.cfg-card:hover{
  border-color:rgba(255,255,255,0.06);
  box-shadow:var(--shadow);
}
.cfg-card.is-off{opacity:0.5}
.cfg-card.is-exp{opacity:0.7}
.cfg-row{
  display:flex;
  align-items:center;
  gap:16px;
  padding:14px 18px;
}
.cfg-status-dot{
  width:9px;height:9px;
  border-radius:50%;
  background:var(--green);
  flex-shrink:0;
  box-shadow:0 0 0 3px var(--green-bg);
}
.cfg-card.is-off .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.is-exp .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{
  display:flex;
  flex-direction:column;
  gap:3px;
  min-width:150px;
  flex-shrink:0;
}
.cfg-label{
  font-size:13.5px;
  font-weight:700;
  color:var(--text);
  display:flex;
  align-items:center;
  gap:7px;
}
.cfg-sub-meta{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:10px;
  color:var(--text3);
}
.cfg-uuid-mini{
  font-family:ui-monospace,monospace;
  font-size:9.5px;
  color:var(--accent2);
  background:var(--accent-d);
  padding:2px 8px;
  border-radius:6px;
  cursor:pointer;
  transition:var(--transition);
}
.cfg-uuid-mini:hover{background:rgba(91,141,239,0.12)}
.cfg-divider-v{
  width:1px;
  align-self:stretch;
  background:var(--glass-border);
  flex-shrink:0;
}
.cfg-usage-col{
  flex:1;
  min-width:160px;
  display:flex;
  flex-direction:column;
  gap:5px;
}
.ubar{
  height:5px;
  border-radius:6px;
  background:rgba(255,255,255,0.02);
  overflow:hidden;
}
.ubar-f{
  height:100%;
  border-radius:6px;
  transition:width 0.4s ease;
}
.utxt{font-size:10px;color:var(--text3);display:flex;justify-content:space-between}
.cfg-exp-col{flex-shrink:0;min-width:110px}
.cfg-badges-col{
  display:flex;
  flex-direction:column;
  gap:5px;
  flex-shrink:0;
  align-items:flex-end;
}
.cfg-actions{display:flex;gap:5px;flex-shrink:0}
.proto-chip{
  font-size:9px;
  padding:3px 10px;
  border-radius:8px;
  font-weight:700;
  white-space:nowrap;
}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:var(--purple)}
.pc-ultra{background:var(--green-bg);color:var(--green-t)}
.cfg-sub-tag{
  font-size:9.5px;
  color:var(--text3);
  display:flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
}
.cfg-sub-tag i{color:var(--purple);font-size:11px}

/* ═══════════════════════════════════════════════════════════════════════════════
   ریسپانسیو
   ═══════════════════════════════════════════════════════════════════════════════ */
@media(max-width:880px){
  .cfg-row{flex-wrap:wrap}
  .cfg-divider-v{display:none}
  .cfg-usage-col{min-width:100%;order:5}
}
@media(max-width:768px){
  .cfg-grid{display:grid;grid-template-columns:1fr;gap:13px}
  .cfg-card{border-radius:18px}
  .cfg-row{flex-direction:column;align-items:stretch;gap:12px;padding:16px}
  .cfg-row-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .cfg-identity{min-width:0;flex:1}
  .cfg-usage-col{min-width:0}
  .cfg-exp-col{min-width:0}
  .cfg-badges-col{flex-direction:row;align-items:center;flex-wrap:wrap}
  .cfg-actions{flex-wrap:wrap;border-top:1px solid var(--glass-border);padding-top:10px;margin-top:2px;width:100%}
}
@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-8px 0 40px rgba(0,0,0,0.25)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
  .sub-grid,.cfg-grid,.conn-grid{grid-template-columns:1fr}
}
</style>

def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب v5 — طراحی شیشه‌ای آیفونی"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>X4G Sub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
/* ═══════════════════════════════════════════════════════════════════════════════
   طراحی شیشه‌ای آیفونی - صفحه پابلیک ساب
   ═══════════════════════════════════════════════════════════════════════════════ */
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}

:root{{
  --bg-dark:#0a0a12;
  --bg2-dark:#0f0f1a;
  --glass-dark:rgba(255,255,255,0.04);
  --glass-border-dark:rgba(255,255,255,0.06);
  --glass-shadow-dark:0 8px 40px rgba(0,0,0,0.5);
  --text-dark:#eeeff5;
  --text2-dark:rgba(255,255,255,0.7);
  --text3-dark:rgba(255,255,255,0.35);
  --accent-dark:#5b8def;
  --accent2-dark:#7aa3ff;
  --accent-d-dark:rgba(91,141,239,0.08);
  --green-dark:#2dd4a0;
  --green-bg-dark:rgba(45,212,160,0.08);
  --green-t-dark:#5be0b0;
  --red-dark:#f87171;
  --red-bg-dark:rgba(248,113,113,0.08);
  --red-t-dark:#fb9292;
  --amber-dark:#fbbf24;
  --amber-bg-dark:rgba(251,191,36,0.08);
  --amber-t-dark:#fcd34d;
  --purple-dark:#a78bfa;
  --purple-bg-dark:rgba(167,139,250,0.08);
  --purple-t-dark:#c4b5fd;

  --bg-light:#eef0f5;
  --bg2-light:#e4e7ef;
  --glass-light:rgba(255,255,255,0.6);
  --glass-border-light:rgba(255,255,255,0.7);
  --glass-shadow-light:0 8px 40px rgba(0,0,0,0.06);
  --text-light:#12121e;
  --text2-light:rgba(0,0,0,0.65);
  --text3-light:rgba(0,0,0,0.3);
  --accent-light:#3b6fd4;
  --accent2-light:#5a88e8;
  --accent-d-light:rgba(59,111,212,0.06);
  --green-light:#0d9e6e;
  --green-bg-light:rgba(13,158,110,0.06);
  --green-t-light:#0a805a;
  --red-light:#dc2626;
  --red-bg-light:rgba(220,38,38,0.06);
  --red-t-light:#b91c1c;
  --amber-light:#d97706;
  --amber-bg-light:rgba(217,119,6,0.06);
  --amber-t-light:#b45309;
  --purple-light:#7c3aed;
  --purple-bg-light:rgba(124,58,237,0.06);
  --purple-t-light:#6d28d9;

  --bg:var(--bg-dark);
  --bg2:var(--bg2-dark);
  --glass:var(--glass-dark);
  --glass-border:var(--glass-border-dark);
  --glass-shadow:var(--glass-shadow-dark);
  --text:var(--text-dark);
  --text2:var(--text2-dark);
  --text3:var(--text3-dark);
  --accent:var(--accent-dark);
  --accent2:var(--accent2-dark);
  --accent-d:var(--accent-d-dark);
  --green:var(--green-dark);
  --green-bg:var(--green-bg-dark);
  --green-t:var(--green-t-dark);
  --red:var(--red-dark);
  --red-bg:var(--red-bg-dark);
  --red-t:var(--red-t-dark);
  --amber:var(--amber-dark);
  --amber-bg:var(--amber-bg-dark);
  --amber-t:var(--amber-t-dark);
  --purple:var(--purple-dark);
  --purple-bg:var(--purple-bg-dark);
  --purple-t:var(--purple-t-dark);
  --shadow:var(--glass-shadow);
  --transition:all 0.35s cubic-bezier(0.4,0,0.2,1);
}}

[data-theme="light"]{{
  --bg:var(--bg-light);
  --bg2:var(--bg2-light);
  --glass:var(--glass-light);
  --glass-border:var(--glass-border-light);
  --glass-shadow:var(--glass-shadow-light);
  --text:var(--text-light);
  --text2:var(--text2-light);
  --text3:var(--text3-light);
  --accent:var(--accent-light);
  --accent2:var(--accent2-light);
  --accent-d:var(--accent-d-light);
  --green:var(--green-light);
  --green-bg:var(--green-bg-light);
  --green-t:var(--green-t-light);
  --red:var(--red-light);
  --red-bg:var(--red-bg-light);
  --red-t:var(--red-t-light);
  --amber:var(--amber-light);
  --amber-bg:var(--amber-bg-light);
  --amber-t:var(--amber-t-light);
  --purple:var(--purple-light);
  --purple-bg:var(--purple-bg-light);
  --purple-t:var(--purple-t-light);
}}

html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif;color:var(--text);font-size:14px;transition:var(--transition)}}

.bg-fx{{
  position:fixed;inset:0;
  background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(91,141,239,0.08),transparent 62%),var(--bg);
  z-index:0;pointer-events:none;transition:var(--transition);
}}
.grid-fx{{
  position:fixed;inset:0;
  background-image:linear-gradient(rgba(255,255,255,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.02) 1px,transparent 1px);
  background-size:46px 46px;
  z-index:0;pointer-events:none;
}}

.wrap{{
  position:relative;z-index:10;
  max-width:900px;margin:0 auto;
  padding:24px 16px 64px;
}}

.top{{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:26px;gap:10px;
}}
.brand{{
  display:flex;align-items:center;gap:11px;min-width:0;
}}
.brand-img{{
  width:40px;height:40px;
  border-radius:50%;overflow:hidden;
  border:1px solid var(--glass-border);
  box-shadow:0 0 30px rgba(91,141,239,0.1);
  flex-shrink:0;
}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{
  font-size:14.5px;font-weight:800;color:var(--text);
  letter-spacing:-0.01em;
}}
.brand-sub{{font-size:9.5px;color:var(--text3);font-weight:500}}
.top-actions{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.icon-btn{{
  width:36px;height:36px;
  border-radius:12px;
  background:var(--glass);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid var(--glass-border);
  color:var(--text2);
  display:flex;align-items:center;justify-content:center;
  font-size:16px;cursor:pointer;
  transition:var(--transition);
}}
.icon-btn:hover{{background:var(--accent-d);color:var(--accent2);border-color:rgba(255,255,255,0.06)}}

/* ── اطلاعات گروه ── */
.sub-info{{
  background:var(--glass);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  border:1px solid var(--glass-border);
  border-radius:24px;
  padding:24px 24px 22px;
  margin-bottom:16px;
  box-shadow:var(--shadow);
  position:relative;
  overflow:hidden;
}}
.sub-info::before{{
  content:'';
  position:absolute;top:0;right:0;
  width:160px;height:160px;
  background:radial-gradient(circle at top right,rgba(91,141,239,0.06),transparent 70%);
  pointer-events:none;
}}
.sub-eyebrow{{
  font-size:10px;font-weight:700;color:var(--accent2);
  text-transform:uppercase;letter-spacing:0.12em;
  margin-bottom:8px;display:flex;align-items:center;gap:6px;
}}
.sub-eyebrow i{{font-size:13px}}
.sub-name{{
  font-size:23px;font-weight:800;color:var(--text);
  margin-bottom:6px;letter-spacing:-0.02em;
}}
.sub-desc{{
  font-size:12.5px;color:var(--text2);
  line-height:1.8;margin-bottom:14px;
}}
.sub-meta-row{{
  font-size:10.5px;color:var(--text3);
  margin-bottom:14px;
  display:flex;align-items:center;gap:6px;flex-wrap:wrap;
}}
.sub-sub-box{{
  background:var(--accent-d);
  border:1px solid var(--glass-border);
  border-radius:14px;
  padding:12px 14px;
  display:flex;align-items:center;gap:9px;flex-wrap:wrap;
}}
.sub-sub-url{{
  font-family:ui-monospace,monospace;
  font-size:10px;color:var(--accent2);
  word-break:break-all;flex:1;min-width:140px;
}}

/* ── آمار ── */
.stats-bar{{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:10px;margin-bottom:18px;
}}
.stat-card{{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:18px;
  padding:16px 17px;
  transition:var(--transition);
}}
.stat-card:hover{{
  border-color:rgba(255,255,255,0.06);
  transform:translateY(-1px);
}}
.stat-label{{
  font-size:9px;color:var(--text3);
  font-weight:700;text-transform:uppercase;
  letter-spacing:0.07em;margin-bottom:7px;
}}
.stat-val{{
  font-size:22px;font-weight:800;color:var(--text);
  line-height:1;letter-spacing:-0.01em;
}}
.stat-sub{{font-size:9.5px;color:var(--text3);margin-top:6px}}

/* ── کپی همه ── */
.copy-all-bar{{
  display:flex;align-items:center;gap:12px;
  background:linear-gradient(120deg,var(--accent) 0%,#7a5cf0 100%);
  border-radius:20px;padding:16px 19px;
  margin-bottom:18px;
  box-shadow:0 10px 40px rgba(91,141,239,0.15);
  flex-wrap:wrap;
}}
.copy-all-text{{flex:1;min-width:160px}}
.copy-all-title{{
  font-size:13.5px;font-weight:800;color:#fff;
  display:flex;align-items:center;gap:6px;
}}
.copy-all-sub{{font-size:10px;color:rgba(255,255,255,0.75);margin-top:3px}}
.copy-all-btn{{
  background:#fff;color:#1D4ED8;
  border:none;border-radius:14px;
  padding:10px 20px;
  font-family:inherit;font-size:12.5px;font-weight:800;
  cursor:pointer;display:flex;align-items:center;gap:6px;
  transition:var(--transition);white-space:nowrap;
}}
.copy-all-btn:hover{{
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(0,0,0,0.1);
}}
.copy-all-btn:active{{transform:translateY(0) scale(0.97)}}

/* ── جستجو و نوار ابزار ── */
.toolbar{{
  display:flex;align-items:center;
  justify-content:space-between;gap:12px;
  margin-bottom:16px;flex-wrap:wrap;
}}
.toolbar-left{{display:flex;align-items:center;gap:8px}}
.cfg-title{{
  font-size:12px;font-weight:800;color:var(--text2);
  display:flex;align-items:center;gap:6px;
  text-transform:uppercase;letter-spacing:0.07em;
}}
.cfg-title i{{color:var(--accent);font-size:15px}}
.search-box{{position:relative;min-width:180px;flex:1}}
.search-box input{{
  width:100%;padding:8px 36px 8px 12px;
  border-radius:12px;border:1px solid var(--glass-border);
  background:var(--glass);
  backdrop-filter:blur(12px);
  color:var(--text);
  font-family:inherit;font-size:11.5px;
  outline:none;transition:var(--transition);
}}
.search-box input:focus{{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-d);
}}
.search-box i{{
  position:absolute;right:10px;top:50%;
  transform:translateY(-50%);
  color:var(--text3);font-size:13px;
}}
.export-btns{{display:flex;gap:5px}}
.btn-sm{{padding:6px 12px;font-size:10.5px;border-radius:10px}}

/* ── کارت‌های کانفیگ ── */
.cfg-grid{{display:grid;gap:13px}}

.cfg-card{{
  background:var(--glass);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border:1px solid var(--glass-border);
  border-radius:20px;
  transition:var(--transition);
  position:relative;overflow:hidden;
}}
.cfg-card:hover{{
  border-color:rgba(255,255,255,0.06);
  box-shadow:var(--shadow);
}}
.cfg-top{{
  padding:17px 19px 15px;
  position:relative;
}}
.cfg-top::after{{
  content:'';
  position:absolute;top:0;right:0;
  width:3px;height:100%;
  background:var(--green);
}}
.cfg-card.inactive .cfg-top::after{{background:var(--red)}}
.cfg-card.expired .cfg-top::after{{background:var(--amber)}}

.cfg-head{{
  display:flex;align-items:flex-start;
  justify-content:space-between;gap:8px;
  margin-bottom:12px;flex-wrap:wrap;
}}
.cfg-label{{
  font-size:14.5px;font-weight:700;color:var(--text);
}}
.cfg-badges{{
  display:flex;gap:5px;flex-wrap:wrap;margin-top:6px;
}}
.proto-chip{{
  font-size:9px;padding:3px 10px;border-radius:8px;
  font-weight:800;letter-spacing:0.02em;
}}
.pc-ws{{background:var(--accent-d);color:var(--accent2)}}
.pc-xhttp{{background:var(--purple-bg);color:var(--purple-t)}}
.pc-ultra{{background:var(--green-bg);color:var(--green-t)}}

.cfg-status{{
  display:flex;align-items:center;gap:5px;
  font-size:10px;font-weight:700;
  padding:4px 12px;border-radius:20px;
  white-space:nowrap;
}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.cfg-status.warn{{background:var(--amber-bg);color:var(--amber-t)}}

.cfg-exp{{
  font-size:10px;font-weight:700;margin-top:4px;
  display:flex;align-items:center;gap:4px;
}}
.cfg-exp.ok{{color:var(--green-t)}}
.cfg-exp.warn{{color:var(--amber-t)}}
.cfg-exp.exp{{color:var(--red-t)}}

.cfg-usage{{margin-bottom:4px}}
.ubar{{
  height:6px;border-radius:6px;
  background:rgba(255,255,255,0.02);
  overflow:hidden;margin-bottom:5px;
}}
.ubar-f{{
  height:100%;border-radius:6px;
  transition:width 0.5s ease;
}}
.utxt{{
  font-size:10px;color:var(--text3);
  display:flex;justify-content:space-between;
}}

.cfg-details{{
  display:grid;grid-template-columns:1fr 1fr;
  gap:6px;margin-top:9px;
  padding:8px 10px;
  background:var(--accent-d);
  border-radius:10px;
  font-size:9.5px;color:var(--text3);
}}
.cfg-details-item{{display:flex;align-items:center;gap:4px}}
.cfg-details-item i{{font-size:11px;color:var(--accent2)}}
.cfg-details-item span{{font-weight:600;color:var(--text2)}}

/* ── خط جداکننده بلیطی ── */
.cfg-tear{{
  position:relative;height:0;
  border-top:1.5px dashed var(--glass-border);
  margin:0 19px;
}}
.cfg-tear::before,.cfg-tear::after{{
  content:'';
  position:absolute;top:50%;
  width:18px;height:18px;border-radius:50%;
  background:var(--bg);
  transform:translateY(-50%);
  border:1px solid var(--glass-border);
}}
.cfg-tear::before{{right:-28px}}
.cfg-tear::after{{left:-28px}}

.cfg-bottom{{padding:15px 19px 18px}}
.cfg-link-toggle{{
  width:100%;
  display:flex;align-items:center;justify-content:space-between;
  gap:10px;
  background:transparent;
  border:1px dashed var(--glass-border);
  border-radius:12px;
  padding:10px 13px;
  cursor:pointer;
  font-family:inherit;
  color:var(--text2);
  font-size:11.5px;font-weight:600;
  transition:var(--transition);
}}
.cfg-link-toggle:hover{{
  background:var(--accent-d);
  border-color:rgba(255,255,255,0.06);
  color:var(--accent2);
}}
.cfg-link-toggle .ltl{{display:flex;align-items:center;gap:7px}}
.cfg-link-toggle i.ti-chevron-down{{transition:transform 0.2s}}
.cfg-link-toggle.open i.ti-chevron-down{{transform:rotate(180deg)}}

.cfg-vless-wrap{{
  display:grid;
  grid-template-rows:0fr;
  transition:grid-template-rows 0.25s ease;
}}
.cfg-vless-wrap.open{{grid-template-rows:1fr}}
.cfg-vless-inner{{overflow:hidden}}
.cfg-vless{{
  background:rgba(0,0,0,0.08);
  border:1px solid var(--glass-border);
  border-radius:10px;
  padding:11px 13px;
  font-size:9.8px;
  font-family:ui-monospace,monospace;
  color:var(--accent2);
  word-break:break-all;
  line-height:1.7;
  margin-top:9px;
  max-height:90px;
  overflow-y:auto;
}}
[data-theme="light"] .cfg-vless{{background:rgba(0,0,0,0.03)}}

.cfg-actions{{
  display:flex;gap:7px;flex-wrap:wrap;margin-top:11px;
}}

/* ── دکمه‌ها ── */
.btn{{
  font-family:inherit;font-size:11.5px;font-weight:700;
  border-radius:12px;padding:8px 16px;
  cursor:pointer;display:inline-flex;align-items:center;gap:5px;
  border:none;transition:var(--transition);white-space:nowrap;
}}
.btn i{{font-size:13px}}
.btn-p{{
  background:linear-gradient(135deg,var(--accent),#7a5cf0);
  color:#fff;
  box-shadow:0 4px 16px rgba(91,141,239,0.15);
}}
.btn-p:hover{{transform:translateY(-1px);box-shadow:0 6px 24px rgba(91,141,239,0.25)}}
.btn-g{{
  background:var(--accent-d);
  color:var(--accent2);
  border:1px solid rgba(91,141,239,0.04);
}}
.btn-g:hover{{background:rgba(91,141,239,0.12)}}
.btn-pur{{
  background:var(--purple-bg);
  color:var(--purple-t);
  border:1px solid rgba(167,139,250,0.04);
}}
.btn-pur:hover{{background:rgba(167,139,250,0.12)}}

.conn-chip{{
  display:inline-flex;align-items:center;gap:4px;
  font-size:9.5px;padding:3px 10px;border-radius:20px;
  background:var(--green-bg);color:var(--green-t);font-weight:700;
}}
.dot{{
  width:5px;height:5px;border-radius:50%;
  background:var(--green);display:inline-block;
  animation:pulse 2s infinite;
}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}

/* ── صفحه قفل ── */
.lock-stage{{
  display:flex;align-items:center;justify-content:center;
  min-height:78vh;padding:20px 0;
}}
.lock-card{{
  background:var(--glass);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--glass-border);
  border-radius:28px;
  padding:0;
  text-align:center;max-width:380px;
  width:100%;box-shadow:var(--shadow);
  overflow:hidden;position:relative;
}}
.lock-banner{{
  background:linear-gradient(150deg,var(--accent-d),transparent 70%);
  padding:38px 30px 26px;
  position:relative;
}}
.lock-shield{{
  width:64px;height:64px;
  border-radius:18px;
  background:var(--accent-d);
  border:1px solid var(--glass-border);
  display:flex;align-items:center;justify-content:center;
  margin:0 auto 18px;
  position:relative;
}}
.lock-shield::after{{
  content:'';
  position:absolute;inset:-7px;
  border-radius:22px;
  border:1px solid var(--glass-border);
  animation:breathe 2.6s ease-in-out infinite;
}}
@keyframes breathe{{0%,100%{{transform:scale(1);opacity:0.5}}50%{{transform:scale(1.08);opacity:0}}}}
.lock-shield i{{font-size:28px;color:var(--accent2)}}
.lock-title{{font-size:18px;font-weight:800;margin-bottom:6px;color:var(--text);letter-spacing:-0.01em}}
.lock-sub{{font-size:12px;color:var(--text3);line-height:1.7}}
.lock-form{{padding:24px 30px 30px}}
.lock-field{{position:relative;margin-bottom:13px}}
.lock-inp{{
  width:100%;padding:13px 44px 13px 44px;
  border-radius:14px;border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.06);
  color:var(--text);
  font-family:inherit;font-size:14px;
  outline:none;text-align:center;
  letter-spacing:0.14em;transition:var(--transition);
}}
.lock-inp:focus{{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-d);
}}
.lock-eye{{
  position:absolute;left:13px;top:50%;
  transform:translateY(-50%);
  background:none;border:none;
  color:var(--text3);cursor:pointer;
  font-size:16px;padding:4px;display:flex;
}}
.lock-eye:hover{{color:var(--accent2)}}
.lock-lockicon{{
  position:absolute;right:14px;top:50%;
  transform:translateY(-50%);
  color:var(--text3);font-size:15px;pointer-events:none;
}}
.lock-err{{
  color:var(--red-t);font-size:11.5px;
  margin-bottom:10px;min-height:16px;
  display:flex;align-items:center;justify-content:center;gap:5px;
}}
.lock-btn{{width:100%;justify-content:center;padding:13px;font-size:13px;border-radius:14px}}
.lock-footer{{
  padding:14px 30px;border-top:1px solid var(--glass-border);
  font-size:10px;color:var(--text3);
  display:flex;align-items:center;justify-content:center;gap:6px;
}}

.empty-state{{
  text-align:center;padding:80px 20px;
  color:var(--text3);
}}
.empty-state i{{font-size:38px;display:block;margin-bottom:14px}}

.toast{{
  position:fixed;bottom:24px;left:50%;
  transform:translateX(-50%) translateY(40px);
  background:var(--glass);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  border:1px solid var(--glass-border);
  color:var(--text);
  border-radius:14px;
  padding:10px 22px;font-size:12.5px;font-weight:600;
  opacity:0;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);
  z-index:999;pointer-events:none;
  display:flex;align-items:center;gap:7px;
  box-shadow:var(--shadow);
  white-space:nowrap;
}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(45,212,160,0.1);background:var(--green-bg);color:var(--green-t)}}
.toast.err{{border-color:rgba(248,113,113,0.1);background:var(--red-bg);color:var(--red-t)}}

.qr-modal{{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,0.5);
  backdrop-filter:blur(8px);
  z-index:600;align-items:center;justify-content:center;
  padding:20px;
}}
.qr-modal.open{{display:flex}}
.qr-box{{
  background:var(--glass);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--glass-border);
  border-radius:24px;
  padding:26px;text-align:center;
  max-width:340px;width:100%;
  box-shadow:var(--shadow);
}}
.qr-title{{font-size:13.5px;font-weight:800;margin-bottom:16px;color:var(--text)}}
.qr-img{{border-radius:14px;overflow:hidden;margin-bottom:15px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:10px;border-radius:14px}}

.footer{{
  text-align:center;padding-top:28px;
  font-size:10.5px;color:var(--text3);
}}
.footer a{{color:var(--accent2);font-weight:700}}

/* ── ریسپانسیو ── */
@media(max-width:640px){{
  .stats-bar{{grid-template-columns:1fr 1fr}}
  .sub-name{{font-size:19px}}
  .copy-all-bar{{flex-direction:column;align-items:stretch}}
  .copy-all-btn{{justify-content:center}}
  .wrap{{padding:16px 12px 50px}}
  .lock-banner{{padding:32px 22px 22px}}
  .lock-form{{padding:20px 22px 26px}}
  .cfg-details{{grid-template-columns:1fr}}
  .toolbar{{flex-direction:column;align-items:stretch}}
  .search-box{{min-width:unset}}
  .export-btns{{justify-content:flex-start}}
}}
@media(max-width:420px){{
  .stats-bar{{grid-template-columns:1fr}}
}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>

<div class="toast" id="toast"></div>

<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="wrap">
  <div class="top">
    <div class="brand">
      <div class="brand-img"><img src="data:image/png;base64,{LOGO_B64}" alt="X4G"></div>
      <div><div class="brand-name">X4G</div><div class="brand-sub">v9.5</div></div>
    </div>
    <div class="top-actions">
      <button class="icon-btn" id="theme-toggle" onclick="toggleTheme()" title="تغییر تم"><i class="ti ti-sun" id="theme-icon"></i></button>
    </div>
  </div>

  <div id="root">
    <div class="empty-state"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>در حال بارگذاری...</div>
  </div>

  <div class="footer">پشتیبانی: <a href="https://t.me/Farajian2004f" target="_blank">@Farajian2004f</a> · X4G v9.5</div>
</div>

<script>
const UUID_KEY='{uuid_key}';
let savedPw='';
let allLinksData=[];

let isDark=localStorage.getItem('x4g-pub-theme')!=='light';
function applyTheme(dark){{
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  document.getElementById('theme-icon').className='ti '+(dark?'ti-sun':'ti-moon');
}}
function toggleTheme(){{isDark=!isDark;localStorage.setItem('x4g-pub-theme',isDark?'dark':'light');applyTheme(isDark)}}
applyTheme(isDark);

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
function toFa(n){{return String(n).replace(/\\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}}
function daysLeft(exp){{
  if(!exp)return null;
  const diff=Math.ceil((new Date(exp)-Date.now())/(864e5));
  return diff;
}}
function expText(exp){{
  if(!exp)return '<span class="cfg-exp ok"><i class="ti ti-infinity"></i> نامحدود</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="cfg-exp exp"><i class="ti ti-calendar-x"></i> منقضی شده</span>';
  if(d<=3)return '<span class="cfg-exp warn"><i class="ti ti-alert-triangle"></i> '+toFa(d)+' روز مانده</span>';
  if(d<=7)return '<span class="cfg-exp warn"><i class="ti ti-clock"></i> '+toFa(d)+' روز مانده</span>';
  return '<span class="cfg-exp ok"><i class="ti ti-calendar-check"></i> '+toFa(d)+' روز مانده</span>';
}}
function protoChip(p){{
  if(p==='xhttp-stream-one')return '<span class="proto-chip pc-ultra"><i class="ti ti-bolt"></i> XHTTP ULTRA</span>';
  if(p&&p.startsWith('xhttp'))return '<span class="proto-chip pc-xhttp">'+esc(p).replace('xhttp-','')+'</span>';
  return '<span class="proto-chip pc-ws">VLESS · WS</span>';
}}
function statusText(l){{
  if(!l.active)return '<span class="cfg-status no"><i class="ti ti-circle-x"></i> غیرفعال</span>';
  if(l.expired)return '<span class="cfg-status warn"><i class="ti ti-alert-triangle"></i> منقضی</span>';
  const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
  if(pct>=90)return '<span class="cfg-status warn"><i class="ti ti-alert-triangle"></i> نزدیک به اتمام</span>';
  return '<span class="cfg-status ok"><i class="ti ti-circle-check"></i> فعال</span>';
}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

function toggleLink(i){{
  const wrap=document.getElementById('vw-'+i);
  const btn=document.getElementById('vt-'+i);
  const open=wrap.classList.toggle('open');
  btn.classList.toggle('open',open);
  btn.querySelector('.ltl span').textContent = open ? 'پنهان کردن لینک' : 'نمایش لینک کانفیگ';
}}

function filterLinks(q){{
  q=q.trim().toLowerCase();
  document.querySelectorAll('.cfg-card').forEach(card=>{{
    const label=card.dataset.label||'';
    const note=card.dataset.note||'';
    const visible=!q||label.includes(q)||note.includes(q);
    card.style.display=visible?'':'none';
  }});
}}

function copySubLink(subUrl){{
  const url=subUrl+(savedPw?'?pw='+encodeURIComponent(savedPw):'');
  navigator.clipboard.writeText(url).then(()=>toast('لینک ساب کپی شد ✓','ok'));
}}

function copySubBase64(subUrl){{
  const url=subUrl+(savedPw?'?pw='+encodeURIComponent(savedPw):'');
  const b64=btoa(url);
  navigator.clipboard.writeText(b64).then(()=>toast('لینک ساب (Base64) کپی شد ✓','ok'));
}}

function exportJSON(){{
  const links=window._x4gLinks||[];
  if(!links.length){{toast('کانفیگی برای خروجی نیست','err');return}}
  const data=links.map(l=>({{label:l.label,vless:l.vless,sub:l.sub}}));
  navigator.clipboard.writeText(JSON.stringify(data,null,2))
    .then(()=>toast('JSON کپی شد ✓','ok'));
}}

function exportYAML(){{
  const links=window._x4gLinks||[];
  if(!links.length){{toast('کانفیگی برای خروجی نیست','err');return}}
  let yaml='# X4G Configs\\n';
  links.forEach((l,i)=>{{
    yaml+=`\\n${{i+1}}:
  label: ${{l.label}}
  vless: ${{l.vless}}
  sub: ${{l.sub}}\\n`;
  }});
  navigator.clipboard.writeText(yaml).then(()=>toast('YAML کپی شد ✓','ok'));
}}

async function loadData(pw=''){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}

function renderLock(name,errMsg=''){{
  document.getElementById('root').innerHTML=`
    <div class="lock-stage">
      <div class="lock-card">
        <div class="lock-banner">
          <div class="lock-shield"><i class="ti ti-shield-lock"></i></div>
          <div class="lock-title">${{esc(name)}}</div>
          <div class="lock-sub">این گروه با رمز محافظت شده. برای دیدن کانفیگ‌ها رمز رو وارد کنید.</div>
        </div>
        <div class="lock-form">
          <div class="lock-err" id="lock-err">${{errMsg ? '<i class="ti ti-alert-circle"></i> '+esc(errMsg) : ''}}</div>
          <div class="lock-field">
            <i class="ti ti-lock lock-lockicon"></i>
            <input class="lock-inp" type="password" id="lock-pw" placeholder="••••••••" autofocus>
            <button class="lock-eye" type="button" onclick="togglePwVis()"><i class="ti ti-eye" id="lock-eye-icon"></i></button>
          </div>
          <button class="btn btn-p lock-btn" onclick="submitLock()"><i class="ti ti-lock-open"></i> ورود به گروه</button>
        </div>
        <div class="lock-footer"><i class="ti ti-shield-check"></i> اتصال شما رمزنگاری‌شده است</div>
      </div>
    </div>
  `;
  const inp=document.getElementById('lock-pw');
  inp.addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}});
}}

function togglePwVis(){{
  const inp=document.getElementById('lock-pw');
  const icon=document.getElementById('lock-eye-icon');
  const toText = inp.type==='password';
  inp.type = toText ? 'text' : 'password';
  icon.className = 'ti '+(toText ? 'ti-eye-off' : 'ti-eye');
}}

async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{renderLock(data.name,'رمز اشتباه است');return}}
  savedPw=pw;
  renderContent(data);
}}

function renderContent(d){{
  allLinksData=d.links;
  const activeCount=d.links.filter(l=>l.active&&!l.expired).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
  const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');

  window._x4gSubUrl  = subUrl;
  window._x4gSubName = d.name;
  window._x4gLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    sub   : l.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''),
    label : l.label,
  }}));

  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div class="sub-eyebrow"><i class="ti ti-folders"></i> گروه دسترسی</div>
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div class="sub-meta-row">
        <i class="ti ti-clock"></i> آخرین بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}
        <span style="margin-right:12px"><i class="ti ti-calendar"></i> ${{new Date(d.updated_at||Date.now()).toLocaleDateString('fa-IR')}}</span>
      </div>
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(subUrl)}}</span>
        <button class="btn btn-pur" style="padding:7px 12px;font-size:10.5px"
          onclick="copySubLink('${{esc(baseSubUrl)}}')">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-pur" style="padding:7px 12px;font-size:10.5px"
          onclick="copySubBase64('${{esc(baseSubUrl)}}')">
          <i class="ti ti-base64"></i> Base64
        </button>
        <button class="btn btn-g" style="padding:7px 12px;font-size:10.5px"
          onclick="showQR('${{esc(d.name)}} — کل گروه', '${{esc(subUrl)}}')">
          <i class="ti ti-qrcode"></i> QR کل
        </button>
      </div>
    </div>

    <div class="copy-all-bar">
      <div class="copy-all-text">
        <div class="copy-all-title"><i class="ti ti-copy"></i> کپی همه‌ی کانفیگ‌ها</div>
        <div class="copy-all-sub">تمام لینک‌های فعال این گروه را یک‌جا کپی کن</div>
      </div>
      <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> کپی همه (${{toFa(activeCount)}})</button>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{toFa(activeCount)}}</div>
        <div class="stat-sub">از ${{toFa(d.links.length)}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{toFa(d.active_connections)}}</div>
        <div class="stat-sub" style="color:var(--green-t);display:flex;align-items:center;gap:4px"><span class="dot"></span> آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف</div>
        <div class="stat-val" style="font-size:17px;margin-top:3px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">همه کانفیگ‌ها</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">تاریخ ایجاد</div>
        <div class="stat-val" style="font-size:14px;margin-top:3px">${{new Date(d.created_at||Date.now()).toLocaleDateString('fa-IR')}}</div>
        <div class="stat-sub">${{d.has_password ? '🔒 رمزدار' : '🔓 عمومی'}}</div>
      </div>
    </div>

    <div class="toolbar">
      <div class="toolbar-left">
        <div class="cfg-title"><i class="ti ti-link"></i> کانفیگ‌ها (${{toFa(d.links.length)}})</div>
      </div>
      <div class="search-box">
        <i class="ti ti-search"></i>
        <input type="text" id="search-input" placeholder="جستجو در کانفیگ‌ها..." oninput="filterLinks(this.value)">
      </div>
      <div class="export-btns">
        <button class="btn btn-sm btn-pur" onclick="exportJSON()"><i class="ti ti-file-code"></i> JSON</button>
        <button class="btn btn-sm btn-pur" onclick="exportYAML()"><i class="ti ti-file-text"></i> YAML</button>
      </div>
    </div>

    <div class="cfg-grid">
      ${{d.links.map((l, i) => {{
        const pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
        const cardCls = !l.active ? 'inactive' : (l.expired ? 'expired' : '');
        return `
          <div class="cfg-card ${{cardCls}}" data-label="${{esc(l.label).toLowerCase()}}" data-note="${{esc((l.note||'').toLowerCase())}}">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${{esc(l.label)}}</div>
                  <div class="cfg-badges">
                    ${{protoChip(l.protocol)}}
                    ${{l.connections > 0 ? `<span class="conn-chip"><span class="dot"></span> ${{toFa(l.connections)}} اتصال</span>` : ''}}
                    ${{l.note ? `<span class="conn-chip" style="background:var(--accent-d);color:var(--accent2)"><i class="ti ti-note"></i> ${{esc(l.note)}}</span>` : ''}}
                  </div>
                </div>
                <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
                  ${{statusText(l)}}
                  ${{expText(l.expires_at)}}
                </div>
              </div>
              <div class="cfg-usage">
                <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
                <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{lim}}</span></div>
              </div>
              <div class="cfg-details">
                <div class="cfg-details-item"><i class="ti ti-fingerprint"></i> Fingerprint: <span>${{esc(l.fingerprint||'chrome')}}</span></div>
                <div class="cfg-details-item"><i class="ti ti-route"></i> پورت: <span>${{l.port||443}}</span></div>
                <div class="cfg-details-item"><i class="ti ti-calendar"></i> ساخته شده: <span>${{new Date(l.created_at).toLocaleDateString('fa-IR')}}</span></div>
                <div class="cfg-details-item"><i class="ti ti-gauge"></i> سرعت: <span>${{l.speed_limit_bytes?((l.speed_limit_bytes*8/1024/1024).toFixed(1)+' Mbps'):'نامحدود'}}</span></div>
              </div>
            </div>
            <div class="cfg-tear"></div>
            <div class="cfg-bottom">
              <button class="cfg-link-toggle" id="vt-${{i}}" onclick="toggleLink(${{i}})">
                <span class="ltl"><i class="ti ti-eye"></i> <span>نمایش لینک کانفیگ</span></span>
                <i class="ti ti-chevron-down"></i>
              </button>
              <div class="cfg-vless-wrap" id="vw-${{i}}">
                <div class="cfg-vless-inner">
                  <div class="cfg-vless">${{esc(l.vless_link)}}</div>
                </div>
              </div>
              <div class="cfg-actions">
                <button class="btn btn-p"
                  onclick="navigator.clipboard.writeText(window._x4gLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))">
                  <i class="ti ti-copy"></i> کپی لینک
                </button>
                <button class="btn btn-g"
                  onclick="showQR(window._x4gLinks[${{i}}].label, window._x4gLinks[${{i}}].vless)">
                  <i class="ti ti-qrcode"></i> QR
                </button>
                <button class="btn btn-pur btn-sm"
                  onclick="navigator.clipboard.writeText(window._x4gLinks[${{i}}].sub).then(()=>toast('ساب کپی شد ✓','ok'))">
                  <i class="ti ti-rss"></i> ساب
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}

function copyAllConfigs(){{
  const links=window._x4gLinks||[];
  if(!links.length){{toast('کانفیگی برای کپی نیست','err');return}}
  const text=links.map(l=>l.vless).join('\\n');
  navigator.clipboard.writeText(text).then(()=>toast('همه‌ی '+toFa(links.length)+' کانفیگ کپی شد ✓','ok'));
}}

async function autoRefresh(){{
  try{{
    const data = await loadData(savedPw);
    if (!data.locked) renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    if (data.locked) {{ renderLock(data.name); return; }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML =
      '<div class="empty-state" style="color:var(--red-t)"><i class="ti ti-alert-circle"></i>خطا در بارگذاری</div>';
  }}
}}

init();
</script>
</body></html>"""