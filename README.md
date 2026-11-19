[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/queenxaz/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/queenxaz/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# THE WORLD TODAY — Thursday 19 November 2026

A one-page newspaper front page summing up the world news of
Thursday 19 November 2026, drawn programmatically with Pillow.

Lead story: Grand Theft Auto VI launches worldwide after 13 years —
a 99 on Metacritic and Take-Two shares up 6.5%. Also on the page:
the first Trump–Xi–Putin trilateral summit in Shenzhen, the ICJ's
Rohingya genocide ruling, Ukraine's third strike on the Crimean
Bridge this week, Iran's retaliation in the Gulf, Anthropic's record
$81.3bn IPO, COP31, a Van Gogh artist record at $190.4m, Cyclone
Akvan, and a markets box plus a world map of the day's hot spots —
20 stories in all.

## Run

```
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` renders the page with `render.py` (Pillow). If Pillow is
unavailable it falls back to the pre-rendered `entry.jpg` shipped in
this repository, so both runs always write identical bytes.

## Files

- `main.py` — entry point; writes `/output/entry.png`
- `render.py` — the front-page generator (all drawing code)
- `entry.jpg` — the rendered front page (1024×1024)
- `fonts/` — DejaVu fonts bundled so rendering is identical anywhere
- `LICENSE` — MIT
