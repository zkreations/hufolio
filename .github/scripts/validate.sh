#!/usr/bin/env bash
set -euo pipefail

PUBLIC_DIR="exampleSite/public"

if [ ! -d "$PUBLIC_DIR" ]; then
  echo "Error: $PUBLIC_DIR does not exist. Run 'hugo --themesDir ../.. -s exampleSite --gc --minify' first."
  exit 1
fi

echo "[1/5] Checking Zero JavaScript constraint..."
js_files=$(find "$PUBLIC_DIR" -type f -name "*.js")
if [ -n "$js_files" ]; then
  echo "FAILED: Found unauthorized JavaScript files: $js_files"
  exit 1
fi
echo "      OK: Zero JavaScript files emitted."

echo "[2/5] Checking CSS budget (< 10 KB)..."
css_count=0
for css in "$PUBLIC_DIR"/css/*.css; do
  [ -e "$css" ] || continue
  css_count=$((css_count + 1))
  size=$(wc -c < "$css" | tr -d ' ')
  echo "      Bundle: $(basename "$css") ($size bytes)"
  if [ "$size" -ge 10240 ]; then
    echo "FAILED: CSS bundle exceeds 10 KB budget ($size >= 10240 bytes)"
    exit 1
  fi
done
if [ "$css_count" -eq 0 ]; then
  echo "FAILED: No CSS bundle found in $PUBLIC_DIR/css/"
  exit 1
fi
echo "      OK: CSS bundle is within ultralight budget."

echo "[3/5] Verifying HTML Contract and XPath selectors on posts..."
posts_dir="$PUBLIC_DIR/posts"
if [ ! -d "$posts_dir" ]; then
  echo "FAILED: Posts directory not found at $posts_dir"
  exit 1
fi

post_count=0
for post in "$posts_dir"/*; do
  [ -d "$post" ] || continue
  post_name=$(basename "$post")
  html_file="$post/index.html"
  if [ ! -f "$html_file" ]; then
    echo "FAILED: Missing index.html in $post"
    exit 1
  fi
  post_count=$((post_count + 1))

  # Contract element assertions (supports both minified and unminified attribute quotes)
  grep -Eq '<article class=["'\'']?article["'\'']?[ >]' "$html_file" || { echo "FAILED: [$post_name] Missing <article class=\"article\">"; exit 1; }
  grep -Eq '<h1 class=["'\'']?article-title["'\'']?[ >]' "$html_file" || { echo "FAILED: [$post_name] Missing <h1 class=\"article-title\">"; exit 1; }
  grep -Eq '<span class=["'\'']?article-author["'\'']?[ >]' "$html_file" || { echo "FAILED: [$post_name] Missing <span class=\"article-author\">"; exit 1; }
  grep -Eq '<time class=["'\'']?article-date["'\'']?[[:space:]]+datetime=' "$html_file" || { echo "FAILED: [$post_name] Missing <time class=\"article-date\"> with datetime"; exit 1; }
  grep -Eq '<div class=["'\'']?article-body["'\'']?[ >]' "$html_file" || { echo "FAILED: [$post_name] Missing <div class=\"article-body\">"; exit 1; }
  grep -Eq '<header class=["'\'']?article-header["'\'']?>' "$html_file" || { echo "FAILED: [$post_name] Missing article-header"; exit 1; }

  if [ "$post_name" = "post-with-cover" ]; then
    grep -Eq '<figure class=["'\'']?article-cover.*["'\'']?>[[:space:]]*<img[[:space:]]+src=' "$html_file" || { echo "FAILED: [post-with-cover] Missing cover figure"; exit 1; }
  fi

  if [ "$post_name" = "post-no-description" ]; then
    header_content=$(sed -n '/<header class=["'\'']\?article-header["'\'']\?>/,/<\/header>/p' "$html_file")
    if echo "$header_content" | grep -Eq '<p class=["'\'']?article-description["'\'']?>'; then
      echo "FAILED: [post-no-description] Header should not render <p class=\"article-description\">"
      exit 1
    fi
  fi
done

if [ "$post_count" -eq 0 ]; then
  echo "FAILED: No generated post directories found."
  exit 1
fi
echo "      OK: All $post_count post scenarios conform strictly to the HTML Contract."

echo "[4/5] Checking static pages (Instant View exclusion)..."
for page_name in "about" "static-page-about"; do
  html_file="$PUBLIC_DIR/$page_name/index.html"
  if [ ! -f "$html_file" ]; then
    echo "FAILED: Static page index not found at $html_file"
    exit 1
  fi

  if grep -Eq '<article class=["'\'']?article["'\'']?[ >]' "$html_file"; then
    echo "FAILED: Static page [$page_name] contains class 'article' (would trigger Instant View)"
    exit 1
  fi

  if ! grep -Eq '<article class=["'\'']?page["'\'']?[ >]' "$html_file"; then
    echo "FAILED: Static page [$page_name] missing <article class=\"page\">"
    exit 1
  fi
done
echo "      OK: Static pages correctly scoped under class 'page'."

echo "[5/5] Checking robots.txt, sitemap.xml, and RSS feeds..."
for f in "robots.txt" "sitemap.xml" "index.xml"; do
  if [ ! -f "$PUBLIC_DIR/$f" ]; then
    echo "FAILED: $f not generated."
    exit 1
  fi
done
echo "      OK: All metadata and feed files verified."

echo ""
echo "SUCCESS: All automated validation checks passed!"
