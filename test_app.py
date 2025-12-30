import unittest
from app import analyze_ticket, assign_agent
 
class TestTicketFunctions(unittest.TestCase):
 
    def test_analyze_ticket_high_priority(self):
        priority, category = analyze_ticket("System is down immediately!")
        self.assertEqual(priority, "High")
 
    def test_analyze_ticket_medium_priority(self):
        priority, category = analyze_ticket("There is a slow network issue.")
        self.assertEqual(priority, "Medium")
 
    def test_analyze_ticket_low_priority(self):
        priority, category = analyze_ticket("Request for information.")
        self.assertEqual(priority, "Low")
 
    def test_assign_agent_specialist(self):
        agent = assign_agent("network")
        self.assertIn("network", agent["expertise"])
 
    def test_assign_agent_no_specialist(self):
        agent = assign_agent("unknown_category")
        self.assertIn(agent["name"], ["Agent A", "Agent B", "Agent C"])
 
if __name__ == '__main__':
    unittest.main()