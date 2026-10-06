import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_ai_review_contract.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def result(verdict="PASS", findings=None):
    return {"schema_version":"1.0","verdict":verdict,"summary":"reviewed","findings":findings or [],"reviewer":{"adapter":"fake","model":"test","provider_review_id":None}}

class ReviewContractTests(unittest.TestCase):
    def test_pass(self): MODULE.validate_result(result())
    def test_block_requires_block_finding(self):
        with self.assertRaises(ValueError): MODULE.validate_result(result("BLOCK"))
    def test_block_finding(self): MODULE.validate_result(result("BLOCK",[{"severity":"BLOCK","message":"bug","location":{"path":"src/app.py","line":12}}]))
    def test_provider_failure_is_not_a_verdict(self):
        with self.assertRaises(ValueError): MODULE.validate_result(result("UNAVAILABLE"))

if __name__ == "__main__": unittest.main()
