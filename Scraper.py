import feedparser
import os
import telegram
import time
import asyncio

# --- خواندن متغیرها از GitHub Secrets ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SENT_LINKS_FILE = 'sent_links.txt'

# --- لیست آدرس‌های RSS ---
# می‌توانید هر تعداد آدرس که می‌خواهید به این لیست اضافه کنید
RSS_URLS = [
    "https://politepol.com/fd/iaUGKLxDkHEl.xml",
    "https://politepol.com/fd/UZ2qXgtomoYd.xml", # <--- آدرس دوم به عنوان مثال اضافه شد
    # "https://example.com/another-feed.xml" # آدرس بعدی را اینجا وارد کنید
]

async def send_to_telegram(message):
    """یک پیام متنی دریافت کرده و به صورت غیرهمزمان به تلگرام ارسال می‌کند."""
    if not BOT_TOKEN or not CHAT_ID:
        print("خطا: توکن ربات یا شناسه چت تعریف نشده است.")
        return False
    
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(
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
    """استخراج اخبار از تمام فیدهای RSS موجود در لیست."""
    print("در حال دریافت اخبار از فیدهای RSS شما...")
    new_news_list = []
    sent_links = get_sent_links()
    
    # برای جلوگیری از ارسال لینک تکراری در همین اجرا (اگر در دو فید مختلف باشد)
    current_run_links = set()

    # حلقه برای خواندن تمام آدرس‌های RSS
    for url in RSS_URLS:
        print(f"در حال بررسی فید: {url}")
        try:
            feed = feedparser.parse(url)
            print(f"-> فید شامل {len(feed.entries)} آیتم است.")
            
            for entry in feed.entries:
                title = entry.title
                link = entry.link

                # اگر لینک معتبر بود و قبلا ارسال نشده بود
                if link and link not in sent_links and link not in current_run_links:
                    new_news_list.append({'title': title, 'link': link})
                    current_run_links.add(link) # لینک به لیست موقت اضافه می‌شود

        except Exception as e:
            print(f"-> خطا در خواندن فید {url}: {e}")
            
    print(f"-> {len(new_news_list)} خبر جدید برای ارسال پیدا شد.")
    return new_news_list

async def main():
    """تابع اصلی برای اجرای کل فرآیند."""
    # اخبار به ترتیب از قدیمی به جدید ارسال می‌شوند
    latest_news = list(reversed(get_news_from_rss()))
    
    if latest_news:
        print(f"در حال ارسال {len(latest_news)} خبر جدید به تلگرام...")
        
        newly_sent_links = []
        for news in latest_news:
            message = (
                f"📰 **{news['title']}**\n\n"
                f"🔗 [مشاهده خبر]({news['link']})"
            )
            
            if await send_to_telegram(message):
                newly_sent_links.append(news['link'])
                await asyncio.sleep(1) # استفاده از asyncio.sleep به جای time.sleep

        if newly_sent_links:
            save_new_links(newly_sent_links)
            print(f"-> {len(newly_sent_links)} لینک جدید با موفقیت ارسال و ذخیره شد.")
    else:
        print("-> خبر جدیدی برای ارسال پیدا نشد.")

    print("--- Script Finished ---")


if __name__ == "__main__":
    asyncio.run(main())
