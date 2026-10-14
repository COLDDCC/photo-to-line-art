# Design direction

TasteSkill v2 (`design-taste-frontend`) was installed using the publisher's CLI and applied to the existing public page.

Direction: **The page is the object**. Seed: **1543781543**.

## Brief and inventory
International photo-to-hatching converter; browser-local images; no account; no watermark; selected single snow peak photograph; two genuine renderers; pale cyan sky; unprinted snow; blue cross-hatched regions; PNG up to 2000 pixels; six languages; separate artist collection.

## Argument and proof
- Convert photos into line-based artwork: show the real original beside its generated result in the first screen.
- Two rendering choices are meaningfully different: show actual outputs of both algorithms on the same source photo.
- The workflow is simple: describe the actual upload, adjustment and download steps.
- Human-made art is distinct: a separate collection section, with no invented sales links or artworks.
- State limits plainly: local processing, image sizes, hatching versus outlines.

## Idea and interaction
On this page, the selected snow photograph and its unprinted snow regions become a pair of paper proofs on a shared artboard. The live interaction is the genuine converter with mode, density, width and contrast controls.

## Decisions
Preserve the approved ivory ground, blue ink, actual photo and existing algorithms. Native CSS; one system font. Rewrite accumulated style overrides into a single token-based stylesheet. Use flat tonal surfaces, readable type and square buttons. Keep basic controls visible and move secondary controls into a native disclosure. Below the editor, alternate artwork proofs, a paper workflow slip, artist notes and open FAQ text.

The dealt hospitality-style striped hero, large empty footer and automatic image crossfade conflict with the explicit compact first-screen editor and stable original/result comparison. They were adapted to a working paper artboard rather than introducing decorative stripes, a full-viewport footer or changing the user's photo. No new stock images or invented proof were introduced. The user-selected photo is preserved; its original photographer/license remain unverified in PHOTO-CREDIT.md.

## Verification
- TasteSkill source lint: zero failures, zero warnings.
- JavaScript syntax, localization-key coverage and selected-photograph rendering checked.
- The full TasteSkill browser inspector and screenshot-based rubric were not run: this environment does not expose the supported browser QA capability. No visual score is claimed.
- The artist's name, collection photos and purchase destination still await real content.
