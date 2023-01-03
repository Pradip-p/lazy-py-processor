import requests
import bs4
import pandas as pd
import csv

csv_columns = ['title','url','username','date']

SUBREDDITS_CSV = "subreddits.csv"

# SUBREDDIT_URL = "old.reddit.com/r/islam"
# SUBREDDIT_URL =  "https://old.reddit.com/r/islam/new/"
# SUBREDDIT_URL = 'https://old.reddit.com/subreddits/new/'

posts = []  # list to store dictionaries representing each post

def scrape_subreddit(url):

    """Scrape all posts on a subreddit by iterating through pages and returning a list of dictionaries containing post information."""

    # send request to subreddit URL and parse HTML response
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers, timeout=10)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # extract information for each post on the current page
    for post in soup.find_all("div", class_="entry unvoted"):
    # extract title, URL, submitter username, and submission date
        
        try:
            title = post.find("a", class_="title").text
        except AttributeError:
            title = ''
        
        try:
            url = post.find("a", class_="title").get("href")
        except AttributeError:
            url = ''

        
        try:
            username = post.find("a", class_="author").text
        except AttributeError:
            username = ''

        try:
            date = post.find("time").get("datetime")
        except AttributeError:
            date = ''

        data = {"title": title, "url": url, "username": username, "date": date}
        # store information in a dictionary and add it to the list of posts
        posts.append(data)

    # # check for a "next" button to see if there are more pages to scrape    
    next_button = soup.find("span", class_="next-button")

    if next_button:
    #if there is a "next" button, scrape the next page by calling the function recursively
        next_url = next_button.find("a").get("href")

        scrape_subreddit(next_url)
        
    with open(SUBREDDITS_CSV, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        writer.writerows(posts)


def search_and_scrape_subreddits(search_query):
    """Scrape all posts on a list of subreddits matching a particular search query."""

    # url = f"https://old.reddit.com/search?q={search_query}"
    url = f"https://old.reddit.com/subreddits/search?q={search_query}"

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers, timeout=10)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    # extract information for each post on the current page
    for post in soup.find_all("div", class_="entry unvoted"):
        url = post.find("a", class_="title").get("href")

        scrape_subreddit(url)
        print("page scraped")

    next_button = soup.find("span", class_="next-button")

    if next_button:
        #if there is a "next" button, scrape the next page by calling the function recursively
        next_url = next_button.find("a").get("href")
        print("next page continue...")
        search_and_scrape_subreddits(next_url)
        print('completed next page!')
        


if __name__ == "__main__":

    SEARCH_QUERY = "pillow"

    SEARCH_QUERY = 'islam'

    # scrape multiple subreddits
    posts = search_and_scrape_subreddits(SEARCH_QUERY)
