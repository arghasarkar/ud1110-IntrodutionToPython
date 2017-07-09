''' Importing the requests module. This will allow us to send requests to Wikipedia and download the webpage. '''
import requests
''' The webpage is HTML. We shall use the BeautifulSoup4 HTML parser to find the links '''
from bs4 import BeautifulSoup

''' Importing URL Lib for joining the relative and the absolute URL'''
import urllib

# Slowing down the bot
from time import sleep

# Constants
HALT_TIME_IN_SECONDS = 2

def continue_crawl(search_history, target_url, max_steps=25):
    if len(search_history) > max_steps:
        print("Error: Search history has exceeded length: {}".format(len(search_history)))
        return False

    if str(search_history[-1]) == target_url:
        print("Target URL reached:")
        return False

    if len(set(search_history)) < len(search_history):
        print("Error: Stuck in a loop")
        return False

    return True


def find_first_link(url):
    # get the HTML from "url", use the requests library
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # find the first link in the article
    first_link = None
    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            first_link = element.find("a", recursive=False).get("href")
            break

    # return the first link as a string, or return None if there is no link
    if not first_link:
        return None
    else:
        first_link = urllib.parse.urljoin('https://en.wikipedia.org/', first_link)
        print(first_link)
        return first_link


def web_crawl():

    # Starting URL
    start_url = "https://en.wikipedia.org/wiki/Special:Random"

    # Target URL
    target_url = "https://en.wikipedia.org/wiki/Philosophy"

    # List containing visited history
    article_chain = [start_url]

    while continue_crawl(article_chain, target_url):
        # download html of last article in article_chain
        # find the first link in that html
        first_link = find_first_link(article_chain[-1])
        # add the first link to article chain
        article_chain.append(first_link)

        if (not first_link):
            print("Error: Article with no links found.")
            break

        if (first_link == target_url):
            print("\n\nWe have found the article! DING!!! DING!!! DING!!!\n\n")
            print(str(article_chain))
            break

        # delay for about two seconds
        sleep(HALT_TIME_IN_SECONDS)

if __name__ == "__main__":
    web_crawl()

