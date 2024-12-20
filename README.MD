# MyHome.ge Property Copy Posting Automation Tool

## Overview

This Python tool automates the process of copying and reposting property listings from [myhome.ge](https://myhome.ge). It extracts property details and images from provided links and creates new posts with updated descriptions.

## Features

- **Automated Data Extraction**: Retrieves property details and images from myhome.ge.
- **Image Downloading**: Saves all images associated with the property listing.
- **Automated Posting**: Reposts the property with a new description and the same photos.

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3 installed.
2. **Chrome WebDriver**: Download and install the Chrome WebDriver from [ChromeDriver](https://sites.google.com/chromium.org/driver/). Ensure it's compatible with your Chrome version.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/DavidMsGitHub/my-home-ge-automation.git
    cd my-home-ge-automation
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure `config.json`**:
    Create a `config.json` file in the project directory with the following format:
    ```json
    {
      "credentials": {
        "email": "your_email@example.com",
        "password": "your_password"
      },
      "contact": {
        "name": "Your Name",
        "number": "Your Phone Number"
      },
      "webdriver-location": "path/to/chromedriver"
    }
    ```
    - Replace placeholder values with your actual details.
    - Ensure the WebDriver path is correct.

## Usage

1. **Run the Script**:
    ```bash
    python main.py
    ```

2. **Follow Prompts**:
    - Enter the link of the property post you want to copy.
    - Enter the new description for the reposted property.

   The script will extract data from the provided link and create a new post with the updated description.

## Testing

This tool has been tested on:
- **macOS Monterey**
- **Windows 10**

With:
- **Chrome and ChromeDriver Version 126.0.6478.126 (Official Build) (x86_64)**

## Notes

- Ensure your Chrome WebDriver version matches your Chrome browser version.
- For security, avoid committing sensitive information like passwords to public repositories.
- 
## Acknowledgments

Thanks to the Selenium team for their powerful browser automation tools.
