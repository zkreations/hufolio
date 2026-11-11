# Hufolio

> A minimalist, typography-driven editorial theme for [Hugo](https://gohugo.io/) inspired by [Telegra.ph](https://telegra.ph/), optimized for [Telegram Instant View](https://instantview.telegram.org/) with zero JavaScript and zero external dependencies.

[![CI](https://github.com/zkreations/hufolio/actions/workflows/ci.yml/badge.svg)](https://github.com/zkreations/hufolio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/zkreations/hufolio/blob/main/LICENSE)
[![Hugo Extended](https://img.shields.io/badge/Hugo%20Extended-%3E%3D%200.164.0-ff4088.svg)](https://gohugo.io/)
[![Zero JavaScript](https://img.shields.io/badge/JavaScript-0%20KB-brightgreen.svg)](#features)

---

## Philosophy

Hufolio is designed for writers, essayists, and independent publishers who value **clarity, speed, and cognitive calm**. 

Taking direct cues from Telegra.ph's legendary simplicity, Hufolio removes all ornamental distractions — no cards, no box shadows, no decorative carousels, and no unnecessary layout chrome. Your thoughts and words take center stage, typeset in high-legibility Inter typography on a centered, comfortable reading column.

Technical elegance matches aesthetic minimalism:
- **Zero Runtime JavaScript:** Zero client-side scripts, zero trackers, zero vulnerabilities.
- **Zero Node.js / npm Dependencies:** Pure Hugo native pipeline using Hugo Pipes.
- **Instantaneous Performance:** Total core payload under 4 KB gzip (HTML + minified CSS).
- **Telegram Instant View Native:** Pre-engineered HTML Contract and tested XPath template for instantaneous reading inside Telegram mobile apps.

---

## Features

- **Typography First:** Local [Inter](https://rsms.me/inter/) font (Regular, Medium, SemiBold, and Italic) bundled as optimized WOFF2 with zero external font requests.
- **Native Color Themes:** Seamless light and dark modes powered by CSS custom properties and system `prefers-color-scheme`.
- **Telegram Instant View Support:** Ready-to-deploy `.iv` template with full support for covers, blockquotes, code blocks, tables, and nested lists.
- **Flexible Page Bundles:** Automatic cover image resolution from Page Bundles (`cover.*`, `featured.*`, or front matter `image`).
- **Comprehensive SEO & Social Cards:** Automated Open Graph, Twitter Cards, canonical links, and auto-computed image dimension metadata.
- **Accessible by Design:** Strict WCAG 2.1 AA color contrast compliance, visible focus outlines, sequential heading hierarchy, and skip-to-content links.
- **Syndication & Discovery:** Standard RSS 2.0 feed and XML sitemap generation.
- **SEO & AI-ready:** Open Graph, Twitter Cards, canonical URLs, RSS autodiscovery, production-aware `robots.txt`, and structured `llms.txt` / `llms-full.txt` support.
- **Multilingual & i18n:** Native internationalization support with built-in English (`en`) and Spanish (`es`) translations.
- **Zero Build Fatigue:** Powered exclusively by Hugo Extended.

---

## Requirements

- **[Hugo Extended](https://gohugo.io/installation/) `>= 0.164.0`** (required for Hugo Pipes asset bundling and minification).

Verify your installed version:
```bash
hugo version
```

---

## Installation

You can install Hufolio using either **Hugo Modules** (recommended) or as a **Git submodule**.

### Method 1: Hugo Modules (Recommended)

*(Note: Hugo Modules require [Go](https://go.dev/) installed on your machine or CI runner)*

1. Initialize your Hugo project as a module if you haven't already:
   ```bash
   hugo mod init github.com/yourusername/my-site
   ```

2. Add Hufolio to your `hugo.toml`:
   ```toml
   [module]
     [[module.imports]]
       path = "github.com/zkreations/hufolio"
   ```

3. Fetch the theme:
   ```bash
   hugo mod get github.com/zkreations/hufolio
   ```

### Method 2: Git Submodule

1. Add the repository as a submodule inside your site's `themes` directory:
   ```bash
   git submodule add https://github.com/zkreations/hufolio.git themes/hufolio
   ```

2. Specify the theme in your `hugo.toml`:
   ```toml
   theme = "hufolio"
   ```

---

## Configuration Reference

Here is a complete, production-ready `hugo.toml` configuration:

```toml
baseURL = "https://example.com/"
title = "My Minimalist Journal"
defaultContentLanguage = "en"
theme = "hufolio"

# SEO, AI & Crawlers
enableRobotsTXT = true
enableGitInfo = true
disableKinds = ["taxonomy", "term"]

[outputs]
  home = ["html", "rss", "llms", "llmsfull"]

[menus]
  [[menus.main]]
    name = "About"
    pageRef = "/about"
    weight = 1

[params]
  description = "Essays on software craftsmanship, design, and minimalism."
  author = "Jane Doe"
  author_role = "Writer & Minimalist"
  author_bio = "Essays on design, technology, and clarity."
  date_format = "02 Jan 2006"
  home_posts_limit = 10
  show_reading_time = true
  footer_text = "All rights reserved."

  [[params.social]]
    name = "GitHub"
    url = "https://github.com/zkreations"
```

### Supported Parameters (`[params]`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `description` | string | `""` | Site description used for meta tags and homepage fallback. |
| `author` | string / map | `""` | Author name (`author = "Name"`) or map (`author.name`, `author.role`, `author.bio`). |
| `author_role` | string | `""` | Optional author role/tagline displayed in the homepage sidebar profile. |
| `author_bio` | string | `""` | Optional author bio displayed in the homepage sidebar profile. |
| `date_format` | string | `"02 Jan 2006"` | Date display format (Go time format string). |
| `home_posts_limit` | int | `10` | Number of posts displayed on the homepage feed before showing pagination. |
| `show_reading_time` | bool | `true` | Display estimated reading time on post cards and feeds. |
| `mainSections` | []string | `["posts"]` | Content sections treated as articles in feed, stats, and LLM exports. |
| `footer_text` | string | `""` | Optional text displayed alongside the copyright in the footer. |
| `social` | []map | `[]` | List of social links with `name` and `url` displayed in the footer. |

### Search Engines & LLMs

#### robots.txt

Enable standard `robots.txt` generation in your `hugo.toml`:

```toml
enableRobotsTXT = true
```

The theme conditions crawler access automatically:
- **Production (`hugo.IsProduction`):** Allows all crawlers and links to `sitemap.xml`.
- **Development / Previews:** Blocks all crawlers (`Disallow: /`) to prevent indexing test or staging builds.

#### llms.txt & llms-full.txt

Hufolio includes native support for the [llmstxt.org](https://llmstxt.org) standard for AI models and assistants. Enable the formats under `[outputs]` in your `hugo.toml`:

```toml
[outputs]
  home = ["html", "rss", "llms", "llmsfull"]
```

- **`/llms.txt`**: A concise Markdown index of your posts and pages with summaries and links to supplementary resources.
- **`/llms-full.txt`**: A complete consolidated Markdown document with full page content (`.RawContent`) for context-window feeding.

### Internationalization (i18n)

Hufolio provides multilingual support via Hugo's native `i18n` framework. Built-in translations are provided for:
- English (`en`)
- Spanish (`es`)

To set the language of your site, configure `defaultContentLanguage` in `hugo.toml`:

```toml
defaultContentLanguage = "es" # or "en"
```

---

## Content Management

### Creating Articles

Generate a new article using Hugo's archetype:

```bash
# Standalone Markdown file
hugo new posts/digital-minimalism.md

# Or as a Page Bundle (recommended when including images)
hugo new posts/digital-minimalism/index.md
```

### Front Matter Reference

Each article supports the following front matter attributes:

```yaml
---
title: "Digital Minimalism and Editorial Writing"
description: "Why eliminating visual noise produces deeper reading experiences."
date: 2026-11-08T12:00:00Z
author: "Jane Doe"
draft: false
# Optional cover image path (if not using bundle automatic detection)
# image: "cover.jpg"
---
```

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | String | **Yes** | Post title rendered as `<h1>` and used in meta tags. |
| `description` | String | Recommended | Post subtitle rendered under the title and used in Open Graph/SEO. |
| `date` | Timestamp | Recommended | Publication date formatted as ISO 8601. |
| `author` | String | Optional | Post author. Falls back to `params.author` if omitted. |
| `image` | String | Optional | Explicit cover image path (relative or bundle resource). |
| `image_alt` | String | Optional | Descriptive alternative text for the cover image (`alt` attribute). |
| `draft` | Boolean | Optional | Set to `true` to exclude the post from production builds. |

### Cover Image Resolution Cascade

When rendering the featured cover image, Hufolio looks for images in this exact order:
1. Explicit `image` field in front matter (`.Params.image`).
2. A bundle resource named `cover.*` (e.g. `cover.jpg`, `cover.png`, `cover.webp`).
3. A bundle resource named `featured.*` (e.g. `featured.jpg`, `featured.png`).
4. The first image found within the Page Bundle.

When resolved, the cover image is rendered above the content with explicit `width`, `height`, `loading="eager"`, and `decoding="async"` for optimal LCP performance.

### Static Pages

To create standalone pages (such as `/about/` or `/privacy/`):

```bash
hugo new about.md
```

Hufolio renders static pages with `<article class="page">`. This intentional distinction keeps your static pages visually cohesive while preventing Telegram Instant View from incorrectly activating on non-editorial landing pages.

---

## Telegram Instant View

Hufolio includes native, battle-tested support for **Telegram Instant View 2.1**.

### How to Enable Instant View for Your Domain

1. Deploy your site to your custom domain (e.g., `https://example.com`).
2. Log into the [Telegram Instant View Checklist](https://instantview.telegram.org/my/) with your Telegram account.
3. In the **Target Pages** field, enter the URL of any article on your site:
   ```text
   https://example.com/posts/digital-minimalism/
   ```
4. Copy and paste the official template rules below into the code editor on the left:
   ```text
   ~version: "2.1"

   # Match single article pages governed by Hufolio's HTML Contract
   ?exists: //article[contains(@class, 'article')]

   $article: //article[contains(@class, 'article')]

   title: $article//h1[contains(@class, 'article-title')]
   subtitle: $article//p[contains(@class, 'article-description')]
   author: $article//span[contains(@class, 'article-author')]
   published_date: $article//time[contains(@class, 'article-date')]/@datetime
   cover: $article//figure[contains(@class, 'article-cover')]//img

   $body: $article//div[contains(@class, 'article-body')]

   @remove: $body//a[contains(@class, 'heading-anchor')]

   # Unwrap code syntax highlighting wrappers generated by Hugo Chroma
   @unwrap: $body//div[contains(@class, 'highlight')]

   # Unwrap responsive table overflow wrapper
   @unwrap: $body//div[contains(@class, 'table-wrapper')]

   body: $body
   ```
5. Review the mobile preview panel on the right. Verify that:
   - The title, author, and date match.
   - The cover image renders cleanly.
   - Headings, lists, quotes, tables, and code blocks display seamlessly.
6. Click **Mark as checked**. Repeat for 10 diverse articles to unlock public Instant View links for your entire domain.

### HTML Contract Guarantee

Telegram Instant View depends on stable DOM selectors. Hufolio guarantees the following immutable HTML structure for all articles:

```html
<article class="article">
  <header class="article-header">
    <h1 class="article-title">...</h1>
    <p class="article-description">...</p>
    <div class="article-meta">
      <span class="article-author">...</span>
      <time class="article-date">...</time>
    </div>
  </header>
  <figure class="article-cover">
    <img ...>
  </figure>
  <div class="article-body">
    ... markdown content ...
  </div>
</article>
```

---

## Deployment Guides

Hufolio builds into pure static assets in milliseconds and can be hosted anywhere.

### 1. Cloudflare Pages

1. Log into your Cloudflare Dashboard and select **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
2. Select your repository.
3. Configure build settings:
   - **Framework preset:** `Hugo`
   - **Build command:** `hugo --gc --minify`
   - **Build output directory:** `public`
4. Add the following **Environment variable**:
   - Variable name: `HUGO_VERSION`
   - Value: `0.164.0` (or later)
5. Click **Save and Deploy**.

### 2. Netlify

Add a `netlify.toml` file to the root of your project:

```toml
[build]
  publish = "public"
  command = "hugo --gc --minify"

[context.production.environment]
  HUGO_VERSION = "0.164.0"
```

Netlify will automatically detect this configuration upon connecting your repository.

### 3. GitHub Pages

Create a file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo Extended
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true

      - name: Build with Hugo
        run: hugo --gc --minify

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

In your repository settings, navigate to **Settings** > **Pages** and set **Source** to **GitHub Actions**.

---

## Local Development & Testing

To test Hufolio locally using the included `exampleSite`:

```bash
# Clone the repository
git clone https://github.com/zkreations/hufolio.git
cd hufolio

# Start local server with the example site
hugo server --themesDir ../.. -s exampleSite
```

Open `http://localhost:1313/` in your browser.

### Running Automated Validation

Hufolio includes an automated validation suite to verify the HTML contract and performance budgets:

```bash
# 1. Build the example site
hugo --themesDir ../.. -s exampleSite --gc --minify

# 2. Run contract & budget validation
bash .github/scripts/validate.sh
```

---

## License

Hufolio is open-source software licensed under the [MIT License](LICENSE).

Crafted with care by [zkreations](https://www.zkreations.com).