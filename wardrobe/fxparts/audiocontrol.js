// wardrobe/fxparts/audiocontrol.js: AudioControl, the game's volume envelope on an effect's AudioSource (2026-11-13, the
// Bat: plans/fx_bat/parts.md part 5 and its Verification, skills_a.md Parts 2). Generic: the Bat's nefariousWhip_hit is
// the only cued user so far; the Mole, Monkey, Panda and Whale each have one effect with it.
//
// AudioControl.cs (BB DecompiledSource; the opaque predicates read by hand, every `continue` dead, the `break`s live):
// - fields (:233-248, 6 floats = 24 bytes): minVolume, maxVolume, delay, fadein, middle, fadeout (wardrobe_fx.py LAYOUTS)
// - Start (:38-110): no AudioSource -> "Audio is missing", the component off. Its clock starts (Time.time); delay > 0 ->
//   playOnAwake off and Stop(); volume = minVolume when fadein > 0, else maxVolume.
// - Update (:112-215), t from Start: t < delay -> min; else fadein > 0 and t < delay + fadein -> Lerp(min, max, (t -
//   delay) / fadein) and Play() when not playing (the only Play: the clip starts from its beginning there); else middle >
//   0 and t < ... + middle -> max; else fadeout > 0 and t < ... + fadeout -> Lerp(max, min, ...); else min. So with a
//   delay and no fadein the sound never plays again (kept as the game does it).
// nefariousWhip_hit (min 0, max 1, delay 0.5, fadein 0.5, middle 4, fadeout 0.2; its loop `nefariousWhip`): silent to
// 0.5 s, the loop starts there and rises to 1 by 1.0 s, holds to 5.0 s, falls to 0 by 5.2 s, then plays on silently
// until the effect goes (EffectControl life 5 + afterLife 5 = 10 s).
//
// The page: the node's AudioSource handle is index.html's fx.sounds entry { node, comp, h } (parts.md Interfaces 2; every
// AudioSource the Fx started, loop or not), else its fx.loops entry { node, h } (the looping ones). A playOnAwake-off
// source has no handle: the part starts it itself at Play(). The new handle goes into both entries, so Fx.dispose (and
// the sound button's stop, fx.loops) stops it; the part's own dispose stops it too (harmless twice). The clock is the
// effect's age (the Fx is built at age 0, Start's frame). APPROXIMATED: Play() is made on the first frame at or after
// the delay even if a long frame jumped past the fade-in (the game would miss it: a frame longer than 0.5 s).
export default function register(api) {
  api.part("AudioControl", (fx, node, c, mat, nodeDef) => {
    const src = nodeDef?.comps?.find(x => x.type === "AudioSource");
    if (!src) { console.warn("AudioControl: Audio is missing", fx.name, node.name); return null; }   // Start's own error, the component off
    const num = x => (Number.isFinite(+x) ? +x : 0);
    const min = num(c.minVolume), max = num(c.maxVolume), delay = num(c.delay), fadein = num(c.fadein), middle = num(c.middle), fadeout = num(c.fadeout);
    // the AudioSource's handle; looked up at build (the extractor keeps the components' order, AudioSource first) and
    // once more at the first update, in case a node lists AudioControl before its AudioSource
    let entry = null, loopEntry = null, h = null, playing = false, first = true;
    const put = nh => { h = nh; if (entry) entry.h = nh; if (loopEntry) loopEntry.h = nh; };
    const find = () => {
      entry = fx.sounds?.find(s => s.node === node && (!s.comp || s.comp === src)) || null;
      loopEntry = fx.loops?.find(l => l.node === node) || null;
      h = entry?.h || loopEntry?.h || null;       // the AudioSource Fx started (playOnAwake), or null
      if (delay > 0 && h) { h.stop(); put(null); }   // playOnAwake = false; Stop()
      playing = !!h;
      h?.setVolume(fadein > 0 ? min : max);       // Start's volume
    };
    find();
    const lerp = (a, b, u) => a + (b - a) * Math.min(1, Math.max(0, u));   // Mathf.Lerp clamps u
    const volume = t => {
      if (t < delay) return min;
      if (fadein > 0 && t < delay + fadein) return lerp(min, max, (t - delay) / fadein);
      if (middle > 0 && t < delay + fadein + middle) return max;
      if (fadeout > 0 && t < delay + fadein + middle + fadeout) return lerp(max, min, (t - delay - fadein - middle) / fadeout);
      return min;
    };
    return { node,
      update() {
        if (first) { first = false; if (!h && !entry && !loopEntry) find(); }
        const t = fx.age, v = volume(t);
        // Play(): only inside the fade-in phase's branch, from the clip's beginning, at the volume of this frame
        if (!playing && fadein > 0 && t >= delay) { playing = true; put(api.Sound.play(fx.cls, src.clip, v, !!src.loop)); }
        h?.setVolume(v);
      },
      dispose() { h?.stop(); } };
  });
}
