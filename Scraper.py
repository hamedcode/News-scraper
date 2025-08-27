import feedparser
import os

print("--- Script Started (RSS Diagnostic Mode) ---")

# آدرس فید RSS شما
RSS_URL = "https://politepol.com/fd/ngcVl4aeTdc8.xml"

print(f"در حال تجزیه فید RSS از آدرس: {RSS_URL}")

try:
    # خواندن و تجزیه فید RSS
    feed = feedparser.parse(RSS_URL)

    # بررسی اینکه آیا فید به درستی خوانده شده و آیتمی دارد یا نه
    if not feed.entries:
        print("خطا: هیچ آیتمی در فید RSS پیدا نشد. فید ممکن است خالی یا نامعتبر باشد.")
    else:
        print(f"موفقیت: تعداد {len(feed.entries)} آیتم در فید پیدا شد.")
        print("\n--- در حال تحلیل اولین آیتم برای مشاهده تمام داده‌های موجود ---")

        # انتخاب اولین آیتم خبری
        first_entry = feed.entries[0]

        # چاپ تمام کلیدهای موجود برای این آیتم
        print(f"فیلدهای داده موجود برای اولین آیتم: {list(first_entry.keys())}")

        # چاپ محتوای فیلدهای مهم و رایج
        print("\n--- محتوای فیلدهای کلیدی ---")
        print(f"entry.title: {first_entry.get('title', 'موجود نیست')}")
        print(f"entry.link: {first_entry.get('link', 'موجود نیست')}")
        print(f"entry.summary: {first_entry.get('summary', 'موجود نیست')}")
        print(f"entry.description: {first_entry.get('description', 'موجود نیست')}")
        print(f"entry.published: {first_entry.get('published', 'موجود نیست')}")
        print(f"entry.id: {first_entry.get('id', 'موجود نیست')}")

except Exception as e:
    print(f"-> خطا: یک خطای پیش‌بینی نشده رخ داد: {e}")

print("\n--- Script Finished ---")
