import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from greeting import greet
class GreetingTest(unittest.TestCase):
    def test_greet(self): self.assertEqual("Hello, Ada!", greet("Ada"))
