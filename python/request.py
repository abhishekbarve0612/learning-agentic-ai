
import requests

def fetch_single_note():
    url = "https://jsonplaceholder.typicode.com/posts/2"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    print(f"title: {data['title']}")

    return data

if __name__ == "__main__":
    fetch_single_note()
