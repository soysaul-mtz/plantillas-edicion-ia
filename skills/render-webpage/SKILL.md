---
name: render-webpage
description: Read the real content of a web page that WebFetch can't see because it's rendered client-side with JavaScript (React/Vue/Next.js SPA, ClickFunnels/Kajabi/Systeme.io-style landing/funnel/registration pages, page builders). Use this whenever WebFetch returns only a `<title>` or a near-empty body, whenever the user says a link "won't load" / "the page is blank" / "solo ves el título", or proactively for any landing page, funnel, checkout, or registration page before assuming the content isn't accessible. Renders the page with a real installed browser in headless mode and extracts full text plus a full-page screenshot — no new browser download required.
---

# Reading JavaScript-rendered pages

WebFetch converts raw HTML to markdown but never executes JavaScript. Most modern landing
pages, funnel builders, and SPA frameworks render their entire body via client-side JS, so
WebFetch (and plain `curl`) only see an empty `<body>` and whatever's in `<title>`/meta tags.
This is a hard limitation of that tool, not a sign the content is unreachable — a real
browser still renders it fine.

**Don't give up and ask the user for a screenshot until you've tried this first.** Screenshots
are a fine fallback when this doesn't work (some sites block automation, require login, etc.)
but this approach gets full text (better for exact copy/pricing/quotes) and works
non-interactively.

## How it works

Launch a real, already-installed Chromium-based browser (Chrome, Opera, Brave, Edge, Vivaldi,
Chromium) in headless mode via `playwright-core` — the lightweight driver package with no
bundled browser download (~1 package, installs in seconds, vs. Playwright's normal ~300MB
Chromium download). Pointing it at a browser the user already has installed means this works
immediately on any machine with a mainstream browser, no large download, no extra disk usage
left behind.

## Steps

1. **Find an installed Chromium-based browser.** Check common locations, in order of
   likelihood (adjust for the OS if not macOS):
   ```bash
   for p in \
     "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     "/Applications/Opera.app/Contents/MacOS/Opera" \
     "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
     "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
     "/Applications/Vivaldi.app/Contents/MacOS/Vivaldi" \
     "/Applications/Chromium.app/Contents/MacOS/Chromium" \
     /usr/bin/google-chrome /usr/bin/google-chrome-stable /usr/bin/chromium /usr/bin/chromium-browser /usr/local/bin/chromium; do
     [ -x "$p" ] && echo "$p"
   done
   ```
   Firefox/Safari don't work here (Playwright's CDP-based `chromium.launch` needs a
   Chromium-family binary) — skip them even if found, and fall back to the screenshot method
   if none of the above exist.

2. **`playwright-core` is already bundled with this skill** (installed once at
   `~/.claude/skills/render-webpage/node_modules`) — nothing to install per use. If it's ever
   missing (fresh machine, skill copied elsewhere), install it in the skill's own directory so
   the script's `node_modules` resolution finds it, not in the user's project:
   ```bash
   cd ~/.claude/skills/render-webpage && npm init -y >/dev/null 2>&1 && npm install playwright-core
   ```

3. **Run the bundled script** against the URL, writing output to a scratch path (e.g.
   `/tmp/render-webpage/<name>`):
   ```bash
   mkdir -p /tmp/render-webpage
   node ~/.claude/skills/render-webpage/scripts/fetch.mjs "<url>" "/tmp/render-webpage/<name>" "<executablePath>"
   ```
   - 2nd arg — the output prefix; the script writes `<prefix>.txt` (full visible text) and
     `<prefix>.png` (full-page screenshot).
   - 3rd arg — the browser path found in step 1.

4. **Read `<outPrefix>.txt` first** — it's usually enough (headings, prices, CTAs, dates, all
   in reading order). Fall back to viewing `<outPrefix>.png` with the Read tool when layout,
   design, or something the text extraction garbled matters (tables, side-by-side comparisons,
   images with embedded text).

5. **If a page still comes back thin** (e.g. text length under ~50 chars, or just an error
   page), that page genuinely blocks automation (bot detection, requires auth, geo-blocked) —
   at that point it's reasonable to ask the user for a screenshot instead of retrying further.

## Notes

- `waitUntil: "networkidle"` plus a 2s extra wait covers most hydration delays; some pages
  (chat widgets, analytics beacons) never go fully idle — the script catches that timeout and
  proceeds with whatever rendered, which is usually complete already.
- This reads pages the same way a person looking at them in a browser would — use it for
  public pages the user has a legitimate reason to read (their own sites, competitor research,
  public docs), same judgment as using WebFetch. Don't use it to bypass a login wall or
  paywall on content that isn't the user's.
- No cleanup needed beyond the scratch directory — `playwright-core` never downloaded a
  browser, so there's no multi-hundred-MB Chromium binary left on disk.
