import os
from textwrap import dedent

from dotenv import load_dotenv

# 1. Core Imports
from google import genai
from crewai import Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# Local imports (ensure trip_agents.py and trip_tasks.py are in the same folder)
from trip_agents import TripAgents
from trip_tasks import TripTasks

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def build_llm():
    google_key = os.getenv('GOOGLE_API_KEY')
    if google_key:
        return 'gemini/gemini-2.0-flash'
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        return os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
    return None


def verify_gemini_connection(city):
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return False, 'GOOGLE_API_KEY is not set.'

    try:
        client = genai.Client(api_key=api_key)
        test_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f'Give me one extremely famous landmark in {city}.'
        )
        return True, test_response.text.strip()
    except Exception as error:
        return False, str(error)


def build_fallback_plan(origin, city, date_range, interests, reason):
    return dedent(f"""
    ## Fallback Trip Plan

    Real-time AI planning is currently unavailable.
    Reason: {reason}

    This fallback plan is a static itinerary based on your inputs and does not include live pricing, live weather, or API-fetched places.

    ### Trip Summary
    - Origin: {origin}
    - Destination: {city}
    - Date Range: {date_range}
    - Interests: {interests}

    ### Suggested 7-Day Outline
    Day 1: Arrival, settle near the city center, and take an evening walk around the main historic district.
    Day 2: Visit the main university area, identify campus buildings, admissions offices, and nearby study-friendly cafes.
    Day 3: Explore major academic neighborhoods, libraries, and public transport routes between housing and university zones.
    Day 4: Review accommodation options, estimate commute times, and shortlist affordable food spots near the university.
    Day 5: Spend the day in museums, public plazas, and cultural landmarks to understand the city beyond academics.
    Day 6: Compare student services, co-working or library spaces, and practical essentials such as supermarkets and pharmacies.
    Day 7: Keep a flexible day for follow-up campus visits, paperwork, or meeting student support offices before departure.

    ### Packing Suggestions
    - Passport and study documents
    - Printed and digital copies of university paperwork
    - Comfortable walking shoes
    - Weather-appropriate layers
    - Charger, adapter, and backup battery
    - Notebook or laptop for campus visits

    ### Budget Guidance
    - Accommodation: check student-friendly hotels, hostels, or short-stay rentals near the university area
    - Transport: plan for airport transfer plus 7 days of metro or bus use
    - Food: budget for a mix of groceries, cafes, and one or two restaurant visits
    - Miscellaneous: include museum tickets, local SIM or data, and emergency cash buffer

    ### Next Step
    Re-run the app once your LLM/API access is available to generate a live researched itinerary with actual places, weather, and costs.
    """).strip()


llm = build_llm()

# 3. The CrewAI Controller Class
class TripCrew:
    def __init__(self, origin, cities, date_range, interests, llm=None):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests
        self.llm = llm

    def run(self):
        # Initialize the logic from your supporting files
        if self.llm is None:
            return build_fallback_plan(
                self.origin,
                self.cities,
                self.date_range,
                self.interests,
                'LLM provider is not configured.'
            )

        try:
            agents = TripAgents(self.llm)
            tasks = TripTasks()

            # Create the Agents (Note: ensure your TripAgents class passes 'llm' to these)
            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            # Define the Tasks
            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.cities,
                self.interests,
                self.date_range
            )
            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range
            )
            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            # Assemble the Crew
            crew = Crew(
                agents=[
                    city_selector_agent,
                    local_expert_agent,
                    travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                verbose=True
            )

            result = crew.kickoff()
            return result
        except Exception as error:
            return build_fallback_plan(
                self.origin,
                self.cities,
                self.date_range,
                self.interests,
                f'Crew execution failed: {error}'
            )

# 4. Main Execution Block
if __name__ == "__main__":
    print("\n## Welcome to Trip Planner Crew")
    print('-------------------------------')
    
    # Gather User Inputs
    location = input("From where will you be traveling? ")
    cities = input("What cities are you interested in? ")
    date_range = input("What is the date range? ")
    interests = input("What are your interests/hobbies? ")

    # --- DYNAMIC API CONNECTION TEST ---
    # This uses your 'cities' input to verify the AI can see the destination
    print(f"\n[System] Verifying connection and checking location: {cities}...")
    verified, verification_message = verify_gemini_connection(cities)
    if verified:
        print(f"[System] API Verified. Landmark found: {verification_message}")
    else:
        print(f"[System] Live verification unavailable: {verification_message}")
        print("[System] Continuing with fallback-safe trip planning.")

    # --- RUN THE CREW ---
    print("\n[System] Starting the Trip Planning Crew. This may take a minute...")
    
    trip_crew = TripCrew(location, cities, date_range, interests, llm=llm)
    result = trip_crew.run()
    
    print("\n\n########################")
    print("## Here is your Trip Plan")
    print("########################\n")
    print(result)
  
