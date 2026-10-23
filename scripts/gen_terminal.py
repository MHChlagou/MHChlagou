import sys
from html import escape

CW = 8.4          # forced glyph advance (textLength) so typing steps line up
FS = 14
X0 = 24
CMD_X = X0 + 2 * CW
CYCLE = 16.0
CLEAR_AT = 14.6
CHAR_S = 0.085    # seconds per typed char

GREEN, CYAN, RED, GREY, FG, YELLOW = "#3fb950", "#58a6ff", "#f85149", "#8b949e", "#e6edf3", "#d29922"

out = []
defs = []


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def visible_from(t):
    return f'<set attributeName="opacity" to="1" begin="cycle.begin+{fmt(t)}s" dur="{fmt(CLEAR_AT - t)}s"/>'


def prompt(y, t):
    out.append(f'<text x="{X0}" y="{y}" fill="{GREEN}" opacity="0">${visible_from(t)}</text>')


def typed(y, t, cmd, cid):
    n = len(cmd)
    width = n * CW
    dur = n * CHAR_S
    steps = ";".join(fmt(i * CW) for i in range(n + 1))
    defs.append(
        f'<clipPath id="{cid}"><rect x="{fmt(CMD_X)}" y="{y - FS}" width="0" height="{FS + 6}">'
        f'<animate attributeName="width" values="{steps}" calcMode="discrete" '
        f'begin="cycle.begin+{fmt(t)}s" dur="{fmt(dur)}s" fill="freeze"/></rect></clipPath>'
    )
    out.append(
        f'<text x="{fmt(CMD_X)}" y="{y}" fill="{FG}" textLength="{fmt(width)}" lengthAdjust="spacingAndGlyphs" '
        f'clip-path="url(#{cid})" opacity="0">{escape(cmd)}{visible_from(t)}</text>'
    )
    xs = ";".join(fmt(CMD_X + i * CW) for i in range(n + 1))
    out.append(
        f'<rect x="{fmt(CMD_X)}" y="{y - FS + 2}" width="{CW}" height="{FS + 2}" fill="{FG}" opacity="0">'
        f'<animate attributeName="x" values="{xs}" calcMode="discrete" begin="cycle.begin+{fmt(t)}s" dur="{fmt(dur)}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.8" begin="cycle.begin+{fmt(t)}s" dur="{fmt(dur + 0.3)}s"/></rect>'
    )
    return t + dur


def line(y, t, spans):
    parts = "".join(
        f'<tspan x="{fmt(X0 + col * CW)}" fill="{color}"{weight}>{escape(text)}</tspan>'
        for col, color, text, weight in spans
    )
    out.append(f'<text y="{y}" opacity="0">{parts}{visible_from(t)}</text>')


t = 0.3
prompt(70, t)
t = typed(70, t + 0.4, "whoami", "c1") + 0.4
line(94, t, [(0, FG, "Mohamed Hedi CHLAGOU", ' font-weight="bold"'), (21, GREY, "·", ""), (23, CYAN, "Tech Lead DevSecOps & Pentester", "")])
t += 0.6
prompt(128, t)
t = typed(128, t + 0.4, "lintel run --hook pre-push", "c2") + 0.4
for i, (check, tool) in enumerate([("secrets", "gitleaks"), ("sast", "opengrep"), ("sca", "osv-scanner")]):
    line(152 + i * 24, t, [(2, GREEN, "✔", ""), (4, CYAN, check, ""), (14, GREY, tool, ""), (29, GREEN, "0 findings", "")])
    t += 0.35
t += 0.3
prompt(234, t)
t = typed(234, t + 0.4, "git push origin main", "c3") + 0.5
line(258, t, [(0, GREY, "→", ""), (2, FG, "build", ""), (8, YELLOW, "▸", ""), (10, FG, "scan", ""), (15, YELLOW, "▸", ""),
              (17, FG, "sign", ""), (22, YELLOW, "▸", ""), (24, FG, "deploy", ""), (32, GREEN, "✔ shipped", ' font-weight="bold"')])
t += 0.7
prompt(286, t)
out.append(
    f'<rect x="{fmt(CMD_X)}" y="{286 - FS + 2}" width="{CW}" height="{FS + 2}" fill="{FG}" opacity="0">'
    f'<set attributeName="opacity" to="0.8" begin="cycle.begin+{fmt(t)}s" dur="{fmt(CLEAR_AT - t)}s"/>'
    f'<animate attributeName="fill" values="{FG};#0d1117" calcMode="discrete" dur="1s" repeatCount="indefinite"/></rect>'
)
assert t < CLEAR_AT, t

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="310" viewBox="0 0 860 310" role="img" aria-labelledby="title">
<title id="title">Terminal: whoami, lintel pre-push scan with zero findings, git push ships a signed build</title>
<defs>
{chr(10).join(defs)}
</defs>
<style>
text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: {FS}px; }}
.title {{ font-size: 12px; }}
</style>
<rect width="0" height="0"><animate id="cycle" attributeName="x" from="0" to="0" begin="0s;cycle.end" dur="{fmt(CYCLE)}s"/></rect>
<rect x="0.5" y="0.5" width="859" height="309" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M10.5 0.5 H849.5 A10 10 0 0 1 859.5 10.5 V36.5 H0.5 V10.5 A10 10 0 0 1 10.5 0.5 Z" fill="#161b22" stroke="#30363d"/>
<circle cx="22" cy="18.5" r="6" fill="#ff5f56"/>
<circle cx="42" cy="18.5" r="6" fill="#ffbd2e"/>
<circle cx="62" cy="18.5" r="6" fill="#27c93f"/>
<text class="title" x="430" y="23" fill="{GREY}" text-anchor="middle">hedi@secops: ~/MHChlagou</text>
{chr(10).join(out)}
</svg>
'''
sys.stdout.write(svg)
