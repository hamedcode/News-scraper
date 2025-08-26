import requests
from bs4 import BeautifulSoup
import os

# نام فایلی که لینک‌های ارسال شده در آن ذخیره می‌شود
SENT_LINKS_FILE = 'sent_links.txt'

def get_sent_links():
    """لینک‌های قبلاً ارسال شده را از فایل می‌خواند."""
    if not os.path.exists(SENT_LINKS_FILE):
        return set()
    with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_new_links(links):
    """لینک‌های جدید را به فایل اضافه می‌کند."""
    with open(SENT_LINKS_FILE, 'a', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

def scrape_tgju_news():
    """
    اخبار ویژه را از سایت tgju.org استخراج کرده و فقط موارد جدید را برمی‌گرداند.
    """
    URL = "https://www.tgju.org/news/tag/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%DB%8C%DA%98%D9%87"
    BASE_URL = "https://www.tgju.org"
    
    new_news_list = []
    sent_links = get_sent_links()

    try:
        # ارسال درخواست HTTP به سایت
        response = requests.get(URL, timeout=15)
        response.raise_for_status()  # بررسی موفقیت‌آمیز بودن درخواست

        # تجزیه محتوای HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # پیدا کردن تمام آیتم‌های خبری با استفاده از سلکتور CSS
        news_elements = soup.select(".news-item-row h2 a")

        for element in news_elements:
            title = element.get_text(strip=True)
            relative_link = element.get('href')
            
            if not relative_link:
                continue

            full_link = BASE_URL + relative_link
            
            # اگر لینک جدید بود، آن را به لیست اخبار جدید اضافه کن
            if full_link not in sent_links:
                new_news_list.append({'title': title, 'link': full_link})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the website: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return new_news_list

if __name__ == "__main__":
    latest_news = scrape_tgju_news()
    
    if latest_news:
        print(f"Found {len(latest_news)} new news items:\n")
        
        # در اینجا در آینده کد ارسال به تلگرام قرار می‌گیرد
        # فعلاً فقط آنها را چاپ می‌کنیم
        for index, news in enumerate(latest_news):
            print(f"{index + 1}. Title: {news['title']}")
            print(f"   Link: {news['link']}\n")
            # message = f"**{news['title']}**\n[Read More]({news['link']})"
            # send_to_telegram(message) # این تابع در مرحله بعد اضافه می‌شود

        # لینک‌های اخبار جدید را برای جلوگیری از ارسال مجدد، ذخیره می‌کنیم
        new_links_to_save = [news['link'] for news in latest_news]
        save_new_links(new_links_to_save)
    else:
        print("No new news items found or an error occurred.")

