import pathlib
import sys
from html import escape

GREEN, CYAN, GREY, FG, EDGE, PANEL, BG = "#3fb950", "#58a6ff", "#8b949e", "#e6edf3", "#30363d", "#161b22", "#0d1117"
CHIP_CHAR_W = 6.6
STYLE = '''<style>
.sans { font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
</style>'''

# icons are drawn in a 44x44 box, stroke colour comes from the parent group
ICONS = {
    "shield": '<path d="M22 7 L34 12 V21 C34 29 28 35 22 37 C16 35 10 29 10 21 V12 Z"/><path d="M16 22 L20 26 L28 17"/>',
    "prompt": ('<path d="M10 11 H34 A3 3 0 0 1 37 14 V27 A3 3 0 0 1 34 30 H21 L14 36 V30 H10 A3 3 0 0 1 7 27 V14 A3 3 0 0 1 10 11 Z"/>'
               '<path d="M22 16 V22 M22 25.5 V26"/>'
               '<animate attributeName="opacity" values="1;1;0.2;1;0.4;1;1" keyTimes="0;0.8;0.82;0.84;0.86;0.88;1" dur="4s" repeatCount="indefinite"/>'),
    "helm": ('<g><circle cx="22" cy="22" r="11"/><circle cx="22" cy="22" r="3"/>'
             + "".join(f'<path d="M22 22 V8" transform="rotate({i * 360 / 7:.1f} 22 22)"/>' for i in range(7))
             + '<animateTransform attributeName="transform" type="rotate" values="0 22 22;360 22 22" dur="20s" repeatCount="indefinite"/></g>'),
    "wallet": ('<path d="M9 14 H33 A2 2 0 0 1 35 16 V32 A2 2 0 0 1 33 34 H11 A2 2 0 0 1 9 32 Z"/><path d="M9 14 L28 9 V14"/>'
               '<path d="M35 20 H28 A4 4 0 0 0 28 28 H35"/><circle cx="29" cy="24" r="1" fill="currentColor"/>'),
    "candles": "".join(
        f'<path d="M{x} {top} V{bot}"/><rect x="{x - 3}" y="{y}" width="6" height="{h}" rx="1">'
        f'<animate attributeName="height" values="{h};{h2};{h}" dur="{d}s" repeatCount="indefinite"/></rect>'
        for x, top, bot, y, h, h2, d in [(13, 12, 34, 17, 10, 14, 3.1), (22, 8, 30, 12, 13, 8, 2.6), (31, 10, 36, 15, 14, 18, 3.7)]
    ),
}


def chips(x, y, items):
    out = []
    for item in items:
        w = len(item) * CHIP_CHAR_W + 18
        out.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{PANEL}" stroke="{EDGE}"/>'
                   f'<text x="{x + w / 2:.1f}" y="{y + 15}" class="mono" font-size="11" text-anchor="middle" fill="#c9d1d9">{escape(item)}</text>')
        x += w + 8
    return "".join(out)


def frame(w, h, accent, sweep_begin):
    return f'''<defs>
  <linearGradient id="top" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.05"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
  <radialGradient id="halo" cx="0" cy="0" r="{w * 0.6:.0f}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{accent}" stop-opacity="0.12"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10"/></clipPath>
</defs>
{STYLE}
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#halo)"/>
  <rect width="{w}" height="2" fill="url(#top)"/>
  <rect x="-160" y="0" width="160" height="{h}" fill="url(#sweep)" transform="skewX(-20)">
    <animate attributeName="x" values="-160;{w + 160};{w + 160}" keyTimes="0;0.25;1" dur="8s" begin="{sweep_begin}s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="none" stroke="{EDGE}"/>'''


def icon_box(x, y, accent, icon):
    return (f'<rect x="{x}" y="{y}" width="44" height="44" rx="10" fill="{accent}" fill-opacity="0.1" stroke="{accent}" stroke-opacity="0.45"/>'
            f'<g transform="translate({x} {y})" fill="none" stroke="{accent}" color="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>')


def small_card(app, sweep_begin):
    w, h = 424, 184
    lines = "".join(f'<text x="24" y="{104 + i * 19}" class="sans" font-size="13.5" fill="{GREY}">{escape(t)}</text>' for i, t in enumerate(app["desc"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(app["name"])}: {escape(" ".join(app["desc"]))}</title>
{frame(w, h, app["accent"], sweep_begin)}
{icon_box(24, 24, app["accent"], app["icon"])}
<text x="82" y="43" class="sans" font-size="18" font-weight="700" fill="{FG}">{escape(app["name"])}</text>
<text x="82" y="62" class="mono" font-size="10.5" letter-spacing="1.5" fill="{app["accent"]}">{escape(app["kicker"])}</text>
<text x="{w - 22}" y="42" class="mono" font-size="16" text-anchor="end" fill="{GREY}">↗</text>
{lines}
{chips(24, 142, app["chips"])}
</svg>
'''


def featured_card(app):
    w, h = 860, 200
    lines = "".join(f'<text x="28" y="{112 + i * 21}" class="sans" font-size="15" fill="{GREY}">{escape(t)}</text>' for i, t in enumerate(app["desc"]))
    gx, gy = 700, 92
    hooks = ["pre-commit", "commit-msg", "pre-push"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(app["name"])}: {escape(" ".join(app["desc"]))}</title>
{frame(w, h, app["accent"], 0)}
{icon_box(28, 28, app["accent"], app["icon"])}
<text x="88" y="50" class="sans" font-size="24" font-weight="700" fill="{FG}">{escape(app["name"])}</text>
<text x="88" y="70" class="mono" font-size="11" letter-spacing="1.5" fill="{app["accent"]}">{escape(app["kicker"])}</text>
{lines}
{chips(28, 156, app["chips"])}
<g class="mono" font-size="11">
  <line x1="560" y1="{gy}" x2="840" y2="{gy}" stroke="{EDGE}" stroke-width="2" stroke-dasharray="3 6"/>
  <text x="560" y="{gy - 16}" fill="{GREY}">git commit</text>
  <text x="840" y="{gy - 16}" text-anchor="end" fill="{GREEN}">✔ clean</text>
  <circle r="6" cy="{gy}" fill="#d29922">
    <animate attributeName="cx" values="560;{gx};{gx};840;840" keyTimes="0;0.35;0.6;0.95;1" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="fill" values="#d29922;{GREEN}" keyTimes="0;0.6" calcMode="discrete" dur="4s" repeatCount="indefinite"/>
  </circle>
  <g transform="translate({gx} {gy})">
    <circle r="26" fill="{BG}" stroke="{EDGE}" stroke-width="1.5">
      <animate attributeName="stroke" values="{EDGE};#d29922;{GREEN};{EDGE}" keyTimes="0;0.35;0.6;0.95" calcMode="discrete" dur="4s" repeatCount="indefinite"/>
    </circle>
    <path d="M0 -15 L12 -10 V-1 C12 7 6 12 0 14 C-6 12 -12 7 -12 -1 V-10 Z" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round"/>
  </g>
  {"".join(f'<text x="{gx}" y="{gy + 48 + i * 15}" text-anchor="middle" fill="{GREY}" opacity="0.5">{h}<animate attributeName="opacity" values="0.5;1;0.5" keyTimes="0;{0.4 + i * 0.06:.2f};1" dur="4s" repeatCount="indefinite"/></text>' for i, h in enumerate(hooks))}
</g>
</svg>
'''


APPS = {
    "lintel": {"name": "Lintel", "kicker": "FEATURED · OPEN-SOURCE DEVSECOPS TOOL", "accent": GREEN, "icon": "shield",
                   "desc": ["One Go binary that turns your Git hooks into a security", "checkpoint: secrets, SAST, SCA and lint behind one YAML spec."],
                   "chips": ["Go", "gitleaks", "opengrep", "osv-scanner", "Sigstore"]},
    "prompt-breach": {"name": "PROMPT//BREACH", "kicker": "AI SECURITY · TRAINING GAME", "accent": "#f778ba", "icon": "prompt",
                          "desc": ["Cyberpunk prompt-injection simulator. Attack a bot", "as red team, then defend it as blue team."],
                          "chips": ["TypeScript", "6 missions", "in-browser"]},
    "k8s-course": {"name": "Formation Kubernetes", "kicker": "TRAINING · SLIDES (FR)", "accent": "#326ce5", "icon": "helm",
                       "desc": ["Interactive Kubernetes course slides,", "passphrase-protected with staticrypt."],
                       "chips": ["Slidev", "Vue", "staticrypt"]},
    "monthly-money": {"name": "Monthly Money", "kicker": "PERSONAL FINANCE · PWA", "accent": "#e3b341", "icon": "wallet",
                          "desc": ["Offline-first monthly money tracker, installable", "on any device. Your data never leaves it."],
                          "chips": ["TypeScript", "Vite", "offline-first"]},
    "trading-course": {"name": "Trading: Zéro → Maîtrise", "kicker": "COURSE (FR) · 63 CHAPTERS", "accent": "#f0883e", "icon": "candles",
                           "desc": ["10 levels and 10 exams: risk management,", "order flow, macro and Python backtesting."],
                           "chips": ["Docusaurus", "Python"]},
}

out_dir = pathlib.Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "lintel.svg").write_text(featured_card(APPS["lintel"]))
for i, key in enumerate(["prompt-breach", "k8s-course", "monthly-money", "trading-course"]):
    (out_dir / f"{key}.svg").write_text(small_card(APPS[key], 1 + i * 1.5))
