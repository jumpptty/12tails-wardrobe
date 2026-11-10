"""Wait until the account's weekly usage reaches a threshold, then exit (user 2026-11-10: "how to make you stop
automatically when this number reaches 98%?"). Run in the background while a workflow runs; when it exits, Claude stops
the workflow (TaskStop) and resumes it after the reset (Workflow resumeFromRunId).
Reads Anthropic's usage endpoint (the numbers /usage and the banner show) with the saved Claude login; the token is
sent only there and never printed (the user allowed this, 2026-11-10).
  py -3 -I pipeline/usage_watch.py [threshold=98] [every_seconds=300]
  py -3 -I pipeline/usage_watch.py --once      prints the current weekly % and the reset time"""
import json, os, sys, time, urllib.request


def weekly():
    p = os.path.join(os.environ["USERPROFILE"], ".claude", ".credentials.json")
    tok = json.load(open(p, encoding="utf-8"))["claudeAiOauth"]["accessToken"]   # re-read: the login refreshes it
    req = urllib.request.Request("https://api.anthropic.com/api/oauth/usage", headers={
        "Authorization": f"Bearer {tok}", "anthropic-beta": "oauth-2025-04-20", "User-Agent": "claude-code"})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode())["seven_day"]
    return float(d["utilization"]), d["resets_at"]


if __name__ == "__main__":
    if "--once" in sys.argv:
        print("weekly %.1f%%, resets %s" % weekly())
        sys.exit(0)
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else 98.0
    every = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    # The endpoint rate-limits hard (2026-11-10: every 60 s check got 429 "Retry-After: 0" for an hour, so the guard was
    # blind): back off on failure (doubling, up to 15 min), say so once it has been blind 30 min, log each success.
    wait, blind_since, warned = every, None, False
    while True:
        try:
            pct, resets = weekly()
            if pct >= limit:
                print(f"REACHED: weekly {pct:.1f}% >= {limit:g}% (resets {resets})", flush=True)
                sys.exit(0)
            print(f"{time.strftime('%H:%M')} weekly {pct:.1f}%", flush=True)
            wait, blind_since, warned = every, None, False
        except Exception as e:      # a network blip or the rate limit: try again later, never stop the work on it
            blind_since = blind_since or time.time()
            print(f"{time.strftime('%H:%M')} check failed: {e}", flush=True)
            if not warned and time.time() - blind_since >= 1800:
                print("BLIND: no successful check for 30 min", flush=True)
                warned = True
            wait = min(wait * 2, 900.0)
        time.sleep(wait)
