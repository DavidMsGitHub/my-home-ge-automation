from publisher import scrape_and_publish
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
        print("Get ready, we are starting...")
        time.sleep(0.5)
        print("3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(0.8)
        print("START!")
        for link,description in tasks_dict.items():
            scrape_and_publish(link, description)
            print(link, "DONE")

start()

