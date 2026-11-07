"""Generates the R&R tracksuit flat sketch (zip track top + track pants, front & back)."""
import base64, random
random.seed(7)
logo = base64.b64encode(open("rr-mark.png", "rb").read()).decode()
def img(x, y, w, op=1):
    return f'<image href="data:image/png;base64,{logo}" x="{x}" y="{y}" width="{w}" height="{w*0.6:.1f}" opacity="{op}"/>'

stops, x = [], 0.0
while x < 1.0:
    stops.append(f'<stop offset="{x:.3f}" stop-color="#fff" stop-opacity="{random.choice([0.05,0.1,0.15,0.55,0.8,1.0]):.2f}"/>')
    x += random.uniform(0.012, 0.045)

TOP = ("M245 58 Q300 {n} 355 58 L430 80 C480 110 520 250 545 560 L495 578 "
       "C480 420 465 320 450 255 C448 380 446 500 444 625 Q300 634 156 625 "
       "C154 500 152 380 150 255 C135 320 120 420 105 578 L55 560 C80 250 120 110 170 80 Z")

def top(vid, front):
    p = TOP.format(n=96 if front else 74)
    collar = ('<path d="M238 30 Q300 40 362 30 L358 64 Q300 96 242 64 Z" fill="#050505" stroke="#555" stroke-width="1"/>'
              '<path d="M240 32 Q300 42 360 32" stroke="#fff" stroke-width="2.5" fill="none"/>') if front else \
             ('<path d="M238 30 Q300 22 362 30 L358 64 Q300 76 242 64 Z" fill="#050505" stroke="#555" stroke-width="1"/>'
              '<path d="M240 32 Q300 24 360 32" stroke="#fff" stroke-width="2.5" fill="none"/>')
    zip_ = ('<line x1="300" y1="38" x2="300" y2="630" stroke="#bbb" stroke-width="3"/>'
            '<line x1="300" y1="38" x2="300" y2="630" stroke="#000" stroke-width="1.4" stroke-dasharray="1.5 1.5"/>'
            '<rect x="295.5" y="40" width="9" height="20" rx="2" fill="#ddd" stroke="#888"/>'
            '<g stroke="#9a9a9a" stroke-width="2" fill="none"><path d="M212 455 L224 545"/><path d="M388 455 L376 545"/></g>') if front else \
           '<path d="M300 64 L300 598" stroke="#fff" stroke-opacity=".12" stroke-width="1" stroke-dasharray="3 3"/>'
    logo_el = img(352, 128, 44) if front else img(287, 80, 26, .9)
    ny = 70 if front else 64
    return f'''
  <g>
    <clipPath id="c-{vid}"><path d="{p}"/></clipPath>
    <path d="{p}" fill="#0a0a0a"/>
    <g clip-path="url(#c-{vid})">
      <rect width="600" height="720" fill="url(#grid)" opacity=".09"/>
      <rect width="600" height="720" fill="url(#grid)" mask="url(#bandmask)" opacity=".42"/>
      <rect width="600" height="720" fill="url(#pin)" mask="url(#bandmask)" opacity=".2"/>
      <rect width="600" height="720" fill="url(#vfade)"/>
      <path d="M180 80 C124 128 84 264 63 566" stroke="#fff" stroke-width="5" fill="none"/>
      <path d="M420 80 C476 128 516 264 537 566" stroke="#fff" stroke-width="5" fill="none"/>
      <path d="M55 560 L105 578 L101 608 L50 590 Z" fill="url(#rib)"/>
      <path d="M545 560 L495 578 L499 608 L550 590 Z" fill="url(#rib)"/>
      <rect x="140" y="596" width="320" height="40" fill="url(#rib)"/>
      <line x1="150" y1="597" x2="450" y2="597" stroke="#444" stroke-width="1"/>
      <g stroke="#fff" stroke-width="3" fill="none">
        <path d="M262 {ny} Q200 150 152 255 C190 350 198 470 186 597"/>
        <path d="M338 {ny} Q400 150 448 255 C410 350 402 470 414 597"/>
      </g>
      <g stroke="#fff" stroke-opacity=".35" stroke-width="1" stroke-dasharray="3 3" fill="none">
        <path d="M262 {ny+6} Q205 152 158 255 C196 350 204 470 192 597"/>
        <path d="M338 {ny+6} Q395 152 442 255 C404 350 396 470 408 597"/>
      </g>
      {zip_}
      {logo_el}
    </g>
    {collar}
    <path d="{p}" fill="none" stroke="#9a9a9a" stroke-width="1.5"/>
  </g>'''

PANT = ("M40 40 L320 40 L322 78 C332 300 318 500 304 690 L216 694 C208 500 196 330 180 262 "
        "C164 330 152 500 144 694 L56 690 C42 500 28 300 38 78 Z")

def pants(vid, front):
    extras = ('<g stroke="#777" stroke-width="2" fill="none"><path d="M62 92 L82 205"/><path d="M298 92 L278 205"/></g>'
              '<path d="M180 78 L180 255" stroke="#333" stroke-width="1" stroke-dasharray="3 3"/>'
              '<g stroke="#eee" stroke-width="2.2" fill="none" stroke-linecap="round">'
              '<path d="M172 62 C168 90 164 105 158 125"/><path d="M188 62 C192 90 196 105 202 125"/></g>'
              '<g fill="#eee"><circle cx="172" cy="60" r="3"/><circle cx="188" cy="60" r="3"/></g>'
              + img(228, 112, 38)) if front else \
             ('<path d="M44 120 Q180 140 316 120" stroke="#333" stroke-width="1" stroke-dasharray="3 3" fill="none"/>'
              '<path d="M180 78 L180 255" stroke="#333" stroke-width="1" stroke-dasharray="3 3"/>'
              '<path d="M232 150 L292 150" stroke="#777" stroke-width="2"/>')
    return f'''
  <g>
    <clipPath id="c-{vid}"><path d="{PANT}"/></clipPath>
    <path d="{PANT}" fill="#0b0b0b"/>
    <g clip-path="url(#c-{vid})">
      <rect width="360" height="720" fill="url(#sheen)"/>
      <rect x="0" y="40" width="360" height="38" fill="url(#rib)"/>
      <line x1="38" y1="78" x2="322" y2="78" stroke="#444"/>
      <rect x="0" y="672" width="360" height="30" fill="url(#rib)"/>
      <g stroke="#bbb" stroke-width="2"><path d="M58 672 L55 630"/><path d="M302 672 L305 630"/></g>
      {extras}
    </g>
    <path d="{PANT}" fill="none" stroke="#9a9a9a" stroke-width="1.5"/>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2080 820" width="2080" height="820">
  <defs>
    <pattern id="grid" width="4.5" height="4.5" patternUnits="userSpaceOnUse"><rect x=".8" y=".8" width="2.9" height="2.9" fill="#fff"/></pattern>
    <pattern id="pin" width="4.5" height="4.5" patternUnits="userSpaceOnUse"><rect width=".8" height="4.5" fill="#fff"/></pattern>
    <pattern id="rib" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="#050505"/><rect width="1" height="3" fill="#1c1c1c"/></pattern>
    <linearGradient id="bandgrad" x1="0" x2="600" y1="0" y2="0" gradientUnits="userSpaceOnUse">{''.join(stops)}</linearGradient>
    <mask id="bandmask"><rect width="600" height="720" fill="url(#bandgrad)"/></mask>
    <linearGradient id="vfade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity=".1"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" x2="360" y1="0" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff" stop-opacity=".07"/>
      <stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".65" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".8" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="2080" height="820" fill="#f2f1ee"/>
  <g transform="translate(10,70)">{top("tf", True)}</g>
  <g transform="translate(590,70)">{top("tb", False)}</g>
  <g transform="translate(1250,70)">{pants("pf", True)}</g>
  <g transform="translate(1660,70)">{pants("pb", False)}</g>
  <g font-family="Helvetica, Arial, sans-serif" fill="#222" text-anchor="middle" font-size="17" letter-spacing="4">
    <text x="310" y="790">TRACK TOP · FRONT</text><text x="890" y="790">TRACK TOP · BACK</text>
    <text x="1430" y="790">PANTS · FRONT</text><text x="1840" y="790">PANTS · BACK</text>
    <text x="1040" y="38" font-size="15" letter-spacing="3" fill="#666">R&amp;R · TRACKSUIT · POLYESTER TRICOT · BLACK / WHITE</text>
  </g>
</svg>'''
open("rr-tracksuit.svg", "w").write(svg)
open("index.html", "w").write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>R&amp;R Tracksuit</title>'
  '<style>body{margin:0;background:#f2f1ee;display:flex;justify-content:center}svg{max-width:100%;height:auto}</style>'
  f'</head><body>{svg}</body></html>')
