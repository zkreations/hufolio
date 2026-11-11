---
title: "Article with Multiple Inline Figures"
description: "Testing inline image rendering, local asset resolution, and semantic captions."
date: 2026-11-01T15:00:00-05:00
author: "zkreations"
draft: false
---

This article demonstrates how Hufolio handles multiple inline images embedded within Markdown prose.

Here is the first photographic figure:

![First Demonstration Image](img-1.jpg "Architectural representation of primary layout grid")

The custom Markdown render hook ensures each image is emitted inside a `<figure class="article-figure">` with natural `width` and `height` attributes to prevent Cumulative Layout Shift (CLS), accompanied by an optional `<figcaption>`.

Here is a secondary illustration positioned further down the page:

![Second Demonstration Image](img-2.jpg "Secondary visual demonstration of editorial hierarchy")

Both images resolve seamlessly from this Page Bundle, and Telegram Instant View accurately maps them to native photo blocks with captions.
