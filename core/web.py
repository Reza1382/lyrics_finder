import urllib.request


def fetch_page(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            html_bytes = response.read()
            html_text = html_bytes.decode("utf-8", errors="ignore")
            return html_text
    except Exception as e:
        print(f"Error fetching page: {e}")
        return None


url = "https://www.musixmatch.com/lyrics/Taylor-Swift/love-story-1"
html = fetch_page(url)
if html:
    with open("debug_musixmatch.html", "w", encoding="utf-8") as f:
        f.write(html)
else:
    print("HTML is None. Error fetching page !!")

# https://genius.com/Ed-sheeran-perfect-lyrics
# https://genius.com/Taylor-swift-love-story-lyrics
# https://magerta.ir/entertainment/music/lyrics-translation-love-story-taylor-swift/
# https://musiclyrics.com/taylor-swift/love-story-lyrics/
