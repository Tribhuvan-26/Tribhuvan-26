import base64, random, sys
d = sys.argv[1]
b64 = lambda f: base64.b64encode(open(f"{d}/f/{f}", "rb").read()).decode()
random.seed(26)
INK, PAPER, RED = "#0A0A0A", "#F2F1EC", "#E61919"
# barcode
bars, x = [], 930
while x < 1150:
    w = random.choice([2, 2, 3, 5, 7]); bars.append(f'<rect x="{x}" y="346" width="{w}" height="38"/>'); x += w + random.choice([2, 3, 4])
ticker = "FULL-STACK  ///  MOBILE  ///  AGENTIC AI  ///  CLOUD ARCHITECTURE  ///  SHIPPING END TO END  ///  BUILT IN PUBLIC  ///  "
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420">
<defs>
<style>
@font-face {{ font-family: AB; src: url(data:font/woff2;base64,{b64("archivo.woff2")}) format("woff2"); }}
@font-face {{ font-family: JM; src: url(data:font/woff2;base64,{b64("mono.woff2")}) format("woff2"); }}
.m {{ font-family: JM, 'Courier New', monospace; font-size: 13px; letter-spacing: .12em; fill: {INK}; }}
.mb {{ font-weight: 700; }}
.blink {{ animation: b 1.1s steps(1) infinite; }}
@keyframes b {{ 50% {{ opacity: 0; }} }}
.tick {{ animation: t 22s linear infinite; }}
@keyframes t {{ to {{ transform: translateX(-1100px); }} }}
</style>
<clipPath id="bar"><rect x="18" y="292" width="1164" height="40"/></clipPath>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0"/></filter>
</defs>
<rect width="1200" height="420" fill="{PAPER}"/>
<rect x="17" y="17" width="1166" height="386" fill="none" stroke="{INK}" stroke-width="2"/>

<!-- top telemetry row -->
<text class="m" x="32" y="42">[ UNIT / TRB-26 ]</text>
<text class="m" x="250" y="42">PROFILE.README</text>
<text class="m" x="560" y="42">REV 2026.11</text>
<rect class="blink" x="920" y="31" width="12" height="12" fill="{RED}"/>
<text class="m mb" x="942" y="42">STATUS: SHIPPING</text>
<line x1="18" y1="58" x2="1182" y2="58" stroke="{INK}" stroke-width="2"/>
<line x1="230" y1="18" x2="230" y2="58" stroke="{INK}"/><line x1="540" y1="18" x2="540" y2="58" stroke="{INK}"/><line x1="900" y1="18" x2="900" y2="58" stroke="{INK}"/>

<!-- macro type -->
<text x="26" y="270" font-family="AB, 'Arial Black', Impact, sans-serif" font-size="236" textLength="1148" lengthAdjust="spacingAndGlyphs" fill="{INK}">TRIBHUVAN</text>
<text x="1150" y="96" font-family="AB, 'Arial Black', sans-serif" font-size="34" fill="{RED}">®</text>

<!-- red ticker bar -->
<rect x="18" y="292" width="1164" height="40" fill="{RED}"/>
<g clip-path="url(#bar)"><g class="tick">
{"".join(f'<text class="m mb" x="{18+i*1100}" y="317" textLength="1100" style="fill:{PAPER};font-size:15px">{ticker}</text>' for i in range(3))}
</g></g>

<!-- bottom grid -->
<line x1="18" y1="332" x2="1182" y2="332" stroke="{INK}" stroke-width="2"/>
<line x1="300" y1="332" x2="300" y2="402" stroke="{INK}"/><line x1="600" y1="332" x2="600" y2="402" stroke="{INK}"/><line x1="900" y1="332" x2="900" y2="402" stroke="{INK}"/>
<text class="m" x="32" y="358" style="fill:{RED}">01 / ROLE</text><text class="m mb" x="32" y="384">FULL-STACK ENGINEER</text>
<text class="m" x="314" y="358" style="fill:{RED}">02 / STACK</text><text class="m mb" x="314" y="384">REACT · NEXT · FLUTTER</text>
<text class="m" x="614" y="358" style="fill:{RED}">03 / FOCUS</text><text class="m mb" x="614" y="384">AGENTIC AI + CLOUD</text>
<g fill="{INK}">{"".join(bars)}</g>
<text class="m" x="1158" y="384" style="font-size:18px">+</text>
<g class="m" style="font-size:16px"><text x="292" y="338">+</text><text x="592" y="338">+</text><text x="892" y="338">+</text></g>

<rect width="1200" height="420" filter="url(#grain)" opacity=".18" style="mix-blend-mode:multiply"/>
</svg>'''
open(f"{d}/banner.svg", "w", encoding="utf-8").write(svg)
print(len(svg))
