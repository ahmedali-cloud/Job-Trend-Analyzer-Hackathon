import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import altair as alt
from analyzer.analyze import load_data

st.set_page_config(page_title="Job Trend Analyzer", layout="wide")
st.title("💼 Real-Time Job Trend Analyzer")

# Button to refresh data
if st.button("🔄 Refresh Data from RemoteOK"):
    with st.spinner("Scraping latest jobs..."):
        import scraper.remoteok_scraper
        scraper.remoteok_scraper.scrape_remoteok()
        st.success("✅ Data refreshed!")

df = load_data()

if df.empty:
    st.warning("No job data available.")
else:
    # Keyword Search Filter (Bonus)
    st.subheader("🧰 Filter Jobs")
    keyword = st.text_input("🔍 Search Keyword (e.g. Data Analyst)")

    all_titles = sorted(df["title"].dropna().unique())
    all_locations = sorted(df["location"].dropna().unique())

    selected_title = st.selectbox("Filter by Title", ["All"] + all_titles)
    selected_location = st.selectbox("Filter by Location", ["All"] + all_locations)

    # Apply filters
    if keyword:
        df = df[df["title"].str.contains(keyword, case=False, na=False) | 
                df["company"].str.contains(keyword, case=False, na=False)]

    if selected_title != "All":
        df = df[df["title"] == selected_title]

    if selected_location != "All":
        df = df[df["location"] == selected_location]

    # Chart - Top 5 Job Titles (Bar & Pie)
    st.subheader("📊 Top 5 Job Titles (Bar & Pie View)")

    top_titles = df["title"].value_counts().head(5).reset_index()
    top_titles.columns = ["Job Title", "Count"]

    # Bar Chart
    bar_chart = alt.Chart(top_titles).mark_bar(color='skyblue').encode(
        x=alt.X('Job Title:N', sort='-y'),
        y=alt.Y('Count:Q'),
        tooltip=['Job Title', 'Count']
    ).properties(
        width=400,
        height=300,
        title="Top 5 Job Titles (Bar)"
    )

    # Pie Chart
    pie_chart = alt.Chart(top_titles).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Job Title", type="nominal"),
        tooltip=["Job Title", "Count"]
    ).properties(
        width=400,
        height=300,
        title="Top 5 Job Titles (Pie)"
    )

    # Display side-by-side
    col1, col2 = st.columns(2)
    col1.altair_chart(bar_chart, use_container_width=True)
    col2.altair_chart(pie_chart, use_container_width=True)

    # Top 5 Locations Table
    st.subheader("🌍 Top 5 Locations")
    top_locations = df["location"].value_counts().head(5).reset_index()
    top_locations.columns = ['Location', 'Count']
    st.table(top_locations)

    # Posting Trends Over Time (Line Chart)
    if 'date_posted' in df.columns and not df['date_posted'].isnull().all():
        df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
        date_counts = df.groupby(df['date_posted'].dt.date).size().reset_index(name='Count')

        st.subheader("📈 Job Postings Over Time")
        line_chart = alt.Chart(date_counts).mark_line(point=True).encode(
            x='date_posted:T',
            y='Count:Q',
            tooltip=['date_posted', 'Count']
        ).properties(
            width=800,
            height=300,
            title="Job Postings Over Time"
        )
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.info("📅 No valid 'date_posted' data available for trend chart.")

    # Skills Frequency Chart
    if 'skills' in df.columns and df['skills'].notnull().any():
        from collections import Counter
        skills_series = df['skills'].dropna().apply(lambda x: [skill.strip() for skill in x.split(',')])
        all_skills = [skill for sublist in skills_series for skill in sublist if skill]

        skill_counts = Counter(all_skills).most_common(10)
        skill_df = pd.DataFrame(skill_counts, columns=['Skill', 'Count'])

        st.subheader("🛠️ Top Skills Required")
        skills_bar_chart = alt.Chart(skill_df).mark_bar(color='orange').encode(
            x=alt.X('Count:Q'),
            y=alt.Y('Skill:N', sort='-x'),
            tooltip=['Skill', 'Count']
        ).properties(
            width=600,
            height=300,
            title="Top 10 Skills Required"
        )
        st.altair_chart(skills_bar_chart, use_container_width=True)
    else:
        st.info("🛠️ No skill data available.")

    # Full Job Listings Table
    st.subheader("📝 Job Listings")
    df_display = df.reset_index(drop=True).copy()
    df_display.index = df_display.index + 1  # Start index from 1
    st.dataframe(df_display[["title", "company", "location", "date_posted", "link"]])
