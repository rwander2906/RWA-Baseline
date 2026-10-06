"""Tests for the user documentation release gate."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys, unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_user_documentation import validate

GUIDE="# Anwenderhandbuch\\n\\n## Installation und Start\\nX\\n## Bedienung\\nX\\n## Konfiguration\\nX\\n## Fehler und Support\\nX\\n## Version und Gültigkeit\\nX\\n"
class UserDocumentationGateTests(unittest.TestCase):
    def project(self):
        td=TemporaryDirectory(); root=Path(td.name); (root/"docs/user/screenshots").mkdir(parents=True); (root/"docs/user/README.md").write_text(GUIDE,encoding="utf-8"); return td,root
    def test_valid_guide_passes(self):
        td,root=self.project(); self.addCleanup(td.cleanup); self.assertEqual([],validate(root))
    def test_missing_reference_blocks_release(self):
        td,root=self.project(); self.addCleanup(td.cleanup); (root/"docs/user/README.md").write_text(GUIDE+"\\n![UI](screenshots/missing.png)\\n",encoding="utf-8"); self.assertTrue(any("missing local reference" in x for x in validate(root)))
    def test_secret_like_file_blocks_release(self):\n        td,root=self.project(); self.addCleanup(td.cleanup); (root/"docs/user/example.key").write_text("secret",encoding="utf-8"); self.assertTrue(any("forbidden secret-like file" in x for x in validate(root)))\n    def test_screenshot_outside_canonical_folder_blocks_release(self):
        td,root=self.project(); self.addCleanup(td.cleanup); (root/"docs/user/ui.png").write_bytes(b"x"); (root/"docs/user/README.md").write_text(GUIDE+"\\n![UI](ui.png)\\n",encoding="utf-8"); self.assertTrue(any("screenshot outside" in x for x in validate(root)))
if __name__=="__main__": unittest.main()
