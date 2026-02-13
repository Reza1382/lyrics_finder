from core.lyrics import get_lyrics, clean_lyrics


def run_cli():
    song_name = input("Enter song name: ")
    lyrics = get_lyrics(song_name)
    print("\nLyrics Result:\n")
    print(clean_lyrics(lyrics))
