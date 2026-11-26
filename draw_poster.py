#!/usr/bin/env python3
"""Draw '25 November 2026 in one image' — a 1024x1024 news poster.

Hand-drawn with Pillow: no photos, no network, no copied artwork.
Every story is drawn from the seven headlines of the day; the lead story
(the Nvidia-led AI sell-off) gets the biggest panel, the other six share
a 2x3 grid in descending importance. Deterministic: fixed fonts, fixed
coordinates, no randomness, no timestamps, so two runs are byte-identical.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"

# ---- palette ------------------------------------------------------------
INK = (11, 17, 32)        # page background, deep navy
PANEL = (21, 30, 49)      # story panel
PANEL_ALT = (26, 37, 60)  # lead panel, slightly lighter
PAPER = (242, 245, 250)   # main text
MUTED = (154, 167, 189)   # secondary text
FAINT = (110, 124, 148)   # captions
GOLD = (217, 164, 65)     # header rule + date
RED = (229, 72, 77)       # lead accent (sell-off)
LEAD_FILL = (58, 24, 32)  # area under the lead chart line

# one accent colour per grid story, so the seven stories separate at a glance
STORIES = [
    # tag, headline, detail line, big stat, accent
    ("MIDDLE EAST", "Tankers hit by mines",
     "Mines strike shipping in the Strait of Hormuz",
     "OIL CHOKEPOINT", (232, 163, 61)),
    ("TECH / COURTS", "Huawei found guilty",
     "Verdict lands against the tech giant in a US court",
     "US COURT", (167, 139, 250)),
    ("CRYPTO", "Bitcoin falls below $60,000",
     "Crypto slides as risk appetite fades",
     "< $60,000", (247, 147, 26)),
    ("WAR IN UKRAINE", "Ukraine sinks Russian warship",
     "Naval strike claims a warship off the Libyan coast",
     "OFF LIBYA", (87, 168, 232)),
    ("LATIN AMERICA", "Colombia hostage crisis",
     "A hostage standoff grips the country",
     "STANDOFF", (67, 181, 125)),
    ("SPACE", "Pakistani astronaut reaches China's station",
     "Docks at China's Tiangong station in orbit",
     "TIANGONG", (46, 196, 182)),
]


def font(size, bold=False):
    return ImageFont.truetype(SANS_BOLD if bold else SANS, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rounded_panel(draw, box, fill, radius=14):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_header(draw):
    draw.text((28, 20), "25 NOVEMBER 2026", font=font(46, bold=True), fill=PAPER)
    draw.text((28, 70), "WEDNESDAY  ·  THE WORLD IN ONE IMAGE",
              font=font(19, bold=True), fill=GOLD)
    # right-hand chip: story count
    chip = "7 STORIES"
    cw = draw.textlength(chip, font=font(20, bold=True)) + 36
    draw.rounded_rectangle([W - 28 - cw, 26, W - 28, 66], radius=20,
                           outline=GOLD, width=2)
    draw.text((W - 28 - cw + 18, 34), chip, font=font(20, bold=True), fill=GOLD)
    draw.line([(28, 104), (W - 28, 104)], fill=GOLD, width=2)


def draw_lead(draw):
    x0, y0, x1, y1 = 28, 118, W - 28, 386
    rounded_panel(draw, [x0, y0, x1, y1], PANEL_ALT)
    draw.rectangle([x0, y0, x0 + 8, y1], fill=RED)  # red spine on the left
    draw.text((x0 + 28, y0 + 16), "LEAD STORY  ·  MARKETS",
              font=font(19, bold=True), fill=RED)
    draw.text((x0 + 28, y0 + 42), "AI sell-off rattles Asia",
              font=font(54, bold=True), fill=PAPER)
    draw.text((x0 + 28, y0 + 108),
              "Nvidia-led rout sinks chip stocks;",
              font=font(24), fill=MUTED)
    draw.text((x0 + 28, y0 + 138),
              "fear spreads from Wall Street to Asia.",
              font=font(24), fill=MUTED)

    # the two numbers that carry the story
    for i, (num, label) in enumerate([("−2.8%", "NIKKEI"), ("−5.3%", "KOSPI")]):
        sx = x0 + 560 + i * 200
        draw.text((sx, y0 + 96), num, font=font(52, bold=True), fill=RED)
        draw.text((sx + 4, y0 + 158), label, font=font(19, bold=True), fill=PAPER)

    # falling market line across the bottom of the panel (a sell-off falls)
    chart = [x0 + 28, y1 - 14, x1 - 28, y1 - 72]
    cx0, cy1, cx1, cy0 = chart
    for gy in (cy0 + 14, cy0 + 28, cy0 + 42, cy0 + 56):
        draw.line([(cx0, gy), (cx1, gy)], fill=(52, 64, 90), width=1)
    pts = [(cx0, cy0 + 4), (cx0 + 130, cy0 + 12), (cx0 + 260, cy0 + 8),
           (cx0 + 390, cy0 + 26), (cx0 + 520, cy0 + 22), (cx0 + 650, cy0 + 40),
           (cx0 + 780, cy0 + 36), (cx1, cy0 + 54)]
    fill_pts = pts + [(cx1, cy1), (cx0, cy1)]
    draw.polygon(fill_pts, fill=LEAD_FILL)
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.ellipse([cx1 - 6, cy0 + 48, cx1 + 6, cy0 + 60], fill=RED)


def draw_grid(draw):
    cols, rows = 2, 3
    gx, gy = 28, 400
    cw, ch, gap = 478, 186, 12
    for idx, (tag, head, detail, stat, accent) in enumerate(STORIES):
        col, row = idx % cols, idx // cols
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        rounded_panel(draw, [x0, y0, x1, y1], PANEL)
        draw.rectangle([x0, y0, x1, y0 + 6], fill=accent)  # accent top bar
        draw.text((x0 + 20, y0 + 18), tag, font=font(16, bold=True), fill=accent)
        # story number, top right
        num = f"{idx + 2:02d}"
        nw = draw.textlength(num, font=font(20, bold=True))
        draw.text((x1 - 20 - nw, y0 + 16), num, font=font(20, bold=True), fill=FAINT)
        lines = wrap_text(draw, head, font(29, bold=True), cw - 40)
        ly = y0 + 46
        for line in lines[:2]:
            draw.text((x0 + 20, ly), line, font=font(29, bold=True), fill=PAPER)
            ly += 35
        draw.text((x0 + 20, y0 + 122), detail, font=font(18), fill=MUTED)
        draw.text((x0 + 20, y0 + 146), stat, font=font(26, bold=True), fill=accent)


def draw_footer(draw):
    draw.text((28, 996),
              "Sources: market data and wire reports  ·  Drawn entirely in code with Pillow",
              font=font(15), fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_footer(draw)
    img.save(OUT)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
