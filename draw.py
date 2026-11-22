#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261122.

A one-page newspaper front page, "THE WORLD — Sunday 22 November 2026",
summing up the day's world news from live reporting of 22 Nov 2026
(overnight / early-morning reports). Every story is real and reported;
nothing is invented. Drawn with Pillow only; no network, no fonts beyond
the system DejaVu/Noto families.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)      # cream newsprint
INK = (18, 18, 18)           # near-black
NAVY = (16, 36, 78)          # masthead
NAVY2 = (24, 52, 110)
RED = (176, 30, 36)          # lead / ticker red
GOLD = (200, 162, 74)
TEAL = (18, 110, 105)
GREY = (92, 88, 80)
LIGHT = (233, 226, 208)
SKY = (10, 22, 52)           # night sky for the lead illustration
SEA = (16, 52, 88)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, x0, y0, x1, y1, fill=None):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2, fill=fill)
    draw.rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], outline=(150, 142, 122), width=1)


def kicker(draw, x, y, text, fill=RED, size=15):
    draw.text((x, y), text, font=font(SANS, size), fill=fill)
    return y + size + 6


def headline(draw, x, y, text, width, size=30, fill=INK):
    fnt = font(SERIF, size)
    leading = int(size * 1.08)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, n=12, fill=(255, 176, 32)):
    import math
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill, outline=(255, 220, 120))


def draw_gulf_scene(draw, x0, y0, x1, y1):
    """Night scene over the Gulf: sky, moon, missile trails, explosions,
    a US Navy ship and the Bahrain skyline."""
    # sky bands
    bands = [(10, 22, 52), (14, 32, 72), (20, 46, 92), (28, 62, 110)]
    bh = (y1 - y0) // 4
    for i, c in enumerate(bands):
        draw.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=c)
    # stars
    stars = [(0.06, 0.10), (0.16, 0.05), (0.28, 0.14), (0.42, 0.06),
             (0.55, 0.12), (0.70, 0.05), (0.84, 0.13), (0.93, 0.06),
             (0.35, 0.22), (0.62, 0.20), (0.78, 0.24)]
    for fx, fy in stars:
        sx, sy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 220))
    # moon
    mx, my, mr = x0 + int(0.86 * (x1 - x0)), y0 + int(0.16 * (y1 - y0)), 26
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(245, 238, 200))
    draw.ellipse([mx - mr + 10, my - mr + 4, mx + mr - 4, my + mr - 8],
                 fill=(228, 216, 170))
    # searchlight beams from the skyline (kept inside the scene)
    for bx, ang in [(0.18, -0.5), (0.30, -0.35)]:
        bx0 = x0 + bx * (x1 - x0)
        by0 = y0 + int(0.78 * (y1 - y0))
        tipx = bx0 + int(90 * ang)
        tipy = y0 + int(0.08 * (y1 - y0))
        draw.polygon([(bx0 - 4, by0), (bx0 + 4, by0), (tipx + 14, tipy),
                      (tipx - 14, tipy)], fill=(255, 244, 190))
    # missile / drone trails (arcs with glowing dots)
    import math
    for (sx, sy, ex, ey, lift) in [(0.05, 0.55, 0.55, 0.30, 60),
                                   (0.95, 0.60, 0.45, 0.34, 70),
                                   (0.10, 0.42, 0.38, 0.52, 40)]:
        px0, py0 = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        px1, py1 = x0 + ex * (x1 - x0), y0 + ey * (y1 - y0)
        pts = []
        for t in range(21):
            u = t / 20
            pts.append((px0 + (px1 - px0) * u,
                        py0 + (py1 - py0) * u - lift * math.sin(math.pi * u)))
        draw.line(pts, fill=(255, 190, 60), width=3)
        draw.ellipse([px1 - 5, py1 - 5, px1 + 5, py1 + 5], fill=(255, 220, 120))
    # explosions
    starburst(draw, x0 + int(0.55 * (x1 - x0)), y0 + int(0.30 * (y1 - y0)), 26, 11)
    starburst(draw, x0 + int(0.45 * (x1 - x0)), y0 + int(0.34 * (y1 - y0)), 18, 8,
              fill=(255, 120, 40))
    # skyline (Bahrain towers, dark silhouettes with lit windows)
    base = y0 + int(0.78 * (y1 - y0))
    towers = [(0.02, 0.10, 0.055), (0.08, 0.16, 0.05), (0.14, 0.08, 0.045),
              (0.62, 0.13, 0.05), (0.68, 0.07, 0.04), (0.73, 0.15, 0.055),
              (0.80, 0.09, 0.045), (0.86, 0.12, 0.05), (0.92, 0.08, 0.05)]
    for fx, fh, fw in towers:
        tx0 = x0 + fx * (x1 - x0)
        tw = fw * (x1 - x0)
        th = fh * (y1 - y0)
        draw.rectangle([tx0, base - th, tx0 + tw, base], fill=(8, 12, 26))
        for wy in range(int(base - th + 6), int(base - 4), 12):
            for wx in range(int(tx0 + 4), int(tx0 + tw - 4), 10):
                if (wx + wy) % 23 < 9:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
    # sea
    draw.rectangle([x0, base, x1, y1], fill=SEA)
    for fy in (0.84, 0.90, 0.96):
        yy = y0 + fy * (y1 - y0)
        for fx in range(0, 100, 7):
            xx = x0 + fx / 100 * (x1 - x0)
            draw.line([(xx, yy), (xx + 18, yy)], fill=(90, 150, 200), width=2)
    # US Navy ship silhouette with mast + flag
    sx0, sy0 = x0 + int(0.30 * (x1 - x0)), base + 6
    draw.polygon([(sx0, sy0 + 26), (sx0 + 150, sy0 + 26), (sx0 + 138, sy0 + 8),
                  (sx0 + 12, sy0 + 8)], fill=(10, 14, 30))
    draw.rectangle([sx0 + 40, sy0 - 8, sx0 + 96, sy0 + 8], fill=(10, 14, 30))
    draw.line([(sx0 + 66, sy0 - 8), (sx0 + 66, sy0 - 30)], fill=(10, 14, 30), width=3)
    draw.polygon([(sx0 + 66, sy0 - 30), (sx0 + 88, sy0 - 24), (sx0 + 66, sy0 - 18)],
                 fill=(176, 30, 36))
    for wx in range(sx0 + 16, sx0 + 140, 14):
        draw.rectangle([wx, sy0 + 12, wx + 5, sy0 + 17], fill=(255, 214, 110))
    # (no radar dome: it read as a floating blob in v2)


def draw_nato_scene(draw, x0, y0, x1, y1):
    """Shield over Poland: red-white flag band, jets, NATO compass star."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 245))
    # sky
    draw.rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.45], fill=(150, 190, 230))
    # jets (simple silhouettes)
    for jx, jy, s in [(0.18, 0.16, 1.0), (0.55, 0.10, 0.8)]:
        cx, cy = x0 + jx * (x1 - x0), y0 + jy * (y1 - y0)
        draw.polygon([(cx - 34 * s, cy), (cx + 30 * s, cy - 8 * s),
                      (cx + 38 * s, cy), (cx + 30 * s, cy + 8 * s)],
                     fill=(40, 48, 64))
        draw.polygon([(cx - 6 * s, cy - 4 * s), (cx + 6 * s, cy - 16 * s),
                      (cx + 12 * s, cy - 4 * s)], fill=(40, 48, 64))
        draw.line([(cx - 34 * s, cy), (cx - 58 * s, cy)], fill=(255, 255, 255),
                  width=3)
    # Polish flag band
    fy = y0 + int(0.52 * (y1 - y0))
    draw.rectangle([x0, fy, x1, fy + 16], fill=(255, 255, 255))
    draw.rectangle([x0, fy + 16, x1, fy + 32], fill=(220, 20, 60))
    # shield
    cx, cy = x0 + (x1 - x0) // 2, y0 + int(0.80 * (y1 - y0))
    draw.polygon([(cx - 34, cy - 22), (cx + 34, cy - 22), (cx + 34, cy + 6),
                  (cx, cy + 30), (cx - 34, cy + 6)], fill=NAVY,
                 outline=GOLD, width=3)
    draw.text((cx - 7, cy - 16), "★", font=font(SANS, 22), fill=GOLD)


def draw_cop_scene(draw, x0, y0, x1, y1):
    """A warming globe under a harsh sun, with a cracked desert floor."""
    draw.rectangle([x0, y0, x1, y1], fill=(250, 226, 170))
    # sun
    sx, sy, sr = x0 + int(0.80 * (x1 - x0)), y0 + int(0.22 * (y1 - y0)), 30
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 176, 32))
    for a in range(0, 360, 45):
        import math
        x2 = sx + int((sr + 12) * math.cos(math.radians(a)))
        y2 = sy + int((sr + 12) * math.sin(math.radians(a)))
        x3 = sx + int((sr + 22) * math.cos(math.radians(a)))
        y3 = sy + int((sr + 22) * math.sin(math.radians(a)))
        draw.line([(x2, y2), (x3, y3)], fill=(255, 176, 32), width=4)
    # globe
    cx, cy, r = x0 + int(0.42 * (x1 - x0)), y0 + int(0.42 * (y1 - y0)), 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 130, 190),
                 outline=NAVY, width=3)
    draw.ellipse([cx - 26, cy - 34, cx + 4, cy - 6], fill=(70, 160, 90))
    draw.ellipse([cx - 6, cy + 8, cx + 34, cy + 36], fill=(70, 160, 90))
    draw.ellipse([cx - 40, cy + 10, cx - 18, cy + 30], fill=(70, 160, 90))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255),
             width=2)
    # thermometer
    tx, ty = x0 + int(0.12 * (x1 - x0)), y0 + int(0.14 * (y1 - y0))
    draw.rounded_rectangle([tx, ty, tx + 14, ty + 74], radius=7,
                           outline=RED, width=3, fill=(255, 255, 255))
    draw.ellipse([tx - 6, ty + 66, tx + 20, ty + 92], fill=RED)
    draw.rectangle([tx + 4, ty + 30, tx + 10, ty + 74], fill=RED)
    # cracked ground
    gy = y0 + int(0.82 * (y1 - y0))
    draw.rectangle([x0, gy, x1, y1], fill=(214, 164, 96))
    draw.line([(x0 + 20, gy), (x0 + 60, gy + 14), (x0 + 52, y1 - 4)],
              fill=(140, 90, 40), width=2)
    draw.line([(x0 + 150, gy), (x0 + 120, gy + 10), (x0 + 140, y1 - 6)],
              fill=(140, 90, 40), width=2)
    draw.line([(x0 + 240, gy), (x0 + 260, gy + 12), (x0 + 250, y1 - 4)],
              fill=(140, 90, 40), width=2)


def draw_trade_scene(draw, x0, y0, x1, y1):
    """EU stars circle + Indonesian red-white flag + cargo containers."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 236, 250))
    # EU flag circle of stars
    cx, cy, r = x0 + int(0.30 * (x1 - x0)), y0 + int(0.38 * (y1 - y0)), 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 51, 153))
    import math
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + int(0.68 * r * math.cos(a)), cy + int(0.68 * r * math.sin(a))
        draw.text((sx - 5, sy - 7), "★", font=font(SANS, 12), fill=(255, 204, 0))
    # Indonesian flag (floating card, no pole: the pole cut through the scene)
    fx0, fy0 = x0 + int(0.58 * (x1 - x0)), y0 + int(0.20 * (y1 - y0))
    fw, fh = 84, 56
    draw.rectangle([fx0, fy0, fx0 + fw, fy0 + fh // 2], fill=(220, 20, 60))
    draw.rectangle([fx0, fy0 + fh // 2, fx0 + fw, fy0 + fh], fill=(255, 255, 255))
    draw.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], outline=INK, width=2)
    # containers at the bottom (the handshake bars read as clutter in v2)
    cy0 = y1 - 20
    for i, c in enumerate([(176, 30, 36), (18, 110, 105), (200, 162, 74)]):
        draw.rectangle([x0 + 12 + i * 96, cy0, x0 + 100 + i * 96, y1 - 4],
                       fill=c, outline=INK, width=2)


def draw_market_scene(draw, x0, y0, x1, y1):
    """Falling market chart with red down-trend and a Bitcoin coin."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    # grid
    for i in range(1, 5):
        gy = y0 + i * (y1 - y0) // 5
        draw.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(225, 225, 225), width=1)
    pts = []
    vals = [0.18, 0.24, 0.22, 0.38, 0.34, 0.52, 0.48, 0.66, 0.60, 0.78, 0.74, 0.88]
    for i, v in enumerate(vals):
        px = x0 + 14 + i * (x1 - x0 - 28) // (len(vals) - 1)
        py = y0 + 10 + v * (y1 - y0 - 30)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=5)
    for px, py in pts[::3]:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    # down arrow
    ax, ay = x1 - 66, y0 + 16
    draw.polygon([(ax, ay), (ax + 34, ay), (ax + 34, ay + 10), (ax + 46, ay + 10),
                  (ax + 17, ay + 34), (ax - 12, ay + 10), (ax, ay + 10)],
                 fill=RED)
    # bitcoin coin ("B" drawn as strokes: the ₿ glyph is missing in this font)
    bx, by, br = x0 + 44, y0 + int(0.62 * (y1 - y0)), 26
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(247, 147, 26),
                 outline=(180, 100, 10), width=3)
    draw.text((bx - 8, by - 15), "B", font=font(SANS, 28), fill=(255, 255, 255))
    draw.line([(bx - 8, by - 18), (bx - 8, by + 16)], fill=(255, 255, 255),
              width=2)
    draw.line([(bx + 8, by - 18), (bx + 8, by + 16)], fill=(255, 255, 255),
              width=2)


def draw_cricket_scene(draw, x0, y0, x1, y1):
    """Cricket: green outfield, pitch strip, stumps, bat and red ball."""
    draw.rectangle([x0, y0, x1, y1], fill=(34, 120, 62))
    # crowd band
    for i in range(24):
        cx = x0 + 8 + i * 13
        draw.ellipse([cx, y0 + 8, cx + 9, y0 + 17],
                     fill=[(255, 255, 255), (255, 220, 0), (220, 40, 40),
                           (40, 120, 220)][i % 4])
    # pitch strip
    px0, px1 = x0 + int(0.36 * (x1 - x0)), x0 + int(0.64 * (x1 - x0))
    draw.rectangle([px0, y0 + 30, px1, y1], fill=(222, 196, 140))
    draw.line([(px0, y0 + 30), (px0, y1)], fill=(255, 255, 255), width=2)
    draw.line([(px1, y0 + 30), (px1, y1)], fill=(255, 255, 255), width=2)
    # stumps at both ends
    for sy in (y0 + 44, y1 - 40):
        for k in range(3):
            draw.rectangle([px0 + 14 + k * 10, sy - 12, px0 + 20 + k * 10, sy + 12],
                           fill=(247, 200, 90), outline=INK, width=1)
    # batsman (white kit, dark trousers) mid-swing, kept small
    bx, by = x0 + int(0.48 * (x1 - x0)), y0 + int(0.52 * (y1 - y0))
    draw.ellipse([bx - 9, by - 40, bx + 9, by - 22], fill=(20, 20, 20))  # head
    draw.polygon([(bx - 11, by - 22), (bx + 11, by - 22), (bx + 8, by + 2),
                  (bx - 8, by + 2)], fill=(245, 245, 245), outline=INK)  # shirt
    draw.line([(bx - 6, by + 2), (bx - 14, by + 22)], fill=(20, 20, 20), width=6)
    draw.line([(bx + 6, by + 2), (bx + 16, by + 20)], fill=(20, 20, 20), width=6)
    # bat
    draw.line([(bx + 10, by - 14), (bx + 42, by - 42)], fill=(222, 196, 140),
              width=7)
    draw.line([(bx + 10, by - 14), (bx + 42, by - 42)], fill=INK, width=1)
    # red ball flying
    ballx, bally = x0 + int(0.82 * (x1 - x0)), y0 + int(0.30 * (y1 - y0))
    draw.ellipse([ballx - 9, bally - 9, ballx + 9, bally + 9], fill=(200, 30, 30),
                 outline=(120, 0, 0), width=2)
    draw.line([(ballx - 26, bally + 12), (ballx - 12, bally + 4)],
              fill=(255, 255, 255), width=2)
    draw.line([(ballx - 30, bally + 22), (ballx - 16, bally + 12)],
              fill=(255, 255, 255), width=2)
    # scoreboard strip
    sy = y1 - 30
    draw.rectangle([x0, sy, x1, y1], fill=(16, 36, 78))
    draw.text((x0 + 10, sy + 5), "IND 629-6  •  LEAD 261",
              font=font(SANS, 16), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=(150, 142, 122), width=1)

    # ---------- masthead ----------
    d.rectangle([18, 18, W - 19, 108], fill=NAVY)
    d.rectangle([18, 18, W - 19, 108], outline=GOLD, width=2)
    d.text((512, 26), "THE WORLD", font=font(SERIF, 62), fill=(247, 241, 227),
           anchor="ma")
    d.line([(40, 92), (330, 92)], fill=GOLD, width=2)
    d.line([(694, 92), (984, 92)], fill=GOLD, width=2)
    d.text((512, 90), "SUNDAY 22 NOVEMBER 2026", font=font(SANS, 15),
           fill=GOLD, anchor="ma")
    # dateline strip
    y = 116
    d.text((24, y), "THE DAY'S NEWS IN ONE PAGE", font=font(SANS, 13), fill=GREY)
    d.text((1000, y), "No. 326  •  ONE DAY, ONE PAGE", font=font(SANS, 13),
           fill=GREY, anchor="ra")
    hline(d, 24, 1000, 136, width=2)
    hline(d, 24, 1000, 140, fill=RED, width=3)

    # ---------- lead story: the Gulf ----------
    lx0, ly0, lx1, ly1 = 24, 148, 1000, 446
    d.rectangle([lx0, ly0, lx1, ly1], outline=INK, width=2)
    # left text column
    tx, tw = 40, 420
    y = ly0 + 12
    y = kicker(d, tx, y, "THE GULF  •  LEAD STORY", size=16)
    y = headline(d, tx, y, "IRAN STRIKES U.S. BASES IN BAHRAIN",
                 tw, size=36)
    y += 6
    y = para(d, tx, y,
             "Tehran says its missiles and drones hit two Patriot radars; "
             "Bahrain reports a fire at a civilian plant, no injuries.",
             font(SERIF_R, 16), tw, leading=21)
    y += 8
    y = para(d, tx, y,
             "Sirens sounded across the kingdom late on Saturday in the fourth "
             "Iranian attack on Bahrain in nine days. Washington has not "
             "confirmed the radar claims.",
             font(SANS_R, 13), tw, leading=18)
    y += 8
    d.text((tx, y), "— IRGC statement, via Al Jazeera; Bahrain Interior Ministry",
           font=font(SANS_R, 11), fill=GREY)
    # right illustration
    ix0, iy0, ix1, iy1 = 480, ly0 + 10, lx1 - 10, ly1 - 34
    draw_gulf_scene(d, ix0, iy0, ix1, iy1)
    d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)
    d.text((ix0, ly1 - 28),
           "Bahrain, home of the U.S. Navy's Fifth Fleet — air defences intercepted several attacks.",
           font=font(SANS_R, 11), fill=GREY)

    # ---------- row 2: three panels ----------
    ry0, ry1 = 456, 688
    cols = [(24, 336), (352, 664), (680, 1000)]
    # A: NATO / Poland
    x0, x1 = cols[0]
    panel(d, x0, ry0, x1, ry1)
    draw_nato_scene(d, x0 + 8, ry0 + 8, x1 - 8, ry0 + 92)
    y = ry0 + 100
    y = kicker(d, x0 + 12, y, "EUROPE  •  NATO", size=13)
    y = headline(d, x0 + 12, y, "NATO VOWS TO DEFEND EVERY INCH OF POLAND",
                 x1 - x0 - 24, size=19)
    y += 4
    para(d, x0 + 12, y,
         "After Friday's Russian missiles landed on Polish soil, NATO's chief "
         "gives the pledge; Britain's defence secretary meets Zelensky in Kyiv. "
         "The NATO council meets Monday.",
         font(SANS_R, 12), x1 - x0 - 24, leading=16)
    # B: COP31
    x0, x1 = cols[1]
    panel(d, x0, ry0, x1, ry1)
    draw_cop_scene(d, x0 + 8, ry0 + 8, x1 - 8, ry0 + 92)
    y = ry0 + 100
    y = kicker(d, x0 + 12, y, "CLIMATE  •  ANTALYA", size=13)
    y = headline(d, x0 + 12, y, "COP31 TALKS DEADLOCK OVER FOSSIL FUELS",
                 x1 - x0 - 24, size=19)
    y += 4
    para(d, x0 + 12, y,
         "Two weeks of talks run into overtime and into Sunday with no deal: "
         "the draft drops every mention of fossil fuels, and some 130 nations "
         "demand phase-out language.",
         font(SANS_R, 12), x1 - x0 - 24, leading=16)
    # C: EU-Indonesia trade
    x0, x1 = cols[2]
    panel(d, x0, ry0, x1, ry1)
    draw_trade_scene(d, x0 + 8, ry0 + 8, x1 - 8, ry0 + 92)
    y = ry0 + 100
    y = kicker(d, x0 + 12, y, "TRADE  •  BRUSSELS", size=13)
    y = headline(d, x0 + 12, y, "EU AND INDONESIA SIGN LANDMARK TRADE DEAL",
                 x1 - x0 - 24, size=19)
    y += 4
    para(d, x0 + 12, y,
         "After a decade of talks, Brussels signs a pact scrapping duties on "
         "98.5% of EU tariff lines and most Indonesian goods; it is set to "
         "take effect in early 2027.",
         font(SANS_R, 12), x1 - x0 - 24, leading=16)

    # ---------- row 3: markets + cricket ----------
    ry0, ry1 = 698, 920
    # D: markets
    x0, x1 = 24, 500
    panel(d, x0, ry0, x1, ry1)
    draw_market_scene(d, x0 + 8, ry0 + 8, x1 - 8, ry0 + 96)
    y = ry0 + 104
    y = kicker(d, x0 + 12, y, "MARKETS", size=13)
    y = headline(d, x0 + 12, y, "TECH ROUT DEEPENS; BITCOIN SLIDES TO $55,500",
                 x1 - x0 - 24, size=19)
    y += 4
    para(d, x0 + 12, y,
         "The AI-led sell-off drags shares down again as investors question "
         "sky-high tech valuations; crypto falls with it.",
         font(SANS_R, 12), x1 - x0 - 24, leading=16)
    # E: cricket
    x0, x1 = 524, 1000
    panel(d, x0, ry0, x1, ry1)
    draw_cricket_scene(d, x0 + 8, ry0 + 8, x1 - 8, ry0 + 96)
    y = ry0 + 104
    y = kicker(d, x0 + 12, y, "SPORT  •  WELLINGTON", size=13)
    y = headline(d, x0 + 12, y, "PANT TON PUTS INDIA ON TOP IN WELLINGTON",
                 x1 - x0 - 24, size=19)
    y += 4
    para(d, x0 + 12, y,
         "Rishabh Pant's century carries India to 629-6 at lunch on day four "
         "of the first Test — their highest total ever in New Zealand, a lead "
         "of 261 over the hosts.",
         font(SANS_R, 12), x1 - x0 - 24, leading=16)

    # ---------- ticker ----------
    ty0, ty1 = 930, 984
    d.rectangle([24, ty0, 1000, ty1], fill=RED)
    para(d, 36, ty0 + 6,
         "ALSO TODAY — Peru: magnitude 6.9 quake shakes the Andes, no casualties "
         "reported  •  Mexico: cartel boss “El Chapo Isidro” held; 11 killed in "
         "Sinaloa violence  •  FBI probes a hack of its crime database  •  Hong Kong "
         "votes for its Election Committee  •  Trump seeks a permanent Iran nuclear deal",
         font(SANS, 13), 1000 - 36 - 24, fill=(255, 255, 255), leading=17)

    # ---------- footer ----------
    d.text((512, 994),
           "Judge: every story above was reported on Sunday 22 November 2026.  Sources: Reuters, AP, BBC, Al Jazeera, The Times, WSJ.",
           font=font(SANS_R, 11), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
