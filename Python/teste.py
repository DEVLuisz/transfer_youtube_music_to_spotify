from ytmusicapi import YTMusic

ytmusic = YTMusic(auth="headers_auth.json")
ytmusic.origin = "https://music.youtube.com"  # Força a definição da origem

try:
    playlists = ytmusic.get_library_playlists()
    print("Autenticação bem-sucedida! 🎉")
    print(playlists)
except Exception as e:
    print(f"Erro na autenticação: {e}")
