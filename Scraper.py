import feedparser
import os
from bs4 import BeautifulSoup
import telegram
import time
import asyncio

# --- خواندن متغیرها از GitHub Secrets ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SENT_LINKS_FILE = 'sent_links.txt'

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
    """استخراج اخبار و اصلاح لینک‌ها از فید RSS."""
    print("در حال دریافت اخبار از فید RSS شما...")
    # شما می‌توانید هر زمان که خواستید این آدرس را تغییر دهید
    RSS_URL = "https://politepol.com/fd/iaUGKLxDkHEl.xml" 
    
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
                politepol_link = link_tag.get('href')
                # با استفاده از .get() مطمئن می‌شویم که اگر 'summary' نبود، برنامه خطا ندهد
                summary = entry.get('summary', '') 

                if politepol_link:
                    final_link = politepol_link.replace("https://politepol.com/news/", "https://tgju.org/news/")
                else:
                    continue

                if final_link not in sent_links:
                    new_news_list.append({
                        'title': true_title, 
                        'link': final_link,
                        'summary': summary.strip() # .strip() برای حذف فاصله‌های اضافی
                    })

    except Exception as e:
        print(f"-> خطا در خواندن فید RSS: {e}")
        
    print(f"-> {len(new_news_list)} خبر جدید برای ارسال پیدا شد.")
    return new_news_list

async def main():
    """تابع اصلی برای اجرای کل فرآیند."""
    latest_news = list(reversed(get_news_from_rss()))
    
    if latest_news:
        print(f"در حال ارسال {len(latest_news)} خبر جدید به تلگرام...")
        
        newly_sent_links = []
        for news in latest_news:
            # --- اصلاحیه اصلی اینجاست: ساخت پیام به صورت شرطی ---
            
            # بخش عنوان همیشه وجود دارد
            title_part = f"📰 **{news['title']}**"
            
            # بخش توضیحات فقط در صورتی اضافه می‌شود که خالی نباشد
            summary_part = ""
            if news['summary']:
                summary_part = f"\n------------------------------------\n📝 {news['summary']}"
            
            # بخش لینک همیشه وجود دارد
            link_part = f"\n\n🔗 [مشاهده خبر در TGJU.org]({news['link']})"
            
            # ترکیب نهایی بخش‌ها
            message = f"{title_part}{summary_part}{link_part}"
            
            if await send_to_telegram(message):
                newly_sent_links.append(news['link'])
                time.sleep(1)

        if newly_sent_links:
            save_new_links(newly_sent_links)
            print(f"-> {len(newly_sent_links)} لینک جدید با موفقیت ارسال و ذخیره شد.")
    else:
        print("-> خبر جدیدی برای ارسال پیدا نشد.")

    print("--- Script Finished ---")


if __name__ == "__main__":
    asyncio.run(main())
