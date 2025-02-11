import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from tqdm import tqdm  # Para barra de progresso

# Configuração do Spotify API (Credenciais via variáveis de ambiente)
SPOTIPY_CLIENT_ID = "SEU SPOTIFY CLIENT ID"
SPOTIPY_CLIENT_SECRET = "SEU SPOTIFY CLIENT SECRET"
SPOTIPY_REDIRECT_URI = "SEU SPOTIFY REDIRECT URI"
USERNAME = "SEU NOME DE USUÁRIO DO SPOTIFY"

# Configuração do YouTube Music API (usando cookies de autenticação)
ytmusic = YTMusic(auth="headers_auth.json")  # Arquivo com o cookie de autenticação
ytmusic.origin = "https://music.youtube.com"  # Define manualmente a origem

# Verifica se a autenticação foi bem-sucedida
print(f"SAPISID: {ytmusic.sapisid}")  # Deve exibir um valor válido

# Autenticação no Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private"
))

def get_ytmusic_playlist(playlist_id):
    """Obtém músicas da playlist do YouTube Music"""
    playlist = ytmusic.get_playlist(playlist_id)
    songs = []
    for track in playlist['tracks']:
        title = track['title']
        artist = track['artists'][0]['name']
        songs.append((artist.lower(), title.lower()))  # Converte para minúsculas para melhor ordenação
    return songs

def search_spotify_song(title, artist):
    """Busca a música no Spotify usando um título simplificado"""
    query = f"{artist} {title}"
    results = sp.search(q=query, type="track", limit=3)  # Busca até 3 resultados para aumentar as chances de acerto
    for track in results["tracks"]["items"]:
        if artist.lower() in track["artists"][0]["name"].lower():  # Confirma se o artista corresponde
            return track["id"]
    return None

def check_existing_playlist(name):
    """Verifica se uma playlist com o mesmo nome já existe"""
    playlists = sp.current_user_playlists()["items"]
    for playlist in playlists:
        if playlist["name"].lower() == name.lower():
            return playlist["id"]
    return None

def create_spotify_playlist(name, description="Playlist transferida do YouTube Music"):
    """Cria uma nova playlist no Spotify"""
    playlist = sp.user_playlist_create(USERNAME, name, public=True, description=description)
    return playlist['id']

def add_songs_to_playlist(playlist_id, song_ids):
    """Adiciona músicas à playlist do Spotify"""
    sp.playlist_add_items(playlist_id, song_ids)

def main():
    youtube_playlist_id = input("Insira o ID da playlist do YouTube Music: ")
    playlist_name = input("Nome para a nova playlist no Spotify: ")

    print("Obtendo músicas do YouTube Music...")
    yt_songs = get_ytmusic_playlist(youtube_playlist_id)

    # Ordena músicas por nome do artista e depois pelo nome da música
    yt_songs.sort()

    print("Buscando músicas no Spotify...")
    spotify_song_ids = []
    not_found = []

    for artist, title in tqdm(yt_songs, desc="Processando músicas", unit="música"):
        song_id = search_spotify_song(title, artist)
        if song_id:
            spotify_song_ids.append(song_id)
        else:
            not_found.append(f"{artist} - {title}")

    print(f"Músicas encontradas: {len(spotify_song_ids)}")
    print(f"Músicas não encontradas: {len(not_found)}")

    if not spotify_song_ids:
        print("Nenhuma música foi encontrada no Spotify. Encerrando...")
        return

    print("Criando playlist no Spotify...")
    existing_playlist_id = check_existing_playlist(playlist_name)

    if existing_playlist_id:
        print(f"A playlist '{playlist_name}' já existe. Adicionando músicas a ela...")
        spotify_playlist_id = existing_playlist_id
    else:
        spotify_playlist_id = create_spotify_playlist(playlist_name)

    print("Adicionando músicas à playlist ordenadas...")
    unique_song_ids = list(set(spotify_song_ids))  # Remove duplicatas
    for i in range(0, len(unique_song_ids), 100):  # Spotify limita 100 músicas por requisição
        add_songs_to_playlist(spotify_playlist_id, unique_song_ids[i:i + 100])
        time.sleep(1)  # Evita limite de taxa

    print("Transferência concluída! 🎵 Playlist ordenada criada com sucesso!")

    if not_found:
        print("\nMúsicas que não foram encontradas no Spotify:")
        for song in not_found:
            print(f"- {song}")

if __name__ == "__main__":
    main()
