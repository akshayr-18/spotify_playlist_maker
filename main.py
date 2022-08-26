from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID="68a3d164db8046159b8209b331caddd2"
SPOTIPY_CLIENT_SECRET="c2d7e530a43b489791c92e1225a95560"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date=input("Type the date in YYYY-MM-DD format : ")
billboard_response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
bsoup=BeautifulSoup(billboard_response.text,"html.parser")
temp=bsoup.find_all(name="li",class_="lrv-u-width-100p")
titles=[]
for i in temp:
    title=i.find('h3')
    if title!=None:
        titles.append(title.getText().strip())
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
