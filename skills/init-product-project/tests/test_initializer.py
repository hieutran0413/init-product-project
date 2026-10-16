import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/init_product_project.py'

class InitializerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = self.root / 'project'

    def run_init(self, *extra, name='Đồ dùng "Việt"'):
        return subprocess.run([sys.executable, str(SCRIPT), '--name', name,
            '--type', 'cli', '--path', str(self.target), *extra], capture_output=True, text=True)

    def test_dry_run_and_unicode_yaml(self):
        self.assertEqual(self.run_init('--dry-run').returncode, 0)
        self.assertFalse(self.target.exists())
        self.assertEqual(self.run_init().returncode, 0)
        import yaml
        brief = (self.target / 'docs/product/PRODUCT_BRIEF.md').read_text()
        self.assertEqual(yaml.safe_load(brief.split('---')[1])['project'], 'Đồ dùng "Việt"')

    def test_integration_preserves_all_existing_bytes(self):
        self.assertEqual(self.run_init().returncode, 0)
        (self.target / 'README.md').write_text('custom content')
        before = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*') if p.is_file()}
        self.assertEqual(self.run_init().returncode, 2)
        self.assertEqual(self.run_init('--integrate').returncode, 0)
        self.assertEqual(before, {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*') if p.is_file()})

    def test_conflict_preflight_writes_nothing(self):
        self.target.mkdir()
        (self.target / 'docs').write_text('keep')
        for mode in [[], ['--dry-run']]:
            self.assertEqual(self.run_init('--integrate', *mode).returncode, 2)
            self.assertEqual(list(self.target.iterdir()), [self.target / 'docs'])

    def test_symlink_cannot_write_outside(self):
        self.target.mkdir()
        external = self.root / 'outside'
        external.mkdir()
        (self.target / 'docs').symlink_to(external, target_is_directory=True)
        self.assertEqual(self.run_init('--integrate').returncode, 2)
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.target / 'AGENTS.md').exists())

    def test_invalid_name_writes_nothing(self):
        self.assertEqual(self.run_init(name='\ninvalid').returncode, 2)
        self.assertFalse(self.target.exists())

    def test_feature_status_is_entry_point(self):
        self.assertEqual(self.run_init().returncode, 0)
        docs = self.target / 'docs'
        index = (docs / 'README.md').read_text()
        status = (docs / 'engineering/IMPLEMENTATION_STATUS.md').read_text()
        self.assertIn('[Feature Status](engineering/IMPLEMENTATION_STATUS.md)', index)
        for field in ['What works now', 'What remains', 'Next action', 'Evidence / detail', 'Checked']:
            self.assertIn(field, status)
        self.assertIn('unassessed', status)
        self.assertTrue((docs / 'work-items/active/README.md').is_file())

    def test_workbench_evidence_ignored(self):
        self.assertEqual(self.run_init().returncode, 0)
        subprocess.run(['git', 'init', '-q', str(self.target)], check=True)
        evidence = self.target / 'workbench/evidence/sample.txt'
        evidence.write_text('sample')
        result = subprocess.run(['git', '-C', str(self.target), 'check-ignore', 'workbench/evidence/sample.txt'], capture_output=True)
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
