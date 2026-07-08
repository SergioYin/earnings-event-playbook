import subprocess
import sys
import unittest


class ReleaseGateSmokeTests(unittest.TestCase):
    def test_unittest_discovery_exercises_cli_selfcheck(self):
        result = subprocess.run(
            [sys.executable, "-m", "earnings_event_playbook", "selfcheck"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("selfcheck ok", result.stdout)
        self.assertNotIn("scanned=0", result.stdout)
