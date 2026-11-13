---
name: reskin-from-image
description: Use before and during any skin / reskin / repaint work on a 12 Tails hero after a reference image. Locks design decisions to what the reference image shows, with no identification or lookup of the reference character.
---

# Reskin from the image only

The user (2026-11-13): restrict knowledge of the reference character so there are "absolutely no biases when making
modeling design decisions".

## Rules, for the whole skin task

1. **Don't identify the reference.** Don't work out, guess or say who or what the character is, or what it comes from.
   Refer to it only as "the reference" (or the file name the user gave).
2. **No lookups.** No web search, fetch or image search about the reference, its name, franchise or "official" look.
   Not in subagents either: a subagent's brief gets these same rules and only the image, never a character name.
3. **The image is the only source.** Colours, shapes, materials, patterns, proportions and details come from what is
   visible in the image. Sample colours from the pixels; don't recall them.
4. **Unseen parts** (the back, the soles, a hidden side): decide from the image's own style and palette, and tell the
   user which parts were invented and why. Never fill them in from memory of the character.
5. **Recognising it anyway?** If a name or outside fact comes to mind, ignore it: don't write it down, don't use it,
   and don't let it settle a choice the image leaves open. If a choice can only be settled by outside knowledge, ask
   the user instead.
6. **Write-ups stay clean.** Plans, NOTES.md entries, file names, commit messages and replies describe what is seen
   ("red cape with a gold trim"), never the character's name or source.

## Which equipment sets may be the base

Only these five per class, until the user adds more (user 2026-11-13: "From now on equipment sets are limited to just
these 5 unless I add them later"): **60 = `royal`**, **70 = `legend`**, **`summer`**, **Halloween (Original) = `hallow`**
(BB's; not TTO's `halloween`), and the class's **bug set** (bat butterfly, bison beetle, cat dragonfly, chameleon
mantis, mole bee, monkey spider, panda worm, penguin mosquito, rabbit ant, sheep moth, whale ladyBug, wolf scorpion).
A set = the outfit and its own head piece, weapons and trinket. Never ToT's student set. Shortlist with
`pipeline/wardrobe_outfit_sheet.py <cls> <png> royal legend summer hallow <bug>`.

## Checks that came from mistakes (2026-11-13: the Whale, the Cat)

1. **(Props only now: see 6.) Never hide a piece (alpha 0) on a guess.** Bodies have real openings under straps, coats, buckles and bibs (the
   Whale's coat: no body under it; the Cat's braces: an open shoulder and an open spot on the shorts' back). First run
   `wardrobe_repaint.island_shots(cls, outfit, K, cache, out, cut=[the piece's sheet points])` and look at all eight
   sides: the backdrop or an inside seen through the body = keep that part and paint it as what should be there
   (the braces' ends became the shirt's shoulder and the shorts' waist; only their middle is cut).
2. **A user's "it is still broken" = reproduce it from their angle before fixing again.** The Cat's hollow shoulder was
   "fixed" twice on a wrong guess (a "cap sleeve" that was the chest's pink emblem) before the island render showed
   the cause.
3. **Don't pick texels by the original's colour alone** (pink caught the top's emblem, front and back). Pick by
   island and body position, and print the count and the 3D bounding box of a mask before using it (0 texels and
   24,000 texels were both wrong and both printed).
4. **Four yaws are not enough.** Check eight, and ask the user to look from above and below in the live view (the
   shots turn only round the hero).
5. **Eyes: ask for or use a close-up.** Eyes drawn from a small full-body picture come out generic. A closed-eye face
   preset (one stroke per eye: the Cat's 4 and 5) is the base: its stroke is the upper lid, the eye is painted under
   it on the skin (the user's idea). Match the close-up's lid weight, iris colours, pupil shape, lashes, cheek marks.
6. **An outfit cannot hide anything: not in the game, and (since 2026-11-13) not in the wardrobe.** The game writes the
   worn outfit into an RGB24 texture and draws it with plain `Diffuse` (`<Class>Equipment.cs`), so alpha is thrown
   away and the colour under it shows; the page now does the same (`outfitCut`). A part the design does not want
   (a strap, a shield, a buckle) must be **painted** as what would be there (the shirt under the strap, the skin
   under the shield), never set to alpha 0. Props are different: each follows its own game material (some cut out).
   `wardrobe_repaint.paint_under(out, M, piece, under)` does it (each texel takes the nearest texel of the islands
   under it), last in the painter; it cannot work on texels shared by several copies of a piece (the Whale's
   banknotes): design those instead. Every outfit painter asserts its skin is fully opaque before saving.
7. **Skin and whites come out cooler and pinker under the page's light** than their hex: compare the render's
   pixels with the reference's sample, not the ramp's numbers.

8. **A 3D model as the reference (an in-game enemy): paint part by part, never project the whole model.** A
   whole-model projection (every texel takes the nearest point of the reference) was dropped by the user (2026-11-13:
   "it opens up for a lot of mistake"): hair on the face, bands on a dress, ragged hems. Use
   `pipeline/wardrobe_enemy_ref.py` (the enemy's mesh + eight-side sheet) and `pipeline/wardrobe_borrow.py`: `same_uv`
   first (parts with the enemy's own layout are copied texel for texel), the outfit's own paint in the enemy's palette
   where the shapes differ, `borrow(dst, src)` only between parts named by hand, reading the printed distances (over
   ~3 cm: look, or paint it instead). Left and right: check with `same_uv`, not by eye (a mirrored fit gives ~0 % on
   the face and ears). `pipeline/wardrobe_bat_enemies.py` is the worked example.
9. **Before promising a one-sided detail (one sleeve, one glove), test the mesh:** arms, legs, coats and wings usually
   read the same texels on both sides (count the triangles over one texel and their y: the Bat's summer arms gave
   +0.37 and -0.37). Then mock the options side by side. A piece worn on the other side than the reference
   (a hip cloth) is read at the mirror place (`borrow(flip=True)`). A piece standing off the body (a strap, a rose) is
   never reached by a nearest-point borrow: lay it on by hand (`Job.lay`, a decal).
   The reference's own parts can be mirrored too (an enemy's helmet held only its y >= 0 half: the band came out
   "only half"): read such a part with `absy=True`. Parts that hang differently from the reference's (a coat over
   her dress) are read by view (`borrow(view=1 | -1)` from the front / back, `axis=1` from the side), not by nearest
   point on the body.
10. **A head piece or weapon that only stands in for something (a crown for a rose) is a guess to say out loud**, not
    to slip in: say why it was picked and what it fails at, or paint the detail on the outfit instead.

11. **Don't force the reference onto a part built for something else** (user 2026-11-13: "too forced ... don't force it,
    just use other designs that respect the model there"). Where the outfit's shapes match the reference's (skin-tight
    parts, wings, a panel of similar cut), borrow. Where they don't (a capelet where she has a bare chest and cups, an
    inner dress where she has a waist disc), keep the model's own forms and ornaments in the reference's colours, and
    bring the reference's patterns as whole motifs placed on a fitting piece (a sigil on a coat panel, its border
    along the coat's edges), not as a reading stretched over the wrong shape.
12. **Fit a motif to the piece's own outline, and know that outline first** (user: "you copied the pattern with no extra
    thoughts that the actual shape of the front piece is like this"). Measure the piece (its width per height, where
    it splits or ends), lay the motif across its own width (u = position / the piece's edge there), draw borders
    along the piece's real edge (distance to the island's edge, mirror seams left out), plain cloth where the motif
    has no counterpart (tails). And when the user names a piece, show back which piece was understood (a crop) before
    a full pass: "the coat front piece" cost one round on the wrong piece.
13. **A paint that does not show up = the wrong island, not a lighting quirk.** List every island at that spot with its
    position, normal and present colour (a few lines of numpy over the texel maps) before theorising: a piece's
    front and back faces can be different islands, and a small piece can be a corner of a big island (royal's tab).
14. **Never report a detail as done from a hopeful read of a small render** ("it is subtle from the front" was "it is not
    there"). Measure it: the texture's brightness by body position over the spot, and a close-up at 2x. A soft shade
    under a piece that covers it does not show from the front: say so plainly and show the paint on its own.
15. **Skin, faces, cleavage, folds: copy the game's own painting, never construct them from lines and ramps** (user, of
    two diagonal strokes drawn as a cleavage: "why do you think a straight line is fit to represent a cleavage?").
    Lay the class's own outfit textures side by side for that body part (a front view per outfit from its texel
    maps), pick the one that paints it, and carry its light and shade over (luminance as a share of its skin, on the
    new skin colour). Geometry (borders, stripes, sigils) may be drawn; anatomy is borrowed.
16. **Before painting anatomy on a part, find out what part of the body it is, from the mesh** (user: "the position
    should be the underboob, not the upper cleavage"): print the part's forward position and how its surface faces
    (the normal's z) per height. A surface that comes forward and faces down is an underside: it takes a fold and a
    cast shade, not the detail that belongs higher up. A borrowed painting goes where that anatomy is on THIS mesh.

## Still applies

- The live view from CLAUDE.md ("Painting a skin"), opened before the first pass.
- Wide latitude on what may change (hair, skin, face, high-res), real design, not recolours; final original / new /
  reference comparison.
