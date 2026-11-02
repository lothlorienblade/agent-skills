# Prompting the image generator

## Aspect ratio

Choose the aspect ratio from where the image will be used and state it in the prompt. Never rely on the default, which is a square.

| Destination | Aspect ratio |
| --- | --- |
| Sprite, icon, tile, item, avatar | `square 1:1` |
| Desktop screen background, scene, cover, slide | `landscape 16:9` or `landscape 3:2` |
| Phone screen, poster, character portrait, card art | `portrait 9:16` or `portrait 2:3` |
| Banner, strip, panorama | Wide, but at most `3:1`: the generator does not support narrower strips. Generate at 3:1 and crop |

When the destination has exact pixel dimensions (a game viewport, a UI slot), generate at the closest supported ratio and crop and scale to the exact size afterwards. Exact pixel sizes in the prompt are ignored: a request for 512×512 came back as 1254×1254.

## Prompt structure

Put the parts in this order, one short sentence or phrase each:

1. **Asset and purpose**: "Game sprite of a pickup item for a top-down snake arcade game".
2. **Subject**: what exactly is shown, with the details that matter.
3. **Style**: "glossy cartoon", "flat vector-like illustration", "pixel art, 32×32 grid look", "painterly concept art".
4. **View and composition**: "top-down 3/4 view", "centered, filling about 80% of the frame", "subject on the left third".
5. **Lighting and palette**: "soft top-left light", "warm sunset palette", "limited palette of 5 colors".
6. **Background and format**: "transparent background", "square 1:1".
7. **Exclusions**: "no text, no watermark, no drop shadow on the background".

## Recipes

**Sprite or item**

```text
Game sprite of a red apple pickup for a top-down snake arcade game. Glossy cartoon style, top-down 3/4 view,
centered and filling about 80% of the frame, soft top-left light, clean edges. Transparent background, square 1:1.
No text, no shadow on the background.
```

**Seamless texture**

```text
Seamless tileable texture of short green grass seen from directly above, for a 2D game ground tile. Even lighting,
no visible light direction, no large features near the edges. Square 1:1. No text.
```

Check the seams afterwards by placing four copies side by side.

**Screen background**

```text
Main menu background for a cozy arcade game: a misty pine forest at dusk, painterly style, soft purple and orange
palette, large calm area in the center for the menu buttons, landscape 16:9. No text, no characters.
```

**App icon**

```text
App icon of a stylized fox head, flat geometric style with subtle gradients, centered on a rounded square with a
deep blue background, bold silhouette readable at small sizes, square 1:1. No text.
```

## A set that must match

When several images must look like one set (the skins of a game, a family of icons):

1. Generate the most characteristic piece first and get the user's approval.
2. Pass it with `--reference` to every next call, and repeat the shared style words in each prompt.
3. Name the invariants explicitly: "same palette, same outline thickness, same light direction as the reference".

## Revising a result

Change one thing per attempt and say what must stay the same: "Same apple as before, but make the leaf larger; keep the colors, angle, and lighting." Pass the previous image as a reference.
