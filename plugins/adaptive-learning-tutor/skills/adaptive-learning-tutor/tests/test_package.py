"""Structural guards; these do not execute an LLM or infer learning effectiveness."""
from pathlib import Path
import sys
import json
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_package import PackageError, validate, visible_markdown, yaml_subset
from build_standalone import render

class PackageTests(unittest.TestCase):
    def test_package_structure(self):
        self.assertEqual('structural_checks_passed',validate()['status'])
    def test_default_preserves_preview_preference(self):
        settings=json.loads((ROOT/'assets/settings.default.json').read_text(encoding='utf-8'))
        self.assertEqual('preview',settings['approval_mode'])
    def test_standalone_synchronized(self):
        self.assertEqual(render(),(ROOT/'SYSTEM_PROMPT.md').read_text(encoding='utf-8'))
    def test_standalone_preserves_policy_without_file_dependency(self):
        text=render()
        self.assertIn('preview/read_only',text)
        self.assertNotIn('`assets/settings.default.json`',text)
    def test_yaml_rejects_duplicate_key(self):
        with self.assertRaises(PackageError):yaml_subset('name: a\nname: b')
    def test_yaml_rejects_executable_tags(self):
        with self.assertRaises(PackageError):yaml_subset('value: !!python/object:evil')
    def test_yaml_preserves_booleans(self):
        self.assertIs(yaml_subset('policy:\n  enabled: false')['policy']['enabled'],False)
    def test_code_links_not_scanned(self):
        self.assertNotIn('missing.md',visible_markdown('```text\n[x](missing.md)\n```\nhello'))
    def test_unclosed_fence_rejected(self):
        with self.assertRaises(PackageError):visible_markdown('```python\nx=1')
