from main import TripCrew, build_llm, verify_gemini_connection


def main():
  print("## Welcome to Trip Planner Crew")
  print('-------------------------------')

  location = input("From where will you be traveling from? ")
  cities = input("What are the cities options you are interested in visiting? ")
  date_range = input("What is the date range you are interested in traveling? ")
  interests = input("What are some of your high level interests and hobbies? ")

  print(f"\n[System] Verifying connection and checking location: {cities}...")
  verified, verification_message = verify_gemini_connection(cities)
  if verified:
    print(f"[System] API Verified. Landmark found: {verification_message}")
  else:
    print(f"[System] Live verification unavailable: {verification_message}")
    print("[System] Continuing with fallback-safe trip planning.")

  print("\n[System] Starting the Trip Planning Crew. This may take a minute...")
  trip_crew = TripCrew(location, cities, date_range, interests, llm=build_llm())
  result = trip_crew.run()

  print("\n\n########################")
  print("## Here is you Trip Plan")
  print("########################\n")
  print(result)


if __name__ == "__main__":
  main()
from langchain.tools import BaseTool



