# Search structure and keyword map

## What this site actually does
The site creates hatching from photographs. It does not trace outlines, create a single continuous line, reconstruct vector paths, remove backgrounds, or call a generative image model. Do not add claims for those adjacent queries unless the implementation changes.

## Pages and intent
| Route | Primary intent | Related terms |
| --- | --- | --- |
| `/` | photo to line art converter | image to line art, hatching generator, free online line art converter |
| `/photo-to-cross-hatching/` | photo to cross hatching | cross hatching converter, cross hatch photo effect, intersecting line drawing |
| `/minimalist-line-art/` | minimalist line art generator | simple hatching, photo to minimalist drawing, blue ink hatching |
| `/guides/hatching-vs-cross-hatching/` | technique comparison | hatching vs cross hatching, line art vs outline, density and line width |
| `/zh/` | 照片转线条画 | 图片转排线画、交叉排线、极简线条画 |
| `/ja/` | 写真を線画に変換 | ハッチング、クロスハッチング、写真 線画 無料 |
| `/es/` | foto a dibujo de líneas | tramado cruzado, arte de líneas gratis |
| `/pt/` | foto para desenho de linhas | hachura cruzada, hachura online grátis |
| `/ko/` | 사진을 선화로 변환 | 해칭, 크로스해칭, 무료 선화 |

These are relevance-based clusters informed by current search-result phrasing, not verified search-volume or difficulty estimates. The two focused tool pages start the actual editor in their named mode, and contain specific advice and limits. The guide has distinct informational content. Do not make separate thin pages for every synonym.

## Production domain configuration
The repository has no confirmed public production origin. `site.config.json` therefore leaves `siteUrl` empty. No guessed canonical or sitemap host is emitted.

After choosing a domain, set `siteUrl` to its exact HTTPS origin (or origin plus deployment subdirectory), then run:

```sh
python -m pip install -r requirements.txt
python tools/build-seo.py
```

Or set `SITE_URL=https://your-real-domain` for the build. The generator emits self-canonicals, reciprocal hreflang links on the six equivalent homepages, an x-default English link, Open Graph URLs, valid structured-data URLs, sitemap.xml and its robots.txt reference. Subdirectory hosting is supported.

Commit generated HTML for buildless hosting. Alternatively Cloudflare Pages can run the generator as its build command with `SITE_URL` configured and `.` as output directory. Rebuild whenever translations, the template or specialized content change. Source template: `templates/home.html`. Generator: `tools/build-seo.py`.

There are no automatic language redirects. Each locale has fixed initial HTML. Browsers receive a language suggestion, and users can choose a different version. Home-page language changes retain the active image via in-place navigation. The full topic articles are currently English; their language picker links to the selected localized homepage.

## Checks and release
Run `python tools/check-seo.py` after building. It checks pages without JavaScript, unique titles/descriptions, H1 count, internal assets/links, default tool modes and JSON-LD. A temporary-domain build also checks canonical/hreflang reciprocity and sitemap membership, then is discarded.

The private ChatGPT preview is for review and is not a publicly crawlable production deployment. Public indexing additionally needs a public host, correct domain configuration, a successful sitemap submission in Search Console and time for crawling. Changes here do not guarantee ranking or indexing.

## Research references
- https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
