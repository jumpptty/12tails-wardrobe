// One coroutine's readable flow (clip calls, waits, time checks, state changes; junk predicates dropped): the order a
// skill plays its clips in. node pipeline/clip_flow.js D:/12tails/DecompiledSource/Sheep.cs RPC_holyLight ["extra|regex"]
const fs = require("fs");
const [file, name, extra] = process.argv.slice(2);
const L = fs.readFileSync(file, "utf8").split(/\r?\n/);
const start = L.findIndex(s => new RegExp(`internal sealed class \\$${name}\\$\\d+ : GenericGenerator`).test(s));
if (start < 0) { console.log("not found"); process.exit(1); }
let end = L.findIndex((s, i) => i > start && /internal sealed class \$\w+\$\d+ : GenericGenerator/.test(s));
if (end < 0) end = L.length;
const keep = new RegExp(["case \\d+:", "IL_[0-9A-F]+:", "Yield", "WaitForSeconds", "Time\\.time [<>]", "PlayAnimation", "animation\\.(Play|CrossFade)",
  "actionState = ", "myCommand = ", "wrapMode", "\\.speed =", "addTimeOut", "hasSkill", "getSkillLv", "Random", extra].filter(Boolean).join("|"));
for (let i = start; i < end; i++) {
  const s = L[i];
  if (/if \(-?\d+ - -?\d+ [!=]= -?\d+\)/.test(s)) continue;
  if (keep.test(s)) console.log(`${i + 1}: ${s.trim().slice(0, 170)}`);
}
