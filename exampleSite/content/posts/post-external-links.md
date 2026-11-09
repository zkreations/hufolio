---
title: "Article with External and Relative Links"
description: "Testing hyperlink styling, anchor security attributes, and relative navigation."
date: 2026-11-01T20:00:00-05:00
author: "zkreations"
draft: false
---

Hyperlinks connect digital essays into a broader web of discourse. In Hufolio, links are styled with the theme's singular primary accent color and a subtle underline.

### External Links

External hyperlinks are automatically intercepted by Hufolio's custom `render-link.html` hook to append `rel="noopener noreferrer"` attributes for security and privacy:

- [Hugo Static Site Generator](https://gohugo.io/)
- [Telegra.ph Publishing](https://telegra.ph/)
- [Telegram Instant View Documentation](https://instantview.telegram.org/docs)

### Internal Relative Links

Internal links preserve standard navigation without unnecessary attributes:

- Learn more on our [About Page](/about/)
- Return to the [Home Index](/)
