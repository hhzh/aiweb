# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a VuePress documentation site using vuepress-theme-hope, containing Chinese documentation about AI development tools including Claude Code, Codex, OpenClaw, and related technologies.

## Commands

```bash
# Install dependencies
pnpm install

# Start development server with hot reload
pnpm run docs:dev

# Start dev server with clean cache
pnpm run docs:clean-dev

# Build for production
pnpm run docs:build

# Update theme package
pnpm run docs:update-package
```

## Architecture

- **Source Directory**: `src/` - All documentation content lives here
- **Config Directory**: `src/.vuepress/` - VuePress configuration files
  - `config.ts` - Main VuePress config (site title, language, base path)
  - `theme.ts` - Theme configuration (navbar, sidebar, plugins, markdown features)
  - `navbar.ts` - Navigation bar structure
  - `sidebar.ts` - Sidebar structure
  - `styles/` - Custom SCSS styles

## Documentation Sections

Content is organized into these main directories under `src/`:

- `claudecode/` - Claude Code documentation
- `codex/` - Codex documentation
- `openclaw/` - OpenClaw documentation
- `agent/` - Agent-related documentation
- `skills/` - Skills documentation
- `tool/` - Tool documentation
- `writing/` - Writing-related documentation
- `obsidian/` - Obsidian documentation
- `demo/` - Demo pages
- `guide/` - General guide pages

## Deployment

Deployment is handled via GitHub Actions (`.github/workflows/deploy-docs.yml`):
- Triggers on push to `main` branch
- Uses Node.js 22 and pnpm
- Builds to `src/.vuepress/dist`
- Deploys to `gh-pages` branch

## Markdown Features

The theme has extended markdown support enabled:
- GFM (GitHub Flavored Markdown)
- Code tabs, demo blocks
- Task lists, footnotes
- Custom containers (hint, alert)
- Image lazy loading and size support
- Mark, spoiler, align, attrs
- Include files support
