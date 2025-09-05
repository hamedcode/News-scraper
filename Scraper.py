import feedparser
import os

def run_diagnostic():
    """
    Connects to the new RSS feed and prints all available data for the first item
    to help understand its structure.
    """
    print("--- Script Started (RSS Diagnostic Mode) ---")
    
    # لینک جدید شما اینجا قرار داده شده است
    RSS_URL = "https://politepol.com/fd/iaUGKLxDkHEl.xml"
    
    print(f"در حال تجزیه فید RSS از آدرس: {RSS_URL}")
    
    try:
        feed = feedparser.parse(RSS_URL)
        
        if not feed.entries:
            print("!!! خطا: هیچ آیتمی در این فید RSS پیدا نشد. لطفاً آدرس را بررسی کنید.")
            return
            
        print(f"موفقیت: تعداد {len(feed.entries)} آیتم در فید پیدا شد.")
        print("\n--- در حال تحلیل اولین آیتم برای مشاهده تمام داده‌های موجود ---")
        
        first_entry = feed.entries[0]
        
        # چاپ تمام فیلدهای موجود برای اولین آیتم
        print(f"فیلدهای داده موجود برای اولین آیتم: {list(first_entry.keys())}")
        
        print("\n--- محتوای فیلدهای کلیدی ---")
        
        # چاپ محتوای فیلدهای مهم
        print(f"entry.title: {first_entry.get('title', 'وجود ندارد')}")
        print(f"entry.link: {first_entry.get('link', 'وجود ندارد')}")
        print(f"entry.summary: {first_entry.get('summary', 'وجود ندارد')}")
        print(f"entry.description: {first_entry.get('description', 'وجود ندارد')}")
        print(f"entry.published: {first_entry.get('published', 'وجود ندارد')}")
        print(f"entry.id: {first_entry.get('id', 'وجود ندارد')}")

    except Exception as e:
        print(f"!!! یک خطای پیش‌بینی نشده رخ داد: {e}")

    print("\n--- Script Finished ---")


if __name__ == "__main__":
    run_diagnostic()
