import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; spec=importlib.util.spec_from_file_location("policy",ROOT/"scripts"/"ai_review_policy.py"); P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
def reviewed(v): return {"status":"REVIEWED","result":{"verdict":v}}
class PolicyTests(unittest.TestCase):
 def test_default_outage_is_fail_open(self): self.assertEqual(P.decide([{"status":"UNAVAILABLE"}])["decision"],"WARN")
 def test_fail_closed_outage_blocks(self): self.assertEqual(P.decide([{"status":"UNAVAILABLE"}],outage="fail-closed")["reason"],"provider-unavailable")
 def test_required_without_review_blocks(self): self.assertEqual(P.decide([],mode="required")["decision"],"BLOCK")
 def test_block_blocks(self): self.assertEqual(P.decide([reviewed("BLOCK")])["decision"],"BLOCK")
 def test_disagreement_requires_human(self):
  result=P.decide([reviewed("PASS"),reviewed("BLOCK")]); self.assertEqual(result["decision"],"HUMAN_REQUIRED"); self.assertTrue(result["human_required"])
 def test_agreed_pass(self): self.assertEqual(P.decide([reviewed("PASS"),reviewed("PASS")])["decision"],"PASS")
if __name__=="__main__": unittest.main()
