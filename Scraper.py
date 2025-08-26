import feedparser
import os
import telegram

# --- خواندن متغیرها از GitHub Secrets ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SENT_LINKS_FILE = 'sent_links.txt'

def send_to_telegram(message):
    """ارسال پیام به تلگرام."""
    if not BOT_TOKEN or not CHAT_ID:
        print("خطا: توکن ربات یا شناسه چت تعریف نشده است.")
        return False
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(
            chat_id=CHAT_ID, 
            text=message, 
            parse_mode='Markdown',
            disable_web_page_preview=False
        )
        print("پیام با موفقیت به تلگرام ارسال شد.")
        return True
    except Exception as e:
        print(f"خطا در ارسال پیام به تلگرام: {e}")
        return False

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
    """استخراج اخبار از فید RSS ساخته شده توسط FetchRSS."""
    print("در حال دریافت اخبار از فید RSS...")
    # !!! آدرس RSS که از FetchRSS گرفته‌اید را اینجا جایگزین کنید !!!
    RSS_URL = "آدرس_فید_شما_اینجا" 
    
    new_news_list = []
    sent_links = get_sent_links()
    try:
        feed = feedparser.parse(RSS_URL)
        for entry in feed.entries:
            if entry.link not in sent_links:
                new_news_list.append({'title': entry.title, 'link': entry.link})
    except Exception as e:
        print(f"خطا در خواندن فید RSS: {e}")
    return new_news_list

if __name__ == "__main__":
    latest_news = list(reversed(get_news_from_rss()))
    if latest_news:
        print(f"{len(latest_news)} خبر جدید پیدا شد.")
        newly_sent_links = []
        for news in latest_news:
            message = f"**{news['title']}**\n\n[مشاهده خبر]({news['link']})"
            if send_to_telegram(message):
                newly_sent_links.append(news['link'])
        if newly_sent_links:
            save_new_links(newly_sent_links)
            print(f"{len(newly_sent_links)} لینک جدید با موفقیت ارسال و ذخیره شد.")
    else:
        print("خبر جدیدی پیدا نشد.")
