import feedparser
import os
from bs4 import BeautifulSoup
import telegram

# --- خواندن متغیرها از GitHub Secrets ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SENT_LINKS_FILE = 'sent_links.txt'

def send_to_telegram(message):
    """یک پیام متنی دریافت کرده و به تلگرام ارسال می‌کند."""
    if not BOT_TOKEN or not CHAT_ID:
        print("خطا: توکن ربات یا شناسه چت تعریف نشده است. لطفاً GitHub Secrets را بررسی کنید.")
        return False
    
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(
            chat_id=CHAT_ID, 
            text=message, 
            parse_mode='Markdown',
            disable_web_page_preview=False # برای نمایش پیش‌نمایش لینک
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
                summary = entry.get('summary', '')

                if true_link and true_link not in sent_links:
                    new_news_list.append({
                        'title': true_title, 
                        'link': true_link,
                        'summary': summary
                    })

    except Exception as e:
        print(f"-> خطا در خواندن فید RSS: {e}")
        
    print(f"-> {len(new_news_list)} خبر جدید برای ارسال پیدا شد.")
    return new_news_list

if __name__ == "__main__":
    # برعکس کردن لیست اخبار جدید تا ترتیب ارسال آن‌ها از قدیمی به جدید باشد
    latest_news = list(reversed(get_news_from_rss()))
    
    if latest_news:
        print(f"در حال ارسال {len(latest_news)} خبر جدید به تلگرام...")
        
        newly_sent_links = []
        for news in latest_news:
            # ساخت پیام با فرمت Markdown برای تلگرام
            message = (
                f"**{news['title']}**\n\n"
                f"{news['summary']}\n\n"
                f"[مشاهده خبر]({news['link']})"
            )
            
            # اگر پیام با موفقیت ارسال شد، لینک آن را برای ذخیره شدن آماده کن
            if send_to_telegram(message):
                newly_sent_links.append(news['link'])

        # فقط لینک‌هایی را ذخیره کن که با موفقیت به تلگرام ارسال شده‌اند
        if newly_sent_links:
            save_new_links(newly_sent_links)
            print(f"-> {len(newly_sent_links)} لینک جدید با موفقیت ارسال و ذخیره شد.")
    else:
        print("-> خبر جدیدی برای ارسال پیدا نشد.")

    print("--- Script Finished ---")
