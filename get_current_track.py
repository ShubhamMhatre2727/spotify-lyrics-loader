import requests, json
from generate_auth_token import generate_token

def get_track():
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    # Read the access token from token.json
    with open('auth_token.json') as f:
        data = json.load(f)
        access_token = data['access_token']
        header = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=header)
    if(response.status_code == 200):
        if(response.json()['currently_playing_type'] == "ad"): return {"currently_playing_type": response.json()['currently_playing_type']}

        return {
        "name": response.json()["item"]["name"],
        "artist": response.json()["item"]["artists"][0]["name"],
        "progress": (response.json()["progress_ms"]) / 1000,
        "duration": (response.json()["item"]["duration_ms"]) / 1000,
        "currently_playing_type": response.json()['currently_playing_type']
    }
    else:
        if (response.status_code == 401 and response.json()['error']['message'] == "The access token expired"):
            generate_token()
        else:
            print(f"Error: {response.status_code}")
            return None