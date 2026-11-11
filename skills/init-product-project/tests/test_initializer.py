import json
import re
import importlib.util
import io
from contextlib import redirect_stderr
from unittest.mock import patch
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
        self.root = Path(self.tmp.name).resolve()
        self.target = self.root / 'project'

    def run_init(self, *extra, name='Đồ dùng "Việt"'):
        return subprocess.run([sys.executable, str(SCRIPT), '--name', name,
            '--type', 'cli', '--path', str(self.target), *extra], capture_output=True, text=True)

    def test_dry_run_and_unicode_yaml(self):
        self.assertEqual(self.run_init('--dry-run').returncode, 0)
        self.assertFalse(self.target.exists())
        self.assertEqual(self.run_init().returncode, 0)
        brief = (self.target / 'docs/product/PRODUCT_BRIEF.md').read_text()
        self.assertEqual(json.loads(next(line.removeprefix('project: ') for line in brief.splitlines() if line.startswith('project: '))), 'Đồ dùng "Việt"')

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

    def test_target_and_parent_symlinks_are_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        alias = self.root / 'alias'
        alias.symlink_to(outside, target_is_directory=True)
        for destination in [alias, alias / 'nested']:
            self.target = destination
            for flags in [[], ['--dry-run'], ['--integrate']]:
                result = self.run_init(*flags)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('symlink', result.stderr)
        self.assertEqual(list(outside.iterdir()), [])

    def test_parent_file_conflict_has_no_traceback(self):
        parent = self.root / 'file'
        parent.write_text('preserve')
        self.target = parent / 'nested'
        result = self.run_init()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(parent.read_text(), 'preserve')

    def test_all_project_types_and_readiness_record(self):
        for kind in ['website', 'web-app', 'ios-app', 'android-app',
                     'cross-platform-app', 'desktop-app', 'internal-tool',
                     'api', 'cli', 'library', 'other']:
            destination = self.root / kind
            result = subprocess.run([sys.executable, str(SCRIPT), '--name', 'Test',
                '--type', kind, '--path', str(destination)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            readiness = destination / 'docs/operations/READINESS.md'
            self.assertIn('not-assessed', readiness.read_text())
            for path in destination.rglob('*.md'):
                self.assertNotRegex(path.read_text(), r'\{\{[A-Z0-9_]+\}\}')

    def test_write_failure_reports_recovery(self):
        spec = importlib.util.spec_from_file_location('initializer', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        stderr = io.StringIO()
        with patch.object(sys, 'argv', [str(SCRIPT), '--name', 'Test', '--type', 'cli',
                                       '--path', str(self.target)]), \
             patch.object(module, 'write_plan', side_effect=OSError('disk full')), \
             redirect_stderr(stderr):
            self.assertEqual(module.main(), 1)
        self.assertIn('--integrate', stderr.getvalue())
        self.assertNotIn('Traceback', stderr.getvalue())

    def test_template_like_name_is_not_interpreted(self):
        result = self.run_init(name='Project {{DATE}}')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.target.exists())

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

    def test_generated_document_links_resolve(self):
        self.assertEqual(self.run_init().returncode, 0)
        checked = 0
        for document in self.target.rglob('*.md'):
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                self.assertTrue((document.parent / link.split('#')[0]).exists(),
                                f'{document.relative_to(self.target)} -> {link}')
                checked += 1
        self.assertGreater(checked, 0)

    def test_workbench_evidence_ignored(self):
        self.assertEqual(self.run_init().returncode, 0)
        subprocess.run(['git', 'init', '-q', str(self.target)], check=True)
        evidence = self.target / 'workbench/evidence/sample.txt'
        evidence.write_text('sample')
        result = subprocess.run(['git', '-C', str(self.target), 'check-ignore', 'workbench/evidence/sample.txt'], capture_output=True)
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
