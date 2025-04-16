import requests
import csv
from fastapi import FastAPI
import uvicorn

API_URL = "https://rickandmortyapi.com/api/character"
OUTPUT_FILE = "characters.csv"

app = FastAPI()

def fetch_characters():
    characters = []
    page = 1

    while True:
        response = requests.get(API_URL, params={"page": page})
        if response.status_code != 200:
            break
        data = response.json()
        for character in data["results"]:
            if (
                character["species"] == "Human"
                and character["status"] == "Alive"
                and character["origin"]["name"] == "Earth"
            ):
                characters.append({
                    "Name": character["name"],
                    "Location": character["location"]["name"],
                    "Image": character["image"],
                })
        if data["info"]["next"] is None:
            break
        page += 1
    return characters

def write_to_csv(characters):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Location", "Image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(characters)

@app.get("/characters")
def get_characters():
    return fetch_characters()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    characters = fetch_characters()
    write_to_csv(characters)
    print(f"CSV file '{OUTPUT_FILE}' created successfully!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
	
