"""One-off: apply the 2026-11-10 Sheep edits to pipeline/wardrobe_fx_tto.py (each anchor must match exactly once)."""
p = "pipeline/wardrobe_fx_tto.py"
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''  hands mats[0] to the part)
"""''', '''  hands mats[0] to the part)
- meshes (2026-11-10, the Sheep's Codex book and its shards / prism shells): a MeshFilter with a mesh also gets a
  {"type": "StaticMesh", <mesh>} after it (wardrobe/fxparts/mesh.js draws it with the node's MeshRenderer materials); a
  ParticleSystemRenderer's m_Mesh (mesh render mode) carries its geometry inline as "mesh": <mesh>; <mesh> = the BB
  build's shape (pipeline/wardrobe_fx_mesh.py mesh_dict: name, verts, pos, nrm, uv, col, idx, sub). A Mesh reference
  anywhere else is written {"mesh": name}
- Unity 5.5+'s TrailRenderer (its LineParameters: widthCurve, colorGradient, ...) is written as type
  "TrailRendererModern", so wardrobe/fxparts/trail.js (Unity 3.5's layout, BB's) never misreads it; tto_sheep.js draws it
  and LineRenderer. Both lose the shadow / light-probe / ray-tracing plumbing, as MeshRenderer does
- a material whose shader is not one of Unity's legacy particle shaders also carries "props": its floats and colours by
  name (TTO's own TTO/Sheep/* shaders, Standard, Particles/Standard Unlit: tto_sheep.js reads them)
- CODE_MOVERS: a prefab the game's code moves every frame gets that code as a component of its own at the head of the
  root's comps ({"type": "Sheep.BreathFly"}: the coroutine, not a script in the prefab; tto_sheep.js runs it)
- sounds: BB's rip WAV of the clip's name, else TTO's own AudioClip from the bundle (FMOD through UnityPy)
"""''')

rep('''MB_HEADER = {''', '''# the shadow / lightmap / probe / ray-tracing plumbing of a Line- or TrailRenderer (unlit lines never read it)
RENDERER_PLUMBING = ("m_CastShadows", "m_ReceiveShadows", "m_DynamicOccludee", "m_StaticShadowCaster", "m_MotionVectors",
                     "m_LightProbe", "m_ReflectionProbe", "m_RayTrac", "m_SmallMeshCulling", "m_ForceMeshLod",
                     "m_MeshLodSelectionBias", "m_RenderingLayerMask", "m_Lightmap", "m_StaticBatch", "m_ProbeAnchor")
# prefabs the game's code moves every frame (not a script in the prefab): the code becomes the root's first component,
# so the page runs it before the prefab's own parts each frame (wardrobe/fxparts/tto_sheep.js)
CODE_MOVERS = {
    # TTO1102:Sheep.<BreathFly>d__261::MoveNext@0x1E72EA0: mouth -> the revived ally's chest on an up-arc, then Destroy 0.3
    "gleamingBreath_wisp": "Sheep.BreathFly",
    # TTO1102:Sheep.<CodexOpen>d__265::MoveNext@0x1E73940: the book's drop and bob (CodexBob@0x1E55980), its FlipPivot
    # page turns (CodexFlipAngle@0x1E55A00) before each of the ten reads, Destroy(book, 0.1) after the last
    "grandCodex_book": "Sheep.CodexOpen",
}
MB_HEADER = {''')

rep('''        self.sounds = set()''',
    '''        self.sounds = {}         # clip name -> its AudioClip object (TTO's own, used when BB's rip has no such WAV)''')
rep('''            b.sounds.add(n)
            return n''', '''            b.sounds.setdefault(n, o)
            return n
        if ty == "Mesh":                       # geometry is exported where it is drawn (MeshFilter, mesh particles)
            return {"mesh": o.read_typetree().get("m_Name")}''')
rep('''        # not exported (a Mesh: none of the Wolf's TTO effects names one, every MeshFilter's m_Mesh is null, the
        # scripts build their meshes at run time); say so, so the next class's run shows what needs writing''',
    '''        # not exported; say so, so the next class's run shows what needs writing''')

rep('''        self.mats[n] = {"blend": SHADER_BLEND.get(shn, "shader:" + shn), "tex": tex, "scale": scale, "offset": offset,
                        "tint": colors.get("_TintColor"), "color": colors.get("_Color")}
        return n''', '''        self.mats[n] = {"blend": SHADER_BLEND.get(shn, "shader:" + shn), "tex": tex, "scale": scale, "offset": offset,
                        "tint": colors.get("_TintColor"), "color": colors.get("_Color")}
        if not shn.startswith("Legacy Shaders/"):  # TTO's own shaders, Standard, Particles/Standard Unlit: every number
            self.mats[n]["props"] = {**{k: num(v) for k, v in props["m_Floats"]}, **colors}
        return n''')

rep('''            entry = {"type": ty, **{k: safe(co, v) for k, v in t.items() if k not in DROP}}
            if ty == "ParticleSystem":''', '''            entry = {"type": ty, **{k: safe(co, v) for k, v in t.items() if k not in DROP}}
            if ty in ("MeshFilter", "ParticleSystemRenderer"):
                mo = tto.deref(co.assets_file, t["m_Mesh"]) if (t.get("m_Mesh") or {}).get("m_PathID") else None
                md = mesh().mesh_dict(mo.read()) if mo is not None else None
                if md and md["verts"]:
                    if ty == "ParticleSystemRenderer":
                        entry["mesh"] = md
                    else:
                        node["comps"] += [entry, {"type": "StaticMesh", **md}]
                        continue
            if ty in ("LineRenderer", "TrailRenderer"):
                entry = {k: v for k, v in entry.items() if not k.startswith(RENDERER_PLUMBING)}
                if ty == "TrailRenderer" and "m_Parameters" in t:
                    entry["type"] = "TrailRendererModern"
            if ty == "ParticleSystem":''')

rep('''            node["comps"].append(entry)
    return {"nodes": nodes}''', '''            node["comps"].append(entry)
    if name in CODE_MOVERS:
        nodes[0]["comps"].insert(0, {"type": CODE_MOVERS[name]})
    return {"nodes": nodes}''')

rep('''_bb = None
''', '''_bb = None
_mesh = None


def mesh():
    """pipeline/wardrobe_fx_mesh.py (mesh_dict: the BB build's mesh shape)."""
    global _mesh
    if _mesh is None:
        _mesh = load_path("wardrobe_fx_mesh", os.path.join(HERE, "wardrobe_fx_mesh.py"))
    return _mesh
''')

rep('''    missing = []
    for n in sorted(b.sounds):
        src = bb().rip_wav(a.cls, n)
        if not src:
            missing.append(n); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, n + ".mp3")], check=True)''',
    '''    missing, own = [], []
    for n in sorted(b.sounds):
        src = bb().rip_wav(a.cls, n)
        if not src:                            # a TTO-only clip: its own samples (UnityPy decodes them with FMOD)
            try:
                wav = next(iter(b.sounds[n].read().samples.values()))
            except Exception as e:
                print(f"warning: sound {n}: {e!r}", file=sys.stderr)
                missing.append(n); continue
            src = os.path.join(sdir, f"_{n}.wav")
            open(src, "wb").write(wav)
            own.append(n)
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, n + ".mp3")], check=True)
        if n in own:
            os.remove(src)''')
rep('''    json.dump(merged, open(out, "w", encoding="utf-8"), indent=1)''',
    '''    json.dump(merged, open(out, "w", encoding="utf-8"), separators=(",", ":"))   # compact, as wardrobe_fx.py writes it''')
rep('''          f"{len(b.sounds) - len(missing)} sounds" + (f", missing sounds: {missing}" if missing else ""))''',
    '''          f"{len(b.sounds) - len(missing)} sounds" + (f" ({len(own)} TTO's own: {own})" if own else "")
          + (f", missing sounds: {missing}" if missing else ""))''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
