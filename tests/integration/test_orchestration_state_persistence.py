import tempfile,unittest
from pathlib import Path
from governance.state.atomic_writer import write
class OrchestrationStatePersistenceTest(unittest.TestCase):
 def test_atomic_replace_preserves_complete_value(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"nested/state.yaml";write(p,"old: true\n");write(p,"new: true\n");self.assertEqual("new: true\n",p.read_text(encoding="utf-8"))
