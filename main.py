import requests

USE_API = False

def get_headlines():
    if USE_API:
        try:
            API_KEY = "YOUR_API_KEY"
            url = "https://api.brightdata.com/request"

            payload = {
                "zone": "YOUR_ZONE_NAME",
                "url": "https://www.google.com/search?q=Hyderabad+traffic+today",
                "format": "json"
            }

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            results = data.get("organic", [])

            headlines = []
            for item in results[:3]:
                h = item.get("description") or item.get("title")
                if h:
                    headlines.append(h)

            if headlines:
                return headlines
        except:
            pass

    return [
        "Vehicle movement is slow due to heavy traffic flow",
        "Moderate congestion observed in some areas",
        "Traffic is smooth in outskirts"
    ]

def extract_value(text):
    text = text.lower()
    if "heavy" in text or "slow" in text or "congestion" in text:
        return "Heavy"
    elif "moderate" in text:
        return "Moderate"
    else:
        return "Low"

mapping = {"Low":1, "Moderate":2, "Heavy":3}

def resolve(headlines):
    scores = {}
    values = []

    for i, text in enumerate(headlines):
        value = extract_value(text)
        values.append(value)

        trust = 0.9 - (i * 0.2)
        score = mapping[value] * trust

        scores[value] = scores.get(value, 0) + score

    result = max(scores, key=scores.get)
    return result, scores, values

def main():
    headlines = get_headlines()

    print("\nTraffic Intelligence System\n")

    print("Input Headlines:")
    for h in headlines:
        print("-", h)

    result, scores, values = resolve(headlines)

    print("\nScore Breakdown:")
    for k, v in scores.items():
        print(f"{k}: {round(v,2)}")

    unique = set(values)
    if len(unique) == 1:
        conflict = "No Conflict"
    elif len(unique) == 2:
        conflict = "Moderate Conflict"
    else:
        conflict = "High Conflict"

    total = sum(scores.values())
    confidence = (scores[result] / total) * 100

    print("\nConflict Level:", conflict)
    print("\nFinal Decision:", result, "Traffic")
    print("Confidence:", round(confidence, 2), "%")

if __name__ == "__main__":
    main()