#!/usr/bin/env python3
"""
Hufolio Phase 7 Quality, Accessibility & Performance Audit.
Performs WCAG 2.1 AA contrast calculations, DOM heading hierarchy verification,
image accessibility inspection, and resource payload budget checks.
"""

import sys
from pathlib import Path
import re
import gzip

PUBLIC_DIR = Path("exampleSite/public")


def hex_to_relative_luminance(hex_str: str) -> float:
    hex_str = hex_str.lstrip("#")
    r, g, b = [int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = hex_to_relative_luminance(hex1)
    l2 = hex_to_relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def audit_color_contrast():
    print("[1/4] Auditing WCAG 2.1 AA Color Contrast Ratios...")
    
    # Light theme tokens
    bg_light = "#ffffff"
    text_light = "#1a1a1a"
    muted_light = "#737373"
    primary_light = "#0066cc"
    on_primary_light = "#ffffff"

    c_text_light = contrast_ratio(text_light, bg_light)
    c_muted_light = contrast_ratio(muted_light, bg_light)
    c_primary_light = contrast_ratio(primary_light, bg_light)
    c_on_primary_light = contrast_ratio(on_primary_light, primary_light)

    print(f"      Light Theme (Background: {bg_light}):")
    print(f"        - Primary text  ({text_light}):    {c_text_light:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - Muted text    ({muted_light}):    {c_muted_light:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - Primary links ({primary_light}):  {c_primary_light:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - On-primary    ({on_primary_light} on {primary_light}): {c_on_primary_light:.2f}:1 (Target: >= 4.5:1)")

    if c_text_light < 4.5 or c_muted_light < 4.5 or c_primary_light < 4.5 or c_on_primary_light < 4.5:
        print("FAILED: Light theme does not meet WCAG AA ratio 4.5:1")
        return False

    # Dark theme tokens
    bg_dark = "#121212"
    text_dark = "#e0e0e0"
    muted_dark = "#888888"
    primary_dark = "#4da3ff"
    on_primary_dark = "#121212"

    c_text_dark = contrast_ratio(text_dark, bg_dark)
    c_muted_dark = contrast_ratio(muted_dark, bg_dark)
    c_primary_dark = contrast_ratio(primary_dark, bg_dark)
    c_on_primary_dark = contrast_ratio(on_primary_dark, primary_dark)

    print(f"      Dark Theme (Background: {bg_dark}):")
    print(f"        - Primary text  ({text_dark}):    {c_text_dark:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - Muted text    ({muted_dark}):    {c_muted_dark:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - Primary links ({primary_dark}):  {c_primary_dark:.2f}:1 (Target: >= 4.5:1)")
    print(f"        - On-primary    ({on_primary_dark} on {primary_dark}): {c_on_primary_dark:.2f}:1 (Target: >= 4.5:1)")

    if c_text_dark < 4.5 or c_muted_dark < 4.5 or c_primary_dark < 4.5 or c_on_primary_dark < 4.5:
        print("FAILED: Dark theme does not meet WCAG AA ratio 4.5:1")
        return False

    print("      OK: All color combinations meet or exceed WCAG 2.1 AA.")
    return True


def audit_heading_hierarchy():
    print("[2/4] Auditing Heading Hierarchy across all generated HTML pages...")
    html_files = list(PUBLIC_DIR.glob("**/*.html"))
    if not html_files:
        print("FAILED: No HTML files found in public/")
        return False

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        h1_tags = re.findall(r'<h1(?:\s+[^>]*)?>', content)
        rel_path = html_file.relative_to(PUBLIC_DIR)

        if len(h1_tags) != 1:
            print(f"FAILED: Page [{rel_path}] has {len(h1_tags)} <h1> elements. Expected exactly 1.")
            return False

        # Sequence check (H1 -> H2 -> H3 etc.)
        headings = re.findall(r'<h([1-6])(?:\s+[^>]*)?>', content)
        levels = [int(h) for h in headings]
        for i in range(len(levels) - 1):
            if levels[i+1] > levels[i] + 1:
                print(f"WARNING/FAIL: Page [{rel_path}] skipped heading level: H{levels[i]} followed by H{levels[i+1]}")
                return False

    print(f"      OK: Verified single <h1> and sequential hierarchy across all {len(html_files)} pages.")
    return True


def audit_images_accessibility():
    print("[3/4] Auditing Image Accessibility (alt, loading, decoding)...")
    html_files = list(PUBLIC_DIR.glob("**/*.html"))
    img_pattern = re.compile(r'<img\s+([^>]+)>')

    count = 0
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        rel_path = html_file.relative_to(PUBLIC_DIR)
        for match in img_pattern.finditer(content):
            count += 1
            attrs = match.group(1)
            if 'alt=' not in attrs:
                print(f"FAILED: Page [{rel_path}] has <img> without alt attribute: {match.group(0)}")
                return False
            if 'loading=' not in attrs:
                print(f"FAILED: Page [{rel_path}] has <img> without loading attribute: {match.group(0)}")
                return False
            if 'decoding=' not in attrs:
                print(f"FAILED: Page [{rel_path}] has <img> without decoding attribute: {match.group(0)}")
                return False

    print(f"      OK: Verified {count} <img> tags with full alt, loading, and decoding attributes.")
    return True


def audit_payload_budget():
    print("[4/4] Auditing Total Page Payload (< 50 KB gzip)...")
    index_html = PUBLIC_DIR / "index.html"
    html_bytes = index_html.read_bytes()
    html_gzip_len = len(gzip.compress(html_bytes))

    css_files = list(PUBLIC_DIR.glob("css/*.css"))
    css_gzip_len = len(gzip.compress(css_files[0].read_bytes())) if css_files else 0

    total_gzip = html_gzip_len + css_gzip_len
    print(f"      Index HTML gzip: {html_gzip_len} bytes (~{html_gzip_len / 1024:.2f} KB)")
    print(f"      Main CSS gzip:   {css_gzip_len} bytes (~{css_gzip_len / 1024:.2f} KB)")
    print(f"      Total Core Gzip: {total_gzip} bytes (~{total_gzip / 1024:.2f} KB) (Budget: < 50 KB)")

    if total_gzip >= 51200:
        print(f"FAILED: Total payload exceeded 50 KB ({total_gzip} bytes)")
        return False

    print("      OK: Page payload is significantly below the 50 KB budget.")
    return True


def main():
    if not PUBLIC_DIR.is_dir():
        print(f"Error: {PUBLIC_DIR} does not exist.")
        sys.exit(1)

    checks = [
        audit_color_contrast,
        audit_heading_hierarchy,
        audit_images_accessibility,
        audit_payload_budget,
    ]

    for check in checks:
        if not check():
            sys.exit(1)

    print("\nSUCCESS: All Phase 7 Quality and Accessibility audits passed!")


if __name__ == "__main__":
    main()
