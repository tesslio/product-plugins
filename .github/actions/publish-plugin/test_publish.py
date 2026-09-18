import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

from publish import Registry, archive_contents, fingerprint, main, reconcile


def archive(files, timestamp=0):
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w:gz") as tar:
        for name, content in files.items():
            data = content.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = timestamp
            tar.addfile(info, io.BytesIO(data))
    return out.getvalue()


MANIFEST = {"name": "tessl/test", "version": "1.0.0", "summary": "Test"}
FILES = {"tile.json": json.dumps(MANIFEST), "skills/test/SKILL.md": "Test skill"}


class MemoryRegistry:
    def __init__(self, existing=None):
        self.existing = existing
        self.reads = 0

    def contents(self, name, version):
        self.reads += 1
        return self.existing


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.expected = archive_contents(archive(FILES))

    def test_metadata_and_manifest_formatting_do_not_change_content(self):
        stored = dict(FILES, **{"tile.json": json.dumps(dict(MANIFEST, private=False), indent=2)})
        self.assertEqual(self.expected, archive_contents(archive(stored, timestamp=999)))

    def test_registry_file_filter_and_steering_normalization(self):
        manifest = dict(MANIFEST, steering={"test": {"rules": "rules.md"}})
        source = dict(FILES, **{"tile.json": json.dumps(manifest), "image.png": "ignored", ".secret": "ignored", ".mcp.json": "{}"})
        actual = archive_contents(archive(source))
        self.assertNotIn("image.png", actual)
        self.assertNotIn(".secret", actual)
        self.assertIn(".mcp.json", actual)
        parsed = json.loads(actual["tile.json"])
        self.assertEqual(parsed["rules"], manifest["steering"])
        self.assertNotIn("steering", parsed)

    def test_renaming_and_changing_version_are_conflicts(self):
        renamed = dict(self.expected)
        renamed["other.md"] = renamed.pop("skills/test/SKILL.md")
        self.assertNotEqual(fingerprint(self.expected), fingerprint(renamed))
        changed = dict(FILES, **{"tile.json": json.dumps(dict(MANIFEST, version="1.0.1"))})
        self.assertNotEqual(self.expected, archive_contents(archive(changed)))

    def test_unsafe_duplicate_and_link_entries_rejected(self):
        with self.assertRaises(ValueError):
            archive_contents(archive(dict(FILES, **{"../escape.md": "bad"})))
        for kind in (tarfile.SYMTYPE, tarfile.REGTYPE):
            output = io.BytesIO()
            with tarfile.open(fileobj=output, mode="w:gz") as tar:
                for _ in range(2):
                    item = tarfile.TarInfo("file.md")
                    item.type = kind
                    tar.addfile(item, io.BytesIO())
            with self.assertRaises(ValueError):
                archive_contents(output.getvalue())

    def test_missing_version_is_published_and_verified(self):
        registry = MemoryRegistry()
        calls = []
        def publish():
            calls.append(True)
            registry.existing = self.expected
        self.assertEqual(reconcile(registry, "tessl/test", "1.0.0", self.expected, publish, lambda _: None), "verified")
        self.assertEqual(len(calls), 1)
        self.assertEqual(registry.reads, 2)

    def test_existing_identical_version_is_not_republished(self):
        reconcile(MemoryRegistry(self.expected), "tessl/test", "1.0.0", self.expected,
                  lambda: self.fail("Unexpected publication"), lambda _: None)

    def test_existing_conflicting_version_fails_without_writing(self):
        with self.assertRaisesRegex(RuntimeError, "Content conflict"):
            reconcile(MemoryRegistry({"tile.json": b"different"}), "tessl/test", "1.0.0", self.expected,
                      lambda: self.fail("Unexpected publication"), lambda _: None)

    def test_timeout_after_committed_upload_does_not_upload_twice(self):
        registry = MemoryRegistry()
        calls = []
        def publish():
            calls.append(True)
            registry.existing = self.expected
            raise subprocess.TimeoutExpired("tessl", 600)
        reconcile(registry, "tessl/test", "1.0.0", self.expected, publish, lambda _: None)
        self.assertEqual(len(calls), 1)

    def test_partial_region_success_can_retry_independently(self):
        us, eu = MemoryRegistry(self.expected), MemoryRegistry()
        def fail_upload():
            raise subprocess.CalledProcessError(1, "tessl")
        with self.assertRaisesRegex(RuntimeError, "did not converge"):
            reconcile(eu, "tessl/test", "1.0.0", self.expected, fail_upload, lambda _: None)
        reconcile(us, "tessl/test", "1.0.0", self.expected, lambda: self.fail("US changed"), lambda _: None)
        reconcile(eu, "tessl/test", "1.0.0", self.expected,
                  lambda: setattr(eu, "existing", self.expected), lambda _: None)

    def test_auth_and_server_errors_are_not_missing_versions(self):
        for status in (401, 403, 410, 429, 500):
            registry = Registry("https://api.eu.tessl.io", "test-placeholder")
            with patch.object(registry.opener, "open", side_effect=urllib.error.HTTPError("", status, "", {}, None)):
                with self.assertRaisesRegex(RuntimeError, str(status)):
                    registry.contents("tessl/test", "1.0.0")

    def test_only_metadata_404_means_missing(self):
        registry = Registry("https://api.eu.tessl.io", "test-placeholder")
        with patch.object(registry.opener, "open", side_effect=urllib.error.HTTPError("", 404, "", {}, None)):
            self.assertIsNone(registry.contents("tessl/test", "1.0.0"))
        with patch.object(registry, "get", side_effect=[{"data": {"attributes": {"version": "1.0.0", "archived": False}}}, RuntimeError("HTTP 404")]):
            with self.assertRaises(RuntimeError):
                registry.contents("tessl/test", "1.0.0")

    def test_preflight_checks_workspace_permission(self):
        registry = Registry("https://api.eu.tessl.io", "test-placeholder")
        with patch.object(registry, "get", return_value={"data": {"attributes": {"name": "tessl"}, "meta": {"allowedActions": ["view"]}}}):
            with self.assertRaisesRegex(RuntimeError, "cannot edit"):
                registry.preflight("tessl/test")

    def test_main_packs_with_explicit_region_and_verifies_existing_content(self):
        for target, origin in (("production", "https://api.tessl.io"), ("app-eu", "https://api.eu.tessl.io")):
            with tempfile.TemporaryDirectory() as directory:
                package = Path(directory) / "package"
                (package / ".tessl-plugin").mkdir(parents=True)
                (package / ".tessl-plugin/plugin.json").write_text(json.dumps(MANIFEST))
                calls = []
                def cli(args, **kwargs):
                    calls.append((args, kwargs))
                    self.assertEqual(args[1:3], ["plugin", "pack"])
                    Path(args[-1]).write_bytes(archive(FILES))
                environment = {
                    "PUBLISH_TARGET": target, "PUBLISH_API_URL": origin,
                    "TESSL_PUBLISH_TOKEN": "test-placeholder", "PUBLISH_PATH": str(package),
                    "PUBLISH_NAME": "tessl/test", "PUBLISH_VERSION": "1.0.0",
                    "TESSL_ENV": "development", "TESSL_API_BASE_URL": "http://localhost:4000",
                }
                with patch.dict(os.environ, environment, clear=True), patch("publish.subprocess.run", side_effect=cli), patch("publish.Registry") as factory:
                    factory.return_value.contents.return_value = self.expected
                    main()
                    factory.assert_called_once_with(origin, "test-placeholder")
                    factory.return_value.preflight.assert_called_once_with("tessl/test")
                self.assertEqual(len(calls), 1)
                self.assertEqual(calls[0][1]["env"]["TESSL_ENV"], target)
                self.assertEqual(calls[0][1]["env"]["TESSL_API_BASE_URL"], origin)
                self.assertNotEqual(calls[0][1]["cwd"], str(package))

    def test_target_mismatch_and_missing_token_fail_before_cli(self):
        for env in ({"PUBLISH_TARGET": "app-eu", "PUBLISH_API_URL": "https://api.tessl.io"},
                    {"PUBLISH_TARGET": "app-eu", "PUBLISH_API_URL": "https://api.eu.tessl.io"}):
            with patch.dict(os.environ, env, clear=True), patch("subprocess.run") as run:
                with self.assertRaises(ValueError):
                    main()
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
