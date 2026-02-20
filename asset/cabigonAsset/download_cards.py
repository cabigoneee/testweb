import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin

def download_snorlax_cards():
    """Download all Snorlax card images from LimitlessTCG"""
    
    # URL to scrape
    url = "https://limitlesstcg.com/cards/jp?q=pokemon%3Asnorlax"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Downloading cards to: {output_dir}")
    print(f"Fetching page: {url}")
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all card images - adjust selectors based on actual page structure
        # Common patterns: img tags with card-related classes or within card containers
        card_images = []
        
        # Try multiple selectors to find card images
        selectors = [
            'img.card-image',
            'img[alt*="card"]',
            'div.card img',
            'a[href*="/cards/"] img',
            'img[src*="card"]',
            'img[src*=".png"]'
        ]
        
        for selector in selectors:
            images = soup.select(selector)
            if images:
                card_images.extend(images)
                print(f"Found {len(images)} images with selector: {selector}")
        
        # Remove duplicates
        seen_urls = set()
        unique_images = []
        for img in card_images:
            src = img.get('src') or img.get('data-src')
            if src and src not in seen_urls:
                seen_urls.add(src)
                unique_images.append(img)
        
        print(f"\nTotal unique images found: {len(unique_images)}")
        
        if not unique_images:
            print("\nNo images found. Let me show you the page structure:")
            print("\nAll img tags found:")
            all_imgs = soup.find_all('img')
            for i, img in enumerate(all_imgs[:10]):  # Show first 10
                print(f"{i+1}. src={img.get('src')}, class={img.get('class')}, alt={img.get('alt')}")
            return
        
        # Download each image
        downloaded = 0
        for idx, img in enumerate(unique_images, 1):
            src = img.get('src') or img.get('data-src')
            
            if not src:
                continue
            
            # Make absolute URL
            img_url = urljoin(url, src)
            
            # Skip if not a PNG or JPG
            if not (img_url.lower().endswith('.png') or img_url.lower().endswith('.jpg') or img_url.lower().endswith('.jpeg')):
                continue
            
            # Generate filename
            filename = os.path.basename(img_url.split('?')[0])  # Remove query params
            if not filename:
                filename = f"snorlax_card_{idx}.png"
            
            filepath = os.path.join(output_dir, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                print(f"[{idx}/{len(unique_images)}] Skipping (already exists): {filename}")
                continue
            
            try:
                print(f"[{idx}/{len(unique_images)}] Downloading: {filename}")
                img_response = requests.get(img_url, headers=headers, timeout=30)
                img_response.raise_for_status()
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                downloaded += 1
                print(f"  ✓ Saved: {filename}")
                
                # Be polite - add delay between downloads
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ Error downloading {filename}: {e}")
        
        print(f"\n{'='*50}")
        print(f"Download complete!")
        print(f"Successfully downloaded: {downloaded} images")
        print(f"Location: {output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTip: The page might use JavaScript to load images dynamically.")
        print("If this script doesn't work, you may need to use Selenium or Playwright.")

if __name__ == "__main__":
    download_snorlax_cards()
