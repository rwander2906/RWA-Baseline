import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
B=load("builder","scripts/build_ai_review_package.py"); R=load("renderer","scripts/render_ai_review.py")
class GateTests(unittest.TestCase):
    def test_issue_reference(self): self.assertEqual(B.issue_number_from_text("Refs #39"),39)
    def test_acceptance(self): self.assertEqual(B.acceptance_criteria("## Akzeptanz\\n- A\\n- B"),["A","B"])
    def test_dialog_filters_foreign_bots_and_limits_history(self):
        comments=[{"body":"noise","user":{"login":"other[bot]"},"created_at":"1"},{"body":"human","user":{"login":"dev"},"created_at":"2"},{"body":"<!-- rwa-ai-review --> review","user":{"login":"github-actions[bot]"},"created_at":"3"}]
        dialog=B.review_dialog(comments,limit=2)
        self.assertEqual([x["author"] for x in dialog],["dev","github-actions[bot]"])
    def test_render_location(self):
        wrapper={"status":"REVIEWED","result":{"verdict":"WARN","summary":"x","findings":[{"severity":"WARN","message":"m","location":{"path":"a.py","line":7}}]}}
        self.assertIn("`a.py:7`",R.render(wrapper))
if __name__=="__main__": unittest.main()
