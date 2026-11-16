import base64, io, sys
from PIL import Image, ImageDraw, ImageOps
d = sys.argv[1]
INK, PAPER, RED = "#0A0A0A", "#F2F1EC", "#E61919"
def halftone(src, w, h, ink, step=5):
    S = 2  # render at 2x
    im = ImageOps.fit(Image.open(f"{d}/{src}").convert("L"), (w*S//step, h*S//step))
    im = ImageOps.autocontrast(im, cutoff=4)
    im = im.point(lambda v: int(255*((v/255)**0.8)))
    out = Image.new("RGB", (w*S, h*S), PAPER)
    dr = ImageDraw.Draw(out)
    for y in range(im.height):
        for x in range(im.width):
            r = (1 - im.getpixel((x, y)) / 255) * step * 0.62
            if r > .6:
                cx, cy = x*step + step/2 + (step/2 if y % 2 else 0), y*step + step/2
                dr.ellipse((cx-r, cy-r, cx+r, cy+r), fill=ink)
    buf = io.BytesIO(); out.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()
f64 = lambda n: base64.b64encode(open(f"{d}/f/{n}", "rb").read()).decode()
A = halftone("superman.jpg", 280, 262, INK)
B = halftone("latveria.jpg", 196, 262, RED)
rows = [("NAME", "TRIBHUVAN"), ("ROLE", "FULL-STACK · MOBILE · AI ENGINEER"), ("BUILDS", "PRODUCTS END TO END"),
        ("SHIPS WITH", "REACT · NEXT · FLUTTER · FASTAPI"), ("FOCUS", "AGENTIC AI — SYSTEMS THAT ACT"),
        ("STATUS", "OPEN TO COLLABS / OSS / FREELANCE")]
y0, rh = 62, 52
R = []
for i, (k, v) in enumerate(rows):
    y = y0 + i*rh
    R.append(f'<text class="m" x="36" y="{y+32}" fill="{RED}">{k}</text>'
             f'<line x1="170" y1="{y+30}" x2="250" y2="{y+30}" stroke="{INK}" stroke-dasharray="1 5" stroke-width="2"/>'
             f'<text class="m b" x="262" y="{y+32}">{v}</text>'
             f'<line x1="18" y1="{y+rh}" x2="652" y2="{y+rh}" stroke="{INK}" stroke-opacity=".25"/>')
R[-1] = R[-1].replace('x="262"', 'x="284"') + f'<rect class="blink" x="262" y="{y0+5*rh+21}" width="12" height="12" fill="{RED}"/>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400">
<defs><style>
@font-face{{font-family:JM;src:url(data:font/woff2;base64,{f64("mono.woff2")})}}
@font-face{{font-family:AB;src:url(data:font/woff2;base64,{f64("archivo-full.woff2")})}}
.m{{font-family:JM,'Courier New',monospace;font-size:14px;letter-spacing:.12em;fill:{INK}}}
.b{{font-weight:700}}
.blink{{animation:k 1.1s steps(1) infinite}}@keyframes k{{50%{{opacity:0}}}}
.stamp{{animation:s .5s cubic-bezier(.2,1.6,.4,1) 1s both}}@keyframes s{{from{{opacity:0;transform:scale(1.6)}}}}
</style>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0"/></filter></defs>
<rect width="1200" height="400" fill="{PAPER}"/>
<rect x="17" y="17" width="1166" height="366" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="18" y="18" width="96" height="44" fill="{RED}"/><text class="m b" x="66" y="46" text-anchor="middle" style="fill:{PAPER};font-size:17px">01</text>
<line x1="114" y1="18" x2="114" y2="62" stroke="{INK}" stroke-width="2"/>
<text x="136" y="50" font-family="AB,'Arial Black',sans-serif" font-size="26" fill="{INK}" letter-spacing="1">DOSSIER</text>
<text class="m" x="1164" y="45" text-anchor="end" style="font-size:12px">FILE NO. TRB-26-001  ///  CLASSIFICATION: PUBLIC</text>
<line x1="18" y1="62" x2="1182" y2="62" stroke="{INK}" stroke-width="2"/>
{"".join(R)}
<line x1="652" y1="62" x2="652" y2="382" stroke="{INK}" stroke-width="2"/>
<rect x="672" y="76" width="280" height="262" fill="none" stroke="{INK}" stroke-width="2"/>
<image x="672" y="76" width="280" height="262" href="data:image/png;base64,{A}"/>
<rect x="672" y="76" width="280" height="262" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="968" y="76" width="196" height="262" fill="none" stroke="{INK}" stroke-width="2"/>
<image x="968" y="76" width="196" height="262" href="data:image/png;base64,{B}"/>
<rect x="968" y="76" width="196" height="262" fill="none" stroke="{INK}" stroke-width="2"/>
<text class="m" x="672" y="362" style="font-size:11px"><tspan fill="{RED}">PLATE A</tspan> — DISPOSITION: GOOD</text>
<text class="m" x="968" y="362" style="font-size:11px"><tspan fill="{RED}">PLATE B</tspan> — TRAVEL DOC</text>
<g transform="translate(1066,306) rotate(-9)"><g class="stamp">
<rect x="-92" y="-26" width="184" height="52" fill="{PAPER}" fill-opacity=".55" stroke="{RED}" stroke-width="4"/>
<rect x="-85" y="-19" width="170" height="38" fill="none" stroke="{RED}" stroke-width="1.5"/>
<text x="0" y="11" text-anchor="middle" font-family="AB,'Arial Black',sans-serif" font-size="28" fill="{RED}" letter-spacing="3">CLEARED</text></g></g>
<rect width="1200" height="400" filter="url(#grain)" opacity=".16" style="mix-blend-mode:multiply"/>
</svg>'''
open(f"{d}/dossier.svg", "w", encoding="utf-8").write(svg)
print(len(svg)//1024, "KB")
