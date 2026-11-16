import base64, sys
d = sys.argv[1]
mono = base64.b64encode(open(f"{d}/f/mono.woff2","rb").read()).decode()
ab = base64.b64encode(open(f"{d}/f/archivo.woff2","rb").read()).decode()
INK, PAPER, RED = "#0A0A0A", "#F2F1EC", "#E61919"
head = f'''<defs><style>@font-face{{font-family:JM;src:url(data:font/woff2;base64,{mono})}}
.m{{font-family:JM,'Courier New',monospace;letter-spacing:.12em;font-weight:700}}</style></defs>'''
def strip(n, title, tag):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="60" viewBox="0 0 1200 60">{head}
<rect width="1200" height="60" fill="{PAPER}"/><rect x="1" y="1" width="1198" height="58" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="2" y="2" width="96" height="56" fill="{RED}"/><text class="m" x="50" y="37" text-anchor="middle" font-size="18" fill="{PAPER}">{n}</text>
<line x1="98" y1="2" x2="98" y2="58" stroke="{INK}" stroke-width="2"/>
<text class="m" x="122" y="39" font-size="24" fill="{INK}">{title}</text>
<text class="m" x="1176" y="37" text-anchor="end" font-size="12" fill="{INK}" opacity=".6">{tag}</text></svg>'''
for f,n,t,g in [("h-about","01","ABOUT","/// OPERATOR PROFILE"),("h-stack","02","STACK","/// TOOLING INVENTORY"),
                ("h-stats","03","TELEMETRY","/// LIVE · REFRESHED DAILY"),("h-music","04","NOW PLAYING","/// AUDIO FEED")]:
    open(f"{d}/{f}.svg","w",encoding="utf-8").write(strip(n,t,g))
open(f"{d}/footer.svg","w",encoding="utf-8").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="44" viewBox="0 0 1200 44">{head}
<rect width="1200" height="44" fill="{INK}"/><text class="m" x="24" y="28" font-size="13" fill="{PAPER}">END OF TRANSMISSION</text>
<text class="m" x="600" y="28" text-anchor="middle" font-size="13" fill="{RED}">///////////////</text>
<text class="m" x="1176" y="28" text-anchor="end" font-size="13" fill="{PAPER}">TRB-26 © 2026</text></svg>''')
