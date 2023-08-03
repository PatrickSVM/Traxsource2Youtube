import requests
from bs4 import BeautifulSoup


def get_top_10(URL):
    """
    Function that takes Traxsource URL for top-10
    list and return the list of track titles and
    artists (sorted from 1 to 10)
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    top10 = soup.find_all("div", {"class": "top-item"})

    top10_title = []
    top10_artist = []

    for track_node in top10:
        # Get position of the track
        position = track_node.findAll("div", {"class": "ttib position"})[0].getText()
        position = position.replace("\n", "").strip()

        # Get track infos
        info = track_node.findAll("div", {"class": "ttib info"})[0]
        artist = info.find("a", class_="com-artists").text
        title = info.find("a", class_="com-title").text

        # Add infos
        top10_title.append(title)
        top10_artist.append(artist)

    return top10_title, top10_artist


def get_top_100(URL, n_res=25):
    """
    Same functionality as get_top_10 but for a
    top-100 URL on Traxsource.

    n_res controls how many results are returned.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    top100 = soup.find_all("div", {"class": "trk-row"})

    top100_title = []
    top100_artist = []

    for track in top100[1 : n_res + 1]:
        # Get position of the track
        pos = track.find("div", {"class": "tnum-pos"}).text.replace("\n", "").strip()

        # Get artist infos
        artists = track.find("div", {"class": "artists"}).findChildren("a")
        artists = [art.text for art in artists]
        full_artist = " ".join(artists)

        # Get title info
        title = track.find("div", {"class": "title"}).findChildren("a")[0].text

        # Add infos
        top100_title.append(title)
        top100_artist.append(full_artist)

    return top100_title, top100_artist
