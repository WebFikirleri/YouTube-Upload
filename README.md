# YouTube Video Uploader

This is a command-line application that allows you to upload videos to YouTube. It uses the YouTube Data API v3 for video uploads.

## Features

- Upload videos to YouTube from the command line
- Specify video details like title, description, category, and tags
- Authenticate with YouTube only once, credentials are saved for future sessions
- Display upload progress in the console

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/WebFikirleri/YouTube-Upload.git
    ```
2. Navigate to the project directory:
    ```bash
    cd YouTube-Upload
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
## Obtaining Your `client_secrets.json` File

Follow these steps to get your `client_secrets.json` file from the Google Cloud Console:

1. Go to the Google Cloud Console.

2. Click the project drop-down and select or create the project for which you want to add an API key.

3. Click the hamburger menu in the top left of the screen and select "APIs & Services > Credentials".

4. On the "Credentials" page, click "Create credentials > OAuth client ID".

5. If this is your first time creating a client ID, you may need to configure your "OAuth consent screen" first. Fill out the required fields and save.

6. Once the "OAuth consent screen" is configured, you'll be taken back to the "Create OAuth client ID" page. Here, select "Desktop app" for the "Application type", give it a name, and click "Create".

7. After the OAuth client is created, click the download icon on the right side of the client to download your `client_secrets.json` file.

8. Save this file in the same directory as your Python script. Make sure the filename is `client_secrets.json`.

Please note that this file contains sensitive information, including your client ID and client secret. Do not share this file with others, and do not commit it to public source control.

## Usage

To upload a video to YouTube, run the following command:

```bash
python ytu.py --file path_to_your_video --title "Your Video Title" --description "Your Video Description" --category "Your Video Category"
```

You can also specify a text file for the video description:
```bash
python ytu.py --file path_to_your_video --title "Your Video Title" --descriptionFile path_to_your_description_file --category "Your Video Category"
```
To list available video categories:
```bash
python ytu.py --listCategories --region_code "Your Region Code"
```
## Releases
Compiled binaries for this application are available in the Releases section. The available binaries are ytu for Unix-like operating systems and ytu.exe for Windows.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Donation and Support

This project is created and maintained by volunteers who dedicate their free time to maintain it, fix bugs, and implement new features. Your support will help ensure the longevity and continuous development of this project.

If you find this project useful and appreciate the work we're doing, please consider making a donation. Any amount, big or small, is a huge help and is greatly appreciated!

You can donate via:

- **Patreon**: https://www.patreon.com/mrtakdnz
- **Ko-fi**: https://ko-fi.com/webfikirleri
- or just **Subscribe YouTube**: https://youtube.com/@PSRulez

If you're unable to make a donation, you can still support us by starring this GitHub repository and sharing it with your friends and colleagues. You can also contribute to the project by submitting pull requests.

Thank you for your support!

## License
This project is licensed under the terms of the GNU General Public License v3.0.
