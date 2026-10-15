# Photo to Line Art

Browser-local photo-to-hatching converter. No conversion API, login or watermark. Photos stay on the visitor’s device.

## Features
- Detailed hatching with diagonal, horizontal, vertical and cross-hatched strokes.
- Illustrative mode with a conservative sky mask, broad tonal regions and open white highlights.
- Side-by-side original/result, density, width, contrast, ink and paper colors.
- JPG / PNG / WebP, up to 10 MB; PNG download up to 2000 pixels on its longest side, without upscaling small originals.
- Six prerendered language homepages: English, 简体中文, 日本語, Español, Português, 한국어.
- Dedicated cross-hatching and minimalist tool pages, plus a technique guide.
- Independent artist collection configured in `artist.js`; real purchase information has not yet been supplied.

## Run locally
Use `python -m http.server 8080` from the repository root and open http://localhost:8080. A local HTTP server is recommended because the example photo is loaded into Canvas.

## Rebuild SEO pages

```sh
python -m pip install -r requirements.txt
python tools/build-seo.py
python tools/check-seo.py
```

Edit the source layout in `templates/home.html`, translations in `i18n.js`, and specialized page copy in `tools/build-seo.py`. The generated homepage and locale/topic directories are committed for buildless hosting. Do not edit generated HTML without updating its source.

## Production domain
Set the exact public `siteUrl` in `site.config.json` and rebuild before submitting to Search Console. You can also provide it through the `SITE_URL` build environment variable. Without a confirmed domain, the generator deliberately omits absolute canonical/hreflang URLs and sitemap.xml rather than guessing. It still generates all pages and crawlable language links. See `SEO.md` for the keyword map and release checklist.

## Hosting
GitHub Pages: Settings → Pages → Deploy from a branch → main / (root). This instruction does not enable Pages by itself.

Cloudflare Pages: framework None, no build command needed for the committed pages, output directory `.`. If you want to regenerate during deployment, run the Python generator with dependencies installed and configure `SITE_URL`.

The separate private ChatGPT preview is for review; it is not the public production origin.

## Structure
- `index.html`, `zh/`, `ja/`, `es/`, `pt/`, `ko/`: generated locale pages.
- `photo-to-cross-hatching/`, `minimalist-line-art/`: generated working tool pages.
- `guides/hatching-vs-cross-hatching/`: static informational guide.
- `app.js`: image loading, both renderers, presets and export.
- `i18n.js`: translations, stable language routes and browser-language suggestion.
- `styles.css`: approved light paper/blue-ink interface.
- `artist.js`: real artist/gallery/shop configuration.
- `tools/`: reproducible page generator and SEO checks.

## Scope
This is a raster hatching tool, not outline tracing, single-line vector generation, automatic cutout or generative AI. Illustrative mode is currently best for clear blue skies and bright, well-separated subjects. Handcrafted composition is not reproduced automatically. See `PHOTO-CREDIT.md` for the user-selected example photograph’s provenance status.

Repository: https://github.com/COLDDCC/photo-to-line-art
