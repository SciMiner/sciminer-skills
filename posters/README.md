# SciMiner Skill Posters

Phone-size (9 : 19.5) HTML posters showcasing every skill in this repo.

## Files

- `index.html` — gallery of all 14 posters
- `hero.html` — overview poster for the SciMiner agent
- `<skill>.html` — one poster per skill (13 total)
- `styles.css` — shared stylesheet (themed per skill)
- `generate.py` — regenerates every poster from the SKILL data in this script

## View

```bash
cd posters
python3 -m http.server 8765
# then open http://127.0.0.1:8765/index.html
```

On a phone, each poster fills the screen. On desktop, posters are framed
in a phone-shaped card.

## Export to images

For PNG export at 3x retina resolution:

```bash
# requires `playwright install chromium` first
python3 - <<'PY'
import asyncio, pathlib
from playwright.async_api import async_playwright

OUT = pathlib.Path("png"); OUT.mkdir(exist_ok=True)
URL = "http://127.0.0.1:8765"
NAMES = ["hero"] + [p.stem for p in pathlib.Path(".").glob("*.html")
                    if p.stem not in ("index", "hero")]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width":390,"height":844},
                                  device_scale_factor=3)
        for name in NAMES:
            page = await ctx.new_page()
            await page.goto(f"{URL}/{name}.html", wait_until="networkidle")
            await page.screenshot(path=str(OUT/f"{name}.png"), full_page=False)
            await page.close()
        await b.close()

asyncio.run(main())
PY
```

## Regenerate

Edit the `SKILLS` list inside `generate.py`, then:

```bash
python3 generate.py
```

All `<skill>.html` files (and `hero.html`, `index.html`) are rewritten —
`styles.css` is not touched.
