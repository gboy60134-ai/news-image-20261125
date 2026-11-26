# Build notes — news-image-20261125 v2 ("Red Wednesday")

## The seven stories (25 November 2026 — same stories as v1, no swaps)

1. Nvidia / AI sell-off — LEAD. Nikkei −2.8%, Kospi −5.3%.
2. Tankers hit by mines in the Strait of Hormuz.
3. Huawei found guilty in a US court.
4. Bitcoin below $60,000.
5. Ukraine sinks a Russian warship off Libya.
6. Colombia hostage crisis.
7. Pakistani astronaut reaches the Chinese space station (Tiangong).

Only the figures above are used; no other numbers appear on the poster.

## Layout choice

- Header: date "25 NOVEMBER 2026" + "WEDNESDAY · THE WORLD IN ONE IMAGE" + a
  "7 STORIES" chip, gold rule underneath.
- Lead panel (full width, ~28% of the height): biggest headline, the two index
  numbers in large red type, and a falling market line with a red end-dot —
  the chart must fall, because the story is a sell-off.
- Grid 2×3 for stories 2–7 in descending importance: each cell has a distinct
  accent colour top bar, a region tag, a headline (max 2 lines), a detail line,
  a big key stat, and a story number (02–07) so the seven separate at a glance.
- Footer: small source/method note, kept legible.

## What was verified

- `python3 draw_poster.py` run twice: byte-identical PNGs both times
  (sha256 47172d7f49ad0c371b51948411a20dfbcfc1d16ec6e1a70e8a0f374a46c19fed).
- Rendered and viewed the PNG at full size: all 7 stories present and
  readable, nothing cut off at the edges, no overlapping labels.
- Two real defects found on the first render and fixed with a genuine second
  edit of draw_poster.py: (1) the lead sublines ran underneath the −2.8% /
  −5.3% stats — sublines shortened to fit the left column; (2) the market
  line rose left-to-right, which reads as a rally — inverted so it falls,
  and the end-dot moved to the low end.
- 1024×1024 RGB PNG, drawn entirely with PIL shapes/text (DejaVu fonts),
  no external images, no network. LICENSE is the kit starter's MIT license.
- Written fresh in this session; the old v1 entry's script and files were
  never read or copied.
