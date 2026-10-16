import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; spec=importlib.util.spec_from_file_location("pub",ROOT/"scripts"/"publish_ai_review_issue_comment.py"); P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
class DialogTests(unittest.TestCase):
 def test_comment_contains_stable_marker_and_finding(self):
  result={"status":"REVIEWED","result":{"verdict":"WARN","summary":"Check","findings":[{"severity":"WARN","message":"Fix","location":{"path":"a.py","line":4}}],"reviewer":{"adapter":"fake","model":"m"}}}; decision={"decision":"WARN","reason":"review-warning"}
  text=P.render(result,decision,"run","abc"); self.assertIn(P.MARKER,text); self.assertIn("a.py:4",text); self.assertIn("Policy: **WARN**",text)
 def test_unavailable_is_documented(self):
  text=P.render({"status":"UNAVAILABLE"},{"decision":"WARN","reason":"provider-unavailable-fail-open"},"run","abc"); self.assertIn("UNAVAILABLE",text)
if __name__=="__main__": unittest.main()
