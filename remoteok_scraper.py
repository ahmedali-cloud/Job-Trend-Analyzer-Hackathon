import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_remoteok():
    categories = [
        "remote-dev-jobs",
        "remote-design-jobs",
        "remote-data-jobs",
        "remote-customer-support-jobs",
        "remote-marketing-jobs"
    ]
    
    base_url = "https://remoteok.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    jobs = []

    for category in categories:
        url = f"{base_url}{category}"
        print(f"🔍 Scraping: {url}")
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print("Error fetching page:", e)
            continue

        for job in soup.find_all("tr", class_="job"):
            try:
                title = job.find("h2").text.strip()
                company = job.find("h3").text.strip()
                tags = [tag.text.strip() for tag in job.find_all("span", class_="tag")]
                date_posted = job.find("time")["datetime"] if job.find("time") else "N/A"
                link = "https://remoteok.com" + job["data-href"]
                location_tag = job.find("div", class_="location")
                location = location_tag.text.strip() if location_tag else "Remote"

                jobs.append({
                    "title": title,
                    "company": company,
                    "date_posted": date_posted,
                    "link": link,
                    "location": location
                })
            except:
                continue

    df = pd.DataFrame(jobs)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/remoteok_jobs.csv", index=False)
    print(f"✅ Scraped {len(df)} jobs from RemoteOK and saved to 'data/remoteok_jobs.csv'.")

if __name__ == "__main__":
    scrape_remoteok()
