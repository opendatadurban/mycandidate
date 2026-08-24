# MyCandidate marketing & docs site

This directory is a small, dependency-free static site describing the MyCandidate
project. It is deployed to Netlify independently of the Flask application in the
rest of this repository — see `netlify.toml` at the repository root.

- `index.html` — project homepage
- `technical/` — technical documentation, kept in its own directory
- `code-of-conduct.html` — the project's Code of Conduct (also at the repo root as `CODE_OF_CONDUCT.md`)
- `assets/` — shared CSS and images

There is no build step. To preview locally, open `index.html` in a browser or
serve this folder with any static file server, e.g. `npx serve site`.
