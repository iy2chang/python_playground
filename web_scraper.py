import csv
import time
import requests

from bs4 import BeautifulSoup

def fetch_page(url):
    """Fetch the HTML content of a web page"""

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.text
    except requests.exceptions.ConnectionError:
        print(f"Couldn't connect.")
    except requests.exceptions.Timeout:
        print(f"Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")

    return None

def parse_stories(html):
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    title_elements = soup.find_all("span", class_="titleline")

    for title_element in title_elements:
        link_tag = title_element.find("a")

        if not link_tag:
            continue

        title = link_tag.get_text()
        url = link_tag.get("href", "")

        title_row = title_element.find_parent("tr", class_="athing")
        score = 0

        if title_row:
            meta_row = title_row.find_next_sibling("tr")
            if meta_row:
                score_element = meta_row.find("span", class_="score")
                if score_element:
                    score_text = score_element.get_text()
                    score = int(score_text.split()[0])
        
        stories.append({
            "title": title,
            "url": url,
            "score": score
        })
    
    return stories

def display_stories(stories, sort_by_score=False):
    if not stories:
        print("No stories found.")
        return
    
    if sort_by_score:
        stories = sorted(stories, key=lambda s: s["score"], reverse=True)
    
    print(f"\n{'=' * 60}")
    print(f"Hacker News - Top {len(stories)} Stories")
    if sort_by_score:
        print(" (sorted by score)")
    print(f"{'=' * 60}\n")

    for i, story in enumerate(stories, start=1):
        print(f" {i:>2}. [{story['score']:>4} pts] {story['title']}")
        
        if story["url"].startswith("http"):
            print(f" {story['url']}")
        print()

def save_to_csv(stories, filename="hacker_news.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url", "score"])
        writer.writeheader()
        writer.writerows(stories)

    print(f"Saved {len(stories)} stories to {filename}")

def main():
    print("=" * 60)
    print("Hacker News Web Scrapper")
    print("=" * 60)

    url = "https://news.ycombinator.com"

    print(f"\n Fetching {url}...")
    html = fetch_page(url)

    if not html:
        print("Failed to fetch the page. Exiting.")
        return
    
    print("Page fetched successfully")

    print("Parsing stories")
    stories = parse_stories(html)
    print(f"Found {len(stories)} stories!\n")

    if not stories:
        return
    
    while True:
        print("Options:")
        print("1. View stories (original order)")
        print("2. View stories (sorted by score)")
        print("3. Save to CSV file")
        print("4. Refresh (fetch again)")
        print("5. Quit")

        choice = input("\nChoose (1-5): ").strip()

        if choice == "1":
            display_stories(stories)
        elif choice == "2":
            display_stories(stories, sort_by_score=True)
        elif choice == "3":
            save_to_csv(stories)
        elif choice == "4":
            print("\n Refreshing...")
            time.sleep(1)
            html = fetch_page(url)
            if html:
                stories = parse_stories(html)
                print(f"Refreshed! Found {len(stories)} stories.\n")
        elif choice == "5":
            print("\nGoodbye\n")
            break
        else:
            print("Please choose 1-5.\n")

if __name__ == "__main__":
    main()