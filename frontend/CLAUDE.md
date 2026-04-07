# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI chat platform frontend built with Vue 3 + TypeScript + TailwindCSS v4 + DaisyUI v5 + Pinia + Vue Router.

## Package Manager

**Use `pnpm` for all package management operations.**

## Development Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start Vite dev server |
| `pnpm build` | Build for production (includes type-check) |
| `pnpm build-only` | Build without type-check |
| `pnpm preview` | Preview production build locally |
| `pnpm type-check` | Run TypeScript type checking |

## Architecture

### Tech Stack
- **Vue 3** with Composition API (`<script setup>`)
- **Pinia** for state management
- **Vue Router 4** for navigation
- **TailwindCSS v4** with CSS-first configuration
- **DaisyUI v5** component library
- **Vite** as build tool

### Key Configuration

**Path Alias**: `@` resolves to `./src` directory (configured in `vite.config.ts`)

**Tailwind/DaisyUI Setup** (`src/style/main.css`):
```css
@import "tailwindcss";
@plugin "daisyui";
```
No `tailwind.config.js` needed - uses Tailwind v4's automatic content detection.

### State Management

Pinia stores located in `src/stores/`:
- `user.ts` - Authentication state (token, userInfo, login/logout actions)

### Routing

Router configured in `src/router/index.ts` with navigation guards:
- `/login` - Requires guest (redirects to /chat if authenticated)
- `/chat` - Requires auth (redirects to /login if not authenticated)
- `/` - Redirects to `/chat`

### Component Structure

- `src/views/` - Page-level components (Login.vue, Chat.vue)
- `src/components/` - Reusable components (Sidebar.vue)
- Chat page uses DaisyUI `drawer` pattern for responsive sidebar layout
