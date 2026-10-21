from crewai import Agent

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
# print("I am in trip_agents")

class TripAgents():
  def __init__(self, llm=None):
    self.llm = llm

  def city_selection_agent(self):
    return Agent(
      role="City Selection Expert",
      goal="Select the best city based on weather, season, and prices",
      backstory='An expert in analyzing travel data to pick ideal destinations',
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet
      ],
      llm=self.llm,
      verbose=True
    )
    """    # Concretize the tools
    internet_tool = self._concretize_tool(SearchTools.search_internet)
    browser_tool = self._concretize_tool(BrowserTools.scrape_and_summarize_website)
    
    # Debug prints
    print("Internet Tool:", internet_tool)
    print("Browser Tool:", browser_tool)
    
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices',
        backstory='An expert in analyzing travel data to pick ideal destinations',
        tools=[
#           internet_tool,  # Pass the tool instance directly
           BrowserTools.scrape_and_summarize_website,
           SearchTools.search_internet
       ],
        verbose=True
    )
    """
  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
      llm=self.llm,
        verbose=False)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
            CalculatorTools.calculate,
        ],
        llm=self.llm,
        verbose=False)
    
  def _concretize_tool(self, tool):
    # Ensure the tool's class has a concrete `_run` method
    if not hasattr(tool.__class__, "_run") or getattr(tool.__class__, "_run") is None:
        def dummy_run(self, *args, **kwargs):
            return None
        setattr(tool.__class__, "_run", dummy_run)
    
    # Clear the abstract methods set
    if hasattr(tool.__class__, "__abstractmethods__"):
        tool.__class__.__abstractmethods__ = frozenset()
    
    # Instantiate the tool if it's not already an instance
    if isinstance(tool, type):  # If the tool is a class, instantiate it
        tool = tool()
    
    return tool 
