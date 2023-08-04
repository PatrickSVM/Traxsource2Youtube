from traxsource2youtube.youtube import update_top10_playlist, get_authenticated_service

if __name__ == "__main__":
    url = "https://www.traxsource.com/genre/17/nu-disco-indie-dance"
    name = "Nu Disco / Indie Dance - Top 10 Charts on Traxsource"
    desc = (
        "Playlist with the latest Nu Disco / Indie Dance - Top 10 Charts on Traxsource"
    )

    # Get authenticated client
    client = get_authenticated_service()

    # Update the playlist
    update_top10_playlist(url=url, name=name, description=desc, client=client)
