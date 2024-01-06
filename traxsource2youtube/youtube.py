import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery

from time import sleep
from traxsource2youtube.traxsource import get_top_10


def get_authenticated_service():
    """
    Helper function to authenticate with the YouTube API.
    """

    # Define the necessary scopes required for the YouTube Data API v3
    scopes = ["https://www.googleapis.com/auth/youtube"]

    # Load or create credentials file (store it in a file for future use)
    credentials_file = "youtube_credentials.pickle"

    if os.path.exists(credentials_file):
        with open(credentials_file, "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "secrets_file.json", scopes
        )
        credentials = flow.run_local_server(port=0)

        with open(credentials_file, "wb") as token:
            pickle.dump(credentials, token)

    # Create and return the authenticated YouTube Data API service
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def get_video_info(video_id, client):
    """
    Function that extracts and prints inforamtion about
    a video with id video_id.
    """
    try:
        # Call the videos().list() method to get video information
        video_info = (
            client.videos()
            .list(
                part="snippet,statistics",
                id=video_id,
            )
            .execute()
        )

        # Extract the relevant information from the response
        video_title = video_info["items"][0]["snippet"]["title"]
        video_description = video_info["items"][0]["snippet"]["description"]
        view_count = video_info["items"][0]["statistics"]["viewCount"]
        like_count = video_info["items"][0]["statistics"]["likeCount"]

        # Print or return the information as needed
        print(f"Video Title: {video_title}")
        print(f"Video Description: {video_description}")
        print(f"Views: {view_count}")
        print(f"Likes: {like_count}")

    except Exception as e:
        print(f"Error: {e}")


def get_song_id(name, client):
    """
    Function that searches for videos with the provided
    name and returns the id of the top ranked video.
    """
    try:
        # Call the search().list() method to search for videos
        search_response = (
            client.search()
            .list(q=name, part="snippet", type="video", maxResults=1, safeSearch="none")
            .execute()
        )

        if search_response["pageInfo"]["totalResults"] == 0:
            return None
        
        # Extract video ID of the first
        for search_result in search_response.get("items", []):
            video_id = search_result["id"]["videoId"]
            video_title = search_result["snippet"]["title"]
            video_description = search_result["snippet"]["description"]

        return video_id

    except Exception as e:
        print(f"Error: {e}")


def get_playlist_ids(client, print_infos=False):
    """
    Function that prints all playlist titles and
    IDs for the authenticated youtube account.
    """
    try:
        # Call the playlists().list() method to get playlists associated with the authenticated user
        playlist_response = (
            client.playlists()
            .list(
                part="id,snippet",
                mine=True,
                maxResults=50,  # Set the maximum number of playlists to retrieve (default is 5)
            )
            .execute()
        )

        playlist_infos = {}

        # Extract and display the playlist IDs
        for playlist in playlist_response.get("items", []):
            playlist_id = playlist["id"]
            playlist_title = playlist["snippet"]["title"]

            playlist_infos[playlist_title] = playlist_id

            if print_infos:
                print(f"Playlist ID: {playlist_id}")
                print(f"Playlist Title: {playlist_title}")
                print()

        return playlist_infos

    except Exception as e:
        print(f"Error: {e}")


def create_playlist(playlist_title, playlist_description, client):
    """
    Function that creates a new playlist according
    to the provided name and description. The ID of
    the new playlist is returned.
    """
    try:
        # Call the playlists().insert() method to create a new playlist
        playlist_response = (
            client.playlists()
            .insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": playlist_title,
                        "description": playlist_description,
                    },
                    "status": {
                        "privacyStatus": "public",  # Set the privacy status ("public", "private", or "unlisted")
                    },
                },
            )
            .execute()
        )

        # Extract and display the playlist ID of the newly created playlist
        playlist_id = playlist_response["id"]
        print(f"New playlist created with ID: {playlist_id}")

        return playlist_id

    except Exception as e:
        print(f"Error: {e}")


def add_video_to_playlist(playlist_id, video_id, client):
    """
    Function to add a video to a playlist.
    """

    # Add the video to the playlist
    request = client.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    )

    response = request.execute()


def add_multiple_videos_to_playlist(playlist_id, video_ids, client):
    """
    Function to add multiple videos at once to a playlist.
    This method is more efficient in terms of api quota.

    !!!This does not seem to work properly.!!!
    """
    try:
        # Create a batch request object
        batch = client.new_batch_http_request()

        # Add each video ID to the batch request
        for video_id in video_ids:
            request = client.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            )
            resp = batch.add(request)
            print(resp)

        # Execute the batch request
        batch.execute()

        print(f"{len(video_ids)} videos have been added to the playlist.")

    except Exception as e:
        print(f"An HTTP error occurred: {e}")


def update_top10_playlist(url, name, description, client):
    # Check if playlist exists or whether it needs to be created
    playlist_dict = get_playlist_ids(client=client, print_infos=False)

    if name in playlist_dict:
        # Exists - delete it
        client.playlists().delete(id=playlist_dict[name]).execute()
        print(f"Playlist '{name}' has been deleted.\n")

    # Create playlist
    playlist_id = create_playlist(
        playlist_title=name, playlist_description=description, client=client
    )

    # Retrieve songs
    titles, artists = get_top_10(URL=url)

    print("\n\nAdding the following tracks:\n")

    for title, artist in zip(titles, artists):
        # Get video id of top result
        query = f"{artist} - {title}"
        video_id = get_song_id(name=query, client=client)

        if video_id is None:
            print("Song is skipped, no API results - it is too fresh!/n")
            continue

        # Add video to playlist
        try:
            add_video_to_playlist(playlist_id=playlist_id, video_id=video_id, client=client)
            print(f"{title} - {artist}\n")
        except Exception as e:
            print(f"Video is skipped as error occured. Related query: {title=} and {artist=}\n")


        # Sleep for one second
        sleep(1)

    print("All tracks successfully added.\n")
    print(f"Playlist '{name}' is up to date!\n")
