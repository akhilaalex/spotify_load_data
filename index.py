import base64
import requests
from dotenv import load_dotenv
import os 
import json
import boto3

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# create a token for spotify
def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        response = requests.post(
            url='https://accounts.spotify.com/api/token',
            headers={'Authorization': f'Basic {encoded_credentials}'},
            data={'grant_type': 'client_credentials'}
        )

        # # Check if the request succeeded
        # if response.status_code != 200:
        #     print("Error:", response.text)
        #     return None
        #
        # token = response.json()['access_token']
        # return token
        print("token generated successfully")
        return response.json()['access_token']


    except Exception as e:
        print("error in token generation ")



print(access_token())

# combine client id and client_secret
# Converts the credentials string into base64 format,
# This is required for HTTP Basic Authentication
# Url is This is Spotify's token endpoint - the URL where you request access tokens # Headers are used for Tells Spotify who you are , Basic indicates we're using Basic Authentication # Data : Tells Spotify which OAuth flow you're using, client_credentials means: "I'm an app requesting access # to public data" (not user-specific data)


# ltest release in spotify

def get_new_relaese():
   try:
       token = access_token()
       headers = {'Authorization': f'Bearer {token}'}
       Param = {'limit': 50}
       response = requests.get('https://api.spotify.com/v1/browse/new-releases',
                               headers=headers,
                               params=Param)

       # Check if the request succeeded
       if response.status_code == 200:
           data = response.json()
           releases = []
           albums = data['albums']['items']
           for album in albums:
               info = {
                   'album_name': album['name'],
                   'artist_name' : album['artists'][0]['name'],
                   'release_date' : album['release_date'],
                   'album_type' : album['album_type'],
                   'total_tracks' : album['total_tracks'],
                   'spotify_url' : album['external_urls']['spotify'],
                   'album_image' : album['images'][0]['url'] if album['images'] else None


               }
               print(json.dumps(info, indent=2))
               print("*" *30)
               # releases.append(a)
            # print(releases)
           # print(response.json())


   except Exception as e:
       print("error in latest release data fetching from spotify")


get_new_relaese()
