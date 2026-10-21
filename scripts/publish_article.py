#!/usr/bin/env python3
"""Publish an X article to dinoilievski.com.

Usage:
    python3 scripts/publish_article.py <x-status-url-or-id> [--promote "Section heading"]...
                                        [--description "..."] [--index-desc "..."]

Fetches the full article via the FxTwitter API (no X auth needed), renders a
plain static page under writing/, and inserts the entry into the homepage
Writing list, sitemap.xml, and llms.txt. Idempotent: re-running for an
already-published article changes nothing.

Then commit + push (or let the Publish Article GitHub Action do it) and
Vercel deploys.
"""

import argparse
import html
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.dinoilievski.com"
AUTHOR_HANDLE = "realkdi"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%%TITLE%% — Dino Ilievski</title>
  <meta name="description" content="%%DESCRIPTION%%">
  <link rel="canonical" href="%%CANONICAL%%">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <meta property="og:title" content="%%TITLE%%">
  <meta property="og:description" content="%%DESCRIPTION%%">
  <meta property="og:type" content="article">
  <meta property="og:url" content="%%CANONICAL%%">
  <meta property="og:image" content="https://www.dinoilievski.com/og.png">
  <meta property="article:published_time" content="%%DATE_ISO%%">
  <meta property="article:author" content="Dino Ilievski">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%%TITLE%%">
  <meta name="twitter:description" content="%%DESCRIPTION%%">
  <meta name="twitter:image" content="https://www.dinoilievski.com/og.png">
  <meta name="author" content="Dino Ilievski">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <script type="application/ld+json">
%%JSON_LD%%
  </script>
  <style>
    :root {
      --bg: #FBF9F5;
      --ink: #1C1A17;
      --ink-soft: #5C574F;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    html {
      background: var(--bg);
    }

    body {
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, system-ui, sans-serif;
      font-size: 17px;
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }

    a {
      color: inherit;
      text-decoration-thickness: 1px;
      text-underline-offset: 0.18em;
    }

    a:focus-visible {
      outline: 1px solid var(--ink);
      outline-offset: 4px;
    }

    .wrap {
      max-width: 34rem;
      margin: 0 auto;
      padding: 0 28px;
    }

    .header-inner {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 20px 32px;
      flex-wrap: wrap;
      padding: 48px 0 0;
    }

    .brand {
      font-family: Newsreader, Georgia, serif;
      font-size: 1.35rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      text-decoration: none;
    }

    .socials {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 22px;
      list-style: none;
    }

    .socials a {
      font-size: 0.9rem;
      color: var(--ink-soft);
      text-decoration: none;
    }

    .socials a:hover {
      color: var(--ink);
    }

    main.wrap {
      padding: 5rem 28px 4.5rem;
    }

    .kicker {
      margin-bottom: 0.85rem;
      font-size: 0.95rem;
      color: var(--ink-soft);
    }

    .kicker a {
      text-decoration: none;
    }

    .kicker a:hover {
      color: var(--ink);
    }

    h1 {
      font-family: Newsreader, Georgia, serif;
      font-size: 2rem;
      font-weight: 500;
      letter-spacing: -0.025em;
      line-height: 1.25;
    }

    .byline {
      margin-top: 1rem;
      font-size: 0.9rem;
      color: var(--ink-soft);
    }

    .article-body {
      margin-top: 2.5rem;
      font-family: Newsreader, Georgia, serif;
      font-size: 1.13rem;
      line-height: 1.75;
    }

    .article-body p + p {
      margin-top: 1.4rem;
    }

    .article-body ol,
    .article-body ul {
      margin: 1.4rem 0 0 1.4rem;
    }

    .article-body li + li {
      margin-top: 0.5rem;
    }

    .article-body h2 {
      margin: 2.6rem 0 1rem;
      font-size: 1.45rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1.3;
    }

    .article-footer {
      margin-top: 3.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid #E8E4D9;
      font-family: Inter, system-ui, sans-serif;
      font-size: 0.95rem;
      color: var(--ink-soft);
    }

    .article-footer p + p {
      margin-top: 0.6rem;
    }

    @media (max-width: 600px) {
      .header-inner {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        padding-top: 32px;
      }

      main.wrap {
        padding-top: 3.5rem;
        padding-bottom: 4.5rem;
      }

      h1 {
        font-size: 1.7rem;
      }
    }
  </style>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="../index.html">Dino Ilievski</a>
      <ul class="socials">
        <li><a href="mailto:dino.ilievski@gmail.com">dino.ilievski@gmail.com</a></li>
        <li><a href="https://calendar.app.google/ZNhWDkPHRFbm629B9" target="_blank" rel="noopener">Book time</a></li>
        <li><a href="https://x.com/realkdi" target="_blank" rel="noopener">X</a></li>
        <li><a href="https://linkedin.com/in/realkdi" target="_blank" rel="noopener">LinkedIn</a></li>
      </ul>
    </div>
  </header>

  <main class="wrap">
    <article>
      <p class="kicker"><a href="../index.html#writing">Writing</a></p>
      <h1>%%TITLE%%</h1>
      <p class="byline">By Dino Ilievski · <time datetime="%%DATE_ISO%%">%%DATE_LABEL%%</time></p>

      <div class="article-body">
%%BODY%%
      </div>

      <footer class="article-footer">
        <p>Originally published on <a href="%%X_URL%%" target="_blank" rel="noopener">X</a>.</p>
        <p><a href="../index.html#writing">More writing</a> · <a href="../index.html">Dino Ilievski</a> — Building Ancha.</p>
      </footer>
    </article>
  </main>
</body>
</html>
"""


def slugify(title: str) -> str:
    slug = title.lower().replace("'", "").replace("\u2019", "")
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def truncate(text: str, limit: int = 300) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text.rfind(". ", 0, limit)
    return text[: cut + 1] if cut > 80 else text[:limit].rsplit(" ", 1)[0] + "…"


def render_body(blocks, promote):
    out, open_list = [], None
    for block in blocks:
        text = html.escape(block["text"])
        list_tag = {"ordered-list-item": "ol", "unordered-list-item": "ul"}.get(block["type"])
        if list_tag:
            if open_list != list_tag:
                if open_list:
                    out.append(f"        </{open_list}>")
                out.append(f"        <{list_tag}>")
                open_list = list_tag
            out.append(f"          <li>{text}</li>")
            continue
        if open_list:
            out.append(f"        </{open_list}>")
            open_list = None
        if block["type"] == "header-two" or block["text"] in promote:
            out.append(f"        <h2>{text}</h2>")
        elif block["type"] == "header-three":
            out.append(f"        <h3>{text}</h3>")
        elif block["type"] == "blockquote":
            out.append(f"        <blockquote><p>{text}</p></blockquote>")
        else:
            out.append(f"        <p>{text}</p>")
    if open_list:
        out.append(f"        </{open_list}>")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("status", help="X status URL or ID, e.g. https://x.com/realkdi/status/123…")
    parser.add_argument("--promote", action="append", default=[],
                        help="Plain paragraph text to render as an <h2> (repeatable)")
    parser.add_argument("--description", help="Meta description (default: excerpt of first paragraph)")
    parser.add_argument("--index-desc", help="One-liner under the homepage title (default: article preview)")
    args = parser.parse_args()

    match = re.search(r"(\d{10,})", args.status)
    if not match:
        print("Could not find a status ID in the input.", file=sys.stderr)
        return 1
    status_id = match.group(1)

    with urllib.request.urlopen(f"https://api.fxtwitter.com/status/{status_id}") as resp:
        data = json.load(resp)
    tweet = data.get("tweet") or {}
    article = tweet.get("article")
    if not article:
        print(f"Status {status_id} has no article attached.", file=sys.stderr)
        return 1
    if (tweet.get("author") or {}).get("screen_name") != AUTHOR_HANDLE:
        print(f"Refusing: author is not @{AUTHOR_HANDLE}.", file=sys.stderr)
        return 1

    title = article["title"]
    slug = slugify(title)
    page_path = ROOT / "writing" / f"{slug}.html"

    created = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
    local = created.astimezone(ZoneInfo("America/Los_Angeles"))
    date_iso = local.strftime("%Y-%m-%d")
    date_label = f"{local.strftime('%b')} {local.day}, {local.year}"

    index_path = ROOT / "index.html"
    index = index_path.read_text()
    if f"writing/{slug}.html" in index and page_path.exists():
        print(f"Already published: {title} ({date_label}) — nothing to do.")
        return 0

    blocks = article["content"]["blocks"]
    description = args.description or truncate(blocks[0]["text"])
    index_desc = args.index_desc or truncate(article.get("preview_text") or blocks[0]["text"], 160)
    canonical = f"{SITE}/writing/{slug}.html"
    x_url = f"https://x.com/realkdi/status/{status_id}"

    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": date_iso,
        "dateModified": date_iso,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "url": canonical,
        "author": {
            "@type": "Person",
            "name": "Dino Ilievski",
            "url": f"{SITE}/",
            "sameAs": ["https://x.com/realkdi", "https://linkedin.com/in/realkdi"],
        },
        "publisher": {"@type": "Person", "name": "Dino Ilievski", "url": f"{SITE}/"},
        "isBasedOn": x_url,
    }, indent=4)

    page = (PAGE_TEMPLATE
            .replace("%%TITLE%%", html.escape(title))
            .replace("%%DESCRIPTION%%", html.escape(description, quote=True))
            .replace("%%CANONICAL%%", canonical)
            .replace("%%DATE_ISO%%", date_iso)
            .replace("%%DATE_LABEL%%", date_label)
            .replace("%%X_URL%%", x_url)
            .replace("%%JSON_LD%%", json_ld)
            .replace("%%BODY%%", render_body(blocks, set(args.promote))))
    page_path.parent.mkdir(exist_ok=True)
    page_path.write_text(page)
    print(f"Wrote {page_path.relative_to(ROOT)}")

    # Homepage: newest first, right after <ul class="articles">
    li = f"""        <li>
          <a href="writing/{slug}.html">
            <span class="article-title">{html.escape(title, quote=False)}</span>
            <span class="article-desc">{html.escape(index_desc, quote=False)}</span>
            <time datetime="{date_iso}">{date_label}</time>
          </a>
        </li>
"""
    index, n = re.subn(r'(<ul class="articles">\n)', r"\1" + li, index, count=1)
    if n:
        index_path.write_text(index)
        print("Updated index.html")

    # Sitemap: after the homepage <url> block
    sitemap_path = ROOT / "sitemap.xml"
    sitemap = sitemap_path.read_text()
    if canonical not in sitemap:
        entry = f"""  <url>
    <loc>{canonical}</loc>
    <lastmod>{date_iso}</lastmod>
  </url>
"""
        sitemap, n = re.subn(r"(</url>\n)", r"\1" + entry, sitemap, count=1)
        if n:
            sitemap_path.write_text(sitemap)
            print("Updated sitemap.xml")

    # llms.txt: first entry under "## Writing"
    llms_path = ROOT / "llms.txt"
    llms = llms_path.read_text()
    if canonical not in llms:
        entry = f"- [{title}]({canonical}) ({date_label}): {index_desc}\n"
        llms, n = re.subn(r"(## Writing\n(?:.*\n)*?)(\n- \[)", r"\1" + entry + r"\2", llms, count=1)
        if not n:  # no entries yet
            llms, n = re.subn(r"(## Writing\n)", r"\1\n" + entry, llms, count=1)
        if n:
            llms_path.write_text(llms)
            print("Updated llms.txt")

    print(f"Published: {title} ({date_label}) -> {canonical}")
    print("Review, then commit + push to deploy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
