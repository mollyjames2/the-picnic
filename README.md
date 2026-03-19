# The Picnic

*a story about a very good day*

A short narrative adventure game built with **PyGame**, playable in the browser via **pygbag** and deployed automatically to **GitHub Pages**.

---

## Story

You play as **Sam**, heading out on a picnic with your partner **Maggie** and friend **Molly**.
Pack the basket, choose a destination, find the perfect spot, and enjoy the afternoon — while Sam works up to something special.

The choices you make throughout the story are quietly remembered and woven into the ending.

---

## Scenes

| # | Scene | Summary |
|---|-------|---------|
| 0 | Title screen | Press ENTER to begin |
| 1 | Kitchen | Pack the picnic basket — collect items scattered around the room and bring them to the basket |
| 2 | Kitchen | Molly arrives; choose a destination (beach, woods, or viewpoint); everyone walks to the car |
| 3 | Car | Conversation on the drive; a question about living here (choice remembered for later) |
| 4 | Arrival | Explore the location to find the perfect picnic spot — some spots have consequences |
| 5 | Picnic | Settle in; a series of conversational choices about home, comfort, and adventure |
| 6 | Proposal | Sam gives a speech drawn from your earlier choices, then gets down on one knee |

---

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Move Sam |
| ENTER | Advance dialogue / confirm choice / interact |
| Up / Down | Navigate choice menus |

---

## Running Locally

```bash
python main.py
```

Build the browser version:

```bash
pygbag .
```

The web build is written to `build/` (not committed).

---

## Environment

Python 3.11 with **pygame 2.6.1** and **pygbag 0.9.3**.

Create the conda environment from `environment.yml`:

```bash
conda env create -f environment.yml
conda activate game
```

---

## Project Structure

```
main.py              Entry point — game loop, sprite loading, global state
data/
  game_config.py     Title, subtitle, character names
  dialogue.py        All dialogue strings and choice text
engine/
  settings.py        Resolution (800×600), FPS, colours, fonts, paths
  assets.py          SpriteManager and GIF frame loader
  movement.py        move_player and follow_leader helpers
  transitions.py     GIF playback transitions
  dialogue.py        text_box and draw_3d_box UI helpers
scenes/
  scene_0.py         Title screen
  scene_1.py         Kitchen — pack the basket
  scene_2.py         Molly arrives, destination choice, drive-away
  scene_3.py         Car conversation, living-here choice
  scene_4.py         Spot exploration with vignettes
  scene_5.py         Picnic conversation choices
  scene_6.py         Proposal ending
assets/
  sprites/           Character and background sprites
  GIFs/              Animated sequences (kitchen, solar flare, hay fever)
  pictures/          Car interior, ring, destination backgrounds
  fonts/             Monospace TTF font
.github/workflows/   GitHub Actions deploy to GitHub Pages
```

---

## Deployment

Pushing to `main` triggers a GitHub Actions workflow that builds the game with **pygbag** and deploys it to **GitHub Pages** via the `gh-pages` branch.

### Required setup (once per repo)

**1. Add the deploy token**

In **Settings → Secrets and variables → Actions**, create a secret:

```
Name:  GH_TOKEN
Value: <your personal access token with repo scope>
```

**2. Enable GitHub Pages**

In **Settings → Pages**, set source to **Deploy from a branch** and select the `gh-pages` branch.

The `gh-pages` branch is created automatically on the first deploy run.

Your game will be live at:

```
https://<your-github-username>.github.io/<repo-name>/
```
