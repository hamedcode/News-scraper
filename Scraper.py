import feedparser
import os
from bs4 import BeautifulSoup

# نام فایلی که لینک‌های ارسال شده در آن ذخیره می‌شود
SENT_LINKS_FILE = 'sent_links.txt'

print("--- Script Started (Extracting Title, Link, and Summary) ---")

def get_sent_links():
    """خواندن لینک‌های قبلاً ارسال شده."""
    if not os.path.exists(SENT_LINKS_FILE):
        return set()
    with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_new_links(links):
    """ذخیره لینک‌های جدید."""
    with open(SENT_LINKS_FILE, 'a', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

def get_news_from_rss():
    """استخراج اخبار (عنوان، لینک و توضیحات) از فید RSS."""
    print("در حال دریافت اخبار از فید RSS شما...")
    RSS_URL = "https://politepol.com/fd/ngcVl4aeTdc8.xml"
    
    new_news_list = []
    sent_links = get_sent_links()
    try:
        feed = feedparser.parse(RSS_URL)
        print(f"-> فید RSS شامل {len(feed.entries)} آیتم است.")
        
        for entry in feed.entries:
            title_html = BeautifulSoup(entry.title, 'html.parser')
            link_tag = title_html.find('a')
            
            if link_tag:
                true_title = link_tag.get_text(strip=True)
                true_link = link_tag.get('href')
                
                # --- اصلاحیه اینجاست: استخراج توضیحات از فیلد summary ---
                summary = entry.get('summary', 'توضیحات موجود نیست.')

                if true_link and true_link not in sent_links:
                    new_news_list.append({
                        'title': true_title, 
                        'link': true_link,
                        'summary': summary
                    })

    except Exception as e:
        print(f"-> خطا در خواندن فید RSS: {e}")
        
    print(f"-> {len(new_news_list)} خبر جدید برای پردازش پیدا شد.")
    return new_news_list

if __name__ == "__main__":
    latest_news = get_news_from_rss()
    
    if latest_news:
        # نمایش اطلاعات کامل در لاگ برای بررسی
        print("\n--- اخبار جدید یافت شده ---")
        for news in latest_news:
            print(f"عنوان: {news['title']}")
            print(f"لینک: {news['link']}")
            print(f"توضیحات: {news['summary']}\n")

        # فقط لینک‌ها را برای جلوگیری از ارسال تکراری ذخیره می‌کنیم
        new_links_to_save = [news['link'] for news in latest_news]
        save_new_links(new_links_to_save)
        print(f"-> {len(new_links_to_save)} لینک جدید با موفقیت در فایل ذخیره شد.")
    else:
        print("-> خبر جدیدی برای ذخیره پیدا نشد.")

    print("--- Script Finished ---")
