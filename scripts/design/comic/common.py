import base64, io, json, os, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageOps
RP = os.environ.get("RP") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rp")
D = json.load(open(os.path.join(RP, "data.json"), encoding="utf-8"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
CHARS = "".join(chr(c) for c in range(32, 127)) + "·—■●▲►©®×→←↑↓★"
def font(family, name):
    p = os.path.join(RP, "f", name + ".woff2")
    if not os.path.exists(p):
        q = urllib.parse.quote(CHARS)
        css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?family={family}&text={q}", headers={"User-Agent": UA})).read().decode()
        url = css.split("url(")[1].split(")")[0]
        open(p, "wb").write(urllib.request.urlopen(url).read())
    return f"@font-face{{font-family:{name};src:url(data:font/woff2;base64,{base64.b64encode(open(p,'rb').read()).decode()})}}"
def halftone(src, w, h, ink, paper, step=5, scale=.62):
    S = 2
    im = ImageOps.autocontrast(ImageOps.fit(Image.open(os.path.join(RP, src)).convert("L"), (w*S//step, h*S//step)), cutoff=4)
    out = Image.new("RGBA", (w*S, h*S), paper); dr = ImageDraw.Draw(out)
    for y in range(im.height):
        for x in range(im.width):
            r = (1 - (im.getpixel((x, y))/255)**.8) * step * scale
            if r > .6:
                cx, cy = x*step + step/2 + (step/2 if y % 2 else 0), y*step + step/2
                dr.ellipse((cx-r, cy-r, cx+r, cy+r), fill=ink)
    b = io.BytesIO(); out.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
GRAIN = '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0"/></filter>'
def save(style, svg):
    import xml.dom.minidom
    p = os.path.join(RP, "styles", style + ".svg")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(svg); xml.dom.minidom.parse(p)
    print(style, len(svg)//1024, "KB ok")
