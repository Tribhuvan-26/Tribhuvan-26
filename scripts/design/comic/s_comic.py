import sys, os, math, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
random.seed(7)
INK, P, Y, R, C = "#111111", "#F6EEDA", "#FFD400", "#E4252C", "#00A3E0"
W, H = 1200, 1700


def burst(cx, cy, r1, r2, n=18, rot=0):
    pts = []
    for i in range(n*2):
        a = math.pi*i/n + rot
        r = (r1 if i % 2 == 0 else r2) * (1 + random.uniform(-.08, .08))
        pts.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}")
    return " ".join(pts)


def dots(id_, col, s=10, r=2.4):
    return f'<pattern id="{id_}" width="{s}" height="{s}" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><circle cx="{s/2}" cy="{s/2}" r="{r}" fill="{col}"/></pattern>'


def panel(x, y, w, h, fill, extra="", tilt=0):
    return (f'<g transform="rotate({tilt} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>{extra}'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="6"/></g>')


def caption(x, y, text, w=None, fill=Y, size=20):
    w = w or len(text)*size*.62 + 28
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size+20}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<text class="cap" x="{x+14}" y="{y+size+5}" font-size="{size}">{text}</text>')


img = halftone("superman.jpg", 436, 360, C, P, step=6, scale=.7)
speed = "".join(f'<line x1="330" y1="230" x2="{330+900*math.cos(a):.0f}" y2="{230+900*math.sin(a):.0f}" stroke="{INK}" stroke-width="{random.choice([1,2,3])}" opacity=".35"/>' for a in [i*math.pi/36 for i in range(72)])
stack = ["TYPESCRIPT", "PYTHON", "REACT", "NEXT.JS", "FLUTTER", "NODE.JS", "FASTAPI", "KOTLIN", "JAVA", "DART", "TAILWIND", "SUPABASE", "FIREBASE", "MONGODB", "GCP", "TENSORFLOW", "OPENCV", "VERCEL"]
tags, x, y = "", 50, 920
for s in stack:
    w = len(s)*17 + 34
    if x + w > 1150: x, y = 50, y + 66
    col = random.choice([Y, C, P, R, Y])
    tags += (f'<g transform="rotate({random.uniform(-4,4):.1f} {x+w/2} {y+22})"><rect x="{x}" y="{y}" width="{w}" height="46" rx="6" fill="{col}" stroke="{INK}" stroke-width="3"/>'
             f'<text class="bang" x="{x+w/2}" y="{y+33}" text-anchor="middle" font-size="28" fill="{P if col == R else INK}">{s}</text></g>')
    x += w + 14
stats = [(f'{D["total"]:,}', "CONTRIBUTIONS", "WHAM!", Y, "dR"), (f'{D["streak"]} DAYS', "STREAK &amp; COUNTING", "BOOM!", R, "dY"),
         (f'{D["commits"]:,}', "COMMITS THIS YEAR", "KRAK!", C, "dY"), (f'{D["prs"]}', "PULL REQUESTS", "BLAM!", P, "dC")]
SP = ""
for i, (n, l, sfx, bg, pat) in enumerate(stats):
    x0 = 24 + i*292
    ex = (f'<rect x="{x0}" y="1180" width="276" height="250" fill="url(#{pat})" opacity=".55"/>'
          f'<polygon points="{burst(x0+138, 1292, 100, 70, 14)}" fill="{P if bg != P else Y}" stroke="{INK}" stroke-width="3"/>'
          f'<text class="bang sfx" x="{x0+138}" y="1310" text-anchor="middle" font-size="{60 if len(n) < 7 else 50}" fill="{R if bg != R else INK}" stroke="{INK}" stroke-width="2.5" paint-order="stroke">{n}</text>'
          f'<text class="bang" x="{x0+20}" y="1218" font-size="30" fill="{INK}" transform="rotate(-8 {x0+20} 1218)">{sfx}</text>'
          + caption(x0+12, 1384, l, w=252, size=15))
    SP += panel(x0, 1180, 276, 250, bg, ex, tilt=[-.6, .5, -.4, .7][i])
bars = D["last60"]; mx = max(bars)
BR = "".join(f'<rect x="{50+i*18.5:.1f}" y="{1640-max(3,c/mx*110):.1f}" width="14" height="{max(3,c/mx*110):.1f}" fill="{R if c == mx else INK}"/>' for i, c in enumerate(bars))
pk = bars.index(mx)
langs = "  ·  ".join(f"{n.upper()} {p}%" for n, p in D["langs"][:4])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{dots("dR", R)}{dots("dY", Y, 9, 2.8)}{dots("dC", C)}{dots("dK", INK, 8, 1.4)}<clipPath id="splash"><rect x="24" y="24" width="1152" height="420"/></clipPath>
<style>{font("Bangers", "bangers")}{font("Comic+Neue:wght@700", "comicneue")}
.bang{{font-family:bangers,Impact,sans-serif;letter-spacing:.03em}}
.cap{{font-family:comicneue,'Comic Sans MS',sans-serif;font-weight:700;fill:{INK};letter-spacing:.02em}}
.pop{{transform-box:fill-box;transform-origin:center;animation:p .6s cubic-bezier(.2,1.8,.4,1) both}}@keyframes p{{from{{transform:scale(0)}}}}
.wob{{transform-box:fill-box;transform-origin:center;animation:w 1.6s ease-in-out infinite}}@keyframes w{{50%{{transform:rotate(-6deg) scale(1.08)}}}}
.sfx{{transform-box:fill-box;transform-origin:center;animation:p .5s cubic-bezier(.2,1.8,.4,1) .4s both}}
</style>{GRAIN}</defs>
<rect width="{W}" height="{H}" fill="{P}"/>
{panel(24, 24, 1152, 420, Y, f'<rect x="24" y="24" width="1152" height="420" fill="url(#dR)" opacity=".35"/><g clip-path="url(#splash)">{speed}</g>'
       f'<polygon class="pop" clip-path="url(#splash)" points="{burst(470, 235, 330, 210, 22)}" fill="{R}" stroke="{INK}" stroke-width="5"/>'
       f'<text class="bang" x="470" y="290" text-anchor="middle" font-size="168" fill="{Y}" stroke="{INK}" stroke-width="7" paint-order="stroke" style="filter:drop-shadow(8px 8px 0 {C})">TRIBHUVAN</text>'
       + caption(44, 44, "MEANWHILE, IN THE CODEBASE...", size=22)
       + f'<g transform="rotate(-3 470 380)"><rect x="200" y="356" width="540" height="48" fill="{P}" stroke="{INK}" stroke-width="4"/><text class="bang" x="470" y="392" text-anchor="middle" font-size="32" fill="{INK}">FULL-STACK · MOBILE · AGENTIC AI</text></g>'
       f'<g class="wob"><polygon points="{burst(1000, 170, 130, 90, 12)}" fill="{C}" stroke="{INK}" stroke-width="4"/>'
       f'<text class="bang" x="1000" y="190" text-anchor="middle" font-size="58" fill="{P}" stroke="{INK}" stroke-width="4" paint-order="stroke" transform="rotate(-10 1000 175)">SHIP IT!</text></g>'
       f'<text class="bang" x="1000" y="380" text-anchor="middle" font-size="26" fill="{INK}">ISSUE #26 · NOV 2026</text>')}
{panel(24, 460, 700, 380, P, f'<rect x="24" y="460" width="700" height="380" fill="url(#dC)" opacity=".25"/>'
       + caption(44, 480, "WHO IS THIS MYSTERIOUS DEV?", size=20)
       + f'<path d="M90 560 Q90 530 130 530 H640 Q690 530 690 570 V740 Q690 780 640 780 H260 L200 830 L215 780 H130 Q90 780 90 740 Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
       f'<text class="cap" font-size="23"><tspan x="125" y="585">I BUILD FULL-STACK, MOBILE &amp; AI</tspan><tspan x="125" y="620">PRODUCTS — END TO END!</tspan>'
       f'<tspan x="125" y="665">REACT, NEXT.JS, FLUTTER, NODE, FASTAPI...</tspan><tspan x="125" y="700">AND DEEP IN <tspan fill="{R}">AGENTIC AI</tspan> — SYSTEMS</tspan><tspan x="125" y="735">THAT ACT ON THEIR OWN!</tspan></text>')}
{panel(740, 460, 436, 380, P, f'<image x="740" y="460" width="436" height="380" href="{img}" preserveAspectRatio="xMidYMid slice"/>' + caption(756, 790, "HE SEEMS... FRIENDLY?", w=260, fill="#fff", size=18), tilt=.8)}
{panel(24, 856, 1152, 300, C, f'<rect x="24" y="856" width="1152" height="300" fill="url(#dK)" opacity=".18"/>{tags}' + caption(40, 868, "HIS ARSENAL OF POWERS:", size=20))}
{SP}
{panel(24, 1446, 1152, 230, P, f'<rect x="24" y="1446" width="1152" height="230" fill="url(#dY)" opacity=".5"/>{BR}'
       f'<line x1="40" y1="1640" x2="1160" y2="1640" stroke="{INK}" stroke-width="4"/>'
       + caption(40, 1460, "60 DAYS OF NON-STOP ACTION!", size=20)
       + f'<g class="pop"><polygon points="{burst(50+pk*18.5+7, 1505, 50, 32, 10)}" fill="{R}" stroke="{INK}" stroke-width="3"/><text class="bang" x="{50+pk*18.5+7}" y="1516" text-anchor="middle" font-size="30" fill="{Y}" stroke="{INK}" stroke-width="2" paint-order="stroke">POW! {mx}</text></g>'
       + caption(390, 1460, langs, w=570, fill="#fff", size=15))}
<g transform="rotate(-2 1060 1676)"><rect x="940" y="1652" width="230" height="40" fill="{Y}" stroke="{INK}" stroke-width="3"/><text class="cap" x="1055" y="1679" text-anchor="middle" font-size="18">TO BE CONTINUED...</text></g>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".12" style="mix-blend-mode:multiply"/>
</svg>'''
save("comic", svg)
