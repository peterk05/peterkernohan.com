"""The deploy publishes only the site: every page and asset, none of the repo's tooling."""
import subprocess

from conftest import ROOT, Page, local_file

INTERNAL = ["tests", "specs", "evals", "lessons", "metrics", ".claude", ".github", ".githooks",
            ".gitignore", "scripts"]


def build(tmp_path):
    out = tmp_path / "_site"
    subprocess.run(["bash", str(ROOT / "scripts" / "build-site.sh"), str(out)], check=True)
    return out


def test_build_leaves_out_repo_tooling(tmp_path):
    out = build(tmp_path)
    leaked = [p for p in INTERNAL if (out / p).exists()]
    assert leaked == []


def test_build_keeps_every_page_and_everything_they_reference(tmp_path):
    out = build(tmp_path)
    pages = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html")
             if not any(p.relative_to(ROOT).as_posix().startswith(i + "/") for i in INTERNAL)]
    missing = [p for p in pages if not (out / p).is_file()]
    for name in pages:
        for ref in Page(ROOT / name).refs:
            src = local_file(ref.split("?")[0], name)
            if src is not None and not ref.startswith("http") and src.exists():
                if not (out / src.relative_to(ROOT)).exists():
                    missing.append(f"{name} -> {ref}")
    for f in ["CNAME", ".nojekyll", "robots.txt", "sitemap.xml", "404.html", "assets/og-card.png"]:
        if not (out / f).exists():
            missing.append(f)
    assert missing == []
