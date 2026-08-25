#!/usr/bin/env python3
"""
Sync the shared header and footer from index.html into the sub-pages.

index.html is the single source of truth for site chrome. Edit the nav or the
footer there, run this, and shop.html / checkout.html pick up the change —
their own <main> content is left untouched.

    python3 tools/sync-chrome.py
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBPAGES = {"shop.html": "shop", "checkout.html": "checkout"}

HEADER_START = "<!-- ============ HEADER ============ -->"
HEADER_END   = '<main id="main"'
FOOTER_START = "<!-- ============ FOOTER ============ -->"
FOOTER_END   = "</footer>"


def slice_block(html, start, end, include_end=False):
    i = html.index(start)
    j = html.index(end, i)
    if include_end:
        j += len(end)
    return i, j, html[i:j]


def localise(block, current):
    """Same-page anchors must point back at the home page from a sub-page."""
    block = block.replace('href="#', 'href="index.html#')
    if current == "shop":
        block = block.replace('<a href="shop.html">Shop</a>',
                              '<a href="shop.html" aria-current="page">Shop</a>')
    return block


def main():
    index = open(os.path.join(ROOT, "index.html")).read()
    _, _, header = slice_block(index, HEADER_START, HEADER_END)
    _, _, footer = slice_block(index, FOOTER_START, FOOTER_END, include_end=True)

    for page, current in SUBPAGES.items():
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            print("skip (missing): " + page); continue
        html = open(path).read()
        hi, hj, _ = slice_block(html, HEADER_START, HEADER_END)
        html = html[:hi] + localise(header, current) + html[hj:]
        fi, fj, _ = slice_block(html, FOOTER_START, FOOTER_END, include_end=True)
        html = html[:fi] + localise(footer, current) + html[fj:]
        open(path, "w").write(html)
        print("synced: " + page)


if __name__ == "__main__":
    sys.exit(main())
