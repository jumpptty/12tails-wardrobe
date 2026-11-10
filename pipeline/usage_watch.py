"""Wait until the account's weekly usage reaches a threshold, then exit (user 2026-11-10: "how to make you stop
automatically when this number reaches 98%?"). Run in the background while a workflow runs; when it exits, Claude stops
the workflow (TaskStop) and resumes it after the reset (Workflow resumeFromRunId).
Reads Anthropic's usage endpoint (the numbers /usage and the banner show) with the saved Claude login; the token is
sent only there and never printed (the user allowed this, 2026-11-10).
  py -3 -I pipeline/usage_watch.py [threshold=98] [every_seconds=60]
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
    every = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
    while True:
        try:
            pct, resets = weekly()
            if pct >= limit:
                print(f"REACHED: weekly {pct:.1f}% >= {limit:g}% (resets {resets})", flush=True)
                sys.exit(0)
        except Exception as e:      # a network blip: try again next round, never stop the work on it
            print(f"check failed: {e}", flush=True)
        time.sleep(every)
