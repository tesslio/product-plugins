import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from inventory import inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        self.addCleanup(os.chdir, self.previous)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.package("tiles/one", "1.0.0")
        self.package("tiles/manual", "1.0.0")
        self.package("tiles/local", "1.0.0")
        Path("tiles/local/.local-only").touch()
        self.old = self.commit()
        self.package("tiles/one", "1.1.0")
        self.head = self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def package(self, path, version):
        file = Path(path) / ".tessl-plugin/plugin.json"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps({"name": "test/" + Path(path).name, "version": version}))

    def test_full_inventory_recovers_unchanged_packages(self):
        plan = inventory("tiles", "", ["tiles/manual"], [])
        self.assertEqual([(p["path"], p["version"]) for p in plan], [("tiles/one", "1.1.0")])
        self.assertEqual(plan[0]["ref"], self.head)

    def test_explicit_manual_package_allowed_but_local_only_never(self):
        self.assertEqual(len(inventory("tiles", "tiles/manual", ["tiles/manual"], [])), 1)
        for path in ("tiles/local", "tiles/deleted", "../elsewhere"):
            with self.assertRaises(ValueError):
                inventory("tiles", path, [], [])

    def test_backfill_uses_reviewed_exact_version(self):
        entry = {"path": "tiles/one", "version": "1.0.0", "ref": self.old}
        plan = inventory("tiles", "tiles/one", [], [entry])
        self.assertEqual([p["version"] for p in plan], ["1.1.0", "1.0.0"])
        self.assertEqual(plan[1]["ref"], self.old)
        with self.assertRaises(ValueError):
            inventory("tiles", "tiles/one", [], [dict(entry, version="9.9.9")])
        with self.assertRaises(ValueError):
            inventory("tiles", "tiles/one", [], [dict(entry, ref="main")])

    def test_deleted_and_renamed_directories_follow_current_tree(self):
        self.git("mv", "tiles/one", "tiles/renamed")
        self.commit()
        plan = inventory("tiles", "", [], [])
        self.assertIn("tiles/renamed", [p["path"] for p in plan])
        self.assertNotIn("tiles/one", [p["path"] for p in plan])

    def test_empty_inventory_is_valid(self):
        Path("empty").mkdir()
        self.assertEqual(inventory("empty", "", [], []), [])


if __name__ == "__main__":
    unittest.main()
