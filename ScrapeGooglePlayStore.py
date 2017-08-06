import urllib.request
import json
import re
from bs4 import BeautifulSoup

def get_page(page):

    with urllib.request.urlopen(page) as response:
       html = response.read()
    return BeautifulSoup(html, "html.parser")

def save_app_json(url):

    # Grab the data from the url
    app = {}
    soup = get_page(url)

    # Obtain app attributes
    m = re.search(r"(id=)[^&]+", url)
    app["package_name"] = url[m.start()+3:m.end()]

    app["title"] = soup.find("div", {"class": "id-app-title"}).text
    app["short_description"] = soup.find("meta", {"name": "description"}).get("content")
    app["description"] = soup.find("div", {"class": "show-more-content text-body"}).text
    app["rating"] = soup.find("meta", {"itemprop": "ratingValue"}).get("content")
    app["genre"] = soup.find("span", {"itemprop": "genre"}).text

    result = soup.find("a", {"class": "document-subtitle category"}).get("href")
    m = re.search(r"(category/)+", result)
    app["cat_key"] = result[m.start()+9:]

    app["price"] = soup.find("meta", {"itemprop": "price"}).get("content")
    app["downloads"] = soup.find("div", {"itemprop": "numDownloads"}).text.replace(" ","")
    app["version"] = soup.find("div", {"itemprop": "softwareVersion"}).text
    app["content_rating"] = soup.find("img", {"class": "document-subtitle content-rating-badge"}).get("alt")
    app["market_update"] = soup.find("div", {"itemprop": "datePublished"}).text

    screens = soup.find_all("img", {"class": "screenshot"})
    app["screenshots"] = []
    for screen in screens:
        app["screenshots"].append("https:" + screen.get("src"))

    app["developer"] = soup.find("a", {"class": "document-subtitle primary"}).find("span", {"itemprop": "name"}).text
    app["num_ratings"] = soup.find("span", {"class": "reviews-num"}).text
    app["icon"] = "https:" + soup.find("img", {"class": "cover-image"}).get("src")

    # Store the app attributes into a JSON file
    with open(app["title"].replace(" ","_") + ".json", "w") as fp:
        json.dump(app, fp)


# Example Usage
save_app_json("https://play.google.com/store/apps/details?id=com.rovio.angrybirdsspace.ads&hl=en")
