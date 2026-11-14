"""Nickname looks on the picker tiles, side by side (2026-11-14; user: "see nicknamed items from the class guide in the
bible hub ... sort them first at the top for the wardrobe"). A throwaway mock for the user's pick: the real page, the
Rabbit's weapon and outfit pickers, the nicknamed tiles moved to the top and labelled one way per look (the nicknames
from the Bible's GEAR_NICKNAMES, mapped by the item codes in icons.json). Writes <out>/<look>_<topic>.png and
<out>/compare.html. Exit 1 on a page error.
  uv run --no-project --with playwright python -I pipeline/wardrobe_nick_mocks.py D:/12tails-wardrobe checks/nick_mocks"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
# the Rabbit's nicknamed tiles (data-p / data-o + data-e -> the Bible's nickname), as the map would give them
NICK = {
    "R": {"legendGun": "70 ดล", "legendGunR": "70 ดด", "royalGun": "60 ดล", "royalGunR": "60 ดด", "timeShotgun": "วุธไทม์",
          "championGun": "วุธแชมป์", "pvpBow": "วุธ RP", "pvpBowR": "วุธ RP", "poseidonGun": "วุธดันน้ำ",
          "frozenGun": "วุธแข็ง", "specialGun": "วุธพิเศษ", "spainMusket": "แฟ 65", "antShotgun": "แมลง ดล",
          "antShotgunR": "แมลง ดด", "magistrateGunV": "48 ดด", "standardGunV": "12 ดด", "bdWeapon": "วุธ BD"},
    "outfit": {"legend|": "70 ดล", "legend|R": "70 ดด", "royal|": "60 ดล", "royal|R": "60 ดด", "champion|": "ชุดแชมป์",
               "pvpArmor|": "ชุด RP", "pvpArmor|R": "ชุด RP", "spain|": "แฟ 65", "ant|": "แมลง ดล", "ant|R": "แมลง ดด",
               "magistrate|V": "48 ดด", "standard|V": "12 ดด"},
}
LOOKS = {
    "order": "เรียงขึ้นก่อนอย่างเดียว ไม่แสดงชื่อเล่น",
    "swap": "ชื่อเล่นแทนชื่อ ชื่อเดิมตัวเล็กข้างใต้ (แบบไบเบิล)",
    "chip": "ป้ายชื่อเล่นสีทองบนมุมรูป",
    "line": "ชื่อเดิม + ชื่อเล่นสีทองบรรทัดใต้",
}
CSS = """
.pk-item.is-nick { border-color: color-mix(in srgb, var(--gold) 55%, var(--line)); background: var(--weave), color-mix(in srgb, var(--gold) 8%, var(--panel)); }
.pk-item .nk-chip { position: absolute; left: 6px; top: 6px; padding: 2px 6px 3px; border-radius: 4px; background: var(--gold); color: var(--gold-ink);
  font: 600 11.5px/1.25 system-ui, sans-serif; z-index: 2; white-space: nowrap; }
.pk-item .lbl.nk-main { color: var(--gold); font-weight: 600; font-size: 13px; }
.pk-item .nk-sub { display: block; font-size: 10.5px; line-height: 1.25; color: var(--muted); max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pk-item .nk-line { display: block; font-size: 12px; font-weight: 600; line-height: 1.3; color: var(--gold); }
"""
APPLY = """([topic, look, nick]) => {
  const body = document.getElementById("pkBody"), cells = [...body.children];
  const key = el => { const b = el.querySelector(".pk-item") || el; return topic === "R" ? b.dataset.p : (b.dataset.o != null ? b.dataset.o + "|" + b.dataset.e : null); };
  const named = cells.filter(c => nick[key(c)] != null);
  const order = Object.keys(nick);
  named.sort((a, b) => order.indexOf(key(a)) - order.indexOf(key(b)));
  const first = cells.find(c => !(c.querySelector(".pk-item") || c).dataset.p === "" ) ;
  const lead = topic === "R" ? cells.find(c => (c.querySelector(".pk-item") || c).dataset.p === "") : null;
  for (const c of named.reverse()) body.insertBefore(c, lead ? lead.nextSibling : body.firstChild);
  for (const c of named) {
    const b = c.querySelector(".pk-item") || c, lbl = b.querySelector(".lbl"), n = nick[key(c)];
    if (look === "order") continue;
    b.classList.add("is-nick");
    if (look === "swap") { const old = lbl.innerHTML; lbl.classList.add("nk-main"); lbl.textContent = n; lbl.insertAdjacentHTML("afterend", `<span class="nk-sub">${old}</span>`); }
    if (look === "chip") b.querySelector(".pic").insertAdjacentHTML("beforeend", `<span class="nk-chip">${n}</span>`);
    if (look === "line") lbl.insertAdjacentHTML("afterend", `<span class="nk-line">${n}</span>`);
  }
  body.scrollTop = 0;
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"


async def main():
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=180000)
        await page.evaluate("() => wardrobe.show('rabbit', {})")
        await page.add_style_tag(content=CSS)
        for topic in ("R", "outfit"):
            for look in LOOKS:
                await page.evaluate("() => document.getElementById('pkClose').click()")
                await page.click(f'button[data-t="{topic}"]')
                await page.wait_for_selector("#pkBody .pk-item")
                await page.wait_for_timeout(1500)                 # the icons
                await page.evaluate(APPLY, [topic, look, NICK[topic]])
                await page.wait_for_timeout(400)
                await page.locator("#picker").screenshot(path=str(OUT / f"{look}_{topic}.png"))
        await b.close()
    rows = "".join(f"<section><h2>{k}: {v}</h2><div>" + "".join(f'<img src="{k}_{t}.png">' for t in ("R", "outfit")) + "</div></section>"
                   for k, v in LOOKS.items())
    (OUT / "compare.html").write_text("<!doctype html><meta charset=utf-8><title>Nickname looks</title><style>body{background:#111;color:#eee;"
                                      "font:15px system-ui;margin:16px}section{margin:0 0 28px}img{max-width:49%;margin-right:1%;vertical-align:top;"
                                      "border:1px solid #333}</style>" + rows, encoding="utf-8")
    print("\n".join(errors) or "no page errors")
    return 1 if errors else 0


sys.exit(asyncio.run(main()))
