import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("harness",ROOT/"scripts"/"ai_review_harness.py")
H=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(H)

class HarnessTests(unittest.TestCase):
    def test_fake_provider(self):
        status,result=H.run({"schema_version":"1.0"},"fake","test-model")
        self.assertEqual(status,"REVIEWED")
        self.assertEqual(result["verdict"],"PASS")
        self.assertEqual(result["reviewer"]["adapter"],"fake")

    def test_provider_unavailable_is_not_block(self):
        class Down(H.ReviewProvider):
            def review(self,package,model): raise H.ProviderUnavailable("down")
        original=H.create_provider
        H.create_provider=lambda name: Down()
        try:
            status,result=H.run({},"down","model")
        finally:
            H.create_provider=original
        self.assertEqual(status,"UNAVAILABLE")
        self.assertNotIn("verdict",result)

    def test_unknown_provider(self):
        with self.assertRaises(ValueError): H.run({},"unknown","model")

if __name__=="__main__": unittest.main()
