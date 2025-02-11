import hashlib
import time

def generate_sapisid_hash(cookie, origin="https://music.youtube.com"):
    sapisid = None
    for part in cookie.split("; "):
        if part.startswith("SAPISID="):
            sapisid = part.split("=")[1]
            break

    if not sapisid:
        raise ValueError("SAPISID não encontrado nos cookies!")

    timestamp = str(int(time.time()))
    hash_input = f"{timestamp} {sapisid} {origin}".encode()
    sapisid_hash = hashlib.sha1(hash_input).hexdigest()
    
    return f"SAPISIDHASH {timestamp}_{sapisid_hash}"

# Testando a função
cookie_str = "SAPISID=SEU SAPIDID; ..."  # Use seu cookie completo aqui
authorization = generate_sapisid_hash(cookie_str)

print("Authorization:", authorization)
