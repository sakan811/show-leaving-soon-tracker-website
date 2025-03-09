# Show Leaving Soon Tracker Website

A Vue.js application that displays shows leaving the platform soon, featuring a countdown timer for each show based on the user's local timezone.

## Status

[![Frontend Tests](https://github.com/sakan811/netflix-leaving-soon-tracker-website/actions/workflows/frontend-tests.yml/badge.svg)](https://github.com/sakan811/netflix-leaving-soon-tracker-website/actions/workflows/frontend-tests.yml)

## Accessing the website

<https://show-leaving-soon-tracker-website.vercel.app/>

## Run the Project Locally

### Setup the Project

1. Clone the repository

   ```bash
   git clone https://github.com/sakan811/netflix-leaving-soon-tracker-website.git
   cd netflix-leaving-soon-tracker-website
   ```

2. Sign up for a [RapidAPI](https://rapidapi.com/) account
3. Subscribe to the [Streaming Availability API](https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability)
4. Get your API key from the Streaming Availability API dashboard
5. Create a `.env` file in the `scraper` directory with the following content:

   ```bash
   RAPIDAPI_KEY=your_api_key_here
   ```

### Run the Scraper

1. Navigate to `scraper` directory

    - ```bash
      cd scraper
      ```

2. Run the main.py file to scrape the data

    - ```bash
      python main.py
      ```

### Run the Website Locally

1. Navigate to `frontend` directory

    - ```bash
      cd frontend
      ```

2. Install dependencies

    - ```bash
      npm install
      ```

3. Start the development server

    - ```bash
      npm run dev
      ```

4. Open your browser and navigate to <http://localhost:3000>

## Docs

### Sequence Diagrams

[Click here to view the sequence diagrams](./docs/mermaid-charts.md)
