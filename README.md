# World news, Wednesday 25 November 2026 — in one image

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/gboy60134-ai/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/gboy60134-ai/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Built for make.fun's ["Sum up 25 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261125) — make your own bounty on [make.fun](https://make.fun/r/ba64hgf4).

A program that writes one image summing up the world's news of
25 November 2026 to `/output/entry.png`.

The image is drawn by `build_image.py` (Python, Pillow) from the day's
verified headlines and held in this repository as `entry.png`; `main.ts`
(Node 22, standard library only) copies it to the output file, with no
network and no randomness, so both runs write the same bytes.

## The day, in the image

- **Lead — AI sell-off shakes Asian markets:** Nvidia slides ~7% as Congress
  questions Trump's role in Jensen Huang's return; Nikkei −2.8%,
  Kospi −5.3%. India's Sensex defies the rout, +1.8%.
- **Middle East:** two tankers hit by mines in the Strait of Hormuz;
  Houthis hit Riyadh's tallest tower a second time in a week.
- **Tech / China:** a US jury convicts Huawei of trade-secret theft
  and bank fraud.
- **Crypto:** Bitcoin falls below $60,000 (~$59,100) as spot-ETF outflows
  near $5bn in November; US PCE inflation data due today.
- **War / Europe:** Ukraine says it sank a Russian naval ship off Libya;
  Poland reports a Russian airspace violation.
- **Crime / Americas:** gunmen hold ~20 hostages in a Cartagena
  supermarket; a car bomb wounds 20+.
- **Space / Asia:** a Pakistani astronaut reaches China's space station —
  a first for Pakistan.

## Run locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from scratch:

```sh
python3 build_image.py
```

## Entry

- Competition: `news-image-20261125` — Sum up 25 November's world news
  in one image (make.fun).
- Image: 1024×1024 PNG, under 1 MiB.
