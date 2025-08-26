import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# نام فایلی که لینک‌های ارسال شده در آن ذخیره می‌شود
SENT_LINKS_FILE = 'sent_links.txt'

print("--- Script Started (Selenium Version) ---")

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

def scrape_tgju_with_selenium():
    """
    اخبار را با استفاده از Selenium و یک مرورگر واقعی استخراج می‌کند.
    """
    print("Step 2: Scraping news from TGJU using Selenium...")
    URL = "https://www.tgju.org/news/tag/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%DB%8C%DA%98%D9%87"
    
    new_news_list = []
    sent_links = get_sent_links()

    # تنظیمات مرورگر کروم برای اجرا در محیط GitHub Actions
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # اجرا بدون رابط گرافیکی
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"-> Navigating to {URL}")
        driver.get(URL)
        
        # منتظر می‌مانیم تا حداقل یک آیتم خبری در صفحه بارگذاری شود (حداکثر 20 ثانیه)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".news-item-row h2 a")))
        
        # پیدا کردن تمام المان‌های خبری
        news_elements = driver.find_elements(By.CSS_SELECTOR, ".news-item-row h2 a")
        print(f"-> Selenium found {len(news_elements)} total news elements.")

        for element in news_elements:
            title = element.text
            link = element.get_attribute('href')
            
            if not title or not link:
                continue
            
            if link not in sent_links:
                new_news_list.append({'title': title, 'link': link})

    except TimeoutException:
        print("-> ERROR: Timed out waiting for page elements to load. The site might be slow or blocking.")
    except Exception as e:
        print(f"-> ERROR: An unexpected error occurred with Selenium: {e}")
    finally:
        driver.quit() # حتماً مرورگر را می‌بندیم
        
    print(f"-> Scraping finished. Found {len(new_news_list)} new items to be saved.")
    return new_news_list

if __name__ == "__main__":
    latest_news = scrape_tgju_with_selenium()
    
    if latest_news:
        new_links_to_save = [news['link'] for news in latest_news]
        save_new_links(new_links_to_save)
    else:
        print("Step 3: No new news items to save.")
    
    print("--- Script Finished ---")
