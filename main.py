import requests
from bs4 import BeautifulSoup #, NavigableString
from datetime import datetime
import json

# site_configs = {
#     'who.int': {
#         'title_selector': 'title',
#         'description_selector': 'title',
#         'body_selector': ['article',"section.sf-content.content div.sf-content-block.content-block"],  # Adjust based on actual class if necessary
#         'paragraph_selector': ['p'],
#         'embed_selector': ['a'],
#         'date_posted_selector': 'div[class="date"] span[class="timestamp"]',  # Adjust based on actual class if necessary
#     },
#     'news.un': {
#         'title_selector': 'meta[property="og:title"]',
#         'description_selector': 'meta[property="og:description"]',
#         'body_selector': ['div[class*="clearfix text-formatted"]'],  # Adjust based on actual class if necessary
#         'paragraph_selector': ['h2', 'p'],
#         'embed_selector': ['div[class*="type-twitter"]','div[class*="type-remote_video"]','div[class*="type-entermedia_image"]'],
#         'date_posted_selector': 'time[class="datetime"]',  # Adjust based on actual class if necessary
#     },
#     # Placeholder for other site configurations
#     # 'politico': {},
#     # 'thehill': {},
#     # 'nypost': {},
#     # 'breitbart': {},
#     # 'axios': {},
#     # 'hhs.gov': {},
# }
#
#
# def get_site_config(url, site_configs):
#     for key, config in site_configs.items():
#         if key in url:
#             return config
#     return None
#
#
# def process_element(soup, selector, attr=None, default="Not found"):
#     element = soup.select_one(selector)
#     if not element:
#         return default
#     if attr:
#         return element.get(attr, default).strip()
#     return element.get_text(separator=' ', strip=True)
#
#
# def decompose_embeds(soup, embed_selectors):
#     for selector in embed_selectors:
#         for embed in soup.select(selector):
#             embed.decompose()


def scrape_url(url): # , config):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to access {url} with status code {response.status_code}."}

    soup = BeautifulSoup(response.content, 'html.parser')

    # Modify the way title and description are processed
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else 'Title not found'

    body_tag = soup.find('body')
    body = body_tag.get_text(strip=True) if body_tag else 'Body not found'

    #date_posted = process_date(soup, config['date_posted_selector'])
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'title': title,
        'body': body,
        'date_added': date_added,
        # 'date_posted': date_posted
    }


# def process_body(soup, body_selectors, paragraph_selectors):
#     body_texts = []  # Use a list to collect all text pieces
#     for selector in body_selectors:
#         body_div = soup.select_one(selector)
#         if body_div:
#             # Find all elements that match any tag in paragraph_selectors
#             content_elements = body_div.find_all(paragraph_selectors)
#             for element in content_elements:
#                 # Append the text of each element to the list
#                 body_texts.append(element.get_text(strip=True))
#             # Join all text pieces with a space
#             return ' '.join(body_texts)
#     return "No body content found"



# def process_date(soup, date_selector):
#     time_element = soup.select_one(date_selector)
#     if time_element and time_element.has_attr('datetime'):
#         return datetime.fromisoformat(time_element['datetime'].rstrip('Z')).strftime('%Y-%m-%d %H:%M:%S')
#     elif time_element:
#         return datetime.strptime(time_element.text.strip(), "%d %B %Y").strftime('%Y-%m-%d %H:%M:%S')
#     return "No date posted found"


def scrape_urls(urls):
    scraped_contents = []
    for url in urls:
        # config = get_site_config(url, site_configs)
        # if not config:
        #     scraped_contents.append({"error": "News site not supported"})
        #     continue
        content = scrape_url(url) #, config)
        scraped_contents.append(content)
    return scraped_contents


# Example usage with provided URLs
urls = [
    "https://www.who.int/emergencies/situations/conflict-in-Israel-and-oPt",
    "https://www.who.int/news/item/01-02-2024-global-cancer-burden-growing--amidst-mounting-need-for-services",
    "https://www.who.int/emergencies/disease-outbreak-news/item/2024-DON504",
    "https://news.un.org/en/story/2024/02/1146317",
    "https://news.un.org/en/story/2024/02/1146127",
    "https://news.un.org/en/story/2024/02/1146302",
    "https://news.un.org/en/story/2024/02/1146327",
    "https://news.un.org/en/story/2024/02/1146322",
]

contents = scrape_urls(urls)
json_result = json.dumps(contents, indent=4, ensure_ascii=False)

# Print the JSON-formatted string
print(json_result)
