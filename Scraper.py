import feedparser
import os

# نام فایلی که لینک‌های ارسال شده در آن ذخیره می‌شود
SENT_LINKS_FILE = 'sent_links.txt'

print("--- Script Started (RSS Only) ---")

def get_sent_links():
    """خواندن لینک‌های قبلاً ارسال شده."""
    print("Step 1: Reading previously sent links...")
    if not os.path.exists(SENT_LINKS_FILE):
        print(f"-> '{SENT_LINKS_FILE}' not found. Starting fresh.")
        return set()
    
    with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
        links = set(line.strip() for line in f)
        print(f"-> Found {len(links)} links in the existing file.")
        return links

def save_new_links(links):
    """ذخیره لینک‌های جدید."""
    print(f"Step 3: Saving {len(links)} new links to '{SENT_LINKS_FILE}'...")
    with open(SENT_LINKS_FILE, 'a', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    print("-> Save complete.")

def get_news_from_rss():
    """استخراج اخبار از فید RSS ساخته شده."""
    print("Step 2: Getting news from your RSS feed...")
    # آدرس RSS شخصی شما
    RSS_URL = "https://fetchrss.com/feed/aK4HlnCK_13CaK4I1CdS9ZPj.rss"
    
    new_news_list = []
    sent_links = get_sent_links()
    try:
        feed = feedparser.parse(RSS_URL)
        print(f"-> RSS feed contains {len(feed.entries)} items.")
        
        for entry in feed.entries:
            if entry.link not in sent_links:
                new_news_list.append({'title': entry.title, 'link': entry.link})
    except Exception as e:
        print(f"-> ERROR: An error occurred while parsing the RSS feed: {e}")
        
    print(f"-> Parsing finished. Found {len(new_news_list)} new items to be saved.")
    return new_news_list

if __name__ == "__main__":
    latest_news = get_news_from_rss()
    
    if latest_news:
        new_links_to_save = [news['link'] for news in latest_news]
        save_new_links(new_links_to_save)
    else:
        print("Step 3: No new news items to save.")
    
    print("--- Script Finished ---")
