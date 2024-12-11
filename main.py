from scraper import scrape_and_post
import time


tasks_dict = {}

def start():
    link = input("Paste the link of MyHome Post: ")
    description = input("Type Description you want your post to have: ")
    tasks_dict[link] = description
    again = input("Would you like to add more link (y/n): ").lower()
    if again == "y":
        start()
    else:
        for link,description in tasks_dict.items():
            scrape_and_post(link,description)


start()


