# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Skyzee2704/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Skyzee2704/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

"The World in One Day" — a one-page newspaper front page summing up the
world news of Thursday 19 November 2026 in a single 1024x1024 image.

Lead stories: the first-ever Trump–Xi–Putin trilateral in Shenzhen ("A
nuclear war cannot be won and must never be fought"), the ICJ finding
Myanmar committed genocide against the Rohingya, and the COP31 draft
dropping fossil fuels — and its $120bn aid goal. Plus Anthropic's record
$81.3bn Nasdaq IPO, GTA VI launch day, Trump pushing the Iran decision to
2027, the Houthi missile damage to Riyadh's PIF Tower, Cyclone Akvan
nearing Odisha, a world map with numbered pins, and an "Also on Thursday"
strip. Every figure is verified against at least two sources or
attributed in the image; a red DATE CHECK footer states that every story
happened, or was first reported, on 19 November 2026.

The image is drawn procedurally — no photographs, no downloads. `draw.py`
(Python + PIL, run on the build machine) renders the front page from
scratch with flat-vector editorial illustrations and bundled DejaVu fonts,
writing `entry.png`. `main.py` (stdlib only: `shutil` + `os`) is the
program the grader runs: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, byte-identical on every run.

## Run it

```sh
python3 draw.py        # renders entry.png (1024x1024, PNG)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — entrypoint, stdlib only
- `draw.py` — the procedural newspaper renderer
- `entry.png` — the rendered front page (1024x1024)
- `fonts/` — bundled DejaVu fonts + licence

---

<sub>Entered on [make.fun](https://make.fun/?ref=8mpyaw0z&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
