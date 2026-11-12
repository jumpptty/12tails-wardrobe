"""Headless check of community skins in the page (2026-11-11, NOTES.md "community skins"). The local page with ?ttolock
(the online TTO lock) and ?submitkey=<Cloudflare's always-pass Turnstile test key>; this script's server stands in
for the data's community.json (approved skins for the Sheep's BB mothLatern and standard outfit, and one for her TTO
halloweenLantern that the page must ignore) and for the Worker's api/submit (it records what the page sends). Checks:
  - a TTO piece's menu online: no download, no upload, no "ลายจากผู้เล่น" (user 2026-11-11: "TTO upload should work only on
    private version")
  - a BB piece: one "ลายจากผู้เล่น" entry that opens the pop-up (a card: picture, credit, link; ใส่ในห้องแต่งตัว; ดาวน์โหลด;
    Esc closes)
  - wearing a community skin: one undo step, the nameplate's "ลายโดย ...", the menu's meta, the tile badge ลายผู้เล่น;
    the BB outfit's skin downloads as a PNG at the texture's size, named with its credit
  - the visitor's own skin on the BB piece, then ส่งลายนี้ให้ทีมงาน: the dialog (Turnstile renders and passes), the
    checks before sending (name, link, consent), the request (fields, the PNG at the texture's size), a refusal shown
    in the dialog, the success toast; the outfit's community skin; a phone-sized dialog
  - no page / console errors
Shots in <out>: menu.png, gallery.png, gallery_phone.png, dialog.png, dialog_phone.png. Exit 1 on any failure. Needs the internet (Turnstile's script).
  uv run --no-project --with playwright --with pillow python -I pipeline/wardrobe_community_check.py D:/12tails-wardrobe checks/<dir>"""
import asyncio, email.parser, email.policy, functools, http.server, io, json, sys, threading
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "wardrobe" / "data"
TEST_KEY = "1x00000000000000000000AA"            # Cloudflare's always-pass Turnstile site key


def webp(size, color):
    b = io.BytesIO(); Image.new("RGBA", size, color).save(b, "WEBP", lossless=True); return b.getvalue()


LANTERN_TEX = "Sheep_mothLantern.png"                # the BB mothLatern's texture
LANTERN_SIZE = Image.open(DATA / "props" / "tex" / LANTERN_TEX).size
OUTFIT_SIZE = Image.open(DATA / "sheep" / "tex" / "standard1.webp").size
def one(sid, slot, kind, item, name, link, at, tex):
    return {"id": sid, "cls": "sheep", "name": name, "link": link, "at": at, "face": None, "thumb": None,
            "pieces": [{"slot": slot, "kind": kind, "item": item, "tex": tex}]}


FAKE = {
    "/wardrobe/data/community.json": json.dumps({"sets": [
        one("900001", "R", "weapons", "mothLatern", "ทดสอบ ลายเขียว", "https://example.com/artist", "2026-11-11T00:00:00Z", {LANTERN_TEX: "community/sheep/900001_0.webp"}),
        one("900002", "outfit", "outfits", "standard", "คนที่สอง", "", "2026-11-11T00:00:01Z", {"": "community/sheep/900002_0.webp"}),
        one("900003", "R", "weapons", "halloweenLantern", "ไม่ควรเห็น", "", "2026-11-11T00:00:02Z", {"Sheep_halloweenWeapon.png": "community/sheep/900001_0.webp"}),
        # a whole look (2026-11-12): the outfit and the lantern together, a face, the character's picture
        {"id": "900010", "cls": "sheep", "name": "ชุดเต็ม", "link": "", "at": "2026-11-12T00:00:00Z", "face": 3, "thumb": "community/sheep/900010_p.webp",
         "pieces": [{"slot": "outfit", "kind": "outfits", "item": "standard", "tex": {"": "community/sheep/900010_0.webp"}},
                    {"slot": "R", "kind": "weapons", "item": "mothLatern", "tex": {LANTERN_TEX: "community/sheep/900010_1.webp"}}]}]}, ensure_ascii=False).encode(),
    "/wardrobe/data/community/sheep/900001_0.webp": webp(LANTERN_SIZE, (40, 220, 60, 255)),
    "/wardrobe/data/community/sheep/900002_0.webp": webp(OUTFIT_SIZE, (60, 90, 240, 255)),
    "/wardrobe/data/community/sheep/900010_0.webp": webp(OUTFIT_SIZE, (220, 40, 40, 255)),
    "/wardrobe/data/community/sheep/900010_1.webp": webp(LANTERN_SIZE, (240, 200, 30, 255)),
    "/wardrobe/data/community/sheep/900010_p.webp": webp((360, 480), (200, 180, 160, 255)),
}
POSTS, ANSWER = [], {"body": {"ok": True}, "status": 200}


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in FAKE:
            body = FAKE[path]
            self.send_response(200)
            self.send_header("Content-Type", "application/json" if path.endswith(".json") else "image/webp")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/wardrobe/api/submit":
            self.send_error(404); return
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
            b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + raw)
        fields = {}
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            raw_part = part.get_payload(decode=True)
            fields[name] = raw_part if part.get_filename() else raw_part.decode("utf-8")
        POSTS.append(fields)
        body = json.dumps(ANSWER["body"]).encode()
        self.send_response(ANSWER["status"]); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html?ttolock&submitkey={TEST_KEY}"
MENU = """() => { const el = document.getElementById('pmenu');
  return { open: !el.hidden, meta: el.querySelector('.pm-meta')?.innerText || '', sub: el.querySelector('.pm-sub')?.innerText || '',
    items: [...el.querySelectorAll('.pm-item')].map(b => b.dataset.a + (b.dataset.cs ? ':' + b.dataset.cs : '') + (b.disabled ? '(off)' : '')) }; }"""
SKINS = "() => [...wardrobe.debug().SKINS.entries()].map(([k, v]) => [k, v.by ? v.by.name : null, v.w, v.h])"


async def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    own = OUT.resolve() / "own_skin.png"
    Image.new("RGBA", LANTERN_SIZE, (250, 120, 0, 255)).save(own)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ctx = await b.new_context(viewport={"width": 1366, "height": 768}, accept_downloads=True)
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and "challenges.cloudflare.com" not in ((m.location or {}).get("url", ""))
                and "status of 429" not in m.text and errors.append(m.text))      # the refusal this check asks for
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("() => wardrobe.show('sheep')")
        await page.wait_for_timeout(800)

        async def tile_menu(topic, item):
            if not await page.locator(f'#pkBody .pk-cell[data-slot="{topic}"]').count():
                await page.click(f'#topics [data-t="{topic}"]')
            cell = page.locator(f'#pkBody .pk-cell[data-item="{item}"]').first      # an outfit: one tile per edition
            await cell.wait_for(state="attached"); await cell.scroll_into_view_if_needed()
            await cell.click(button="right"); await page.wait_for_timeout(250)
            return await page.evaluate(MENU)

        m = await tile_menu("R", "halloweenLantern")
        check(m["open"] and not {"png", "glb", "up", "reset", "send", "gallery"} & set(m["items"]),
              f"TTO piece online: no download / upload / community skins ({m['items']})")
        await page.keyboard.press("Escape")
        m = await tile_menu("R", "mothLatern")
        check("gallery" in m["items"] and not any(i.startswith(("cs", "link")) for i in m["items"]), f"one ลายจากผู้เล่น entry: {m['items']}")
        check(not any(i.startswith("send") for i in m["items"]), "no send action before the visitor's own skin")
        await page.screenshot(path=str(OUT.resolve() / "menu.png"))

        await page.click('#pmenu .pm-item[data-a="gallery"]')
        await page.wait_for_selector(".gal-back:not([hidden]) .gal-card")
        await page.wait_for_function("() => document.querySelector('.gal-card img')?.naturalWidth > 0", timeout=15000)
        g = await page.evaluate("""() => [...document.querySelectorAll('.gal-card')].map(c => ({ id: c.dataset.cs, by: c.querySelector('.gal-by').innerText,
          link: c.querySelector('a.gal-link')?.href || null, rel: c.querySelector('a.gal-link')?.rel || null,
          wear: c.querySelector('[data-a="wear"]').innerText, dl: c.querySelector('[data-a="dl"]').disabled }))""")
        # the lantern's skins: the single one and the lantern of the whole look (each piece of a set is offered on its own here)
        check(g == [{"id": "900001#0", "by": "ลายโดย ทดสอบ ลายเขียว", "link": "https://example.com/artist", "rel": "noopener noreferrer",
                     "wear": "ใส่ในห้องแต่งตัว", "dl": False},
                    {"id": "900010#1", "by": "ลายโดย ชุดเต็ม", "link": None, "rel": None, "wear": "ใส่ในห้องแต่งตัว", "dl": False}], f"the pop-up's cards: {g}")
        await page.screenshot(path=str(OUT.resolve() / "gallery.png"))
        await page.keyboard.press("Escape")
        check(await page.locator(".gal-back").is_hidden(), "Esc closes the pop-up")
        await tile_menu("R", "mothLatern")
        await page.click('#pmenu .pm-item[data-a="gallery"]')
        await page.click('.gal-card [data-a="wear"]')
        await page.wait_for_function("() => wardrobe.debug().SKINS.size === 1", timeout=15000)
        check(await page.locator(".gal-back").is_hidden(), "ใส่ในห้องแต่งตัว closes the pop-up")
        sk = await page.evaluate(SKINS)
        check(sk[0][1] == "ทดสอบ ลายเขียว" and tuple(sk[0][2:]) == LANTERN_SIZE, f"community skin on: {sk}")
        check((await page.evaluate("() => wardrobe.debug().C.state.R")) == "mothLatern", "it put the piece on")
        plate = await page.evaluate("() => document.getElementById('plateSub').innerText")
        check("ลายโดย ทดสอบ ลายเขียว" in plate, f"nameplate credit: {plate!r}")
        badge = await page.locator('#pkBody .pk-cell[data-item="mothLatern"] .sk-badge').inner_text()
        check(badge == "ลายผู้เล่น", f"tile badge: {badge!r}")
        m = await tile_menu("R", "mothLatern")
        check("ลายโดย ทดสอบ ลายเขียว" in m["meta"] and "reset" in m["items"], f"menu after: {m['meta']!r}")
        await page.click('#pmenu .pm-item[data-a="gallery"]')
        w = await page.evaluate("() => { const b = document.querySelector('.gal-card [data-a=\"wear\"]'); return [b.innerText, b.disabled, document.querySelector('.gal-card').classList.contains('on')]; }")
        check(w == ["ใส่อยู่", True, True], f"the worn card says ใส่อยู่: {w}")
        await page.keyboard.press("Escape")
        await page.click("#undo"); await page.wait_for_timeout(600)
        check((await page.evaluate(SKINS)) == [], "undo takes it off")

        # the visitor's own skin on the TTO piece, then send it
        await tile_menu("R", "mothLatern")
        async with page.expect_file_chooser() as fc:
            await page.locator('#pmenu .pm-item[data-a="up"]').click()
        await (await fc.value).set_files(str(own))
        await page.wait_for_function("() => wardrobe.debug().SKINS.size === 1", timeout=15000)
        check((await page.evaluate(SKINS))[0][1] is None, "own skin on the BB piece")
        m = await tile_menu("R", "mothLatern")
        check("send" in m["items"], f"send offered: {m['items']}")
        await page.click('#pmenu .pm-item[data-a="send"]')
        await page.wait_for_selector(".send-back:not([hidden]) form.send")
        dlg = page.locator("form.send")
        await dlg.locator('button[type="submit"]').click()
        check(await page.locator(".send-msg").inner_text() == "กรอกชื่อที่จะให้เครดิตก่อน", "no name: asks for it")
        await dlg.locator('input[name="name"]').fill("ผู้ทดสอบ")
        await dlg.locator('input[name="link"]').fill("http://plain.example")
        await dlg.locator('button[type="submit"]').click()
        check(await page.locator(".send-msg").inner_text() == "ลิงก์ต้องขึ้นต้นด้วย https://", "http link refused")
        await dlg.locator('input[name="link"]').fill("https://example.com/me")
        await dlg.locator('button[type="submit"]').click()
        check(await page.locator(".send-msg").inner_text() == "ติ๊กช่องยินยอมก่อนส่ง", "consent asked")
        await dlg.locator('input[name="consent"]').check()
        try:
            await page.wait_for_function("() => document.querySelector('.send-ts input[name=\"cf-turnstile-response\"]')?.value", timeout=30000)
            check(True, "Turnstile rendered and passed (test key)")
        except Exception:
            check(False, "Turnstile rendered and passed (test key)")
        await page.screenshot(path=str(OUT.resolve() / "dialog.png"))
        TOKEN = "() => document.querySelector('.send-ts input[name=\"cf-turnstile-response\"]')?.value || ''"
        first = await page.evaluate(TOKEN)
        ANSWER.update(body={"ok": False, "error": "rate"}, status=429)
        await dlg.locator('button[type="submit"]').click()
        await page.wait_for_function("() => document.querySelector('.send-msg')?.innerText", timeout=15000)
        msg = await page.locator(".send-msg").inner_text()
        check(msg == "ส่งถี่เกินไป รอสักครู่แล้วลองใหม่", f"a refusal shows in the dialog: {msg!r} (requests {len(POSTS)}, errors {errors})")
        ANSWER.update(body={"ok": True}, status=200)
        # a refused send resets the widget (a token works once): wait for a new one
        await page.wait_for_function("() => wardrobe.debug().Send.token", timeout=30000)
        await page.wait_for_timeout(300)
        msg = await page.locator(".send-msg").inner_text()     # the live site wiped it here (2026-11-12): the new token's callback
        check(msg == "ส่งถี่เกินไป รอสักครู่แล้วลองใหม่", f"the refusal stays after the widget passes again: {msg!r}")
        await dlg.locator('button[type="submit"]').click()
        await page.wait_for_selector(".send-back:not(.gal-back)", state="hidden", timeout=15000)
        t = await page.evaluate("() => document.getElementById('toast').textContent")
        check("ส่งลายแล้ว" in t, f"success toast: {t!r}")
        f = POSTS[-1] if POSTS else {}
        got = {k: f.get(k) for k in ("cls", "name", "link", "consent")}
        pieces = json.loads(f.get("pieces") or "[]")
        check(got == {"cls": "sheep", "name": "ผู้ทดสอบ", "link": "https://example.com/me", "consent": "1"} and f.get("token")
              and pieces == [{"slot": "R", "kind": "weapons", "item": "mothLatern", "textures": [{"tex": LANTERN_TEX, "field": "f0"}]}],
              f"the request: {got} {pieces}")
        size = Image.open(io.BytesIO(f["f0"])).size if f.get("f0") else None
        check(size == LANTERN_SIZE, f"the PNG sent is the texture's size: {size}")
        check((f.get("preview") or b"")[:3] == b"\xff\xd8\xff" and f.get("face", "").isdigit(), f"the character's picture (JPEG) and the face: {len(f.get('preview') or b'')} bytes, face {f.get('face')!r}")
        check(len(POSTS) == 2, f"two requests (the refused one, the sent one): {len(POSTS)}")

        # the outfit's community skin
        await page.click("#pkClose"); await page.wait_for_timeout(300)
        m = await tile_menu("outfit", "standard")
        check("gallery" in m["items"], "outfit: the ลายจากผู้เล่น entry")
        await page.click('#pmenu .pm-item[data-a="gallery"]')
        await page.wait_for_selector(".gal-back:not([hidden]) .gal-card")
        check(await page.locator(".gal-card").first.locator(".gal-link").count() == 0, "no link: no line for it")
        async with page.expect_download() as d:
            await page.click('.gal-card [data-a="dl"]')
        dl = await d.value
        path = OUT.resolve() / "community_download.png"; await dl.save_as(str(path))
        check(dl.suggested_filename == "12tails_แกะ_Standard_ลายโดยคนที่สอง.png" and Image.open(path).size == OUTFIT_SIZE,
              f"BB outfit: ดาวน์โหลด saves {dl.suggested_filename} {Image.open(path).size}")
        await page.click('.gal-card [data-a="wear"]'); await page.wait_for_timeout(1500)
        plate = await page.evaluate("() => document.getElementById('plateSub').innerText")
        check("คนที่สอง" in plate, f"outfit skin credited: {plate!r}")

        # ---- whole looks (2026-11-12): the toolbar's ลายผู้เล่น, ลองทั้งชุด, several files at once, ส่งลุคนี้
        await page.click("#pkClose"); await page.wait_for_timeout(300)
        STATE = "() => { const d = wardrobe.debug(); return { outfit: d.C.state.outfit, R: d.C.state.R, face: d.C.state.face, skins: [...d.SKINS.entries()].map(([k, v]) => [k.split('|').slice(1, 3).join('|'), v.by ? v.by.setId : null]).sort() }; }"
        n = await page.locator("#cmN").inner_text()
        check(n == "3", f"the toolbar counts this class's sets (the TTO-only one left out): {n!r}")
        await page.click("#cm")
        await page.wait_for_selector(".gal-back:not([hidden]) .send.gal.sets .gal-card")
        await page.wait_for_function("() => [...document.querySelectorAll('.sets .gal-card img')].every(i => i.naturalWidth > 0)", timeout=15000)
        cards = await page.evaluate("""() => [...document.querySelectorAll('.sets .gal-card')].map(c => ({ id: c.dataset.set,
          n: c.querySelector('.gal-n').innerText, thumb: c.querySelector('img').classList.contains('thumb'), wear: c.querySelector('[data-a="wear"]').innerText }))""")
        check([c["id"] for c in cards] == ["900010", "900002", "900001"] and cards[0]["n"] == "2 ชิ้น" and cards[0]["thumb"] and not cards[1]["thumb"],
              f"set cards, newest first, the look's picture as its thumbnail: {cards}")
        check(cards[1]["wear"] == "ใส่อยู่", f"the worn set says so: {cards[1]}")
        await page.screenshot(path=str(OUT.resolve() / "sets.png"))
        before = await page.evaluate(STATE)
        await page.click('.sets .gal-card[data-set="900010"] [data-a="wear"]')
        await page.wait_for_function("() => [...wardrobe.debug().SKINS.values()].filter(v => v.by?.setId === '900010').length === 2", timeout=15000)
        after = await page.evaluate(STATE)
        check(await page.locator(".gal-back:not([hidden])").count() == 0, "ลองทั้งชุด closes the pop-up")
        check(after["outfit"] == "standard" and after["R"] == "mothLatern" and after["face"] == 3
              and after["skins"] == [["outfits|standard", "900010"], ["weapons|mothLatern", "900010"]], f"one click: both pieces, their skins, the set's face: {after}")
        await page.click("#undo"); await page.wait_for_timeout(800)
        check(await page.evaluate(STATE) == before, f"one undo step takes the whole look off: {await page.evaluate(STATE)}")
        await page.click("#redo"); await page.wait_for_timeout(800)
        await page.evaluate("() => wardrobe.debug().setCommunity({ skins: [{ id: '1', cls: 'sheep', kind: 'weapons', item: 'mothLatern', name: 'x', link: '', at: '1', tex: {} }] })")
        legacy = await page.evaluate("() => wardrobe.debug().SETS.map(s => [s.id, s.pieces[0].slot, s.pieces.length])")
        check(legacy[0] == ["1", "R", 1] and {s[0] for s in legacy[1:]} == {t["id"] for t in json.loads((DATA / "team_sets.json").read_text("utf-8"))["sets"]},
              f"the first format's skins read as sets of one; the team's sets (team_sets.json) come along: {legacy}")
        await page.evaluate(f"() => wardrobe.debug().setCommunity({FAKE['/wardrobe/data/community.json'].decode()})")

        # several files dropped at once: each to the piece its name says (the names this page gives a download), one undo step
        await page.evaluate("() => wardrobe.setOutfit('standard', 1)")
        await page.click("#undo"); await page.wait_for_timeout(300)        # back to a look without the set (whatever undo gives)
        await page.evaluate("() => { const d = wardrobe.debug(); d.SKINS.clear(); }")
        dropped = await page.evaluate(f"""async () => {{
          const mk = async (w, h, rgb, name) => {{ const c = new OffscreenCanvas(w, h), g = c.getContext('2d'); g.fillStyle = rgb; g.fillRect(0, 0, w, h);
            return new File([await c.convertToBlob({{ type: 'image/png' }})], name, {{ type: 'image/png' }}); }};
          const files = [await mk({OUTFIT_SIZE[0]}, {OUTFIT_SIZE[1]}, '#2a8', '12tails_แกะ_Standard_สี1.png'),
                         await mk({LANTERN_SIZE[0]}, {LANTERN_SIZE[1]}, '#a2f', '12tails_แกะ_Moth Latern_ลายของคุณ (1).png'),
                         await mk(8, 8, '#000', 'holiday photo.png')];
          const n = wardrobe.debug().C ? 0 : 0; await wardrobe.debug().dropMany(files);
          return document.getElementById('toast').textContent; }}""")
        st = await page.evaluate(STATE)
        check(st["skins"] == [["outfits|standard", None], ["weapons|mothLatern", None]] and st["R"] == "mothLatern",
              f"dropped files went to their pieces (the lantern put on): {st} / {dropped!r}")
        check("ไม่รู้จัก 1 ไฟล์" in dropped and "holiday photo.png" in dropped, f"the file with an unknown name is reported: {dropped!r}")
        check(await page.locator("#sendlook").is_visible(), "ส่งลุคนี้ shows once own skins are worn")
        undo_n = await page.evaluate("() => document.getElementById('undo').disabled")
        await page.click("#undo"); await page.wait_for_timeout(800)
        st2 = await page.evaluate(STATE)
        check(not undo_n and st2["skins"] == [], f"one undo step takes every dropped skin off: {st2}")
        await page.click("#redo"); await page.wait_for_timeout(800)

        # ส่งลุคนี้: every worn piece with an own skin, each can be left out; one request
        await page.click("#sendlook")
        await page.wait_for_selector(".send-back:not([hidden]) form.send.look")
        rows = await page.evaluate("() => [...document.querySelectorAll('.look-row')].map(r => r.innerText.split('\\n')[0])")
        check(len(rows) == 2, f"the look lists both pieces: {rows}")
        await page.wait_for_function("() => document.querySelector('.look-pv img')?.naturalWidth > 0", timeout=10000)
        await page.screenshot(path=str(OUT.resolve() / "look_dialog.png"))
        dlg = page.locator("form.send.look")
        await dlg.locator('input[name="name"]').fill("ผู้ส่งชุด")
        await dlg.locator('input[name="link"]').fill("")
        await dlg.locator('input[name="consent"]').check()
        await page.wait_for_function("() => wardrobe.debug().Send.token", timeout=30000)
        n0 = len(POSTS)
        await dlg.locator('button[type="submit"]').click()
        await page.wait_for_selector("form.send.look", state="detached", timeout=15000)
        f = POSTS[-1] if len(POSTS) > n0 else {}
        pieces = json.loads(f.get("pieces") or "[]")
        sizes = [Image.open(io.BytesIO(f[t["field"]])).size for p in pieces for t in p["textures"] if f.get(t["field"])]
        check([(p["slot"], p["item"]) for p in pieces] == [("outfit", "standard"), ("R", "mothLatern")] and sizes == [OUTFIT_SIZE, LANTERN_SIZE],
              f"one request with the whole look: {[(p['slot'], p['item']) for p in pieces]} {sizes}")
        t = await page.evaluate("() => document.getElementById('toast').textContent")
        check("ส่งชุดลาย 2 ชิ้นแล้ว" in t, f"the look's toast: {t!r}")

        # a phone-sized dialog and pop-up
        pp = await (await b.new_context(viewport={"width": 390, "height": 700}, is_mobile=True, has_touch=True)).new_page()
        pp.on("pageerror", lambda e: errors.append("phone: " + str(e)))
        await pp.goto(URL)
        await pp.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await pp.evaluate("() => wardrobe.show('sheep', { R: 'mothLatern' })")
        await pp.evaluate("""async () => { const { SKINS, C } = wardrobe.debug(); const w = 4, h = 4;
          SKINS.set(`${C.cls}|weapons|mothLatern|Sheep_mothLantern.png`, { w, h, data: new Uint8ClampedArray(w * h * 4).fill(200) }); }""")
        await pp.click('#topics [data-t="R"]'); await pp.wait_for_selector("#pkBody .pk-cell")
        await pp.evaluate("""() => { const c = document.querySelector('#pkBody .pk-cell[data-item="mothLatern"]');
          c.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, clientX: 50, clientY: 600 })); }""")
        await pp.wait_for_timeout(300)
        if await pp.locator('#pmenu .pm-item[data-a="send"]').count():
            await pp.locator('#pmenu .pm-item[data-a="send"]').click()
            await pp.wait_for_selector("form.send"); await pp.wait_for_timeout(1500)
            r = await pp.evaluate("() => { const r = document.querySelector('form.send').getBoundingClientRect(); return [r.left, r.right, r.top, r.bottom, innerWidth, innerHeight]; }")
            check(r[0] >= 0 and r[1] <= r[4] and r[2] >= 0 and r[3] <= r[5], f"phone dialog inside the screen: {r}")
            await pp.screenshot(path=str(OUT.resolve() / "dialog_phone.png"))
            await pp.keyboard.press("Escape")
            await pp.evaluate("""() => { const c = document.querySelector('#pkBody .pk-cell[data-item="mothLatern"]');
              c.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, clientX: 50, clientY: 600 })); }""")
            await pp.wait_for_timeout(300)
            await pp.locator('#pmenu .pm-item[data-a="gallery"]').click()
            await pp.wait_for_selector(".gal-back:not([hidden]) .gal-card"); await pp.wait_for_timeout(800)
            r = await pp.evaluate("() => { const r = document.querySelector('.send.gal').getBoundingClientRect(); return [r.left, r.right, r.top, r.bottom, innerWidth, innerHeight]; }")
            check(r[0] >= 0 and r[1] <= r[4] and r[2] >= 0 and r[3] <= r[5], f"phone pop-up inside the screen: {r}")
            await pp.screenshot(path=str(OUT.resolve() / "gallery_phone.png"))
        else:
            check(False, "phone: the send action")
        await b.close()
    check(not errors, f"no page / console errors {errors}")
    print("FAILED: " + "; ".join(fails) if fails else "all ok")
    sys.exit(1 if fails else 0)


asyncio.run(main())
