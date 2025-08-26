import requests
import os

# نام فایلی که لینک‌های ارسال شده در آن ذخیره می‌شود
SENT_LINKS_FILE = 'sent_links.txt'

print("--- Script Started ---")

def get_sent_links():
    """لینک‌های قبلاً ارسال شده را از فایل می‌خواند."""
    print("Step 1: Reading previously sent links...")
    if not os.path.exists(SENT_LINKS_FILE):
        print(f"-> '{SENT_LINKS_FILE}' not found. Starting fresh.")
        return set()
    
    with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
        links = set(line.strip() for line in f)
        print(f"-> Found {len(links)} links in the existing file.")
        return links

def save_new_links(links):
    """لینک‌های جدید را به فایل اضافه می‌کند."""
    print(f"Step 3: Saving {len(links)} new links to '{SENT_LINKS_FILE}'...")
    with open(SENT_LINKS_FILE, 'a', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    print("-> Save complete.")

def scrape_tgju_news_from_api():
    """
    اخبار ویژه را مستقیماً از API سایت tgju.org استخراج می‌کند.
    """
    print("Step 2: Scraping news from TGJU's internal API...")
    API_URL = "https://www.tgju.org/news/ajax"
    BASE_URL = "https://www.tgju.org"
    
    # --- اصلاحیه نهایی: اضافه کردن هدرهای کامل برای شبیه‌سازی یک درخواست واقعی ---
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.tgju.org/news/tag/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%DB%8C%DA%98%D9%87',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    payload = {
        'cat': 'special-news',
        'type': 'news'
    }
    
    new_news_list = []
    sent_links = get_sent_links()

    try:
        response = requests.post(API_URL, headers=HEADERS, data=payload, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        news_items = data.get('items', [])
        print(f"-> API returned {len(news_items)} total news items.")

        for item in news_items:
            title = item.get('title')
            relative_link = item.get('u')
            
            if not title or not relative_link:
                continue

            full_link = BASE_URL + relative_link
            
            if full_link not in sent_links:
                new_news_list.append({'title': title, 'link': full_link})

    except requests.exceptions.RequestException as e:
        print(f"-> ERROR: Could not connect to the API: {e}")
    except Exception as e:
        print(f"-> ERROR: An unexpected error occurred: {e}")
        
    print(f"-> Scraping finished. Found {len(new_news_list)} new items to be saved.")
    return new_news_list

if __name__ == "__main__":
    latest_news = scrape_tgju_news_from_api()
    
    if latest_news:
        new_links_to_save = [news['link'] for news in latest_news]
        save_new_links(new_links_to_save)
    else:
        print("Step 3: No new news items to save.")
    
    print("--- Script Finished ---")
