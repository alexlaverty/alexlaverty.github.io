import requests
import xml.etree.ElementTree as ET

# Replace with your IndexNow API key and host URL
INDEXNOW_API_KEY = 'b219f4fe97ce479f8e57e36600538ef4'
INDEXNOW_ENDPOINT = 'https://www.bing.com/indexnow'

# Replace with your Jekyll site's sitemap URL
SITEMAP_URL = 'https://alexlaverty.github.io/sitemap.xml'

def fetch_sitemap_urls(sitemap_url):
    """Fetch and parse URLs from the sitemap."""
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            sitemap_xml = response.content
            urls = []
            root = ET.fromstring(sitemap_xml)
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                urls.append(loc)
            return urls
        else:
            print(f"Failed to fetch sitemap: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def submit_urls_to_indexnow(urls, api_key):
    """Submit a list of URLs to IndexNow."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "host": "alexlaverty.github.io",
        "key": api_key,
        "keyLocation": "https://alexlaverty.github.io/b219f4fe97ce479f8e57e36600538ef4.txt",
        "urlList": urls
    }
    try:
        response = requests.post(INDEXNOW_ENDPOINT, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Successfully submitted {len(urls)} URLs to IndexNow.")
        else:
            print(f"Failed to submit URLs: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error submitting URLs to IndexNow: {e}")

if __name__ == '__main__':
    urls = fetch_sitemap_urls(SITEMAP_URL)
    if urls:
        submit_urls_to_indexnow(urls, INDEXNOW_API_KEY)
