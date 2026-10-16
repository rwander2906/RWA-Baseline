"""Regression checks for the Actions artifact policy."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_artifact_lifecycle.py"
spec = importlib.util.spec_from_file_location("artifact_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LifecycleTests(unittest.TestCase):
    def test_no_upload_is_valid(self):
        self.assertEqual(module.inspect_workflow("steps:\n  - run: echo ok", "test.yml"), [])

    def test_unbounded_upload_rejected(self):
        workflow = "  - name: Upload\n    uses: actions/upload-artifact@v7\n    with:\n      retention-days: 30\n"
        self.assertEqual(len(module.inspect_workflow(workflow, "test.yml")), 2)

    def test_documented_short_upload_allowed(self):
        workflow = "  # artifact-lifecycle: cross-job\n  - name: Upload\n    uses: actions/upload-artifact@v7\n    with:\n      retention-days: 1\n"
        self.assertEqual(module.inspect_workflow(workflow, "test.yml"), [])

    def test_marker_on_other_step_not_accepted(self):
        workflow = ("  # artifact-lifecycle: diagnostic\n  - name: Previous\n    run: echo ok\n"
                    "  - name: Upload\n    uses: actions/upload-artifact@v7\n    with:\n      retention-days: 1\n")
        self.assertTrue(module.inspect_workflow(workflow, "test.yml"))


if __name__ == "__main__":
    unittest.main()
