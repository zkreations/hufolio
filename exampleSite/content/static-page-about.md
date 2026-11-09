---
title: "Static Verification Page"
description: "A static standalone page verifying that Telegram Instant View remains inactive."
---

This page verifies that non-article documents (such as About, Terms, or Contact pages) do not trigger Instant View generation.

### Structural Guarantee

Because this document is rendered using `<article class="page">` rather than `<article class="article">`, Telegram Instant View's selector rule `?exists: //article[contains(@class, 'article')]` safely evaluates to false.

Readers will always view static pages in their native browser environment.
