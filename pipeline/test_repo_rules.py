r"""The repo keeps game data out of git: every data folder, including one renamed aside before a fresh copy is
restored, is ignored; the page and the scripts are tracked. (Final review of the 2026-11-09 split: the transfer
README once said to rename the old data to wardrobe\data_old, which the whitelist did not ignore.)

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_repo_rules -v
"""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ignored(rel):
    return subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", "--no-index", rel]).returncode == 0


class RepoRules(unittest.TestCase):
    def test_data_folders_ignored(self):
        for rel in ("wardrobe/data/meta.json", "wardrobe/data_old/meta.json", "wardrobe/data-home/cat/rig.json",
                    "wardrobe_data_old/meta.json", "wardrobe_dist/index.html", "tto_config/x.json"):
            with self.subTest(rel=rel):
                self.assertTrue(ignored(rel), f"{rel} is not ignored")

    def test_page_and_scripts_tracked(self):
        for rel in ("wardrobe/index.html", "wardrobe/ui/recolor1.webp", "pipeline/wardrobe_data.py", "wardrobe.cmd",
                    ".gitattributes", "CLAUDE.md"):
            with self.subTest(rel=rel):
                self.assertFalse(ignored(rel), f"{rel} is ignored")

    def test_transfer_readme_sets_old_data_aside_at_the_top(self):
        text = (ROOT / "pipeline" / "transfer_to_drive.ps1").read_text(encoding="utf-8")
        self.assertNotIn("data_old)", text.replace("wardrobe_data_old", ""))
        self.assertIn(r"C:\work\12tails-wardrobe\wardrobe_data_old", text)


if __name__ == "__main__":
    unittest.main()
