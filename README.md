# Traxsource2Youtube

<p align="center">
<img src="https://www.traxsource.com/logos-and-images/logo-standard-background.png" align="center" width="100%" height="100%">
</p>

This repo contains tools to scrape the latest Top-10 Charts from Traxsource and transfer them into a Youtube playlist. 

## Usage

The Youtube API has a quota of 10,000 units per day. As this fills up quite fast (at least with the current implementation), the scripts currently only enable creating the latest top-10 playlists of different genres. 

### GCP prerequisites
1. To use the Youtube API, it is necessary to have a Google Cloud Account (which must be linked to the Youtube account you want to use to create the playlists)
2. Create a new project in GCP
3. Enable "YouTube Data API v3" for this project
4. Create credentials selecting "OAuth client ID" and "Desktop App" as application type
6. Download the credentials and store them in the local directory of the project as "secrets_file.json"
5. Add yourself as a test user for the application in order to be able to authenticate later on (APIs & Services > OAuth consent screen)

### Package usage
First of all, install the package with `pip install .`

Then, run the desired script to scrape the tracks on 
Traxsource and to create the playlist on Youtube. For example, to get the newest charts for the genre [Minimal/Deeptech](https://www.traxsource.com/genre/16/minimal-deep-tech), the following command needs to be run:

```bash
python scripts/minimal_deeptech.py 
```

 If the code is run for the first time, a browser window will pop up, where you need to authenticate yourself. After that, another secrets file called "youtube_credentials".pickle" is created, which will be used for authentication for the following times. 

 Inside the scripts, the name and description of each playlist can be changed.

The script works in both cases, to newly create a playlist or to update an existing one with the newest track list.

