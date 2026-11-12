#!/usr/bin/env bash
set -euo pipefail

PUBLIC_DIR="exampleSite/public"

if [ ! -d "$PUBLIC_DIR" ]; then
  echo "Error: $PUBLIC_DIR does not exist. Run 'hugo --themesDir ../.. -s exampleSite --gc --minify' first."
  exit 1
fi

echo "[1/6] Checking Zero JavaScript constraint..."
js_files=$(find "$PUBLIC_DIR" -type f -name "*.js")
if [ -n "$js_files" ]; then
  echo "FAILED: Found unauthorized JavaScript files: $js_files"
  exit 1
fi
echo "      OK: Zero JavaScript files emitted."

echo "[2/6] Checking CSS budget (< 10 KB)..."
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

echo "[3/6] Verifying Theme Visual Contract (CSS classes on posts)..."
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

  # Theme styling classes (used by _article.css)
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
echo "      OK: All $post_count post scenarios conform strictly to the Theme Visual Contract."

echo "[4/6] Verifying Canonical Instant View Contract (data-iv & meta fallbacks)..."
for post in "$posts_dir"/*; do
  [ -d "$post" ] || continue
  post_name=$(basename "$post")
  html_file="$post/index.html"

  # Canonical Instant View contract (data-iv)
  grep -Eq 'data-iv=["'\'']?article["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"article\""; exit 1; }
  grep -Eq 'data-iv=["'\'']?title["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"title\""; exit 1; }
  grep -Eq 'data-iv=["'\'']?author["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"author\""; exit 1; }
  grep -Eq 'data-iv=["'\'']?date["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"date\""; exit 1; }
  grep -Eq 'data-iv=["'\'']?body["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"body\""; exit 1; }

  # Open Graph fallback contract assertions
  grep -Eq '<meta[[:space:]]+property=["'\'']?og:title["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing og:title meta tag"; exit 1; }
  grep -Eq '<meta[[:space:]]+property=["'\'']?og:site_name["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing og:site_name meta tag"; exit 1; }
  grep -Eq '<meta[[:space:]]+name=["'\'']?telegram:channel["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing telegram:channel meta tag"; exit 1; }

  # Heading anchors must be ignored by Instant View
  if grep -Eq 'class=["'\'']?heading-anchor["'\'']?' "$html_file"; then
    grep -Eq 'data-iv=["'\'']?ignore["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Heading anchor missing data-iv=\"ignore\""; exit 1; }
  fi

  if [ "$post_name" = "post-with-cover" ]; then
    grep -Eq 'data-iv=["'\'']?cover["'\'']?' "$html_file" || { echo "FAILED: [post-with-cover] Missing data-iv=\"cover\""; exit 1; }
  fi

  if [ "$post_name" = "post-no-description" ]; then
    if grep -Eq 'data-iv=["'\'']?description["'\'']?' "$html_file"; then
      echo "FAILED: [post-no-description] Header should not render data-iv=\"description\""
      exit 1
    fi
  else
    grep -Eq 'data-iv=["'\'']?description["'\'']?' "$html_file" || { echo "FAILED: [$post_name] Missing data-iv=\"description\""; exit 1; }
  fi
done
echo "      OK: Canonical Instant View contract (data-iv) verified across all $post_count posts."

echo "[5/6] Checking static pages (Instant View exclusion)..."
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

  if grep -Eq 'data-iv=["'\'']?article["'\'']?' "$html_file"; then
    echo "FAILED: Static page [$page_name] contains data-iv=\"article\" (would trigger Instant View)"
    exit 1
  fi

  if ! grep -Eq '<article class=["'\'']?page["'\'']?[ >]' "$html_file"; then
    echo "FAILED: Static page [$page_name] missing <article class=\"page\">"
    exit 1
  fi
done
echo "      OK: Static pages correctly scoped under class 'page'."

echo "[6/6] Checking robots.txt, sitemap.xml, and RSS feeds..."
for f in "robots.txt" "sitemap.xml" "index.xml"; do
  if [ ! -f "$PUBLIC_DIR/$f" ]; then
    echo "FAILED: $f not generated."
    exit 1
  fi
done
echo "      OK: All metadata and feed files verified."

echo ""
echo "SUCCESS: All automated validation checks passed!"
