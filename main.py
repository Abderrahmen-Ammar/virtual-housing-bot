import asyncio
import requests
import os
from bs4 import BeautifulSoup
import telegram

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"

seen_offers = set()

async def check_offers():
    bot = telegram.Bot(token=BOT_TOKEN)
    print("Bot läuft...")

    while True:
        try:
            response = requests.get(URL)
            soup = BeautifulSoup(response.text, "html.parser")

            offers = soup.find_all("a")  # ggf. anpassen!

            for offer in offers:
                text = offer.get_text(strip=True)

                if "Einzelapartment" in text:
                    link = offer.get("href")

                    if text not in seen_offers:
                        seen_offers.add(text)

                        message = f" Neues Einzelapartment gefunden!\n{text}\n{link}"
                        await bot.send_message(chat_id=CHAT_ID, text=message)

                        print("Neue Wohnung gemeldet!")

        except Exception as e:
            print("Fehler:", e)

        await asyncio.sleep(30)  # realistischer

if __name__ == "__main__":
    asyncio.run(check_offers())

