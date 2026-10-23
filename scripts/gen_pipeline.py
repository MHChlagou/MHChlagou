import sys

CYCLE = 9.0       # packet travels for RUN seconds, then the board holds green
RUN = 8.0
X_START, X_END, Y = 40, 820, 96
GREEN, YELLOW, RED, GREY, FG, EDGE, PANEL = "#3fb950", "#d29922", "#f85149", "#8b949e", "#e6edf3", "#30363d", "#161b22"

STAGES = [
    ("Plan", "threat model"),
    ("Code", "SAST · secrets"),
    ("Build", "SCA · SBOM"),
    ("Test", "DAST · pentest"),
    ("Release", "sign · verify"),
    ("Deploy", "IaC · policy"),
    ("Operate", "Vault · WAF"),
    ("Monitor", "SIEM · alerts"),
]
STEP = 104
X_FIRST = 66
HOLD = RUN / CYCLE


def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


nodes = []
for i, (stage, gate) in enumerate(STAGES):
    x = X_FIRST + i * STEP
    a = (x - X_START) / (X_END - X_START) * HOLD
    b = a + 0.1
    nodes.append(f'''<g>
  <circle cx="{x}" cy="{Y}" r="22" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0">
    <animate attributeName="r" values="22;22;36;36" keyTimes="0;{fmt(a)};{fmt(b)};1" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0;0.8;0;0" keyTimes="0;{fmt(a)};{fmt(a + 0.001)};{fmt(b)};1" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{x}" cy="{Y}" r="22" fill="{PANEL}" stroke="{EDGE}" stroke-width="2">
    <animate attributeName="stroke" values="{EDGE};{GREEN}" keyTimes="0;{fmt(a)}" calcMode="discrete" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
  </circle>
  <text x="{x}" y="{Y + 5}" class="num" text-anchor="middle" fill="{GREY}">{i + 1:02d}<animate attributeName="fill" values="{GREY};{GREEN}" keyTimes="0;{fmt(a)}" calcMode="discrete" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/></text>
  <text x="{x}" y="{Y + 46}" class="stage" text-anchor="middle" fill="{FG}">{stage}</text>
  <text x="{x}" y="{Y + 66}" class="gate" text-anchor="middle" fill="{RED}">{gate}</text>
</g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="190" viewBox="0 0 860 190" role="img" aria-labelledby="title">
<title id="title">DevSecOps pipeline: plan, code, build, test, release, deploy, operate, monitor, each stage behind a security gate</title>
<defs>
  <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
.head {{ font-size: 12px; }}
.num {{ font-size: 13px; font-weight: bold; }}
.stage {{ font-size: 13px; font-weight: bold; }}
.gate {{ font-size: 11px; }}
</style>
<rect x="0.5" y="0.5" width="859" height="189" rx="10" fill="#0d1117" stroke="{EDGE}"/>
<text x="24" y="30" class="head" fill="{GREY}">// secure delivery pipeline</text>
<g>
  <text x="836" y="30" class="head" text-anchor="end" fill="{YELLOW}" opacity="1">● pipeline running
    <animate attributeName="opacity" values="1;0" keyTimes="0;{fmt(HOLD)}" calcMode="discrete" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
  </text>
  <text x="836" y="30" class="head" text-anchor="end" fill="{GREEN}" opacity="0">✔ all gates passed
    <animate attributeName="opacity" values="0;1" keyTimes="0;{fmt(HOLD)}" calcMode="discrete" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
  </text>
</g>
<line x1="{X_START}" y1="{Y}" x2="{X_END}" y2="{Y}" stroke="{EDGE}" stroke-width="2" stroke-dasharray="4 8">
  <animate attributeName="stroke-dashoffset" from="0" to="-12" dur="0.6s" repeatCount="indefinite"/>
</line>
<line x1="{X_START}" y1="{Y}" x2="{X_START}" y2="{Y}" stroke="{GREEN}" stroke-width="2" opacity="0.7">
  <animate attributeName="x2" values="{X_START};{X_END};{X_END}" keyTimes="0;{fmt(HOLD)};1" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
</line>
{chr(10).join(nodes)}
<circle r="5" fill="{GREEN}" filter="url(#glow)">
  <animateMotion path="M{X_START} {Y} H{X_END}" keyPoints="0;1;1" keyTimes="0;{fmt(HOLD)};1" calcMode="linear" dur="{fmt(CYCLE)}s" repeatCount="indefinite"/>
</circle>
</svg>
'''
sys.stdout.write(svg)
