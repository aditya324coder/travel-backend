import streamlit as st

import requests
import os

st.set_page_config(page_title="AI Student Travel Planner", layout="wide")
st.title("AI Travel Planner for Students")
st.write("Smart, budget-friendly trip planning powered by AI")


api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyDbW-z5tFqwXEzgzMLXXeB1YxUxynVH1CU")

with st.form("trip_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        location = st.text_input("Location", "")
        days = st.number_input("Number of Days", min_value=1, value=3)
    with col2:
        budget = st.number_input("Total Budget (INR)", min_value=0, value=5000)
        group_size = st.number_input("Group Size", min_value=1, value=2)
    with col3:
        interests = st.text_input("Interests (comma separated)", "Food, History, Adventure")
    submitted = st.form_submit_button("Generate Itinerary")

if 'itinerary' not in st.session_state:
    st.session_state['itinerary'] = ''

if submitted:
    if not api_key:
        st.error("No Gemini API Key found in code or environment variable.")
    else:
        with st.spinner("Generating itinerary via Gemini API..."):
            prompt = f"""
You are an AI travel planner for students.
Generate a smart, budget-friendly travel itinerary STRICTLY in the structured format below.
Do NOT add extra text, explanations, emojis, or markdown.
Return plain text only, exactly following the sections and labels.

INPUT DETAILS:
Location: {location}
Total Budget (INR): {budget}
Number of Days: {days}
Group Size: {group_size}
Interests: {interests}

========================
DAY-WISE ITINERARY
========================
Day 1:
Title: <Main place / area name>
Plan:
- Morning:
- Afternoon:
- Evening:
- Night:

Day 2:
Title:
Plan:
- Morning:
- Afternoon:
- Evening:
- Night:

(Repeat until all days are covered)

========================
MAP LOCATIONS (COORDINATES)
========================
Day 1:
Place: <Place name>
Latitude: <decimal latitude>
Longitude: <decimal longitude>

Day 2:
Place:
Latitude:
Longitude:

(One primary location per day, coordinates must be accurate)

========================
ESTIMATED BUDGET BREAKDOWN
========================
Category        Amount
Food            <amount>
Stay            <amount>
Transport       <amount>

Total           <total amount>

========================
BUDGET TRAVEL TIPS
========================
- Tip 1
- Tip 2
- Tip 3

IMPORTANT RULES:
1. Locations must be real and match the city.
2. Coordinates must be valid decimal values usable in maps.
3. Keep the plan realistic for students.
4. Stay within the given total budget.
5. Use affordable transport and stays.
6. Do NOT include currency symbols.
7. Do NOT include markdown characters (*, **, ###).
"""
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            body = {
                "contents": [
                    {"role": "user", "parts": [{"text": prompt}]}
                ]
            }
            try:
                resp = requests.post(url, headers=headers, json=body, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                st.session_state['itinerary'] = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state['itinerary'] = ''

itinerary = st.session_state.get('itinerary', '')
if itinerary:
    # Remove MAP LOCATIONS section from output
    import re
    itinerary_clean = re.sub(r"=+\s*MAP LOCATIONS \(COORDINATES\)[^=]*=+([\s\S]*?)(=+|$)", '', itinerary)
    st.subheader("Generated Itinerary (Raw)")
    st.code(itinerary_clean.strip(), language="text")

    # Parse MAP LOCATIONS section for map only
    map_section = re.search(r"=+\s*MAP LOCATIONS \(COORDINATES\)[^=]*=+([\s\S]*?)(=+|$)", itinerary)
    locations = []
    if map_section:
        loc_text = map_section.group(1)
        day_blocks = re.split(r"Day \d+:\s*", loc_text)[1:]
        for block in day_blocks:
            place = re.search(r"Place:\s*(.*)", block)
            lat = re.search(r"Latitude:\s*([\d.\-]+)", block)
            lng = re.search(r"Longitude:\s*([\d.\-]+)", block)
            if place and lat and lng:
                locations.append({
                    "place": place.group(1).strip(),
                    "lat": float(lat.group(1)),
                    "lng": float(lng.group(1)),
                })

    if locations:
        st.subheader("Map Locations")
        try:
            from streamlit_folium import st_folium
            import folium
            icon_url = "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png"
            icon = folium.CustomIcon(icon_url, icon_size=(28, 40), icon_anchor=(14, 40))
            m = folium.Map(location=[locations[0]['lat'], locations[0]['lng']], zoom_start=10)
            for loc in locations:
                folium.Marker([loc['lat'], loc['lng']], popup=loc['place'], icon=icon).add_to(m)
            st_folium(m, width=700, height=400)
        except ImportError:
            st.info("Install streamlit-folium to see map. Showing coordinates table instead.")
            st.table([{**l, 'lat': f"{l['lat']:.5f}", 'lng': f"{l['lng']:.5f}"} for l in locations])
