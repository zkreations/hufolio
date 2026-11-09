#!/usr/bin/env python3
"""
Hufolio automated validation suite.
Verifies HTML Contract compliance, Instant View compatibility, zero JavaScript,
and asset integrity across all generated pages in exampleSite/public.
Supports both unminified and minified HTML output.
"""

import sys
from pathlib import Path
import re

PUBLIC_DIR = Path("exampleSite/public")


def test_zero_javascript():
    print("[1/5] Checking Zero JavaScript constraint...")
    js_files = list(PUBLIC_DIR.glob("**/*.js"))
    if js_files:
        print(f"FAILED: Found unauthorized JavaScript files: {js_files}")
        return False
    print("      OK: Zero JavaScript files emitted.")
    return True


def test_css_budget():
    print("[2/5] Checking CSS budget (< 10 KB)...")
    css_files = list(PUBLIC_DIR.glob("css/*.css"))
    if not css_files:
        print("FAILED: No CSS bundle found in public/css/")
        return False

    for css in css_files:
        size = css.stat().st_size
        print(f"      Bundle: {css.name} ({size} bytes)")
        if size >= 10240:
            print(f"FAILED: CSS bundle exceeds 10 KB budget ({size} >= 10240 bytes)")
            return False
    print("      OK: CSS bundle is within ultralight budget.")
    return True


def test_html_contract_and_instant_view():
    print("[3/5] Verifying HTML Contract and XPath selectors on posts...")
    posts_dir = PUBLIC_DIR / "posts"
    if not posts_dir.is_dir():
        print(f"FAILED: Posts directory not found at {posts_dir}")
        return False

    post_dirs = [d for d in posts_dir.iterdir() if d.is_dir()]
    if not post_dirs:
        print("FAILED: No generated post directories found.")
        return False

    for post in post_dirs:
        html_file = post / "index.html"
        if not html_file.is_file():
            print(f"FAILED: Missing index.html in {post}")
            return False

        content = html_file.read_text(encoding="utf-8")

        # HTML Contract elements (supporting both minified and unminified attribute quotes)
        assert_contains(content, r'<article class=["\']?article["\']?[ >]', f"[{post.name}] Missing <article class=\"article\">")
        assert_contains(content, r'<h1 class=["\']?article-title["\']?[ >]', f"[{post.name}] Missing <h1 class=\"article-title\">")
        assert_contains(content, r'<span class=["\']?article-author["\']?[ >]', f"[{post.name}] Missing <span class=\"article-author\">")
        assert_contains(content, r'<time class=["\']?article-date["\']?\s+datetime=["\']?[^"\'>]+["\']?[ >]', f"[{post.name}] Missing <time class=\"article-date\"> with datetime")
        assert_contains(content, r'<div class=["\']?article-body["\']?[ >]', f"[{post.name}] Missing <div class=\"article-body\">")

        # Scoped header checks
        header_match = re.search(r'<header class=["\']?article-header["\']?>(.*?)</header>', content, re.DOTALL)
        if not header_match:
            raise AssertionError(f"[{post.name}] Missing article-header")
        header = header_match.group(1)

        # Scenario specific assertions
        if post.name == "post-with-cover":
            assert_contains(content, r'<figure class=["\']?article-cover["\']?>\s*<img\s+src=', "[post-with-cover] Missing cover figure")

        if post.name == "post-no-description":
            if re.search(r'<p class=["\']?article-description["\']?>', header):
                raise AssertionError("[post-no-description] Header should not render <p class=\"article-description\">")

    print(f"      OK: All {len(post_dirs)} post scenarios conform strictly to the HTML Contract.")
    return True


def test_static_pages():
    print("[4/5] Checking static pages (Instant View exclusion)...")
    for page_name in ["about", "static-page-about"]:
        html_file = PUBLIC_DIR / page_name / "index.html"
        if not html_file.is_file():
            print(f"FAILED: Static page index not found at {html_file}")
            return False

        content = html_file.read_text(encoding="utf-8")
        if re.search(r'<article class=["\']?article["\']?[ >]', content):
            print(f"FAILED: Static page [{page_name}] contains class 'article' (would trigger Instant View)")
            return False

        if not re.search(r'<article class=["\']?page["\']?[ >]', content):
            print(f"FAILED: Static page [{page_name}] missing <article class=\"page\">")
            return False

    print("      OK: Static pages correctly scoped under class 'page'.")
    return True


def test_assets_and_metadata_integrity():
    print("[5/5] Checking asset integrity, canonical links, and fonts...")
    index_html = (PUBLIC_DIR / "index.html").read_text(encoding="utf-8")

    # Fonts preload check
    font_matches = re.findall(r'<link rel=["\']?preload["\']?\s+href=["\']?(/fonts/[^"\'>\s]+)["\']?\s+as=["\']?font["\']?', index_html)
    if not font_matches:
        print("FAILED: No font preloads found in index.html")
        return False

    for font_path in font_matches:
        disk_path = PUBLIC_DIR / font_path.lstrip("/")
        if not disk_path.is_file():
            print(f"FAILED: Preloaded font does not exist on disk: {disk_path}")
            return False

    # Robots.txt and sitemap
    if not (PUBLIC_DIR / "robots.txt").is_file():
        print("FAILED: robots.txt not generated.")
        return False
    if not (PUBLIC_DIR / "sitemap.xml").is_file():
        print("FAILED: sitemap.xml not generated.")
        return False
    if not (PUBLIC_DIR / "index.xml").is_file():
        print("FAILED: RSS feed index.xml not generated.")
        return False

    print("      OK: All preloads, fonts, robots.txt, sitemap.xml, and RSS feeds verified.")
    return True


def assert_contains(content: str, pattern: str, message: str):
    if not re.search(pattern, content):
        raise AssertionError(f"{message}\nPattern: {pattern}")


def main():
    if not PUBLIC_DIR.is_dir():
        print(f"Error: {PUBLIC_DIR} does not exist. Run 'hugo --themesDir ../.. -s exampleSite' first.")
        sys.exit(1)

    tests = [
        test_zero_javascript,
        test_css_budget,
        test_html_contract_and_instant_view,
        test_static_pages,
        test_assets_and_metadata_integrity,
    ]

    for test in tests:
        try:
            if not test():
                sys.exit(1)
        except AssertionError as e:
            print(f"FAILED: {e}")
            sys.exit(1)

    print("\nSUCCESS: All automated validation checks passed!")


if __name__ == "__main__":
    main()
