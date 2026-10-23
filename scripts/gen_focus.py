import sys
from html import escape

CYCLE = 10.0
SCAN = 1.6        # seconds spent scanning each card
FIRST, GAP = 0.4, 2.0
GREEN, YELLOW, CYAN, GREY, FG, EDGE, PANEL, BG = "#3fb950", "#d29922", "#58a6ff", "#8b949e", "#e6edf3", "#30363d", "#161b22", "#0d1117"
CARD_W, CARD_H = 394, 104
TRACK_W = 210

ICONS = {
    "pipeline": '<circle cx="8" cy="20" r="4"/><circle cx="20" cy="20" r="4"/><circle cx="32" cy="20" r="4"/><path d="M12 20 H16 M24 20 H28"/>',
    "target": '<circle cx="20" cy="20" r="11"/><circle cx="20" cy="20" r="4"/><path d="M20 4 V10 M20 30 V36 M4 20 H10 M30 20 H36"/>',
    "code": '<path d="M15 12 L7 20 L15 28 M25 12 L33 20 L25 28 M22 10 L18 30"/>',
    "shield": '<path d="M20 6 L32 11 V20 C32 28 26 33 20 35 C14 33 8 28 8 20 V11 Z"/><path d="M14 20 L18 24 L26 16"/>',
}

CARDS = [
    ("pipeline", "Secure CI/CD pipelines", "GitLab CI · GitHub Actions · Jenkins"),
    ("target", "Offensive security", "pentesting · Burp Suite · OWASP Top 10"),
    ("code", "Infrastructure as Code", "Terraform · Ansible · Kubernetes"),
    ("shield", "Shift-left security culture", "SAST · SCA · secrets on every commit"),
]


def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def anim(attr, values, key_times, discrete=False):
    mode = ' calcMode="discrete"' if discrete else ""
    return (f'<animate attributeName="{attr}" values="{";".join(values)}" '
            f'keyTimes="{";".join(fmt(k) for k in key_times)}"{mode} dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>')


def state(attr, a, b):
    return anim(attr, [EDGE, YELLOW, GREEN], [0, a, b], discrete=True)


cards = []
clips = []
last_done = 0
for i, (icon, title, sub) in enumerate(CARDS):
    x = 24 + (i % 2) * (CARD_W + 24)
    y = 52 + (i // 2) * (CARD_H + 16)
    start = FIRST + i * GAP
    a, b = start / CYCLE, (start + SCAN) / CYCLE
    last_done = b
    clips.append(f'<clipPath id="card{i}"><rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="8"/></clipPath>')
    cards.append(f'''<g>
  <rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="8" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5">{state("stroke", a, b)}</rect>
  <rect x="{x - 90}" y="{y}" width="90" height="{CARD_H}" fill="url(#beam)" clip-path="url(#card{i})">{anim("x", [str(x - 90), str(x - 90), str(x + CARD_W), str(x + CARD_W)], [0, a, b, 1])}</rect>
  <rect x="{x + 20}" y="{y + 22}" width="40" height="40" rx="8" fill="{BG}" stroke="{EDGE}">{state("stroke", a, b)}</rect>
  <g transform="translate({x + 20} {y + 22})" fill="none" stroke="{GREY}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{anim("stroke", [GREY, YELLOW, GREEN], [0, a, b], discrete=True)}{ICONS[icon]}</g>
  <text x="{x + 80}" y="{y + 38}" class="title" fill="{FG}">{escape(title)}</text>
  <text x="{x + 80}" y="{y + 58}" class="sub" fill="{GREY}">{escape(sub)}</text>
  <rect x="{x + 80}" y="{y + 76}" width="{TRACK_W}" height="6" rx="3" fill="#21262d"/>
  <rect x="{x + 80}" y="{y + 76}" width="0" height="6" rx="3" fill="{YELLOW}">{anim("width", ["0", "0", str(TRACK_W), str(TRACK_W)], [0, a, b, 1])}{anim("fill", [YELLOW, GREEN], [0, b], discrete=True)}</rect>
  <text x="{x + CARD_W - 20}" y="{y + 83}" class="sub" text-anchor="end" fill="{GREY}">queued{anim("opacity", ["1", "0"], [0, a], discrete=True)}</text>
  <text x="{x + CARD_W - 20}" y="{y + 83}" class="sub" text-anchor="end" fill="{YELLOW}" opacity="0">scanning{anim("opacity", ["0", "1", "0"], [0, a, b], discrete=True)}</text>
  <text x="{x + CARD_W - 20}" y="{y + 83}" class="sub" text-anchor="end" fill="{GREEN}" opacity="0">✔ verified{anim("opacity", ["0", "1"], [0, b], discrete=True)}</text>
</g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="330" viewBox="0 0 860 330" role="img" aria-labelledby="title">
<title id="title">Focus areas: secure CI/CD pipelines, offensive security, infrastructure as code, shift-left security culture. Motto: automate everything, trust nothing, verify always.</title>
<defs>
  <linearGradient id="beam" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.8" stop-color="{GREEN}" stop-opacity="0.22"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  {chr(10).join(clips)}
</defs>
<style>
text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
.head {{ font-size: 12px; }}
.title {{ font-size: 15px; font-weight: bold; }}
.sub {{ font-size: 12px; }}
.motto {{ font-size: 14px; }}
</style>
<rect x="0.5" y="0.5" width="859" height="329" rx="10" fill="{BG}" stroke="{EDGE}"/>
<text x="24" y="32" class="head" fill="{GREY}">// focus areas</text>
<text x="836" y="32" class="head" text-anchor="end" fill="{YELLOW}">● scanning{anim("opacity", ["1", "0"], [0, last_done], discrete=True)}</text>
<text x="836" y="32" class="head" text-anchor="end" fill="{GREEN}" opacity="0">✔ 4/4 verified{anim("opacity", ["0", "1"], [0, last_done], discrete=True)}</text>
{chr(10).join(cards)}
<text x="24" y="308" class="motto"><tspan fill="{GREEN}">»</tspan><tspan fill="{FG}"> Automate everything. Trust nothing.</tspan><tspan fill="{GREY}" font-weight="bold"> Verify always.{anim("fill", [GREY, GREEN], [0, last_done], discrete=True)}</tspan></text>
</svg>
'''
sys.stdout.write(svg)
