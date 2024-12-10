from publisher import scrape_and_publish_q, scrape_and_publish
import time


#TODO GADAKETEBA ISE ROM TIPI TAVISIT GANSAZGVROS DA IMIS MIXEDVIT GAUSHVAS SHESABAMISI FUNQCIA

tasks_dict = {}
# type = input("აირჩიე რეჟიმი:\n 1) იყიდება\n 2) ქირავდება\n")

def start():
    link = input("Paste the link of MyHome Post: ")
    description = input("Type Description you want your post to have: ")
    tasks_dict[link] = description
    again = input("Would you like to add more link (y/n): ").lower()
    if again == "y":
        start()
    else:
        for link,description in tasks_dict.items():
            if type == "1":
                scrape_and_publish(link, description)
                print(link, "DONE")
            elif type == "2":
                scrape_and_publish_q(link, description)
                print(link, "DONE")

scrape_and_publish_q("https://www.myhome.ge/pr/19523903/qiravdeba-dghiurad-1-otaxiani-bina-saburtaloze/", "testia es waishleba")



# start()


