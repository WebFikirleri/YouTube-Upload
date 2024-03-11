import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm
import json
import argparse

def get_authenticated_service():

    client_secrets_file = "client_secrets.json"
    
    if not os.path.isfile(client_secrets_file):
        print(f"Sorry, I can't find the file '{client_secrets_file}'!")
        print("For more information, please read the README: https://github.com/WebFikirleri/YouTube-Upload/blob/main/README.md")
        exit()
    
    credentials_file = "credentials.json"

    api_service_name = "youtube"
    api_version = "v3"

    scopes = ["https://www.googleapis.com/auth/youtube.upload","https://www.googleapis.com/auth/youtube.force-ssl"]
    
    credentials = None
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(json.load(f))

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server()

        with open(credentials_file, 'w') as f:
            f.write(json.dumps({
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }))

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube

def list_categories(youtube, region_code):
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=region_code
    )
    response = request.execute()

    for item in response["items"]:
        print(f'ID: {item["id"]}, Title: {item["snippet"]["title"]}')

def upload_video(youtube, file, title, description, category, tags, defaultLanguage):
    tags = tags.split(',')
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category,
                "description": description,
                "title": title,
                "tags": tags,
                "defaultLanguage": defaultLanguage
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(file, chunksize=1024*1024, resumable=True)
    )

    response = None
    file_size = os.path.getsize(file)
    pbar = tqdm(desc='Uploading', total=file_size, unit='B', unit_scale=True)
    while response is None:
        status, response = request.next_chunk()
        if status:
            #print(f"File Size: {file_size} | Progress: {status.resumable_progress}")
            #pbar.update(int(status.resumable_progress))
            pbar.update(1024*1024)
    pbar.close()

    print("Upload Complete!")

def main():
    parser = argparse.ArgumentParser(prog="ytu", description='Upload a video to YouTube', epilog="If you find this app useful, please consider making a donation.")
    parser.add_argument('--file', help='Path to the video file to upload.')
    parser.add_argument('--title', default='', help='Title of the video.')
    parser.add_argument('--description', default='', help='Description of the video. Ignored if --descriptionFile is given.')
    parser.add_argument('--descriptionFile', help='Path to a text file containing the description of the video. This overrides --description.')
    parser.add_argument('--category', default='22', help='ID of the category for the video. Use --listCategories to see available categories.')
    parser.add_argument('--tags', default='', help='Comma-separated tags for the video.')
    parser.add_argument('--defaultLanguage', default='en', help='Language of the video (default is English).')
    parser.add_argument('--listCategories', action='store_true', help='List available category IDs and exit.')
    parser.add_argument('--regionCode', default='US', help='Region code to list categories for (default is US).')

    args = parser.parse_args()
    if not args.listCategories or not args.file:
        parser.print_help()
        exit()
        
    if args.listCategories:
        youtube = get_authenticated_service()
        list_categories(youtube, args.regionCode)
        exit()
    
    if args.descriptionFile:
        with open(args.descriptionFile, 'r') as f:
            description = f.read()
    else:
        description = args.description
        
    if args.file:
        youtube = get_authenticated_service()
        upload_video(youtube, args.file, args.title, description, args.category, args.tags, args.defaultLanguage)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()