"""Render profile/telemetry.svg from live GitHub data. Usage: telemetry.py USER OUT.svg FONTDIR (env GH_TOKEN)."""
import base64, datetime as dt, json, os, sys, urllib.request
USER, OUT, FONTS = sys.argv[1:4]
INK, PAPER, RED = "#0A0A0A", "#F2F1EC", "#E61919"

def gql(q, **v):
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": q, "variables": v}).encode(),
                                 {"Authorization": f"bearer {os.environ['GH_TOKEN']}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req))
    if "errors" in r: sys.exit(r["errors"])
    return r["data"]["user"]

u = gql("""query($l:String!){user(login:$l){createdAt pullRequests{totalCount}
  contributionsCollection{totalCommitContributions restrictedContributionsCount}
  repositories(ownerAffiliations:OWNER,isFork:false,first:100){nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}}}""", l=USER)
today = dt.datetime.now(dt.timezone.utc).date()
days = {}
start = dt.date.fromisoformat(u["createdAt"][:10])
while start <= today:  # calendar API spans at most one year per call
    end = min(start + dt.timedelta(days=364), today)
    c = gql("""query($l:String!,$f:DateTime!,$t:DateTime!){user(login:$l){contributionsCollection(from:$f,to:$t){
      contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}""",
            l=USER, f=f"{start}T00:00:00Z", t=f"{end}T23:59:59Z")
    for w in c["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for x in w["contributionDays"]: days[x["date"]] = x["contributionCount"]
    start = end + dt.timedelta(days=1)

total = sum(days.values())
d, streak = today, 0
if not days.get(str(d)): d -= dt.timedelta(days=1)  # today not counted yet doesn't break the streak
while days.get(str(d)): streak += 1; d -= dt.timedelta(days=1)
last = [days.get(str(today - dt.timedelta(days=i)), 0) for i in range(59, -1, -1)]
commits = u["contributionsCollection"]["totalCommitContributions"] + u["contributionsCollection"]["restrictedContributionsCount"]
prs = u["pullRequests"]["totalCount"]
langs = {}
for r in u["repositories"]["nodes"]:
    for e in r["languages"]["edges"]: langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
tot = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]

f64 = lambda n: base64.b64encode(open(os.path.join(FONTS, n), "rb").read()).decode()
H, top_y = 420, 62
stats = [(f"{total:,}", "CONTRIBUTIONS", "ALL TIME"), (str(streak), "DAY STREAK", "CURRENT"),
         (f"{commits:,}", "COMMITS", "LAST 12 MO"), (str(prs), "PULL REQUESTS", "ALL TIME")]
cells = []
for i, (num, lab, sub) in enumerate(stats):
    x = 18 + i*196
    if i: cells.append(f'<line x1="{x}" y1="{top_y}" x2="{x}" y2="232" stroke="{INK}" stroke-opacity=".25"/>')
    cells.append(f'<text class="m" x="{x+18}" y="{top_y+30}" style="font-size:11px;fill:{RED}">{i+1:02d} / {sub}</text>'
                 f'<text x="{x+16}" y="{top_y+104}" font-family="AB,\'Arial Black\',sans-serif" font-size="54" fill="{RED if i == 1 else INK}">{num}</text>'
                 f'<text class="m b" x="{x+18}" y="{top_y+140}" style="font-size:12px">{lab}</text>')
mx = max(last) or 1
bw, bx0, base = 12, 36, 382
bars = "".join(f'<rect class="bar" style="animation-delay:{i*12}ms" x="{bx0+i*12.4:.1f}" y="{base-max(2,c/mx*110):.1f}" width="{bw-4}" height="{max(2,c/mx*110):.1f}" fill="{RED if i == 59 else INK}" opacity="{1 if c else .2}"/>' for i, c in enumerate(last))
lrows = []
for i, (n, s) in enumerate(top):
    y, p = 118 + i*44, s/tot*100
    lrows.append(f'<text class="m{" b" if i == 0 else ""}" x="820" y="{y}">{n.upper()}</text><text class="m" x="1164" y="{y}" text-anchor="end">{p:.1f}%</text>'
                 f'<rect x="820" y="{y+10}" width="344" height="8" fill="none" stroke="{INK}" stroke-opacity=".3"/>'
                 f'<rect class="grow" x="820" y="{y+10}" width="{344*p/100:.1f}" height="8" fill="{RED if i == 0 else INK}"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}">
<defs><style>
@font-face{{font-family:JM;src:url(data:font/woff2;base64,{f64("jbm.woff2")})}}
@font-face{{font-family:AB;src:url(data:font/woff2;base64,{f64("archivo.woff2")})}}
.m{{font-family:JM,'Courier New',monospace;font-size:14px;letter-spacing:.12em;fill:{INK}}}.b{{font-weight:700}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:up .6s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{transform:scaleY(0)}}}}
.grow{{transform-box:fill-box;animation:gr 1s cubic-bezier(.2,.8,.2,1) .3s both}}@keyframes gr{{from{{transform:scaleX(0)}}}}
.blink{{animation:k 1.1s steps(1) infinite}}@keyframes k{{50%{{opacity:0}}}}
</style>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0"/></filter></defs>
<rect width="1200" height="{H}" fill="{PAPER}"/>
<rect x="17" y="17" width="1166" height="{H-34}" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="18" y="18" width="96" height="44" fill="{RED}"/><text class="m b" x="66" y="46" text-anchor="middle" style="fill:{PAPER};font-size:17px">03</text>
<line x1="114" y1="18" x2="114" y2="62" stroke="{INK}" stroke-width="2"/>
<text x="136" y="50" font-family="AB,'Arial Black',sans-serif" font-size="26" fill="{INK}" letter-spacing="1">TELEMETRY</text>
<rect class="blink" x="880" y="34" width="10" height="10" fill="{RED}"/>
<text class="m" x="1164" y="45" text-anchor="end" style="font-size:12px">LIVE  ///  SYNCED {today:%Y.%m.%d} UTC</text>
<line x1="18" y1="62" x2="1182" y2="62" stroke="{INK}" stroke-width="2"/>
{"".join(cells)}
<line x1="18" y1="232" x2="802" y2="232" stroke="{INK}" stroke-width="2"/>
<text class="m" x="36" y="258" style="font-size:11px;fill:{RED}">05 / ACTIVITY</text><text class="m b" x="784" y="258" text-anchor="end" style="font-size:11px">LAST 60 DAYS  ///  PEAK {mx}</text>
<line x1="36" y1="{base}" x2="784" y2="{base}" stroke="{INK}"/>
{bars}
<line x1="802" y1="62" x2="802" y2="{H-18}" stroke="{INK}" stroke-width="2"/>
<text class="m" x="820" y="88" style="font-size:11px;fill:{RED}">06 / LANGUAGE SPLIT</text>
{"".join(lrows)}
<rect width="1200" height="{H}" filter="url(#grain)" opacity=".16" style="mix-blend-mode:multiply"/>
</svg>'''
open(OUT, "w", encoding="utf-8").write(svg)
print("telemetry:", total, streak, commits, prs)
