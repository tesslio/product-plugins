"""Reconcile one immutable package against an explicitly selected registry."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

# These are public CLI environment coordinates, never inferred from a token.
TARGETS = {
    "production": "https://api.tessl.io",
    "app-eu": "https://api.eu.tessl.io",
}
# The registry filters uploaded files and cleans tile.json before storing it.
# Match that wire contract, not gzip timestamps or tar ownership/mode metadata.
EXTENSIONS = {".md", ".html", ".js", ".mjs", ".cjs", ".ts", ".py", ".sh", ".txt", ".ps1", ".json"}
MANIFEST_FIELDS = {"name", "version", "describes", "docs", "summary", "private", "repository", "rules", "steering", "commands", "skills", "mcpServers"}


def archive_contents(data):
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for entry in archive:
            path = PurePosixPath(entry.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Unsafe archive path")
            if entry.isdir():
                continue
            if not entry.isfile() or str(path) in files:
                raise ValueError("Non-regular or duplicate archive entry")
            name = str(path)
            if name != ".mcp.json" and (path.name.startswith(".") or path.suffix not in EXTENSIONS):
                continue
            content = archive.extractfile(entry).read()
            if name == "tile.json":
                manifest = json.loads(content)
                manifest = {k: v for k, v in manifest.items() if k in MANIFEST_FIELDS}
                manifest.setdefault("private", False)
                if "steering" in manifest:
                    manifest.setdefault("rules", manifest.pop("steering"))
                content = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
            files[name] = content
    if "tile.json" not in files:
        raise ValueError("Packed archive has no tile.json")
    return files


def fingerprint(files):
    # Include paths and lengths so renamed files cannot compare equal.
    digest = hashlib.sha256()
    for path, data in sorted(files.items()):
        digest.update(json.dumps([path, len(data)]).encode() + b"\n" + data)
    return digest.hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward registry credentials to a redirected destination.
        return None


class Registry:
    def __init__(self, origin, token):
        self.origin = origin
        self.token = token
        self.opener = urllib.request.build_opener(NoRedirect)

    def get(self, path, *, archive=False, missing=False):
        request = urllib.request.Request(self.origin + path, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/gzip" if archive else "application/json",
        })
        try:
            with self.opener.open(request, timeout=60) as response:
                data = response.read()
                return data if archive else json.loads(data)
        except urllib.error.HTTPError as error:
            if error.code == 404 and missing:
                return None
            raise RuntimeError(f"Registry GET {path} failed: HTTP {error.code}") from None

    def preflight(self, name):
        workspace = name.split("/")[0]
        data = self.get(f"/v1/workspaces/{workspace}")["data"]
        if data["attributes"]["name"] != workspace or "edit" not in data["meta"]["allowedActions"]:
            raise RuntimeError(f"Publishing token cannot edit workspace {workspace}")

    def contents(self, name, version):
        # Check metadata first: hidden/forbidden files must not look absent.
        path = f"/v1/tiles/{name}/versions/{version}"
        metadata = self.get(path, missing=True)
        if metadata is None:
            return None
        attrs = metadata["data"]["attributes"]
        if attrs["version"] != version or attrs["archived"]:
            raise RuntimeError(f"Version is archived or mismatched: {name}@{version}")
        return archive_contents(self.get(path + "/files", archive=True))


def reconcile(registry, name, version, expected, publish, sleep=time.sleep):
    """Check before every attempt, including after a timed-out upload."""
    for attempt in range(3):
        actual = registry.contents(name, version)
        if actual is not None:
            if actual != expected:
                changed = sorted(p for p in actual.keys() | expected.keys() if actual.get(p) != expected.get(p))
                raise RuntimeError(f"Content conflict for {name}@{version}: {', '.join(changed[:10])}")
            return "verified"
        try:
            publish()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # A CLI failure may happen after the immutable version committed.
            # Read it back before deciding whether another upload is necessary.
            pass
        sleep(5)
    actual = registry.contents(name, version)
    if actual != expected:
        raise RuntimeError(f"Publication did not converge for {name}@{version}")
    return "verified"


def main():
    target = os.environ["PUBLISH_TARGET"]
    origin = os.environ["PUBLISH_API_URL"]
    if TARGETS.get(target) != origin:
        raise ValueError("Target and API origin must be a known matching pair")
    token = os.environ.get("TESSL_PUBLISH_TOKEN", "").strip()
    if not token:
        raise ValueError("Missing environment-scoped TESSL_PUBLISH_TOKEN")
    package = Path(os.environ["PUBLISH_PATH"]).resolve(strict=True)
    if (package / ".local-only").exists():
        raise ValueError("Refusing to publish a .local-only package")
    kind = "plugin" if (package / ".tessl-plugin/plugin.json").is_file() else "tile"
    env = dict(os.environ, TESSL_ENV=target, TESSL_API_BASE_URL=origin,
               TESSL_TOKEN=token, TESSL_PLUGIN="1" if kind == "plugin" else "0",
               TESSL_SHARE_USAGE_DATA="0", CI="true")
    # Run outside the repository so project-level config cannot override packing.
    with tempfile.TemporaryDirectory() as scratch:
        archive = Path(scratch) / "package.tgz"
        subprocess.run(["tessl", kind, "pack", str(package), "--output", str(archive)],
                       cwd=scratch, env=env, check=True, timeout=120)
        expected = archive_contents(archive.read_bytes())
        manifest = json.loads(expected["tile.json"])
        name, version = manifest["name"], manifest["version"]
        if name != os.environ["PUBLISH_NAME"] or version != os.environ["PUBLISH_VERSION"]:
            raise ValueError("Packed identity differs from the reviewed publication plan")
        registry = Registry(origin, token)
        registry.preflight(name)

        def publish():
            subprocess.run(["tessl", kind, "publish", str(package)], cwd=scratch,
                           env=env, check=True, timeout=600)

        outcome = reconcile(registry, name, version, expected, publish)
        line = f"{target}: {name}@{version} {outcome}; content {fingerprint(expected)}"
        print(line)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
                summary.write(line + "\n\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Publication failed: {error}", file=sys.stderr)
        sys.exit(1)
