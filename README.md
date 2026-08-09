# Nora and Samen — Match History (GitHub-synced version)

A shared, read-only match history gallery. Screenshots live directly in this repo's
`/screenshots` folder. Add a file with git, push, and the site updates automatically
for anyone who has the link — you and your friend see the exact same gallery.

No backend, no database, no API tokens, no manual JSON editing.

## How it works

1. You drop an image into `screenshots/` and run `git push`.
2. A GitHub Action (`.github/workflows/update-manifest.yml`) notices the push,
   runs `scripts/generate_manifest.py`, and rebuilds `manifest.json` — a list of
   every screenshot and the exact date/time it was first committed.
3. The Action commits that updated `manifest.json` back to the repo automatically.
4. GitHub Pages redeploys the site (usually within a minute).
5. `index.html` fetches `manifest.json` on load and renders the gallery — no
   database, everything is just static files.

You never write JSON by hand and never touch the website's code to add a screenshot.

## One-time setup

### 1. Create the repo
- Create a new GitHub repository (public or private — private is fine, GitHub Pages
  works with private repos too, though the *published site* itself is visible to
  anyone with the link regardless of repo visibility).
- Push everything in this folder to it:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin https://github.com/<your-username>/<your-repo>.git
  git push -u origin main
  ```

### 2. Enable GitHub Pages
- On GitHub, go to your repo → **Settings** → **Pages**.
- Under "Build and deployment", set **Source** to "Deploy from a branch".
- Set **Branch** to `main` and folder to `/ (root)`. Save.
- GitHub will give you a URL like `https://<your-username>.github.io/<your-repo>/`.
  That's the link you share with your friend.

### 3. Allow the Action to push back to the repo
- Go to **Settings** → **Actions** → **General** → scroll to "Workflow permissions".
- Select **"Read and write permissions"**, then save.
  (Without this, the Action can build `manifest.json` but won't be allowed to commit it back.)

That's it — setup is done.

## Adding a screenshot (your day-to-day workflow)

1. In VS Code, drag your screenshot file into the `screenshots/` folder.
2. Commit and push:
   ```bash
   git add screenshots/your-file.png
   git commit -m "Add screenshot"
   git push
   ```
3. Wait about 30–90 seconds. GitHub runs the Action, updates `manifest.json`, and
   Pages redeploys.
4. Refresh the site (or click the "Refresh" button in the toolbar) — your new
   screenshot appears, timestamped with the moment you committed it.

Your friend doesn't need to do anything — they just open the same link and see
the update too.

## Removing a screenshot

Delete the file from `screenshots/` in VS Code, then commit and push as usual.
The next Action run removes it from `manifest.json` and it disappears from the site.

## What the gallery can do

- Responsive grid, newest screenshots first by default.
- Each card shows the screenshot and its "Uploaded: <date> — <time>" stamp,
  taken straight from your git commit history.
- Click a screenshot for a full-size lightbox view with a close button.
- Download button on each card and inside the lightbox.
- Filter by date, toggle newest/oldest sort.
- Scoreboard-style match counter.
- Manual "Refresh" button to re-check `manifest.json` without a full page reload.
- Friendly empty state if `screenshots/` is empty.

This version is intentionally **read-only in the browser** — there's no upload or
delete button on the page itself, since GitHub Pages can't accept writes from a
visitor. Adding/removing screenshots always happens through git, as described above.

## File structure

```
.
├── index.html                          ← the gallery site
├── manifest.json                       ← auto-generated, do not edit by hand
├── screenshots/                        ← drop your images here
│   └── .gitkeep
├── scripts/
│   └── generate_manifest.py            ← builds manifest.json from git history
└── .github/
    └── workflows/
        └── update-manifest.yml         ← runs the script on every push
```

## Troubleshooting

- **Nothing shows up after pushing**: check the "Actions" tab on GitHub — click
  the latest run and confirm it succeeded. If it failed with a permissions error,
  revisit step 3 above (workflow read/write permissions).
- **Images show as broken**: GitHub Pages is case-sensitive and doesn't like
  spaces in filenames as much as local file systems do — stick to letters,
  numbers, hyphens, and underscores in screenshot filenames.
- **Timestamp looks off**: the date shown is your local commit's author time —
  if you're committing from a machine with the wrong system clock/timezone,
  fix that and future commits will be accurate.
