# ====== SEND TO TELEGRAM ======
import requests
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

filename = "pngtree-open.png"
CHAT_ID = ""


with open(filename, 'rb') as img:
    response = requests.post(url, data={
        'chat_id': CHAT_ID
    }, files={
        'photo': img
    })

print("Sent to Telegram:", response.status_code)