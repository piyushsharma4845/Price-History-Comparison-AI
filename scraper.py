import requests
from bs4 import BeautifulSoup
import re
import time

def fetch_amazon_price(url):
    # Expanded headers to look exactly like a real Windows Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        session = requests.Session()
        # Add a tiny delay to not seem like a fast bot
        time.sleep(1)
        response = session.get(url, headers=headers, timeout=20)
        
        if "Robot Check" in response.text or "captcha" in response.text.lower():
            return "BLOCKED", None

        soup = BeautifulSoup(response.content, "html.parser")

        # --- STEP 1: FIND TITLE (Broader Selectors) ---
        title_tag = (
            soup.find("span", {"id": "productTitle"}) or 
            soup.find("h1", {"id": "title"}) or
            soup.select_one(".a-size-large.product-title-word-break")
        )
        
        if not title_tag:
            # If title is still not found, print to terminal for debugging
            print("Title not found. Amazon might be serving a limited page.")
            return "NOT_FOUND", None
            
        name = title_tag.get_text().strip()

        # --- STEP 2: FIND ACCURATE PRICE (Prioritized) ---
        price = None
        
        # We look for 'priceToPay' - this is what you actually pay at checkout
        selectors = [
            "span.priceToPay span.a-offscreen", 
            "span.apexPriceToPay span.a-offscreen",
            "div.a-section.a-spacing-none.a-spacing-top-mini span.a-color-price",
            "span.a-price-whole"
        ]

        for selector in selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price_text = price_tag.get_text()
                # REGEX: Remove commas, currency symbols, and spaces
                clean_text = re.sub(r'[^\d]', '', price_text)
                
                if clean_text:
                    price = float(clean_text)
                    # Correct for cases where .00 is appended as digits
                    if ".00" in price_text and len(clean_text) > 3:
                        price = price / 100
                    break 

        return name, price

    except Exception as e:
        print(f"Detailed Error: {e}")
        return None, None