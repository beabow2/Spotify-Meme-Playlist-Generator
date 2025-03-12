# Spotify Meme Playlist Generator

Create funny story-telling playlists on Spotify based on themes you provide. This app generates playlists where the song titles, when read in sequence, create a humorous narrative related to your chosen theme.

## Description

The Spotify Meme Playlist Generator connects to your Spotify account and creates custom playlists where the song titles tell a story. Simply enter a theme (like "first date disaster" or "Monday morning"), and the app will search for songs that, when arranged in sequence, create a funny narrative.

## Prerequisites

- A Spotify account
- Python 3.7+ 
- pip package manager

## Setup

### 1. Spotify Developer Setup
- Sign in to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- Click "Create app"
- Go to your new app's Settings page
- Add `http://127.0.0.1:8888/callback` to the list of "Redirect URIs"
- Check "Web API" and "Web Playback SDK" under "APIs used"
- Save your settings
- Copy the app's "Client ID" and "Client Secret"

## Usage

1. Run the application: `main.py`
2. Log in with your Spotify account when prompted
3. Enter a theme for your playlist
4. Review the generated playlist and save it to your Spotify account

## Example

Theme: How to order a pizza

Narrative:
1. Hello
2. I'm hungry
3. Can I order
4. Pizza
5. Extra cheese please
6. How long
7. 30 minutes
8. Too long
9. Hurry up
10. Thank you

![image](https://github.com/user-attachments/assets/caa08263-d06b-4b89-9cf6-8a156f845baa)
