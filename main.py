import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import re
import time

def create_meme_playlist(client_id, client_secret, redirect_uri, theme):
    """
    Create a Spotify meme playlist where song titles build a funny narrative related to the theme.
    
    Args:
        client_id (str): Spotify API client ID
        client_secret (str): Spotify API client secret
        redirect_uri (str): Spotify API redirect URI
        theme (str): Theme for the meme playlist
    
    Returns:
        dict: Result information including playlist URL and songs used
    """
    # Set up authentication
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))
    
    # Get user ID
    user_info = sp.current_user()
    user_id = user_info['id']
    
    # Function to search for a song with an EXACT title match
    def search_exact_song_title(title, limit=50):
        # Clean the search query
        query = f'track:"{title}"'
        results = sp.search(q=query, type='track', limit=limit)
        tracks = results['tracks']['items']
        
        # Filter for tracks that match the exact title (case insensitive)
        exact_matches = []
        for track in tracks:
            # Remove special characters and convert to lowercase for comparison
            clean_track_name = re.sub(r'[^\w\s]', '', track['name'].lower())
            clean_search_title = re.sub(r'[^\w\s]', '', title.lower())
            
            # Check for exact title match (ignoring case and special chars)
            if clean_track_name == clean_search_title:
                exact_matches.append(track)
        
        return exact_matches if exact_matches else None
    
    # Generate narrative sequences based on theme (claude)
    def generate_narrative_sequences(theme):
        narratives = []
        
        # Pizza delivery narrative
        if any(word in theme.lower() for word in ['pizza', 'food', 'delivery']):
            narratives.append([
                "Hello",
                "I'm hungry",
                "Can I order",
                "Pizza",
                "Extra cheese please",
                "How long",
                "30 minutes",
                "Too long",
                "Hurry up",
                "Thank you"
            ])
            
            narratives.append([
                "I need",
                "Pizza",
                "Right now",
                "I'm starving",
                "Please hurry",
                "Where are you",
                "It's cold",
                "I want my money back",
                "Sorry",
                "I was hangry"
            ])
        
        # Dating/Relationship narrative
        elif any(word in theme.lower() for word in ['love', 'date', 'dating', 'relationship']):
            narratives.append([
                "Hey",
                "Are you single",
                "Can I have your number",
                "Text me",
                "Wanna go out",
                "Friday night",
                "I'll pick you up",
                "You look beautiful",
                "Kiss me",
                "I think I love you"
            ])
            
            narratives.append([
                "Hey you",
                "Remember me",
                "From last night",
                "I can't stop thinking about you",
                "Call me",
                "Please",
                "I miss you",
                "Already",
                "Is that weird",
                "Sorry"
            ])
        
        # Work/Office narrative
        elif any(word in theme.lower() for word in ['work', 'office', 'job', 'boss']):
            narratives.append([
                "Good morning",
                "I'm late",
                "Traffic was terrible",
                "Sorry boss",
                "Not again",
                "I'll stay late",
                "Need coffee",
                "Is it Friday yet",
                "Kill me",
                "I quit"
            ])
            
            narratives.append([
                "Hey",
                "Are you available",
                "Quick question",
                "About the project",
                "I'm confused",
                "Help me",
                "Please",
                "By tomorrow",
                "Sorry",
                "Thank you"
            ])
        
        # Coding/Developer narrative
        elif any(word in theme.lower() for word in ['code', 'coding', 'developer', 'programming']):
            narratives.append([
                "Hey you",
                "Are you available",
                "Please answer me",
                "I've been waiting for you",
                "For weeks",
                "OMG",
                "The code is broken",
                "Nothing works",
                "Help me",
                "Please"
            ])
            
            narratives.append([
                "Hey",
                "Code review please",
                "It's urgent",
                "Deadline tomorrow",
                "No pressure",
                "Just kidding",
                "We're doomed",
                "It doesn't work",
                "I hate my life",
                "Coffee break"
            ])
        
        # Gaming narrative
        elif any(word in theme.lower() for word in ['game', 'gaming', 'play']):
            narratives.append([
                "Hey",
                "Wanna play",
                "One more game",
                "I promise",
                "Just one",
                "Oops",
                "It's 3 AM",
                "One more",
                "I hate this game",
                "I'm addicted"
            ])
        
        # Generic narratives for any theme
        narratives.append([
            "Hello",
            f"I love {theme}",
            "So much",
            "Is that weird",
            "Don't judge me",
            "Everyone has secrets",
            "This is mine",
            "Sorry not sorry",
            "The end"
        ])
        
        narratives.append([
            "Hey you",
            "Listen",
            f"About {theme}",
            "I'm obsessed",
            "Help me",
            "I can't stop",
            "Day and night",
            "Please",
            "I need therapy"
        ])
        
        narratives.append([
            "Dear diary",
            f"Today I {theme}",
            "Again",
            "I promised I wouldn't",
            "But here we are",
            "I'm weak",
            "Don't tell anyone",
            "Please",
            "Thank you"
        ])
        
        return narratives
    
    # Try to find songs for a narrative sequence
    def try_create_playlist_from_narrative(narrative):
        print(f"Trying to create a playlist with narrative: {' → '.join(narrative)}")
        
        # Try to find an exact match for each line in the narrative
        found_songs = []
        all_lines_found = True
        
        for line in narrative:
            songs = search_exact_song_title(line)
            if songs:
                # Choose a random song from the matches
                found_songs.append(random.choice(songs))
            else:
                print(f"  Could not find a song with title: '{line}'")
                all_lines_found = False
                break
        
        if all_lines_found and found_songs:
            # Create a new playlist
            playlist_name = f"{theme} - Meme Playlist"
            narrative_text = " → ".join(narrative)
            playlist_description = f"POV: {theme}. A story told through song titles."
            
            playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=True,
                description=playlist_description
            )
            
            # Add the songs to the playlist
            track_uris = [song['uri'] for song in found_songs]
            sp.playlist_add_items(playlist['id'], track_uris)
            
            # Prepare the result
            songs_used = [(song['name'], song['artists'][0]['name']) for song in found_songs]
            
            return {
                'playlist_url': playlist['external_urls']['spotify'],
                'narrative': narrative,
                'songs_used': songs_used
            }
        
        # Wait a bit to avoid rate limiting
        time.sleep(0.2)
        return None
    
    # Try to create a custom narrative by finding common song titles
    def try_create_custom_narrative(theme):
        # Common phrases that might exist as song titles
        common_phrases = [
            "Hello", "Hey", "Hey you", "Hi", "Listen", "Wait", 
            "Please", "Help", "Help me", "I need", "I want", "Give me",
            "Thank you", "Sorry", "I'm sorry", "My bad", "Oops",
            "What", "Why", "How", "When", "Where", "Who",
            "Yes", "No", "Maybe", "I don't know", "I don't care",
            "I love", "I hate", "I miss", "I remember", "I forgot",
            "Call me", "Text me", "Come over", "Stay away", "Leave me alone",
            "Too late", "Not again", "One more time", "Never again",
            "OMG", "WTF", "LOL", "Seriously", "Are you kidding me",
            "I'm fine", "I'm not okay", "Save me", "Kill me",
            "Good morning", "Good night", "Sweet dreams", "Wake up",
            "It's over", "The end", "Finally", "At last"
        ]
        
        # Find which common phrases have matching songs
        available_phrases = []
        for phrase in common_phrases:
            songs = search_exact_song_title(phrase, limit=20)
            if songs:
                available_phrases.append((phrase, random.choice(songs)))
        
        # Also search for theme-specific titles
        theme_songs = search_exact_song_title(theme, limit=20)
        if theme_songs:
            available_phrases.append((theme, random.choice(theme_songs)))
        
        # If we have enough phrases, build a custom narrative
        if len(available_phrases) >= 6:
            # Shuffle to get random phrases
            random.shuffle(available_phrases)
            
            # Select 6-10 phrases for our narrative
            selected_phrases = available_phrases[:random.randint(6, min(10, len(available_phrases)))]
            
            # Create the playlist
            playlist_name = f"{theme} - Meme Playlist"
            narrative = [phrase for phrase, _ in selected_phrases]
            narrative_text = " → ".join(narrative)
            playlist_description = f"POV: {theme}. A story told through song titles."
            
            playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=True,
                description=playlist_description
            )
            
            # Add the songs to the playlist
            track_uris = [song['uri'] for _, song in selected_phrases]
            sp.playlist_add_items(playlist['id'], track_uris)
            
            # Prepare the result
            songs_used = [(song['name'], song['artists'][0]['name']) for _, song in selected_phrases]
            
            return {
                'playlist_url': playlist['external_urls']['spotify'],
                'narrative': narrative,
                'songs_used': songs_used
            }
        
        return None
    
    # Main function to build the meme playlist
    def build_meme_playlist():
        # Try predefined narratives first
        narratives = generate_narrative_sequences(theme)
        random.shuffle(narratives)
        
        for narrative in narratives:
            result = try_create_playlist_from_narrative(narrative)
            if result:
                return result
        
        # If no predefined narrative works, try to build a custom one
        print("Trying to create a custom narrative...")
        result = try_create_custom_narrative(theme)
        if result:
            return result
        
        # If nothing worked
        return {
            'error': 'Could not create a meme playlist with the given theme. Try a different theme with more common words.'
        }
    
    # Execute the main function
    return build_meme_playlist()

# Example usage
if __name__ == "__main__":
    # Collect user input
    client_id = input("Enter your Spotify client ID: ")
    client_secret = input("Enter your Spotify client secret: ")
    redirect_uri = input("Enter your redirect URI (e.g., http://127.0.0.1:8888/callback): ")
    theme = input("Enter a theme for your meme playlist: ")
    
    # Create the playlist
    result = create_meme_playlist(client_id, client_secret, redirect_uri, theme)
    
    # Display the result
    if 'error' in result:
        print(result['error'])
    else:
        print("\nPlaylist created successfully!")
        print(f"Theme: {theme}")
        print("\nNarrative:")
        for i, line in enumerate(result['narrative'], 1):
            print(f"{i}. {line}")
        print("\nSongs in the playlist:")
        for i, (title, artist) in enumerate(result['songs_used'], 1):
            print(f"{i}. '{title}' by {artist}")
        print(f"\nPlaylist URL: {result['playlist_url']}")