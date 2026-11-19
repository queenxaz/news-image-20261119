#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 19 November 2026.

Draws a dense newspaper front page (1024x1024 JPEG) summing up the
world news of Thursday 19 November 2026. Pure Pillow, no network,
fully deterministic: same input -> same bytes on every run.
"""
import io
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (24, 64, 120)
GREY = (96, 96, 96)
RULE = (40, 40, 40)
OCEAN = (188, 214, 232)
LAND = (216, 201, 163)
GOLD = (176, 141, 44)

_HERE = os.path.dirname(os.path.abspath(__file__))


def _font(name, size):
    """Load a font from the repo's fonts/ dir, else system paths, else default."""
    cands = [
        os.path.join(_HERE, "fonts", name),
        "/usr/share/fonts/truetype/dejavu/" + name,
    ]
    for p in cands:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


SERIF_B = lambda s: _font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: _font("DejaVuSerif.ttf", s)
SANS = lambda s: _font("DejaVuSans.ttf", s)
SANS_B = lambda s: _font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def text_block(draw, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text; returns y after the last line."""
    if leading is None:
        leading = font.size + 3
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def headline_cell(draw, x, y, w, tag, head, deck, head_size=21, deck_size=13):
    """One story cell: red tag, bold headline (<=2 lines), one deck line."""
    draw.text((x, y), tag, font=SANS_B(11), fill=RED)
    y += 15
    lines = wrap(draw, head, SERIF_B(head_size), w)[:2]
    for ln in lines:
        draw.text((x, y), ln, font=SERIF_B(head_size), fill=INK)
        y += head_size + 3
    if deck:
        draw.text((x, y), deck, font=SANS(deck_size), fill=(60, 60, 60))
        y += deck_size + 4
    return y


# ---------------------------------------------------------------- continents
# Rough lon/lat outlines, equirectangular projection, drawn inside a box.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # Greenland
    [(-55, 60), (-40, 65), (-30, 70), (-20, 76), (-45, 80), (-60, 76)],
    # South America
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -55), (-73, -40),
     (-70, -20), (-80, -5), (-81, 5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (10, 68), (5, 60), (0, 55), (-5, 50), (-8, 44)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 52),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (97, 15),
     (92, 21), (88, 22), (80, 15), (77, 8), (72, 20), (66, 25), (60, 25),
     (57, 26), (52, 28), (48, 30), (44, 29), (40, 36), (36, 36),
     (30, 36), (28, 40), (30, 45), (35, 50), (30, 55)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]

# (lon, lat, label, label dx, label dy) hot spots for 19 November's news
HOTSPOTS = [
    (121, 22, "SHENZHEN", 5, -5),
    (34, 45, "CRIMEA", -34, -13),
    (35, 31, "GAZA", -40, 5),
    (86, 20, "ODISHA", 5, 4),
    (127, 40, "PYONGYANG", 5, -5),
    (55, 26, "HORMUZ", 5, 7),
    (92, 22, "DHAKA", 5, -15),
]


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=OCEAN, outline=RULE, width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
        py = y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0)
        return (px, py)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=(150, 130, 90))
    f = SANS_B(9)
    for lon, lat, label, dx, dy in HOTSPOTS:
        px, py = proj(lon, lat)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                     outline=(255, 255, 255))
        tw = draw.textlength(label, font=f)
        lx = min(max(px + dx, x0 + 2), x1 - tw - 2)
        draw.text((lx, py + dy), label, font=f, fill=RED)


def draw_vice_city(draw, box):
    """Sunset Vice City skyline panel for the GTA VI lead story."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # sunset gradient bands
    bands = [(255, 122, 89), (255, 94, 120), (214, 69, 150),
             (146, 58, 168), (84, 48, 140)]
    for i, c in enumerate(bands):
        draw.rectangle([x0, y0 + i * h // 5, x1, y0 + (i + 1) * h // 5 + 1],
                       fill=c)
    # sun
    cx, cy, r = x0 + w // 2, y0 + int(h * 0.42), 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 120))
    # skyline silhouettes
    sil = (38, 16, 66)
    heights = [0.42, 0.55, 0.36, 0.62, 0.48, 0.58, 0.40, 0.66, 0.52, 0.44,
               0.60, 0.38, 0.56, 0.46]
    bw = w / len(heights)
    for i, hf in enumerate(heights):
        bx = x0 + i * bw
        top = y1 - hf * h * 0.62
        draw.rectangle([bx + 1, top, bx + bw - 1, y1], fill=sil)
        # lit windows
        wy = top + 6
        while wy < y1 - 8:
            draw.rectangle([bx + 4, wy, bx + 7, wy + 4], fill=(255, 220, 130))
            wy += 12
    # palm trees
    for px, ph in [(x0 + 46, 52), (x1 - 52, 58), (x0 + w - 130, 44)]:
        base = y1
        draw.line([px, base, px + 6, base - ph], fill=(20, 10, 30), width=4)
        tx, ty = px + 6, base - ph
        for dx, dy in [(-26, -8), (-18, -18), (0, -22), (18, -16), (26, -6)]:
            draw.line([tx, ty, tx + dx, ty + dy], fill=(20, 10, 30), width=3)
    # neon sign
    f = SANS_B(30)
    label = "VICE CITY"
    tw = draw.textlength(label, font=f)
    sx = x0 + (w - tw) / 2
    sy = y0 + 8
    for ox, oy in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
        draw.text((sx + ox, sy + oy), label, font=f, fill=(255, 60, 180))
    draw.text((sx, sy), label, font=f, fill=(255, 240, 250))


def draw_flags(draw, box):
    """Three simplified flags: USA, China, Russia."""
    x0, y0, x1, y1 = box
    fw = (x1 - x0 - 16) // 3
    fh = y1 - y0
    # USA
    ux = x0
    for i in range(7):
        draw.rectangle([ux, y0 + i * fh // 7, ux + fw, y0 + (i + 1) * fh // 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([ux, y0, ux + fw * 0.45, y0 + fh * 0.55], fill=(60, 60, 150))
    for r in range(3):
        for c in range(3):
            draw.ellipse([ux + 6 + c * 12, y0 + 6 + r * 12,
                          ux + 10 + c * 12, y0 + 10 + r * 12],
                         fill=(255, 255, 255))
    # China
    cx = x0 + fw + 8
    draw.rectangle([cx, y0, cx + fw, y1], fill=(222, 41, 16))
    for sx, sy in [(10, 8), (30, 12), (34, 26), (26, 36), (10, 28)]:
        draw.ellipse([cx + sx, y0 + sy, cx + sx + 9, y0 + sy + 9],
                     fill=(255, 222, 0))
    # Russia
    rx = x0 + 2 * fw + 16
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([rx, y0 + i * fh // 3, rx + fw, y0 + (i + 1) * fh // 3],
                       fill=c)
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)


def render_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- masthead ----------------
    d.rectangle([0, 0, W, 10], fill=INK)
    d.text((512, 16), "THE WORLD TODAY", font=SERIF_B(60),
           fill=INK, anchor="ma")
    d.text((512, 86), "THURSDAY  19  NOVEMBER  2026",
           font=SANS_B(20), fill=RED, anchor="ma")
    d.text((24, 112), "Vol. IX  —  No. 323", font=SANS(12), fill=GREY)
    d.text((1000, 112), "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
           font=SANS(12), fill=GREY, anchor="ra")
    d.line([24, 130, 1000, 130], fill=RULE, width=3)
    d.line([24, 134, 1000, 134], fill=RULE, width=1)

    # ---------------- lead: GTA VI ----------------
    draw_vice_city(d, (24, 142, 664, 296))
    y = 304
    d.text((24, y), "GAMES  •  LAUNCH DAY", font=SANS_B(12), fill=RED)
    y += 20
    d.text((24, y), "GTA VI IS OUT", font=SERIF_B(40), fill=INK)
    y += 48
    y = text_block(
        d, 24, y,
        "After 13 years, Rockstar's Grand Theft Auto VI launches worldwide "
        "at midnight local time on PS5 and Xbox Series X|S — a 99 on "
        "Metacritic, tied for the highest score ever. Take-Two up 6.5%.",
        SANS(13), 640, leading=17)

    # ---------------- right: Shenzhen summit ----------------
    draw_flags(d, (688, 142, 1000, 198))
    y = 206
    d.text((688, y), "DIPLOMACY  •  APEC", font=SANS_B(12), fill=RED)
    y += 20
    y = text_block(d, 688, y,
                   "Trump, Xi and Putin hold first three-way summit in Shenzhen",
                   SERIF_B(22), 312, leading=26)
    y = text_block(
        d, 688, y,
        "The US, Chinese and Russian leaders meet on the APEC sidelines, "
        "with Ukraine, nuclear arms and Iran on the table. Trump met Putin "
        "and Xi separately first; a trilateral session follows.",
        SANS(13), 312, leading=16)
    d.line([688, 412, 1000, 412], fill=(200, 200, 200), width=1)

    # ---------------- middle band: 3 stories ----------------
    d.line([24, 432, 1000, 432], fill=RULE, width=2)
    col_w, gap = 312, 20
    cells = [
        ("THE HAGUE  •  JUSTICE",
         "World court rules on Rohingya genocide case",
         "ICJ decides Gambia's case against Myanmar."),
        ("WAR IN UKRAINE",
         "Ukraine hits Crimean Bridge a third time this week",
         "Road traffic halted; rail still running."),
        ("MIDDLE EAST",
         "Iran strikes Gulf states after US hit on Qeshm",
         "Tehran retaliates; tanker hit near Hormuz."),
    ]
    for i, (tag, head, deck) in enumerate(cells):
        x = 24 + i * (col_w + gap)
        headline_cell(d, x, 444, col_w, tag, head, deck, head_size=19)
        if i < 2:
            d.line([x + col_w + 10, 444, x + col_w + 10, 548],
                   fill=(200, 200, 200), width=1)

    # ---------------- markets + map band ----------------
    d.line([24, 556, 1000, 556], fill=RULE, width=2)
    d.text((24, 568), "MARKETS", font=SANS_B(13), fill=RED)
    rows = [
        ("Dow Jones", "50,198", "-1.11%"),
        ("S&P 500", "7,324", "-0.23%"),
        ("Nasdaq", "24,430", "+0.42%"),
        ("Nvidia", "$150.96", "-2.89%"),
        ("Take-Two", "$216.61", "+6.5%"),
        ("Gold", "$3,726", "-3.22%"),
        ("Brent crude", "$92.0", "-1.5%"),
        ("Bitcoin", "$62,400", "-2.2%"),
    ]
    y = 590
    for name, val, chg in rows:
        up = chg.startswith("+")
        d.text((24, y), name, font=SANS(13), fill=INK)
        d.text((180, y), val, font=SANS_B(13), fill=INK)
        d.text((258, y), chg, font=SANS_B(13),
               fill=(0, 128, 0) if up else (178, 34, 34))
        y += 17
    d.text((24, y + 2), "Fed minutes point to more hikes; S&P in a 5-day slide.",
           font=SANS(11), fill=GREY)
    d.line([340, 568, 340, 742], fill=(200, 200, 200), width=1)
    d.text((356, 568), "WHERE THE DAY HAPPENED", font=SANS_B(13), fill=RED)
    draw_map(d, (356, 590, 1000, 726))
    d.text((356, 732),
           "Anthropic's record $81.3bn IPO debuts on the Nasdaq today (ANT, $83).",
           font=SANS(12), fill=(60, 60, 60))

    # ---------------- bottom grid: 12 more stories ----------------
    d.line([24, 758, 1000, 758], fill=RULE, width=2)
    grid = [
        ("TECH  •  IPO",
         "Anthropic's record $81.3bn IPO values it at $1.5tn"),
        ("CLIMATE  •  COP31",
         "Ministers race to unblock COP31 climate deal"),
        ("ENERGY",
         "IEA: Hormuz crisis is gravest energy threat yet"),
        ("ART",
         "Van Gogh sells for $190.4m, an artist record"),
        ("BANGLADESH",
         "Yunus ancestral home torched as unrest spreads"),
        ("KOREA",
         "IAEA: North Korea expands uranium enrichment"),
        ("WEATHER",
         "Cyclone Akvan: 100,000 evacuated in Odisha"),
        ("DEFENCE",
         "UK to send Ukraine 1,000 long-range drones"),
        ("EUROPE",
         "EU proposes a new €45bn loan to Ukraine"),
        ("GAZA",
         "Israel in rare ground operation beyond 'yellow line'"),
        ("AMERICAS",
         "US and Venezuela sign military cooperation deal"),
        ("SPORT  •  RUGBY",
         "Wainwright and Adams back for Wales v Australia"),
    ]
    gx, gy = 24, 770
    cw, ch = 312, 52
    for i, (tag, head) in enumerate(grid):
        x = gx + (i % 3) * (cw + 20)
        yy = gy + (i // 3) * ch
        headline_cell(d, x, yy, cw, tag, head, "",
                      head_size=14, deck_size=11)

    # ---------------- footer ----------------
    d.line([24, 978, 1000, 978], fill=RULE, width=1)
    d.text((24, 984),
           "Also: a record 589m children live in conflict zones; Pew: Muslims "
           "to outnumber Christians by 2035; Abu Dhabi talks end with no deal.",
           font=SANS(11), fill=GREY)
    d.text((512, 1008), "THE WORLD TODAY — 19 NOVEMBER 2026",
           font=SANS_B(9), fill=GREY, anchor="ma")
    return img


def render_bytes():
    """Render the front page and return deterministic JPEG bytes."""
    img = render_image()
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88, optimize=False,
             progressive=False)
    return buf.getvalue()


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.jpg"
    with open(out, "wb") as fh:
        fh.write(render_bytes())
    print("wrote", out)
