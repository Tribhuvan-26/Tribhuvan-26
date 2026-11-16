import base64, sys
d = sys.argv[1]
INK, PAPER, RED = "#0A0A0A", "#F2F1EC", "#E61919"
f64 = lambda n: base64.b64encode(open(f"{d}/f/{n}", "rb").read()).decode()
cols = [("A", "LANGUAGES", ["*TYPESCRIPT", "*PYTHON", "JAVASCRIPT", "JAVA", "KOTLIN", "DART", "C"]),
        ("B", "FRONT / MOBILE", ["*REACT", "*NEXT.JS", "*FLUTTER", "TAILWIND", "VITE", "FIGMA"]),
        ("C", "BACK / DATA", ["*NODE.JS", "*FASTAPI", "EXPRESS", "SUPABASE", "FIREBASE", "MONGODB", "MYSQL"]),
        ("D", "CLOUD / AI / OPS", ["GOOGLE CLOUD", "VERCEL", "TENSORFLOW", "OPENCV", "GIT", "GITHUB"])]
X0, W, top, rh = 18, 291, 62, 36
body, n = [], 0
for ci, (k, t, items) in enumerate(cols):
    x = X0 + ci*W
    body.append(f'<rect x="{x+14}" y="{top+12}" width="22" height="22" fill="{RED}"/><text class="m b" x="{x+25}" y="{top+28}" text-anchor="middle" style="fill:{PAPER};font-size:12px">{k}</text>'
                f'<text class="m b" x="{x+46}" y="{top+28}">{t}</text>')
    if ci: body.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top+46+7*rh}" stroke="{INK}" stroke-width="{2 if ci else 0}"/>')
    for ri, it in enumerate(items):
        n += 1; y = top + 46 + ri*rh
        hot = it.startswith("*"); it = it.lstrip("*")
        body.append(f'<text class="m" x="{x+14}" y="{y+23}" style="font-size:11px;opacity:.45">{k}-{ri+1:02d}</text>'
                    f'<text class="m{" b" if hot else ""}" x="{x+64}" y="{y+23}">{it}</text>'
                    + (f'<rect x="{x+W-28}" y="{y+13}" width="12" height="12" fill="{RED}"/>' if hot else f'<rect x="{x+W-27}" y="{y+14}" width="10" height="10" fill="none" stroke="{INK}" stroke-width="1.5" opacity=".5"/>'))
for ri in range(8):
    y = top + 46 + ri*rh
    body.append(f'<line x1="18" y1="{y}" x2="1182" y2="{y}" stroke="{INK}" stroke-opacity="{.9 if ri == 0 else .2}" stroke-width="{2 if ri == 0 else 1}"/>')
fy = top + 46 + 7*rh
H = fy + 40 + 18
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}">
<defs><style>
@font-face{{font-family:JM;src:url(data:font/woff2;base64,{f64("mono.woff2")})}}
@font-face{{font-family:AB;src:url(data:font/woff2;base64,{f64("archivo-full.woff2")})}}
.m{{font-family:JM,'Courier New',monospace;font-size:14px;letter-spacing:.12em;fill:{INK}}}.b{{font-weight:700}}
.scan{{animation:sc 4s linear infinite}}@keyframes sc{{from{{transform:translateY(0)}}to{{transform:translateY({7*rh}px)}}}}
</style>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0"/></filter></defs>
<rect width="1200" height="{H}" fill="{PAPER}"/>
<rect x="17" y="17" width="1166" height="{H-34}" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="18" y="18" width="96" height="44" fill="{RED}"/><text class="m b" x="66" y="46" text-anchor="middle" style="fill:{PAPER};font-size:17px">02</text>
<line x1="114" y1="18" x2="114" y2="62" stroke="{INK}" stroke-width="2"/>
<text x="136" y="50" font-family="AB,'Arial Black',sans-serif" font-size="26" fill="{INK}" letter-spacing="1">INVENTORY</text>
<text class="m" x="1164" y="45" text-anchor="end" style="font-size:12px">{n} UNITS LOGGED  ///  REV 2026.11</text>
<line x1="18" y1="62" x2="1182" y2="62" stroke="{INK}" stroke-width="2"/>
{"".join(body)}
<rect class="scan" x="18" y="{top+46}" width="1164" height="2" fill="{RED}" opacity=".35"/>
<line x1="18" y1="{fy}" x2="1182" y2="{fy}" stroke="{INK}" stroke-width="2"/>
<rect x="36" y="{fy+14}" width="12" height="12" fill="{RED}"/><text class="m" x="58" y="{fy+25}" style="font-size:12px">DAILY DRIVER</text>
<rect x="225" y="{fy+15}" width="10" height="10" fill="none" stroke="{INK}" stroke-width="1.5" opacity=".5"/><text class="m" x="246" y="{fy+25}" style="font-size:12px">IN ROTATION</text>
<text class="m" x="1164" y="{fy+25}" text-anchor="end" style="font-size:12px;fill:{RED}">&gt;&gt;&gt; ALWAYS EXPANDING</text>
<rect width="1200" height="{H}" filter="url(#grain)" opacity=".16" style="mix-blend-mode:multiply"/>
</svg>'''
open(f"{d}/inventory.svg", "w", encoding="utf-8").write(svg); print(H)
