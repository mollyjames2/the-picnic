```markdown
# pygame-pygbag-game-template

A reusable **PyGame + pygbag template** for small browser-playable games that automatically deploy to **GitHub Pages**.

This template lets you build a game with **PyGame**, package it with **pygbag**, and publish it online using **GitHub Actions**.

---

# Deployment

When you push to the `main` branch, GitHub Actions will:

1. Build the game using **pygbag**
2. Publish the generated web files to the `gh-pages` branch
3. Deploy the site with **GitHub Pages**

Your game will be available at:

```
https://<your-github-username>.github.io/<repo-name>/

```

Example:


```
[https://mollyjames2.github.io/ourfirstdate/](https://mollyjames2.github.io/ourfirstdate/)

```


# Creating a New Game From This Template

1. Copy this repository or use it as a template
2. Rename the repository to your new game name
3. Replace the game assets and logic
4. Push the repo to GitHub
5. Follow the setup instructions below


# GitHub Setup

Each new game repo needs two things configured.


## 1. Add the Deploy Token

The deploy workflow uses a repository secret called **GH_TOKEN**.

Create it in your repository:

1. Go to **Settings**
2. Open **Secrets and variables**
3. Click **Actions**
4. Click **New repository secret**

Create:

```

Name: GH_TOKEN
Value: <your personal access token>

```

### Creating the token

1. Go to **GitHub → Settings**
2. Open **Developer Settings**
3. Select **Personal access tokens**
4. Create a **Classic token**
5. Enable permission:

```

repo

```

Copy the token and store it as the `GH_TOKEN` secret.


## 2. Enable GitHub Pages

In your repository:

1. Go to **Settings**
2. Open **Pages**
3. Under **Build and deployment**, set:

```

Source: Deploy from a branch

```

Choose the branch:

```

gh-pages

```

Click **Save**.

The `gh-pages` branch will be created automatically the first time the deploy workflow runs.


# GitHub Pages Setup Summary

This template deploys the built web files to a branch called `gh-pages`.

For each new game repo:

1. Add a repository secret called **GH_TOKEN**
2. Enable GitHub Pages using **Deploy from a branch**
3. Select the **gh-pages** branch

After that, every push to `main` will:

- build the game with **pygbag**
- push the built site to the **gh-pages** branch
- publish it at:

```

https://<your-github-username>.github.io/<repo-name>/

```

Example:

```

https://<your-github-username>.github.io/my-new-game/

````


# Local Development

Run the game locally:

```bash
python main.py
````

Build the web version locally:

```bash
pygbag .
```

This will generate the web build inside the `build/` folder.


# Project Structure

```
assets/        Game art, audio, and fonts
main.py        Main entry point for the game
.github/       GitHub Actions deployment workflow
```


# Notes

* The `build/` folder is generated automatically and should **not** be committed.
* The repository name becomes part of the game URL.
* Each new game can reuse the same deploy workflow.

```

