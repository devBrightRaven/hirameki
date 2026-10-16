import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("vault_route", Path(__file__).resolve().parents[1] / "scripts/vault_route.py")
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.vaults = {}
        for name in ("robot", "brand"):
            p = self.root / name
            (p / ".obsidian").mkdir(parents=True)
            (p / "work").mkdir()
            (p / "AGENTS.md").write_text("## Vault Structure\n\n```yaml\ndaily: work/\n```\n", encoding="utf-8")
            self.vaults[name] = {"root": str(p)}
        self.cfg = {"schema_version": 1, "vaults": self.vaults,
                    "read_default": "brand",
                    "project_bindings": [{"root": str(self.root / "repo"), "vault": "brand"},
                                         {"root": str(self.root / "repo/robot"), "vault": "robot"}],
                    "domain_bindings": {"robotics": "robot", "bright_raven": "brand"}}

    def test_explicit_overrides_conflict(self):
        r = route.select(self.cfg, explicit="robot", domains=["bright_raven"], session="brand")
        self.assertEqual(r["vault_id"], "robot")

    def test_longest_project_binding(self):
        self.assertEqual(route.select(self.cfg, cwd=str(self.root / "repo/robot/sub"))["vault_id"], "robot")

    def test_path_prefix_is_not_binding(self):
        self.assertEqual(route.select(self.cfg, cwd=str(self.root / "repository"))["status"], "needs_selection")

    def test_specific_domain_routes(self):
        self.assertEqual(route.select(self.cfg, domains=["robotics"])["vault_id"], "robot")

    def test_conflicting_domains_stop(self):
        self.assertEqual(route.select(self.cfg, domains=["robotics", "bright_raven"])["status"], "needs_selection")

    def test_project_domain_conflict_stops(self):
        self.assertEqual(route.select(self.cfg, cwd=str(self.root / "repo"), domains=["robotics"])["status"], "needs_selection")

    def test_session_same_task_reused(self):
        self.assertEqual(route.select(self.cfg, session="robot")["vault_id"], "robot")

    def test_context_switch_needs_selection(self):
        self.assertEqual(route.select(self.cfg, session="robot", domains=["bright_raven"])["status"], "needs_selection")

    def test_new_task_resets(self):
        self.assertEqual(route.select(self.cfg, session="robot", domains=["bright_raven"], reset=True)["vault_id"], "brand")

    def test_unknown_write_never_uses_default(self):
        self.assertEqual(route.select(self.cfg)["status"], "needs_selection")
        self.assertEqual(route.select(self.cfg, access="read")["vault_id"], "brand")

    def test_unknown_labels_rejected(self):
        with self.assertRaises(route.RouteError):
            route.select(self.cfg, domains=["research"])

    def test_layout_from_selected_vault(self):
        r = route.layout(route.select(self.cfg, explicit="robot"), ["daily"])
        self.assertEqual(Path(r["folders"]["daily"]), self.root / "robot/work")

    def test_missing_selected_vault_no_fallback(self):
        self.cfg["vaults"]["robot"]["root"] = str(self.root / "missing")
        with self.assertRaises(route.RouteError):
            route.layout(route.select(self.cfg, explicit="robot"), ["daily"])

    def test_escape_rejected(self):
        (self.root / "robot/AGENTS.md").write_text("## Vault Structure\n```yaml\ndaily: ../brand/work/\n```", encoding="utf-8")
        with self.assertRaises(route.RouteError):
            route.layout(route.select(self.cfg, explicit="robot"), ["daily"])

    def test_absolute_folder_rejected(self):
        (self.root / "robot/AGENTS.md").write_text("## Vault Structure\n```yaml\ndaily: C:/outside/\n```", encoding="utf-8")
        with self.assertRaises(route.RouteError):
            route.layout(route.select(self.cfg, explicit="robot"), ["daily"])


if __name__ == "__main__":
    unittest.main()
