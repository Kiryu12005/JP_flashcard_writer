import requests
from pykakasi import kakasi

kks = kakasi()

def get_jisho_reading(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['data']:
            return data['data'][0]['japanese'][0].get('reading', '')
        
    except:
        pass
    return ""


def generate_furigana_sentence(text):
    result = kks.convert(text)
    furigana_sentence = ""
    for item in result:
        kanji = item['orig']
        hira = item['hira']

        if kanji != hira:
            furigana_sentence += f" {kanji}[{hira}]"
        else:
            furigana_sentence += kanji
    
    return furigana_sentence.strip()


def create_anki_card(kanji, reading, meaning, sentence, sentence_trans):
    url = "http://localhost:8765"

    furigana_sentence = generate_furigana_sentence(sentence)

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "JP_Mining",
                "modelName": "JP_Projekt",
                "fields": {
                    "Kanji": kanji,
                    "Reading": reading,
                    "Meaning": meaning,
                    "Sentence": furigana_sentence,
                    "Sentence_Translation": sentence_trans
                },
                "tags": ["japanese_study_tool"]
            }
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=5).json()
        return response
    
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    print("--- Japanese Anki Tool (Type-in Mode) ---")

    while True:
        kanji = input("\n1. Word (Kanji/Kana): ")
        if not kanji: break

        suggested = get_jisho_reading(kanji)
        reading = input(f"2. Reading (Suggested: {suggested}): ") or suggested
        meaning = input("3. Meaning (Word): ")

        raw_sentence = input("4. Japanese Sentence: ")
        furigana_sentence = generate_furigana_sentence(raw_sentence)
        print(f" -> Generated Furigana: {furigana_sentence}")

        sentence_trans = input("5. Sentence Translation: ")

        print("\nSending to Anki...")
        result = create_anki_card(kanji, reading, meaning, furigana_sentence, sentence_trans)

        if result.get("error") is None:
            print(f">> Success! Added: {kanji}")

        else:
            print(f">> ERROR: {result['error']}")
            print("Tip: Check if Anki is open and Note Type is named correctly.")