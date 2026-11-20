# draw.py -- draws "The World in One Day", a one-page newspaper front page
# summing up Thursday 19 November 2026, as a 1024x1024 PNG.
# Procedural art only: every pixel is drawn here with PIL ImageDraw.
# No photos, no downloads, no network, no timestamps. Deterministic.
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W = 1024
H = 1024
CREAM = (244, 238, 221)
PAPER2 = (238, 230, 208)
INK = (24, 24, 24)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (28, 74, 92)
TEAL_LT = (64, 120, 138)
GREY = (104, 99, 88)
GOLD = (198, 158, 38)
SKIN1 = (232, 190, 150)
SKIN2 = (226, 178, 132)
SKIN3 = (240, 205, 170)


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif(size, bold=False):
    return load_font("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return load_font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, max_w, fill=INK, leading=None, align="left"):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.22)
    for line in wrap(draw, text, font, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=font)) / 2
        elif align == "right":
            lx = x + max_w - draw.textlength(line, font=font)
        else:
            lx = x
        draw.text((lx, y), line, font=font, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, font, fill=INK):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.2)


def letterspaced(draw, cx, y, text, font, fill=INK, spacing=4):
    """Draw a short caps line with manual letter spacing, centered."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing
    return y + int(font.size * 1.2)


def rule(draw, x0, y, x1, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def halftone(draw, x0, y0, x1, y1, step=9, color=(214, 200, 168)):
    """Sparse dot texture for flat illustration areas."""
    for yy in range(y0, y1, step):
        for xx in range(x0, y1 if False else x1, step):
            if ((xx // step) + (yy // step)) % 2 == 0:
                draw.ellipse([xx, yy, xx + 2, yy + 2], fill=color)


def draw_flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=RED)
    draw.rectangle([x, y, x + w * 0.42, y + stripe * 7], fill=NAVY)
    for r in range(3):
        for c in range(4):
            sx = x + 4 + c * (w * 0.42 - 8) / 3
            sy = y + 3 + r * (stripe * 7 - 6) / 2
            draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))


def draw_flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=RED, outline=INK, width=1)
    cx, cy = x + w * 0.22, y + h * 0.3
    draw.regular_polygon((cx, cy, 5), 5, fill=GOLD)
    for px, py in [(0.55, 0.2), (0.68, 0.38), (0.62, 0.62), (0.42, 0.62)]:
        draw.regular_polygon((x + w * px, y + h * py, 3), 5, fill=GOLD)


def draw_flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))


def draw_leader(draw, cx, y, skin, hair, suit, tie):
    """One flat geometric leader: head, hair, shoulders, tie."""
    draw.ellipse([cx - 17, y, cx + 17, y + 34], fill=skin, outline=INK, width=2)
    draw.pieslice([cx - 17, y - 3, cx + 17, y + 16], 180, 360, fill=hair)
    draw.rectangle([cx - 15, y + 10, cx + 15, y + 16], fill=hair)
    draw.polygon([(cx - 34, y + 62), (cx - 22, y + 36), (cx + 22, y + 36),
                  (cx + 34, y + 62)], fill=suit, outline=INK)
    draw.polygon([(cx - 7, y + 38), (cx, y + 46), (cx + 7, y + 38),
                  (cx + 4, y + 62), (cx - 4, y + 62)], fill=(255, 255, 255))
    draw.polygon([(cx - 4, y + 44), (cx + 4, y + 44), (cx + 3, y + 60),
                  (cx - 3, y + 60)], fill=tie)


def draw_atom(draw, cx, cy, r, color=NAVY):
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)
    for ang in (0, 60, 120):
        draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
                 fill=color, width=2)


def draw_trilateral(draw, x, y, w, h):
    """Three leaders at one table under three flags, atom emblem."""
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    halftone(draw, x + 4, y + 4, x + w - 4, y + 34)
    # flags on poles
    fw, fh = 74, 44
    for i, fn in enumerate((draw_flag_us, draw_flag_cn, draw_flag_ru)):
        fx = x + 18 + i * (w - 36 - fw) // 2
        draw.line([(fx + fw / 2, y + 8), (fx + fw / 2, y + 8 + fh + 6)],
                  fill=INK, width=2)
        fn(draw, fx, y + 8, fw, fh)
    # leaders
    base = y + h - 78
    draw_leader(draw, x + w * 0.20, base, SKIN1, (232, 205, 120), NAVY, RED)
    draw_leader(draw, x + w * 0.50, base, SKIN2, (40, 40, 40), (60, 60, 60), RED)
    draw_leader(draw, x + w * 0.80, base, SKIN3, (150, 120, 80), (90, 40, 40), NAVY)
    # table
    draw.rectangle([x + 8, base + 62, x + w - 8, base + 74], fill=(122, 84, 52),
                   outline=INK, width=2)
    draw.rectangle([x + 8, base + 62, x + w - 8, base + 68], fill=(150, 108, 66))
    # name plates
    for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
        cx = x + w * (0.20 + 0.30 * i)
        f = sans(10, bold=True)
        tw = draw.textlength(name, font=f)
        draw.rectangle([cx - tw / 2 - 5, base + 46, cx + tw / 2 + 5, base + 60],
                       fill=(255, 255, 255), outline=INK, width=1)
        draw.text((cx - tw / 2, base + 47), name, font=f, fill=INK)
    # atom emblem top-right corner
    draw_atom(draw, x + w - 26, y + 22, 16)


def draw_icj(draw, x, y, w, h):
    """Peace Palace silhouette + scales of justice."""
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    # palace: main block + tower
    draw.rectangle([x + 14, y + h - 46, x + w - 14, y + h - 8], fill=NAVY,
                   outline=INK, width=1)
    draw.rectangle([x + w / 2 - 12, y + 12, x + w / 2 + 12, y + h - 46],
                   fill=NAVY, outline=INK, width=1)
    draw.polygon([(x + w / 2 - 16, y + 12), (x + w / 2 + 16, y + 12),
                  (x + w / 2, y - 2)], fill=RED, outline=INK)
    for i in range(5):
        wx = x + 22 + i * ((w - 44) / 5)
        draw.rectangle([wx, y + h - 38, wx + 10, y + h - 20], fill=CREAM)
    draw.rectangle([x + w / 2 - 6, y + h - 40, x + w / 2 + 6, y + h - 8],
                   fill=CREAM, outline=INK, width=1)
    # scales, right side
    sx = x + w - 34
    sy = y + h - 52
    draw.line([(sx, sy - 26), (sx, sy)], fill=INK, width=2)
    draw.line([(sx - 18, sy - 22), (sx + 18, sy - 22)], fill=INK, width=2)
    draw.line([(sx - 18, sy - 22), (sx - 26, sy - 6)], fill=INK, width=1)
    draw.line([(sx - 18, sy - 22), (sx - 10, sy - 6)], fill=INK, width=1)
    draw.line([(sx + 18, sy - 22), (sx + 10, sy - 6)], fill=INK, width=1)
    draw.line([(sx + 18, sy - 22), (sx + 26, sy - 6)], fill=INK, width=1)
    draw.arc([sx - 30, sy - 12, sx - 6, sy + 2], 0, 180, fill=INK, width=2)
    draw.arc([sx + 6, sy - 12, sx + 30, sy + 2], 0, 180, fill=INK, width=2)


def draw_cop31(draw, x, y, w, h):
    """Thermometer + globe, with FOSSIL FUELS struck through."""
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    # thermometer
    tx = x + 26
    draw.rounded_rectangle([tx, y + 10, tx + 16, y + h - 22], radius=8,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.ellipse([tx - 6, y + h - 30, tx + 22, y + h - 8], fill=RED,
                 outline=INK, width=2)
    draw.rectangle([tx + 5, y + 22, tx + 11, y + h - 22], fill=RED)
    for i in range(4):
        ty = y + 18 + i * 12
        draw.line([(tx + 16, ty), (tx + 22, ty)], fill=INK, width=1)
    # globe
    gx, gy, gr = x + w - 44, y + 28, 17
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=TEAL_LT,
                 outline=INK, width=2)
    draw.ellipse([gx - 8, gy - 12, gx + 2, gy - 2], fill=(120, 190, 110))
    draw.ellipse([gx - 2, gy + 2, gx + 10, gy + 12], fill=(120, 190, 110))
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=INK, width=1)
    # red strike across the thermometer: the draft cuts fossil fuels
    draw.line([(tx - 6, y + h - 12), (tx + 28, y + 6)], fill=RED, width=3)


def draw_icon_anthropic(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    draw.line([(x + 10, y + h - 12), (x + w * 0.4, y + h * 0.45),
               (x + w * 0.62, y + h * 0.6), (x + w - 10, y + 10)],
              fill=RED, width=3)
    draw.polygon([(x + w - 22, y + 10), (x + w - 8, y + 10), (x + w - 8, y + 24)],
                 fill=RED)
    f = sans(12, bold=True)
    draw.text((x + 10, y + 6), "ANT $83", font=f, fill=NAVY)


def draw_icon_gta(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 34), outline=INK, width=1)
    f = serif(26, bold=True)
    draw.text((x + 12, y + 4), "VI", font=f, fill=(255, 255, 255))
    # tiny gamepad: d-pad cross + two buttons
    draw.line([(x + w - 52, y + h - 19), (x + w - 40, y + h - 19)],
              fill=(255, 255, 255), width=3)
    draw.line([(x + w - 46, y + h - 25), (x + w - 46, y + h - 13)],
              fill=(255, 255, 255), width=3)
    draw.ellipse([x + w - 34, y + h - 24, x + w - 26, y + h - 16],
                 fill=RED)
    draw.ellipse([x + w - 22, y + h - 24, x + w - 14, y + h - 16],
                 fill=GOLD)
    draw.line([(x + 12, y + h - 14), (x + 40, y + h - 14)], fill=RED, width=3)


def draw_icon_iran(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    draw.rectangle([x + 14, y + 10, x + w - 14, y + h - 8], fill=(255, 255, 255),
                   outline=INK, width=1)
    draw.rectangle([x + 14, y + 10, x + w - 14, y + 24], fill=RED)
    f = serif(20, bold=True)
    centered(draw, x + w / 2, y + 26, "2027", f, fill=NAVY)
    draw.line([(x + 30, y + 6), (x + 30, y + 14)], fill=INK, width=3)
    draw.line([(x + w - 30, y + 6), (x + w - 30, y + 14)], fill=INK, width=3)


def draw_icon_pif(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=INK, width=1)
    # tower with a jagged crack band
    tx = x + w / 2 - 16
    draw.polygon([(tx, y + h - 6), (tx + 6, y + 6), (tx + 26, y + 6),
                  (tx + 32, y + h - 6)], fill=NAVY, outline=INK)
    for i in range(5):
        wy = y + 12 + i * 7
        draw.line([(tx + 8, wy), (tx + 24, wy)], fill=(255, 255, 255), width=1)
    draw.line([(tx + 8, y + 22), (tx + 16, y + 30), (tx + 10, y + 38)],
              fill=RED, width=2)
    draw.line([(x + 12, y + 12), (x + 34, y + 26)], fill=RED, width=2)
    draw.ellipse([x + 10, y + 8, x + 18, y + 16], fill=GOLD)


def draw_icon_akvan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=TEAL, outline=INK, width=1)
    cx, cy = x + w / 2, y + h / 2 - 2
    for r in (22, 16, 10):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255),
                 width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(214, 190, 140))


def draw_world_map(draw, x, y, w, h, pins):
    """Simplified world map: teal sea, cream continents, numbered pins."""
    draw.rectangle([x, y, x + w, y + h], fill=TEAL, outline=INK, width=1)
    land = (232, 222, 190)
    # North America
    draw.polygon([(x + 8, y + 26), (x + 60, y + 8), (x + 118, y + 18),
                  (x + 112, y + 52), (x + 78, y + 66), (x + 44, y + 58),
                  (x + 16, y + 48)], fill=land, outline=INK)
    # South America
    draw.polygon([(x + 96, y + 76), (x + 132, y + 72), (x + 142, y + 104),
                  (x + 122, y + 140), (x + 104, y + 118)], fill=land, outline=INK)
    # Europe
    draw.polygon([(x + 218, y + 22), (x + 258, y + 14), (x + 272, y + 34),
                  (x + 252, y + 52), (x + 222, y + 46)], fill=land, outline=INK)
    # Africa
    draw.polygon([(x + 224, y + 62), (x + 268, y + 58), (x + 284, y + 88),
                  (x + 268, y + 124), (x + 242, y + 112), (x + 226, y + 86)],
                 fill=land, outline=INK)
    # Asia
    draw.polygon([(x + 280, y + 14), (x + 380, y + 6), (x + 470, y + 22),
                  (x + 462, y + 58), (x + 400, y + 70), (x + 340, y + 56),
                  (x + 296, y + 44)], fill=land, outline=INK)
    # Australia
    draw.polygon([(x + 420, y + 108), (x + 462, y + 104), (x + 470, y + 124),
                  (x + 436, y + 132), (x + 418, y + 122)], fill=land, outline=INK)
    f = sans(11, bold=True)
    for num, (px, py) in pins:
        draw.ellipse([x + px - 9, y + py - 9, x + px + 9, y + py + 9],
                     fill=RED, outline=(255, 255, 255), width=2)
        tw = draw.textlength(str(num), font=f)
        draw.text((x + px - tw / 2, y + py - 8), str(num), font=f,
                  fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # double outer border, classic newspaper
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)
    x0, x1 = 28, 996
    cw = x1 - x0

    # ---- masthead ----
    letterspaced(d, W / 2, 30, "THE WORLD IN ONE DAY", sans(13, bold=True),
                 fill=RED, spacing=5)
    centered(d, W / 2, 52, "Thursday 19 November 2026", serif(54, bold=True))
    rule(d, x0, 122, x1, width=4, fill=RED)
    text_block(d, x0, 130,
               "Trump, Xi and Putin meet in Shenzhen  •  World Court finds "
               "Myanmar guilty of genocide  •  COP31 draft cuts fossil fuels",
               serif(16), cw, fill=RED, align="center", leading=20)

    # ---- stats strip ----
    stats = [
        ("3", "LEADERS AT ONE TABLE"),
        ("90 min", "TRILATERAL, SHENZHEN"),
        ("9–6 (CNN)", "ICJ GENOCIDE VOTE"),
        ("~10,000", "ROHINGYA KILLED (EST.)"),
        ("7–8", "PIF TOWER FLOORS HIT"),
        ("100,000+", "EVACUATED IN ODISHA"),
    ]
    sy = 168
    rule(d, x0, sy, x1, width=1)
    box_w = cw / 6
    for i, (num, label) in enumerate(stats):
        bx = x0 + i * box_w
        centered(d, bx + box_w / 2, sy + 8, num, serif(27, bold=True))
        text_block(d, bx + 4, sy + 40, label, sans(10, bold=True),
                   box_w - 8, fill=GREY, align="center", leading=12)
        if i:
            d.line([(bx, sy + 6), (bx, sy + 56)], fill=GREY, width=1)
    rule(d, x0, sy + 62, x1, width=2)

    # ---- lead row ----
    ly = 240
    lead_h = 228
    # 1. Trilateral, big left panel
    tx, tw = x0, 524
    d.rectangle([tx, ly, tx + tw, ly + lead_h], outline=INK, width=1)
    text_block(d, tx + 10, ly + 6, "1  SHENZHEN — SUMMIT", sans(11, bold=True),
               tw - 20, fill=RED, leading=13)
    draw_trilateral(d, tx + 10, ly + 24, tw - 20, 96)
    y = text_block(d, tx + 10, ly + 126,
                   "Trump, Xi and Putin hold first-ever three-way summit",
                   serif(22, bold=True), tw - 20, leading=26)
    text_block(d, tx + 10, y + 2,
               "90 minutes at Kylin Villa: “A nuclear war cannot be won "
               "and must never be fought.” No breakthrough; Ukraine not "
               "named in the joint statement. — Reuters, CNN",
               serif(12), tw - 20, leading=15)
    # 2. ICJ, top right
    rx, rw = tx + tw + 8, x1 - (tx + tw + 8)
    rh = 110
    d.rectangle([rx, ly, rx + rw, ly + rh], outline=INK, width=1)
    text_block(d, rx + 10, ly + 6, "2  THE HAGUE — JUSTICE", sans(11, bold=True),
               rw - 20, fill=RED, leading=13)
    draw_icj(d, rx + 10, ly + 24, 104, 80)
    text_block(d, rx + 122, ly + 24,
               "World Court: Myanmar committed genocide",
               serif(18, bold=True), rw - 132, leading=21)
    text_block(d, rx + 122, ly + 68,
               "First state ever found guilty by the ICJ. Reparations "
               "ordered; report due in two years. — Le Monde, CNN",
               serif(11), rw - 132, leading=14)
    # 3. COP31, bottom right
    cy = ly + rh + 8
    ch = lead_h - rh - 8
    d.rectangle([rx, cy, rx + rw, cy + ch], outline=INK, width=1)
    text_block(d, rx + 10, cy + 6, "3  ANTALYA — CLIMATE", sans(11, bold=True),
               rw - 20, fill=RED, leading=13)
    draw_cop31(d, rx + 10, cy + 24, 104, 80)
    text_block(d, rx + 122, cy + 24,
               "COP31 draft drops fossil fuels — and its $120bn aid goal",
               serif(18, bold=True), rw - 132, leading=21)
    text_block(d, rx + 122, cy + 68,
               "Thursday text strips both from the deal; talks run to "
               "Friday. — Reuters, CNN",
               serif(11), rw - 132, leading=14)

    # ---- second row: five mid panels ----
    ry = 478
    rh2 = 176
    panels = [
        ("4  NEW YORK — MARKETS", "Anthropic lists on Nasdaq in record IPO",
         "Claude maker raises $81.3bn — the biggest IPO ever — at $83 a "
         "share. Ticker ANT. — WSJ, CNN", draw_icon_anthropic),
        ("5  WORLDWIDE — GAMES", "GTA VI is out, 13 years after GTA V",
         "Launch day on PS5 and Xbox. An estimated $1.84bn in day-one "
         "sales (Sensor Tower estimate).", draw_icon_gta),
        ("6  ABOARD AIR FORCE ONE", "Trump pushes Iran decision to 2027",
         "“I’m not rushing.” Netanyahu presses for strikes; the US leans "
         "on sanctions and a sea blockade.", draw_icon_iran),
        ("7  RIYADH — GULF", "Houthi missile damages PIF Tower",
         "Windows out on 7–8 floors of the 385 m tower; no injuries. "
         "Coalition says debris; witnesses say a direct hit.",
         draw_icon_pif),
        ("8  ODISHA — STORM", "Cyclone Akvan nears India’s coast",
         "Landfall expected Friday. Winds 90–100 km/h; 100,000+ evacuated. "
         "Third cyclone in a month. — IMD", draw_icon_akvan),
    ]
    pw = (cw - 4 * 7) / 5
    for i, (label, head, body, icon) in enumerate(panels):
        px = x0 + i * (pw + 7)
        d.rectangle([px, ry, px + pw, ry + rh2], outline=INK, width=1)
        icon(d, px + 8, ry + 6, pw - 16, 46)
        text_block(d, px + 8, ry + 58, label, sans(10, bold=True),
                   pw - 16, fill=RED, leading=12)
        y = text_block(d, px + 8, ry + 72, head, serif(13, bold=True),
                       pw - 16, leading=15)
        text_block(d, px + 8, y + 2, body, serif(10), pw - 16, leading=13)

    # ---- map + also ----
    my = 664
    mh = 252
    mx, mw = x0, 524
    d.rectangle([mx, my, mx + mw, my + mh], outline=INK, width=1)
    text_block(d, mx + 10, my + 6, "WHERE IT HAPPENED", sans(12, bold=True),
               mw - 20, leading=14)
    pins = [(1, (428, 58)), (2, (228, 36)), (3, (278, 52)), (4, (70, 42)),
            (5, (300, 68)), (6, (392, 72)), (7, (252, 24)), (8, (448, 44))]
    draw_world_map(d, mx + 10, my + 24, mw - 20, 178, pins)
    text_block(d, mx + 10, my + 208,
               "1 Shenzhen  2 The Hague  3 Antalya  4 New York  "
               "5 Riyadh  6 Odisha  7 Berlin  8 Seoul",
               sans(10), mw - 20, leading=13)
    text_block(d, mx + 10, my + 226,
               "Numbers match the stories on this page.",
               serif(10), mw - 20, fill=GREY, leading=13)

    ax = mx + mw + 8
    aw = x1 - ax
    d.rectangle([ax, my, ax + aw, my + mh], outline=INK, width=1)
    text_block(d, ax + 10, my + 6, "ALSO ON THURSDAY", sans(12, bold=True),
               aw - 20, leading=14)
    also = [
        "Berlin: Europe ready to talk to Russia on Ukraine — with Kyiv.",
        "Seoul: Korea’s top court clears ex-PM Han Duck-soo.",
        "Voyager 1 reaches one light-day from Earth, a first. — NASA",
        "Anthropic shares close up 17% on their first day. — Dealroom",
        "COP31 talks due to end Friday; deal may run into overtime.",
        "Trump and Putin met alone for ~40 minutes before the trio.",
        "Myanmar must report back to the Court within two years.",
        "New START, the last US–Russia arms treaty, lapsed in Feb.",
    ]
    ay = my + 26
    for i, item in enumerate(also, 1):
        y = text_block(d, ax + 10, ay, "%d. %s" % (i, item), serif(11),
                       aw - 20, leading=14)
        ay = y + 5
        if i < len(also):
            d.line([(ax + 10, ay - 3), (ax + aw - 10, ay - 3)], fill=(220, 210, 186),
                   width=1)

    # ---- footer: date check ----
    fy = 926
    d.rectangle([x0, fy, x1, fy + 56], fill=RED)
    text_block(d, x0 + 10, fy + 7,
               "DATE CHECK — Every story on this page happened, or was first "
               "reported, on Thursday 19 November 2026. Claims are "
               "attributed, not stated as fact.",
               sans(11, bold=True), cw - 20, fill=(255, 255, 255), leading=14)
    text_block(d, x0 + 10, fy + 38,
               "Sources: Reuters, AP, AFP, BBC, CNN, Le Monde, NASA, IMD. "
               "Drawn procedurally; no photographs.",
               sans(10), cw - 20, fill=(255, 255, 255), leading=13)

    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    print(build())
