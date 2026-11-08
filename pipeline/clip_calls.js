// Which skill clips each hero class plays, per coroutine / method, in file order, with the crossfade and a following
// wrapMode / speed change (the wardrobe's SEQ table in wardrobe/index.html came from this, 2026-11-09).
// node pipeline/clip_calls.js D:/12tails/DecompiledSource wardrobe/data [class...]
const fs = require("fs"), path = require("path");
const [src, data, ...only] = process.argv.slice(2);
const CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"];
const files = fs.readdirSync(src);
for (const cls of only.length ? only : CLASSES) {
  const clips = JSON.parse(fs.readFileSync(path.join(data, cls, "clips.json"), "utf8"));
  const skill = new Set(Object.keys(clips).filter(k => clips[k].group === "skill"));
  const mine = files.filter(f => new RegExp(`^${cls}(_[a-z].*)?\\.cs$`, "i").test(f));
  const seen = new Set();
  console.log(`\n===== ${cls}: ${skill.size} skill clips =====`);
  for (const f of mine) {
    const L = fs.readFileSync(path.join(src, f), "utf8").split(/\r?\n/);
    let cur = "(top)", out = new Map();
    for (let i = 0; i < L.length; i++) {
      const s = L[i];
      let m = s.match(/internal sealed class \$(\w+)\$\d+ : GenericGenerator/);
      if (m) { cur = m[1]; continue; }
      m = s.match(/^\t(?:public|private|internal|protected)[^(]*\s(\w+)\s*\(/);
      if (m && !/class /.test(s)) cur = m[1];
      const re = /(PlayAnimation|CrossFadeQueued|PlayQueued|CrossFade|\.Play|Blend)\("(\w+)"\s*(?:,\s*([^)]*))?\)/g;
      let c;
      while ((c = re.exec(s))) {
        const name = c[2];
        if (!skill.has(name)) continue;
        seen.add(name);
        let extra = "";
        for (let j = i + 1; j < Math.min(L.length, i + 8); j++) {
          const w = L[j].match(/wrapMode = WrapMode\.(\w+)|\["(\w+)"\]\.speed = ([^;]+)|animation\["(\w+)"\]\.time = ([^;]+)/);
          if (w) extra += " " + (w[1] ? "wrap=" + w[1] : w[2] ? `speed(${w[2]})=${w[3]}` : `time(${w[4]})=${w[5]}`);
          if (/PlayAnimation|CrossFade|\.Play\(/.test(L[j])) break;
        }
        if (!out.has(cur)) out.set(cur, []);
        out.get(cur).push(`${name}${c[3] ? "/" + c[3].replace(/\(float\)/, "") : ""}${extra}@${i + 1}`);
      }
    }
    for (const [k, v] of out) console.log(`  ${f}:${k}: ${v.join("  ")}`);
  }
  const miss = [...skill].filter(n => !seen.has(n));
  if (miss.length) console.log(`  (no call found: ${miss.join(" ")})`);
}
