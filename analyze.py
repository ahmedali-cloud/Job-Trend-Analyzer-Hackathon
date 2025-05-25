import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data():
    files = ['data/remoteok_jobs.csv', 'data/indeed_jobs.csv']
    dfs = []

    for file in files:
        if os.path.exists(file) and os.path.getsize(file) > 0:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
            except Exception as e:
                print(f"⚠️ Error reading {file}: {e}")

    if not dfs:
        print("❌ No valid data files found.")
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

def analyze_jobs(df):
    if df.empty:
        print("⚠️ No data to analyze.")
        return

    print("✅ Total jobs:", len(df))

    # Top 5 job titles
    if 'title' in df.columns:
        top_titles = df['title'].value_counts().head(5)
        print("\n📌 Top 5 Job Titles:")
        print(top_titles)

        # Plot job titles
        plt.figure(figsize=(8,5))
        sns.barplot(x=top_titles.values, y=top_titles.index, palette="viridis")
        plt.title("Top 5 Job Titles", fontsize=14)
        plt.xlabel("Number of Jobs", fontsize=12)
        plt.ylabel("Job Title")
        plt.tight_layout()
        os.makedirs("data", exist_ok=True)
        plt.savefig("data/top_job_titles.png")
        plt.show()
    else:
        print("❌ 'title' column not found in data.")

    # Top 5 locations
    if 'location' in df.columns:
        top_locations = df['location'].value_counts().head(5)
        print("\n🌍 Top 5 Locations:")
        print(top_locations)
    else:
        print("❌ 'location' column not found in data.")

if __name__ == "__main__":
    df = load_data()
    analyze_jobs(df)
