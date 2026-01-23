# AI Student Travel Planner

A modern, interactive travel planner for students, powered by Google Gemini AI and built with Streamlit. Generate smart, budget-friendly itineraries with day-wise plans, maps, and travel tips for any city in India.

## Features
- Enter your trip details (location, budget, days, group size, interests)
- Generates a structured, student-friendly itinerary using Gemini AI
- Visualizes daily locations on an interactive map (folium)
- Shows estimated budget breakdown and travel tips
- No Node backend required—everything runs in Python

## Setup
1. **Clone this repo or copy the folder**
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install streamlit-folium folium
   ```
3. (Optional) Set your Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY=your-key-here  # Linux/macOS
   set GEMINI_API_KEY=your-key-here     # Windows
   ```
   Or edit the API key directly in `app.py`.
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Fill in your trip details and click **Generate Itinerary**
- The app will call Gemini AI and display:
  - A structured itinerary (day-wise)
  - An interactive map with daily locations
  - Budget breakdown and travel tips

## Notes
- The app uses the Gemini API key from the environment or hardcoded in `app.py`.
- For best results, use a valid Gemini API key with sufficient quota.
- Map pins use the standard Leaflet marker icon.

## License
MIT
