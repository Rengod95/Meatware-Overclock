"""Filesystem-only installation tests; no live agent or user home is modified."""
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from install import NAME, InstallError, destination, install, inventory

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.home=self.root/'home';self.home.mkdir()
        self.source=self.root/'source';self.source.mkdir()
        (self.source/'SKILL.md').write_text('---\nname: adaptive-learning-tutor\ndescription: test\n---\nTest',encoding='utf-8')
        (self.source/'references').mkdir();(self.source/'references'/'a.md').write_text('a')
    def test_codex_user_path(self):
        self.assertEqual(self.home/'.agents/skills'/NAME,destination('codex','user',home=self.home))
    def test_claude_user_path(self):
        self.assertEqual(self.home/'.claude/skills'/NAME,destination('claude','user',home=self.home))
    def test_pi_shared_path(self):
        self.assertEqual(destination('codex','user',home=self.home),destination('pi','user',home=self.home))
    def test_gemini_user_path(self):
        self.assertEqual(self.home/'.gemini/skills'/NAME,destination('gemini','user',home=self.home))
    def test_project_requires_explicit_directory(self):
        with self.assertRaises(InstallError):destination('codex','project')
    def test_project_path(self):
        self.assertEqual(self.home/'.agents/skills'/NAME,destination('codex','project',project=self.home))
    def test_no_implicit_project_from_cwd(self):
        with self.assertRaises(InstallError):destination('claude','project',project=self.root/'missing')
    def test_custom_requires_path(self):
        with self.assertRaises(InstallError):destination('custom','user')
    def test_custom_path_is_parent(self):
        self.assertEqual(self.root/'custom'/NAME,destination('custom','user',dest=self.root/'custom'))
    def test_dry_run_creates_nothing(self):
        target=destination('codex','user',home=self.home)
        result=install(target,source=self.source)
        self.assertEqual('preview_only',result['status']);self.assertEqual([],list(self.home.iterdir()))
    def test_apply_copies_identical_bytes(self):
        target=self.home/'skills'/NAME;r=install(target,True,self.source)
        self.assertEqual('installed',r['status']);self.assertEqual(inventory(self.source),inventory(target))
    def test_second_install_is_idempotent(self):
        target=self.home/'skills'/NAME;install(target,True,self.source)
        self.assertEqual('already_installed',install(target,True,self.source)['status'])
    def test_different_existing_directory_not_overwritten(self):
        target=self.home/'skills'/NAME;install(target,True,self.source)
        (target/'SKILL.md').write_text('personal edit')
        with self.assertRaises(InstallError):install(target,True,self.source)
        self.assertEqual('personal edit',(target/'SKILL.md').read_text())
    def test_existing_file_not_overwritten(self):
        target=self.home/'file';target.write_text('preserve')
        with self.assertRaises(InstallError):install(target,True,self.source)
        self.assertEqual('preserve',target.read_text())
    def test_nested_destination_rejected(self):
        with self.assertRaises(InstallError):install(self.source/'nested',True,self.source)
    def test_symlink_source_file_rejected(self):
        (self.source/'link').symlink_to(self.source/'SKILL.md')
        with self.assertRaises(InstallError):install(self.home/NAME,True,self.source)
    def test_symlink_destination_parent_rejected(self):
        (self.home/'.agents').symlink_to(self.source,target_is_directory=True)
        with self.assertRaises(InstallError):destination('codex','user',home=self.home)
    def test_pycache_is_not_packaged(self):
        (self.source/'__pycache__').mkdir();(self.source/'__pycache__'/'bad.pyc').write_bytes(b'cache')
        target=self.home/NAME;install(target,True,self.source)
        self.assertFalse((target/'__pycache__').exists())
    def test_existing_lock_blocks_without_destination(self):
        parent=self.home/'skills';parent.mkdir();(parent/f'.{NAME}.install.lock').write_text('existing')
        with self.assertRaises(InstallError):install(parent/NAME,True,self.source)
        self.assertFalse((parent/NAME).exists())
    def test_source_needs_entrypoint(self):
        (self.source/'SKILL.md').unlink()
        with self.assertRaises(InstallError):install(self.home/NAME,source=self.source)
