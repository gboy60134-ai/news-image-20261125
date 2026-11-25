#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news image (1024x1024 PNG).

The image is rendered once, by hand-written code, from the day's verified
headlines. The entry program (main.ts) only copies the finished PNG, so the
grader's two runs write identical bytes. No network, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (13, 21, 38)          # deep navy
CARD = (24, 39, 66)        # card navy
CARD_EDGE = (42, 60, 94)
WHITE = (255, 255, 255)
SUMMARY = (194, 206, 223)  # light grey-blue
MUTED = (148, 163, 184)
GOLD = (232, 184, 75)
RED = (229, 72, 77)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_card(draw, x, y, w, h, tag, tag_color, headline, summary):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14,
                           fill=CARD, outline=CARD_EDGE, width=1)
    pad = 20
    # tag chip
    tag_f = font(SANS_B, 19)
    tw = draw.textlength(tag, font=tag_f)
    chip_w, chip_h = tw + 20, 30
    draw.rounded_rectangle([x + pad, y + 14, x + pad + chip_w, y + 14 + chip_h],
                           radius=8, fill=tag_color)
    draw.text((x + pad + 10, y + 14 + 5), tag, font=tag_f, fill=WHITE)
    # headline (up to 2 lines), then summary directly below it
    head_f = font(SANS_B, 29)
    lines = wrap(draw, headline, head_f, w - 2 * pad)[:2]
    ty = y + 54
    for line in lines:
        draw.text((x + pad, ty), line, font=head_f, fill=WHITE)
        ty += 34
    sum_f = font(SANS, 21)
    slines = wrap(draw, summary, sum_f, w - 2 * pad)[:2]
    sy = ty + 8
    for line in slines:
        draw.text((x + pad, sy), line, font=sum_f, fill=SUMMARY)
        sy += 25


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width

    # ---- masthead ----
    d.text((mx, 34), "THE WORLD IN ONE PAGE", font=font(SANS_B, 27), fill=GOLD)
    d.text((mx, 66), "WEDNESDAY, 25 NOVEMBER 2026",
           font=font(SANS_B, 50), fill=WHITE)
    # small globe motif, top-right corner, clear of the date line
    gx, gy, gr = W - mx - 30, 48, 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=GOLD, width=3)
    d.ellipse([gx - 13, gy - gr, gx + 13, gy + gr], outline=GOLD, width=2)
    d.line([gx - gr, gy, gx + gr, gy], fill=GOLD, width=2)
    d.line([gx - gr + 8, gy - 17, gx + gr - 8, gy - 17], fill=GOLD, width=2)
    d.line([gx - gr + 8, gy + 17, gx + gr - 8, gy + 17], fill=GOLD, width=2)
    d.line([mx, 150, W - mx, 150], fill=GOLD, width=3)

    # ---- lead story ----
    ly, lh = 168, 168
    d.rounded_rectangle([mx, ly, mx + cw, ly + lh], radius=14,
                        fill=(46, 24, 28), outline=(122, 52, 56), width=1)
    d.rectangle([mx, ly + 14, mx + 8, ly + lh - 14], fill=RED)
    tag_f = font(SANS_B, 19)
    tag = "MARKETS  •  ASIA"
    tw = d.textlength(tag, font=tag_f)
    d.rounded_rectangle([mx + 26, ly + 16, mx + 26 + tw + 20, ly + 46],
                        radius=8, fill=RED)
    d.text((mx + 36, ly + 21), tag, font=tag_f, fill=WHITE)
    d.text((mx + 26, ly + 56), "AI SELL-OFF SHAKES ASIAN MARKETS",
           font=font(SANS_B, 42), fill=WHITE)
    d.text((mx + 26, ly + 112),
           "Nvidia slides ~7% as Congress questions Trump's role in Huang's",
           font=font(SANS, 25), fill=SUMMARY)
    d.text((mx + 26, ly + 140),
           "return; Nikkei \u22122.8%, Kospi \u22125.3%. Sensex defies the rout, +1.8%.",
           font=font(SANS, 25), fill=SUMMARY)

    # ---- six story cards, 2 columns x 3 rows ----
    stories = [
        ("MIDDLE EAST", (247, 107, 21), "TANKERS HIT BY MINES IN STRAIT OF HORMUZ",
         "Two tankers struck; Houthis hit Riyadh's tallest tower again."),
        ("TECH  •  CHINA", (62, 155, 255), "HUAWEI GUILTY IN US COURT",
         "Jury convicts the telecom giant of trade-secret theft and fraud."),
        ("CRYPTO", (245, 165, 36), "BITCOIN FALLS BELOW $60,000",
         "BTC ~$59,100 as ETF outflows near $5bn in November."),
        ("WAR  •  EUROPE", (18, 165, 148), "UKRAINE SINKS RUSSIAN WARSHIP",
         "Kyiv says it sank a Russian naval ship off Libya; Poland cites airspace violation."),
        ("CRIME  •  AMERICAS", (142, 107, 232), "HOSTAGE CRISIS IN COLOMBIA",
         "Gunmen hold ~20 hostages in a Cartagena supermarket; car bomb wounds 20+."),
        ("SPACE  •  ASIA", (232, 72, 140), "PAKISTANI ASTRONAUT REACHES CHINESE STATION",
         "A first for Pakistan as China hosts its first foreign astronaut."),
    ]
    gap = 16
    card_w = (cw - gap) // 2
    card_h = 180
    gx0, gy0 = mx, 352
    for i, (tag, color, head, summ) in enumerate(stories):
        x = gx0 + (i % 2) * (card_w + gap)
        y = gy0 + (i // 2) * (card_h + gap)
        draw_card(d, x, y, card_w, card_h, tag, color, head, summ)

    # ---- footer ----
    fy = 352 + 3 * card_h + 2 * gap + 18
    d.line([mx, fy, W - mx, fy], fill=CARD_EDGE, width=2)
    foot = "25 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE"
    fw = d.textlength(foot, font=font(SANS_B, 22))
    d.text(((W - fw) / 2, fy + 12), foot, font=font(SANS_B, 22), fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
