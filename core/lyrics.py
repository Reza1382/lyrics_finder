from core.web import fetch_page


def get_lyrics(artist_name, song_name):
    url = build_lyricskid_url(artist_name, song_name)
    html = fetch_page(url)

    if html:
        lyrics = extract_lyrics_from_meta(html)
        return lyrics if lyrics else f"Lyrics for '{song_name}' not found yet! 😊"
    else:
        return "Couldn't fetch the page."


def extract_lyrics_from_meta(html):
    try:
        marker = '<META name="description" content="'

        # Finding the start of div
        start_index = html.find(marker)
        if start_index == -1:
            return None

        # Finding the ending of div
        end_index = html.find('"', start_index + len(marker))
        if end_index == -1:
            return None

        # Getting the text between teo tags
        lyrics_html = html[start_index + len(marker) : end_index]

        # Replacing the '<br>' by '\n'
        lyrics_text = lyrics_html.strip()

        return lyrics_text
    except Exception as e:
        print(f"Error extracting lyrics: {e}")
        return None


def extract_lyrics_from_genius(html):
    try:
        marker = (
            '<META name="description" content="'  # TODO : write the marker of genius.
        )

        # Finding the start of div
        start_index = html.find(marker)
        if start_index == -1:
            return None

        # Finding the ending of div
        end_index = html.find('"', start_index + len(marker))
        if end_index == -1:
            return None

        # Getting the text between teo tags
        lyrics_html = html[start_index + len(marker) : end_index]

        # Replacing the '<br>' by '\n'
        lyrics_text = lyrics_html.strip()

        return lyrics_text
    except Exception as e:
        print(f"Error extracting lyrics: {e}")
        return None


def clean_lyrics(text):
    import html as html_lib

    text = html_lib.unescape(text)

    # Removing empty lines
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Removing the first line if it contains "from" and similar to our title
    if len(cleaned_lines) > 0 and "from" in cleaned_lines[0].lower():
        cleaned_lines = cleaned_lines[1:]

    return "\n".join(cleaned_lines)


def build_lyricskid_url(artist, song_input):
    artist_text = artist.lower().strip()
    song_text = song_input.lower().strip()

    allowed_char = "abcdefghijklmnopqrstuvwxyz0123456789 "
    artist_name = "".join([c for c in artist_text if c in allowed_char])
    song_name = "".join([c for c in song_text if c in allowed_char])

    artist_part = artist_name.split()
    song_part = song_name.split()

    artist = "-".join(artist_part)
    song = "-".join(song_part)

    url = f"https://lyricskid.com/lyrics/{artist}-lyrics/{song}-lyrics.html"

    return url


# url = build_lyricskid_url("Taylor Swift", "Love Story")
# print(url)
