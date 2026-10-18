import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory so that the trip_planner package is importable.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from docs.technology.languages.python.trip_planner.main1 import TripCrew

# Dummy agent (does nothing)
class DummyAgent:
    pass

# DummyTripAgents replaces the real TripAgents
class DummyTripAgents:
    def city_selection_agent(self):
        return DummyAgent()
    def local_expert(self):
        return DummyAgent()
    def travel_concierge(self):
        return DummyAgent()

# DummyTripTasks replaces the real TripTasks.
# It just returns MagicMock objects for tasks.
class DummyTripTasks:
    def identify_task(self, *args, **kwargs):
        return MagicMock()
    def gather_task(self, *args, **kwargs):
        return MagicMock()
    def plan_task(self, *args, **kwargs):
        return MagicMock()

class TestMain(unittest.TestCase):

    @patch("trip_planner.main.Crew")
    @patch("trip_planner.main.TripTasks", new=DummyTripTasks)
    @patch("trip_planner.main.TripAgents", new=DummyTripAgents)
    def test_tripcrew_run(self, mock_crew):
        # Set up a dummy Crew instance with kickoff() returning a fixed value.
        dummy_crew_instance = MagicMock()
        dummy_crew_instance.kickoff.return_value = "dummy_result"
        mock_crew.return_value = dummy_crew_instance

        # Instantiate TripCrew with test parameters.
        trip = TripCrew(
            origin="TestOrigin",
            cities=["City1", "City2"],
            date_range="2025-05-10 to 2025-05-15",
            interests=["food", "art"]
        )
        result = trip.run()

        # Verify that run() returns our dummy value.
        self.assertEqual(result, "dummy_result")
        dummy_crew_instance.kickoff.assert_called_once()

if __name__ == '__main__':
    unittest.main()