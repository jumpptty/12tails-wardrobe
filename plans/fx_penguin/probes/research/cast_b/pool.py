"""Writes pool.json (the cue entries in plans/fx_penguin/cast_b.md) next to this file and checks it: valid JSON, cue
times in order, known kinds. Read only otherwise.
  py -3 -I checks/fx_penguin_research/cast_b/pool.py"""
import json, os

CE = [0.4, "fx", "castEffect", {"d": 1, "y": 1}]
W = {}
W["iceBlock"] = (
    "Penguin.cs RPC_iceBlock_cast (:31432-32090; RPC_cast1 starts it when the bar ends, :20516-20522; isDoubleSpell :19707): "
    "Double Spell #431 on (passives on; one roll per play: roll doubleSpell): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % "
    "as the bar completes (:20108-20126; luck ignored), a proc draws multiCast at the hero (createEffect :20132-20138; plays its own "
    "Sounds/trippleCast) and adds multiCast Lv 1 (:20144), which tints the hero (0.48, 0.29, 0.78) (CharacterControl.cs:38470-38477) "
    "until Ice Block spends it at 0.4 s (:31594-31611; the tint is left out, as Blink's: plans/fx_penguin/own_skills.md question 3); clip cast3 cut (PlayAnimation(cast3, 0) "
    ":31779) and voice iceBlock1 / iceBlock2 (Random.Range(0, 2) :31830-31874, PlayOneShot :32036-32039) at 0; Yield 0.4 (:32034): "
    "castEffect (the Penguin prefab's castEffect field = Resources penguin/effects/castEffect) 1 m ahead 1 m up (TransformDirection(0, 1, 1) "
    ":31589; plays its own Sounds/castEffect); mBlockCount = sLv + sLv x multiCastLv = 2, 4 on a proc (:31618); each block raycast down to "
    "the ground 1.5 m ahead (:31958, :31985, :31668), RPC_iceBlock_fire: iceBlock, LookRotation(hero forward) (:10716-10744; NEEDS "
    "Penguin_iceBlock), life chaAdjust(6) + 6 = 12 s (:10744, Penguin_iceBlock.cs:51; destroyed with no fade :116-120; CHA ignored): the "
    "centre at 0.4, then Yield 0.1 (:32017) and per i = 1..mBlockCount the right block +1.5 i m, Yield 0.05 (:32023), the left one "
    "-1.5 i m, Yield 0.05 (:32032): 0.5 / 0.55, 0.6 / 0.65, on a proc also 0.7 / 0.75, 0.8 / 0.85; standby when i = mBlockCount + 1 "
    "(:31899-31918): 0.7 s (0.9 on a proc); each block plays its own Sounds/iceBlock; the blocks' ice slow on enemies "
    "(Penguin_iceBlock.cs:169) draws nothing")
ice = [[0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
       [0, "voice", "iceBlock1|iceBlock2"], CE, [0.4, "fx", "iceBlock", {"d": 1.5, "kill": 12}]]
t = 0.5
for i in (1, 2, 3, 4):
    o = {"p": 0.12, "roll": "doubleSpell"} if i > 2 else {}
    ice.append([round(t, 2), "fx", "iceBlock", {"d": 1.5, "x": 1.5 * i, "kill": 12, **o}])
    ice.append([round(t + 0.05, 2), "fx", "iceBlock", {"d": 1.5, "x": -1.5 * i, "kill": 12, **o}])
    t += 0.1

W["snowMan"] = (
    "Penguin.cs RPC_snowMan_cast (:32095-32630, enemy target; the target point 10 m ahead): clip cast3 cut (:32445) and voice snowman1 / "
    "snowman2 at 0 (Random.Range(0, 2) :32486; BB loads Voices/snowMan1 / snowMan2 :32496, :32527, the rip's files are voices/snowman1 / "
    "snowman2, the spelling TTO loads, pseudo/Penguin.c:21195-21196; PlayOneShot :32563, :32576); Yield 0.4 (:32574): castEffect 1 m ahead "
    "1 m up (:32252; plays Sounds/castEffect); snowMan_ring on the target at its feet, the target's rotation (tChar.createEffect "
    ":32313-32331; plays its own Sounds/snowMan); the snowMan status, Lv 2, getDebuff(2 + 4 x 2 = 10 s, CHA vs CHA; CHA ignored) "
    "(:32345-32350): the target's renderers hidden and Effects/snowMan at its feet (CharacterControl.cs:38650-38711); Penguin_snowMan "
    "turns it to the target's rotation, keeps scale 1 for a target 1 m tall or less (Penguin_snowMan.cs:45-63), follows it and destroys "
    "itself when the status ends (:110-129; it has no fields and draws nothing); the target taken as a Penguin-sized enemy facing the hero "
    "(rot 180); Yield 0.4 (:32585): standby 0.8 s (:32377)")
snow = [[0, "voice", "snowman1|snowman2"], CE, [0.4, "fx", "snowMan_ring", {"d": 10, "rot": [0, 180, 0]}],
        [0.4, "fx", "snowMan", {"d": 10, "rot": [0, 180, 0], "kill": 10}]]

W["tornado"] = (
    "Penguin.cs RPC_tornado_cast (:32631-33182; with Typhoon #344 learned it is cast only with no enemy locked: RPC_cast1 :20597-20648, "
    "getTyphoonLv :11123-11126): clip cast3 cut (:32904) and voice tornado1 / tornado2 (Random.Range(0, 2) :32955-32999, PlayOneShot "
    ":33126, :33129) at 0; Yield 0.4 (:33122): castEffect 1 m ahead 1 m up (:32788; plays Sounds/castEffect); the spot getSpawnPos(position "
    "+ (1 + sLv) x forward) = 4 m ahead at sLv 3 (:32804); RPC_tornado_fire (:32821): tornado_ring there, identity (:10851-10869; "
    "EffectControl life 3, plays its own Sounds/cyclone_create) and tornado3 (sLv 3, :10963-10987; NEEDS Penguin_tornado: Init velocity "
    "5 x hero forward, drag 2, Penguin_tornado.cs:98-103, unsteered it slides about 2.4 m, to 6.4 m ahead, "
    "checks/fx_penguin_research/cast_b/storm_sim.py; its own looping Sounds/cyclone), Ice Twister #443 on (:11029); channel chaAdjust(6) = "
    "6 s (:32839): the hero holds the attack state, turning to the storm every frame (:33093-33120), and at 0.4 + 6 = 6.4 s "
    "RPC_tornado_destroy (:33046-33052): standby (:11079) and the storm's onDestroy: destroy clip, Yield 0.4, Destroy (:11106; "
    "Penguin_tornado.cs:928-940, :898): cut 6.4, gone at 6.8 (kill 6.4 after its spawn); left out: tornado_hit and Ice Twister's frost "
    "on enemies the storm meets (Penguin_tornado.cs:266-361), on an enemy with no target-point analogue (no enemy is locked, or the cast "
    "would be Typhoon)")
torn = [[0, "voice", "tornado1|tornado2"], CE, [0.4, "fx", "tornado_ring", {"d": 4}],
        [0.4, "fx", "tornado3", {"d": 4, "cut": 6.4, "kill": 6.4}]]

W["typhoon"] = (
    "Penguin.cs RPC_typhoon_cast (:33183-33644; Tornado cast with an enemy locked and Typhoon #344 learned, passives on: RPC_cast1 "
    ":20597-20626): clip cast3 cut (:33466) and voice typhoon1 / typhoon2 (Random.Range(0, 2) :33507-33548, PlayOneShot :33598, :33601) "
    "at 0; Yield 0.4 (:33587): castEffect 1 m ahead 1 m up (:33340; plays Sounds/castEffect); getSpawnPos(position + (1 + sLv) x forward) "
    "= 4 m ahead at sLv 3 (:33353), RPC_typhoon_fire (:33358): typhoon3 there, identity (:11236-11260; NEEDS Penguin_typhoon; its own "
    "looping Sounds/cyclone, fading in to 0.6, Penguin_typhoon.cs:330, :472), Init(owner, damage, HP talAdjust(300), life chaAdjust(6) = 6, "
    "the target, Ice Twister #443) (:11299-11311): launched rotateH(5 x owner forward, (tID - 1) x 120 deg) with drag 2 "
    "(Penguin_typhoon.cs:848-853; tID is the target's actor number, APPROXIMATED as 1: straight ahead), pushed with force 11 - 3 = 8 at "
    "the target, the 10 m point: to (:356-372); its life is set at Init (:772), so at 0.4 + 6 = 6.4 s Update starts onDestroy "
    "(:81, :270-287): destroy clip, Yield 0.4, Destroy (:1111-1126; Penguin.cs:11360-11378): cut 6.4 here is that life end (the hero "
    "went to standby at 0.8 s and the typhoon does not watch her), gone at 6.8 (kill 6.4 after its spawn); its HP pool talAdjust(300), "
    "drained by the damage it deals (:205, :93), is not modelled (APPROXIMATED: it depends on the enemy's DEF; on a 0-DEF target it "
    "would end after 11 hits); Yield 0.4 (:33596): standby 0.8 s (:33398); left out: every 0.35 s (:110-118) tornado_hit at each "
    "struck enemy's collider centre (:168-183, Penguin.cs:10789-10812) and Ice Twister's 9 % frost on it (:210-238, "
    "CharacterControl.cs:38733-38757): on the struck enemy, as the Sheep's divinityAxe_hit")
ty = [[0, "voice", "typhoon1|typhoon2"], CE, [0.4, "fx", "typhoon3", {"d": 4, "to": [0, 0, 10], "cut": 6.4, "kill": 6.4}]]

W["absoluteZero"] = (
    "Penguin.cs RPC_absoluteZero_cast (:33645-34221, enemy target; the target point 10 m ahead): clip cast3 cut (:34019) and voice "
    "absoluteZero1 / absoluteZero2 (Random.Range(0, 2) :34060-34115) at 0; Yield 0.4 (:34164): castEffect 1 m ahead 1 m up (:33802; plays "
    "Sounds/castEffect); absoluteZero at the target's feet, Quaternion.identity (:33838-33856; drawn in the hero's facing, APPROXIMATED; "
    "AlphaTimer + ShatterMesh, FX/Phoenix; plays its own Sounds/absoluteZero); Yield 0.4 (:34168): standby 0.8 s (:33951); left out: the "
    "ice status's blue tint of the target's body (Lv 4, getDebuff(12), :33903; CharacterControl.cs:38600-38610), on an enemy with no "
    "target-point analogue (no body there); the player's camera colour ramp iceRamp (:33919-33924), a camera effect as the Wolf's were")
az = [[0, "voice", "absoluteZero1|absoluteZero2"], CE, [0.4, "fx", "absoluteZero", {"d": 10}]]

W["blizzard"] = (
    "Penguin.cs RPC_blizzard_cast (:34222-34893, enemy target; the target point 10 m ahead): clip cast3 with a 0.2 s fade "
    "(PlayAnimation(cast3, 0.2) :34675; the Cast tile's step is a cut) and voice blizzard1 / blizzard2 (Random.Range(0, 2) :34716-34771) "
    "at 0; Yield 0.4 (:34820): castEffect 1 m ahead 1 m up (:34380; plays Sounds/castEffect); blizzard on the target at its feet, the "
    "hero's rotation (tChar.createEffect :34424-34442; EffectControl life 6 + afterLife 1, followPosition, its own looping Sounds/blizzard); "
    "six 1 s ticks (i < 6 :34527, Yield 1 :34815, i++ :34467) at 0.4 ... 5.4 s hit every enemy within 12 m but the target "
    "(:34566-34605); at i = 6, 0.4 + 6 x 1 = 6.4 s: standby (:34499), the blizzard left to end on its own 6 s life (it is destroyed only "
    "when the channel is cut short, :34625-34631); left out: the hits (no visual of their own), on enemies near the target with no "
    "target-point analogue; the player's camera motion blur (:34385-34396), a camera effect as the Wolf's were")
bz = [[0, "voice", "blizzard1|blizzard2"], CE, [0.4, "fx", "blizzard", {"d": 10}]]

W["snowBall"] = (
    "Penguin.cs RPC_snowBall_cast (:38064-38589, an enemy target that must be a snowman: 'Can only cast on snowman' :38307; the target "
    "point 10 m ahead): the snowman a Snow Man left there stands at 0 (as the Sheep's seal fields show the seals they need) and goes when "
    "the snowBall status removes snowMan at 0.4 s (CharacterControl.cs:38847; Penguin_snowMan.cs:110-129); clip cast3 cut (:38403) and "
    "voice snowBall1 / snowBall2 (Random.Range(0, 2) :38444-38485, PlayOneShot :38523, :38541) at 0; Yield 0.4 (:38535): castEffect 1 m "
    "ahead 1 m up (:38210; plays Sounds/castEffect); snowBall_cast on the target at its feet, its rotation (tChar.createEffect "
    ":38247-38265; no sound); the snowBall status with the snowman's level and time left (:38287-38298; getStatusTime = the time left, "
    "CharacterControl.cs:19278): the snowman's 10 s less the 1.5 s from its status (Snow Man's 0.4 s) to this one (Snow Man's standby "
    "0.8 s + Snow Ball's cast1 0.7 s + 0.4 s) = 8.5, cut to 8 by the int; snowBall at the target's feet, identity, parented, scale height "
    "+ 0.2 = 1.2 for a Penguin-sized target (CharacterControl.cs:38886-38916; StaticMesh); the status ends at 0.4 + 8 = 8.4 s: "
    "snowBallFx destroyed and snowBall_break at the target's feet, identity (CharacterControl.cs:17558-17580); Yield 0.4 (:38547): "
    "standby 0.8 s (:38335); left out: the shield's burst when damage breaks it, needs an attacker")
sb = [[0, "fx", "snowMan", {"d": 10, "rot": [0, 180, 0], "kill": 0.4}], [0, "voice", "snowBall1|snowBall2"], CE,
      [0.4, "fx", "snowBall_cast", {"d": 10, "rot": [0, 180, 0]}], [0.4, "fx", "snowBall", {"d": 10, "scale": 1.2, "kill": 8}],
      [8.4, "fx", "snowBall_break", {"d": 10}]]

W["cosmicRift"] = (
    "Penguin.cs RPC_cosmicRift_cast (:38590-39061, a self-buff): clip cast3 cut (:38888) and voice cosmicRift1 / cosmicRift2 "
    "(Random.Range(0, 2) :38929-38970, PlayOneShot :39016, :39024) at 0; Yield 0.4 (:39022): castEffect 1 m ahead 1 m up (:38725; plays "
    "Sounds/castEffect) and cosmicRift_ring at the hero (createEffect :38730-38748; followState: cut at the 0.8 s standby; plays its own "
    "Sounds/cosmicRift_ring); Yield 0.2 (:39031): at 0.6 s RPC_AddStatus(cosmicRift, 5, chaAdjust(12) = 12 s; CHA ignored) (:38793): every "
    "Diffuse renderer of the hero gets FX/CosmicRift with its own texture, every other renderer hidden (CharacterControl.cs:38952-39006; "
    "NOT cued: a hero material swap, no effect prefab; plans/fx_penguin/cast_b.md question 2), and cosmicRift at the hero, identity (:39011-39020; followState: cut at 0.8; plays its own "
    "Sounds/cosmicRift); Yield 0.2 (:39014): standby 0.8 s (:38820); the status ends at 0.6 + 12 = 12.6 s: the hero's renderers back to "
    "Diffuse (colour 0.86) and shown (CharacterControl.cs:17605-17671) and cosmicRift again at the hero (:17676-17683)")
cr = [[0, "voice", "cosmicRift1|cosmicRift2"], CE, [0.4, "fx", "cosmicRift_ring", {"cut": 0.8}],
      [0.6, "fx", "cosmicRift", {"cut": 0.8}], [12.6, "fx", "cosmicRift"]]

FRI_CAST3 = (
    "Penguin.cs RPC_cosmicFriday_cast (:39062-39700; RPC_cast1 starts it when the bar ends, :20859-20869): clip cast3 cut "
    "(PlayAnimation(cast3, 0) :39555) and voice cosmicFriday1 / cosmicFriday2 (Random.Range(0, 2) :39596-39637, PlayOneShot :39673, "
    ":39680) at 0; Yield 0.4 (:39691): the cosmicFriday clip cuts in (:39203), its entry has the rest")
FRI = (
    "Penguin.cs RPC_cosmicFriday_cast case 2, 0.4 s into cast3 (Yield 0.4 :39691), times from this clip: PlayAnimation(cosmicFriday, 0) "
    "looped (:39203-39208); castEffect 1 m ahead 1 m up (:39198; plays Sounds/castEffect); cosmicFriday_ring at the hero (createEffect "
    ":39213-39231; followState, ends on its life 1 + 1 s first; plays its own Sounds/cosmicFriday_ring); cosmicFriday at the hero, "
    "InitCosmicFriday (:39250-39279; NEEDS Penguin_cosmicFriday: create clip, Yield 0.5, root looped, following the hero, "
    "Penguin_cosmicFriday.cs:60, :330-406; its own looping Sounds/cosmicFriday); the channel (Yield WaitForFixedUpdate :39678) runs until "
    "the player moves or MP < 25 (:39341-39381), the tile's 6 s: three ticks at 0, 2, 4 s (mUpdateTime + 2 :39387-39395; MP 20 with "
    "Revised Magic #414 :39400) each put cosmicFriday (5, 3 s) on everyone of her layer within 3 m, herself included "
    "(FindAreaTarget(her position, 3, 3, 1 << her layer) :39405-39449, no self-exclusion), whose look is Cosmic Rift's FX/CosmicRift skin "
    "(CharacterControl.cs:39047-39114; NOT cued: a hero material swap, question 2), refreshed until 4 + 3 = 7 s; at 6 s the channel ends: "
    "DestroyCosmicFriday (:39464-39470: destroy clip, Yield 0.5, Destroy, Penguin_cosmicFriday.cs:529-580; cut 6, gone at 6.5) and "
    "standby (:39494); left out: the cosmicFriday status on allies (no allies)")

pool = {
    "cast3": {"why": "(the editor's merge line: cast_a's members + these 8, one per play at even chance; Cosmic Friday has its own tile)",
              "skills": {k: {"why": W[k], "cues": c} for k, c in [
                  ("iceBlock", ice), ("snowMan", snow), ("tornado", torn), ("typhoon", ty), ("absoluteZero", az),
                  ("blizzard", bz), ("snowBall", sb), ("cosmicRift", cr)]}},
    "@CosmicFriday:cast3": {"why": FRI_CAST3, "cues": [[0, "voice", "cosmicFriday1|cosmicFriday2"]]},
    "cosmicFriday": {"why": FRI, "cues": [[0, "fx", "castEffect", {"d": 1, "y": 1}], [0, "fx", "cosmicFriday_ring"],
                                          [0, "fx", "cosmicFriday", {"cut": 6, "kill": 6.5}]]},
}

if __name__ == "__main__":
    entries = list(pool["cast3"]["skills"].values()) + [pool["@CosmicFriday:cast3"], pool["cosmicFriday"]]
    for e in entries:
        ts = [c[0] for c in e["cues"]]
        assert ts == sorted(ts), ts
        for c in e["cues"]:
            assert c[1] in ("fx", "voice", "sound") and isinstance(c[2], str), c
    s = json.dumps(pool, ensure_ascii=False, indent=2)
    json.loads(s)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool.json"), "w", encoding="utf-8").write(s)
    print("ok", {k: len(v["cues"]) for k, v in pool["cast3"]["skills"].items()}, len(pool["cosmicFriday"]["cues"]))
