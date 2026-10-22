import sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 1280
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': w, 'height': 900})
    pg.goto(url); pg.wait_for_timeout(1500)
    pg.screenshot(path=out, full_page='--full' in sys.argv)
    b.close()
