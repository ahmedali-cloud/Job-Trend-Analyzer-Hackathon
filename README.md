# Real-Time Job Trend Analyzer

A Python-based web application that scrapes job listings from Indeed and analyzes trends in real-time.

## Features

- Scrapes job data from Indeed job portal
- Real-time analysis of job trends
- Interactive visualizations
- Search functionality for specific job roles
- Displays top job titles, required skills, and locations
- Automated periodic data updates

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```

## Project Structure

- `app.py`: Main Flask application
- `scraper/`: Contains web scraping modules
  - `indeed_scraper.py`: Indeed scraping logic
- `static/`: Static files (CSS)
- `templates/`: HTML templates
- `data/`: Stored job data

## Technologies Used

- Python 3.8+
- Flask
- BeautifulSoup4
- Selenium
- Pandas
- Matplotlib
- Seaborn
- APScheduler 