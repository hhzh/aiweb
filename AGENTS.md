# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

VuePress documentation site (vuepress-theme-hope, v2.0.0-rc.106) for Chinese AI development tutorials ("小林学AI"). Covers Claude Code, Codex, OpenClaw, Hermes Agent, OpenCode, Agent, Skills, and Tool topics.

All content is in Chinese (zh-CN).

## Commands

```bash
pnpm install                          # Install dependencies (pnpm@9.15.9)
pnpm run docs:dev                     # Dev server with hot reload
pnpm run docs:clean-dev               # Dev server with clean cache
pnpm run docs:build                   # Production build (output: src/.vuepress/dist)
pnpm run docs:update-package          # Update vuepress-theme-hope package
```

No test, lint, or typecheck commands exist.

## Architecture

- **Config**: `src/.vuepress/` — TypeScript (ES modules via `"type": "module"` in package.json)
  - `config.ts` — site title, lang (`zh-CN`), base path (`/`), favicon
  - `theme.ts` — theme plugins (Giscus comments, Badge/VPCard, mermaid, Font Awesome 6 icons), markdown extensions
  - `navbar.ts` / `sidebar.ts` — navigation; sidebar uses `children: "structure"` for auto-generation from file order (no manual sidebar updates needed)
- **Styles**: `src/.vuepress/styles/` — palette.scss (theme color `#096dd9`), config.scss, index.scss
- **Assets**: `src/.vuepress/public/` — logos, favicon
- **Bundler**: `@vuepress/bundler-vite` (explicitly specified; not the default)
- **tsconfig**: targets ES2022 with NodeNext module resolution

## Content Conventions

- Each section directory has a `README.md` as its index page
- Article files use numeric prefixes for ordering: `01-`, `02-`, etc.
- Frontmatter: `title` (display title) and `order` (sidebar ordering)
- Homepage (`src/README.md`) uses `home: true` with hero config and custom HTML

## Publishing Automation

This repo contains 14 Playwright-based publisher skills in `.agents/skills/` for automated article publishing to Chinese dev platforms (CSDN, Juejin, InfoQ, Tencent Cloud, 51CTO, Zhihu, CNBlogs, SegmentFault, Aliyun). A `publish-all` skill publishes to all 8 platforms in sequence. These use the `playwright-cli` CLI tool for browser automation; logs are stored in `.playwright-cli/` (gitignored).

## Deployment

GitHub Actions (`.github/workflows/deploy-docs.yml`) on push to `main`:
- Node.js 22, pnpm, `NODE_OPTIONS: --max_old_space_size=8192`
- Builds to `src/.vuepress/dist`, deploys to `gh-pages` branch

## Key Dependencies

- `vuepress@2.0.0-rc.28`, `vuepress-theme-hope@2.0.0-rc.106`
- `@vuepress/bundler-vite`, `sass-embedded`, `mermaid`
- Package manager: `pnpm@9.15.9` (enforced via `packageManager` field)
