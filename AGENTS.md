# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

VuePress documentation site (vuepress-theme-hope) for Chinese AI development tutorials ("小林学AI"), covering Codex, Codex, OpenClaw, Agent, Skills, and Tool topics.

## Commands

```bash
pnpm install              # Install dependencies
pnpm run docs:dev         # Dev server with hot reload
pnpm run docs:clean-dev   # Dev server with clean cache
pnpm run docs:build       # Production build (output: src/.vuepress/dist)
pnpm run docs:update-package  # Update theme package
```

No test or lint commands exist in this project.

## Architecture

- **Source**: `src/` — all content and config
- **Config**: `src/.vuepress/` — VuePress configuration (TypeScript)
  - `config.ts` — site title, lang (`zh-CN`), base path, head/favicon
  - `theme.ts` — theme config, markdown extensions, plugins (Giscus comments, Badge/VPCard components, mermaid, Font Awesome 6 icons)
  - `navbar.ts` / `sidebar.ts` — navigation structure; sidebar uses `children: "structure"` to auto-generate from directory ordering
- **Styles**: `src/.vuepress/styles/` — palette.scss (theme color `#096dd9`), config.scss, index.scss
- **Assets**: `src/.vuepress/public/` — logos, favicon

## Content Conventions

- Each section directory has a `README.md` as its index page
- Article files use numeric prefix for ordering: `01-`, `02-`, etc. (e.g., `09-Codex-subagent-guide.md`)
- Frontmatter: `title` (display title) and `order` (sidebar ordering) are standard
- Homepage (`src/README.md`) uses `home: true` with hero config and custom HTML
- All content is in Chinese (zh-CN)

## Sidebar Auto-generation

Sidebar uses `children: "structure"` which derives ordering from file names and frontmatter `order`. New articles need only be placed in the correct directory with a numbered prefix — no manual sidebar config update required.

## Deployment

GitHub Actions (`.github/workflows/deploy-docs.yml`) deploys on push to `main`:
- Node.js 22, pnpm, `NODE_OPTIONS: --max_old_space_size=8192`
- Builds to `src/.vuepress/dist`, deploys to `gh-pages` branch

## Key Dependencies

- vuepress `2.0.0-rc.28`, vuepress-theme-hope `2.0.0-rc.106`
- Vue 3, Vite bundler, sass-embedded, mermaid
- Package manager: pnpm (specified via `packageManager` field)
