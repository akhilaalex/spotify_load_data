import base64
import requests
from dotenv import load_dotenv
import os 
import json
import boto3

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

ACCESS_KEY =os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
BUKET_NAME =os.getenv('BUKET_NAME')
REGION_NAME = os.getenv('REGION_NAME')
OBJECT_NAME =os.getenv('OBJECT_NAME')
# LOCAL_FILE_PATH =os.getenv('LOCAL_FILE_PATH')
LOCAL_FILE_PATH = r"C:\Users\Akhila\Desktop\epertslab\spotify_project\spotify_load_data\new_data.json"


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
# Url is This is Spotify's token endpoint - the URL where you request acces
# s tokens # Headers are used for Tells Spotify who you are , Basic indicates we're using Basic Authentication # Data : Tells Spotify which OAuth flow you're using, client_credentials means: "I'm an app requesting access # to public data" (not user-specific data)


# ltest release in spotify
# =========================
# Fetch Spotify new releases
# =========================
def get_new_releases():
    try:
        token = access_token()
        if not token:
            return []

        headers = {'Authorization': f'Bearer {token}'}
        params = {'limit': 50}

        response = requests.get(
            'https://api.spotify.com/v1/browse/new-releases',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()

        releases = []
        for album in data['albums']['items']:
            releases.append({
                'album_name': album.get('name'),
                'artist_name': album['artists'][0].get('name'),
                'release_date': album.get('release_date'),
                'album_type': album.get('album_type'),
                'total_tracks': album.get('total_tracks'),
                'spotify_url': album['external_urls'].get('spotify'),
                'album_image': album['images'][0].get('url') if album['images'] else None
            })

        # Save locally
        with open(LOCAL_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(releases, f, indent=2)

        print(f"✅ Spotify JSON saved locally at {LOCAL_FILE_PATH}")
        return releases

    except Exception as e:
        print("❌ Error fetching Spotify data:", e)
        return []

data= get_new_releases()
print(json.dumps(data, indent=2))


def upload_data_to_s3():
    try:
        S3_client = boto3.client(service_name="s3",
                 region_name = REGION_NAME,
                 aws_access_key_id = ACCESS_KEY,
                 aws_secret_access_key = ACCESS_SECRET)
        S3_client.upload_file(LOCAL_FILE_PATH,BUKET_NAME,OBJECT_NAME)
        print("Uploaded file successfully......")

    except Exception as e:
        print("failed to upload file in s3",e)


upload_data_to_s3()