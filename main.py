from publisher import scrape_and_publish, scrape_and_publish_q
import time

tasks_dict = {}
type = input("აირჩიე რეჟიმი:\n 1) იყიდება\n 2) ქირავდება\n")

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
            if type == "1":
                scrape_and_publish(link, description)
                print(link, "DONE")
            elif type == "2":
                scrape_and_publish_q(link, description)
                print(link, "DONE")

start()


