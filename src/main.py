# src/main.py
import os
import sys
from playwright.sync_api import sync_playwright

# Гарантируем корректный импорт соседних модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import scrapper as scraper
import makePDF as pdf_converter

def launch_chrome_for_testing():
    """Запуск браузера в ручном режиме для входа на сайты и управления профилем."""
    with sync_playwright() as p:
        executable_path = p.chromium.executable_path
        user_data_dir = scraper.get_chrome_testing_user_data_dir()

        print("\n" + "="*50)
        print("Launching Chrome for Testing in interactive mode.")
        print(f"Profile: {user_data_dir}")
        print("="*50)

        if not os.path.exists(executable_path):
            print("\n[!] Chrome for Testing is missing. Install it using: playwright install chromium")
            return

        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=executable_path,
            headless=False,
            args=["--start-maximized"],
            no_viewport=True,
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("\nSelect platform to sign in:")
        print("1. Twitter (x.com)")
        print("2. Discord (discord.com)")
        print("3. Bluesky (bsky.app)")
        print("4. VKontakte (vk.com)")
        print("5. Telegram (web.telegram.org)")
        
        choice = input("Enter choice (1-5) or press Enter to open default page: ").strip()
        if choice == "1":
            page.goto("https://x.com/home")
        elif choice == "2":
            page.goto("https://discord.com/channels/@me")
        elif choice == "3":
            page.goto("https://bsky.app")
        elif choice == "4":
            page.goto("https://vk.com")
        elif choice == "5":
            page.goto("https://web.telegram.org/a")
        else:
            page.goto("https://google.com")

        input("\n[!] Press ENTER in this terminal when you are done to close the browser...")
        browser.close()

def pdf_conversion_menu():
    """Меню генерации PDF из сохраненных JSON."""
    print("\n--- PDF Converter Menu ---")
    print("1. Convert Discord data (disc_msgs.json)")
    print("2. Convert Twitter data (bookmarks.json)")
    print("3. Convert Bluesky data (bsky_bookmarks.json)")
    print("4. Convert VK data (vk_data.json)")
    print("5. Convert Telegram data (telegram_messages.json)")
    print("6. Custom JSON file conversion")
    
    choice = input("Select option (1-6): ").strip()
    
    if choice == "1":
        file_name = "disc_msgs.json"
        out_name = "discord_messages.pdf"
    elif choice == "2":
        file_name = "bookmarks.json"
        out_name = "twitter_bookmarks.pdf"
    elif choice == "3":
        file_name = "bsky_bookmarks.json"
        out_name = "bluesky_bookmarks.pdf"
    elif choice == "4":
        file_name = "vk_data.json"
        out_name = "vk_archive.pdf"
    elif choice == "5":
        file_name = "telegram_messages.json"
        out_name = "telegram_messages.pdf"
    elif choice == "6":
        file_name = input("Enter JSON filename (with extension): ").strip()
        out_name = input("Enter target PDF filename (with extension): ").strip()
    else:
        print("[!] Invalid option.")
        return

    keep_temp = input("Keep temporary PDF chunks? (y/N): ").strip().lower() == 'y'
    pdf_converter.convert_json_to_pdf(file_name, out_name, keep_temp=keep_temp)

def main():
    while True:
        print("\n" + "═"*40)
        print("   SOCIAL MEDIA ARCHIVER PLATFORM")
        print("═"*40)
        print("1. Launch Chrome (Profile / Session setup)")
        print("2. Run Discord Scraper")
        print("3. Run Twitter Bookmarks Scraper")
        print("4. Run Bluesky Saved Posts Scraper")
        print("5. Run VK Scraper (Auto-detect Album/Page)")
        print("6. Run Telegram Scraper")
        print("7. Generate PDF Archive from JSON")
        print("8. Exit")
        print("═"*40)
        
        choice = input("Select an action (1-8): ").strip()
        
        if choice == "1":
            launch_chrome_for_testing()
        elif choice == "2":
            filename = input("Enter output JSON filename (default: disc_msgs.json): ").strip() or "disc_msgs.json"
            scraper.scrape_discord_messages(json_file=filename)
        elif choice == "3":
            filename = input("Enter output JSON filename (default: bookmarks.json): ").strip() or "bookmarks.json"
            scraper.scrape_twitter_bookmarks(json_file=filename)
        elif choice == "4":
            filename = input("Enter output JSON filename (default: bsky_bookmarks.json): ").strip() or "bsky_bookmarks.json"
            scraper.scrape_bluesky_bookmarks(json_file=filename)
        elif choice == "5":
            filename = input("Enter output JSON filename (default: vk_data.json): ").strip() or "vk_data.json"
            scraper.scrape_vk(json_file=filename)
        elif choice == "6":
            filename = input("Enter output JSON filename (default: telegram_messages.json): ").strip() or "telegram_messages.json"
            scraper.scrape_telegram_messages(json_file=filename)
        elif choice == "7":
            pdf_conversion_menu()
        elif choice == "8":
            print("\nExiting program.")
            break
        else:
            print("[!] Unknown menu index. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown signal received.")
