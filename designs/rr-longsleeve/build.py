"""Generates the R&R long-sleeve flat sketch (front + back) as SVG + HTML."""
import base64, random
random.seed(7)
logo = base64.b64encode(open("rr-mark.png","rb").read()).decode()

# Vertical streak bands (black & white take on the reference's light-streak grid)
stops = []
x = 0.0
while x < 1.0:
    stops.append(f'<stop offset="{x:.3f}" stop-color="#fff" stop-opacity="{random.choice([0.05,0.1,0.15,0.55,0.8,1.0]):.2f}"/>')
    x += random.uniform(0.012, 0.045)

def body(neck_ctrl_y):
    return (f"M245 58 Q300 {neck_ctrl_y} 355 58 L430 80 C480 110 520 250 545 560 L495 578 "
            "C480 420 465 320 450 255 C448 380 446 500 444 605 Q300 616 156 605 "
            "C154 500 152 380 150 255 C135 320 120 420 105 578 L55 560 C80 250 120 110 170 80 Z")

def view(vid, neck_ctrl_y, front):
    path = body(neck_ctrl_y)
    logo_el = (f'<image href="data:image/png;base64,{logo}" x="270" y="118" width="60" height="36"/>' if front
               else f'<image href="data:image/png;base64,{logo}" x="287" y="86" width="26" height="16" opacity=".9"/>')
    return f'''
  <g id="{vid}">
    <clipPath id="clip-{vid}"><path d="{path}"/></clipPath>
    <path d="{path}" fill="#0a0a0a"/>
    <g clip-path="url(#clip-{vid})">
      <rect width="600" height="720" fill="url(#grid)" opacity=".09"/>
      <rect width="600" height="720" fill="url(#grid)" mask="url(#bandmask)" opacity=".42"/>
      <rect width="600" height="720" fill="url(#pin)" mask="url(#bandmask)" opacity=".2"/>
      <rect width="600" height="720" fill="url(#vfade)"/>
      <!-- sleeve strips -->
      <path d="M205 75 C150 120 112 260 88 566" stroke="#fff" stroke-width="24" fill="none"/>
      <path d="M395 75 C450 120 488 260 512 566" stroke="#fff" stroke-width="24" fill="none"/>
      <!-- cuffs -->
      <path d="M55 560 L105 578 L101 606 L50 588 Z" fill="#000"/>
      <path d="M545 560 L495 578 L499 606 L550 588 Z" fill="#000"/>
      <!-- raglan + side-panel piping -->
      <g stroke="#fff" stroke-width="3" fill="none">
        <path d="M262 {66 if front else 60} Q200 150 152 255 C190 350 198 470 186 615"/>
        <path d="M338 {66 if front else 60} Q400 150 448 255 C410 350 402 470 414 615"/>
      </g>
      <g stroke="#fff" stroke-opacity=".35" stroke-width="1" stroke-dasharray="3 3" fill="none">
        <path d="M262 {72 if front else 66} Q205 152 158 255 C196 350 204 470 192 615"/>
        <path d="M338 {72 if front else 66} Q395 152 442 255 C404 350 396 470 408 615"/>
      </g>
      <!-- neck binding -->
      <path d="M245 58 Q300 {neck_ctrl_y} 355 58" stroke="#000" stroke-width="12" fill="none"/>
      <path d="M249 66 Q300 {neck_ctrl_y+8} 351 66" stroke="#fff" stroke-opacity=".3" stroke-width="1" stroke-dasharray="3 3" fill="none"/>
      {logo_el}
    </g>
    <path d="{path}" fill="none" stroke="#9a9a9a" stroke-width="1.5"/>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 760" width="1300" height="760">
  <defs>
    <pattern id="grid" width="4.5" height="4.5" patternUnits="userSpaceOnUse">
      <rect x=".8" y=".8" width="2.9" height="2.9" fill="#fff"/>
    </pattern>
    <pattern id="pin" width="4.5" height="4.5" patternUnits="userSpaceOnUse">
      <rect x="0" width=".8" height="4.5" fill="#fff"/>
    </pattern>
    <linearGradient id="bandgrad" x1="0" x2="600" y1="0" y2="0" gradientUnits="userSpaceOnUse">
      {''.join(stops)}
    </linearGradient>
    <mask id="bandmask"><rect width="600" height="720" fill="url(#bandgrad)"/></mask>
    <linearGradient id="vfade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity=".1"/>
      <stop offset=".55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".45"/>
    </linearGradient>
  </defs>
  <rect width="1300" height="760" fill="#f2f1ee"/>
  <g transform="translate(20,60)">{view("front", 118, True)}</g>
  <g transform="translate(680,60)">{view("back", 74, False)}</g>
  <g font-family="Helvetica, Arial, sans-serif" fill="#222" text-anchor="middle">
    <text x="320" y="725" font-size="18" letter-spacing="4">FRONT</text>
    <text x="980" y="725" font-size="18" letter-spacing="4">BACK</text>
    <text x="650" y="36" font-size="15" letter-spacing="3" fill="#666">R&amp;R · PERFORMANCE LONG SLEEVE · BLACK / WHITE</text>
  </g>
</svg>'''
open("rr-longsleeve.svg","w").write(svg)
open("index.html","w").write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>R&amp;R Long Sleeve</title>'
  '<style>body{{margin:0;background:#f2f1ee;display:flex;justify-content:center}}svg{{max-width:100%;height:auto}}</style>'
  f'</head><body>{svg}</body></html>')
