"""Distribution regression tests; never touch a real host configuration."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest
from validate_codex_plugin import ROOT, local_path, validate


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / '.agents', self.root / '.agents')
        shutil.copytree(ROOT / 'plugins', self.root / 'plugins',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.plugin = self.root / 'plugins/adaptive-learning-tutor'
        self.skill = self.plugin / 'skills/adaptive-learning-tutor'

    def change(self, path, function):
        data = json.loads(path.read_text(encoding='utf-8'))
        function(data)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def test_valid_distribution(self):
        self.assertEqual(46, validate(self.root)['core_files_verified'])

    def test_original_bytes_are_checked(self):
        (self.skill / 'SKILL.md').write_text('tampered', encoding='utf-8')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_missing_skill_fails(self):
        (self.skill / 'SKILL.md').unlink()
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_parent_path_rejected(self):
        with self.assertRaises(ValueError):
            local_path(self.root, './../outside')

    def test_absolute_path_rejected(self):
        with self.assertRaises(ValueError):
            local_path(self.root, str(self.root))

    def test_symlink_rejected(self):
        (self.plugin / 'shortcut').symlink_to(self.skill)
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_new_mcp_dependency_rejected(self):
        (self.plugin / '.mcp.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_unexpected_hook_rejected(self):
        self.change(self.plugin / '.codex-plugin/plugin.json',
                    lambda d: d.update(hooks='./hooks/hooks.json'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_duplicate_plugin_rejected(self):
        self.change(self.root / '.agents/plugins/marketplace.json',
                    lambda d: d['plugins'].append(d['plugins'][0].copy()))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_changed_preview_policy_rejected(self):
        self.change(self.skill / 'assets/settings.default.json',
                    lambda d: d.update(approval_mode='adaptive'))
        with self.assertRaises(ValueError):
            validate(self.root)


if __name__ == '__main__':
    unittest.main()
