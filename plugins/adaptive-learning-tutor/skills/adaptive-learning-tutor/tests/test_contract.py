"""Synthetic contract fixtures; none represent a real user or approval."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from check_contract import CHECKS, ContractError, check, fingerprint, validate_relative

def draft():
    return json.loads((ROOT/'assets/lesson-contract.template.json').read_text())
def actual_shape():
    d=draft();d['example']=False;d['plan']['approval_mode']='adaptive';d['plan']['user_request_locator']='synthetic-test://request';return d

def approve(d):
    d['approval']={'kind':'plan_approval','user_message_locator':'synthetic-test://approval','plan_sha256':fingerprint(d['plan'])}
    return d

class ContractTests(unittest.TestCase):
    def test_template_lints_but_is_not_approval(self):
        d=draft();check(d)
        with self.assertRaises(ContractError):check(d,'produce')
    def test_no_artifact_needed_for_concept(self):
        d=actual_shape();check(d,'produce');self.assertEqual([],d['plan']['materials'][0]['source_refs'])
    def test_preview_requires_approval(self):
        d=actual_shape();d['plan']['approval_mode']='preview'
        with self.assertRaises(ContractError):check(d,'produce')
        check(approve(d),'produce')
    def test_series_requires_approval_even_adaptive(self):
        d=actual_shape();d['plan']['scope']='series'
        with self.assertRaises(ContractError):check(d,'produce')
        check(approve(d),'produce')
    def test_request_locator_required(self):
        d=actual_shape();d['plan']['user_request_locator']=' '
        with self.assertRaises(ContractError):check(d,'produce')
    def test_plan_edit_invalidates_approval(self):
        d=approve(actual_shape());d['plan']['question']='changed'
        with self.assertRaises(ContractError):check(d,'produce')
    def test_approval_locator_nonblank(self):
        d=approve(actual_shape());d['approval']['user_message_locator']=' '
        with self.assertRaises(ContractError):check(d,'produce')
    def test_digest_ignores_dictionary_order(self):
        p=actual_shape()['plan'];self.assertEqual(fingerprint(p),fingerprint(dict(reversed(list(p.items())))))
    def test_single_scope_rejects_two_materials(self):
        d=actual_shape();m=copy.deepcopy(d['plan']['materials'][0]);m['id']='m02';d['plan']['materials'].append(m)
        with self.assertRaises(ContractError):check(d)
    def test_duplicate_material_id_rejected(self):
        d=actual_shape();d['plan']['scope']='series';d['plan']['materials']*=2
        with self.assertRaises(ContractError):check(d)
    def test_multiple_entrypoints_supported(self):
        d=actual_shape();d['plan']['entrypoints']=['concept','artifact'];check(d,'produce')
    def test_unknown_entrypoint_rejected(self):
        d=actual_shape();d['plan']['entrypoints']=['magic']
        with self.assertRaises(ContractError):check(d)
    def test_path_traversal_rejected(self):
        for path in ['../outside.md','/etc/passwd','C:/outside','a\\b.md','.']:
            with self.subTest(path=path):
                with self.assertRaises(ContractError):validate_relative(path)
    def test_extra_mastery_key_rejected(self):
        d=actual_shape();d['mastery']=100
        with self.assertRaises(ContractError):check(d)
    def fixture_release(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);root=Path(temp.name)
        (root/'lesson.md').write_text('Example only.\n',encoding='utf-8')
        d=actual_shape();d['plan']['materials'][0]['path']='lesson.md'
        d['reviews']=[{'material_id':'m01','path':'lesson.md','sha256':hashlib.sha256((root/'lesson.md').read_bytes()).hexdigest(),'checks':{k:{'verdict':'pass','location':'lesson.md:1','reason':'synthetic structural fixture only'} for k in CHECKS}}]
        return root,d
    def test_reviewed_file_releases_structurally(self):
        r,d=self.fixture_release();check(d,'release',r)
    def test_changed_file_invalidates_review(self):
        r,d=self.fixture_release();(r/'lesson.md').write_text('modified')
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_missing_location_fails(self):
        r,d=self.fixture_release();d['reviews'][0]['checks']['facts']['location']=None
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_missing_review_fails(self):
        r,d=self.fixture_release();d['reviews']=[]
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_nonapplicable_mapping_allowed_without_artifact(self):
        r,d=self.fixture_release();d['reviews'][0]['checks']['artifact_mapping'].update(verdict='not_applicable',location=None,reason='No artifact in this synthetic concept request.')
        check(d,'release',r)
    def test_nonapplicable_facts_cannot_bypass_review(self):
        r,d=self.fixture_release();d['reviews'][0]['checks']['facts']['verdict']='not_applicable'
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_artifact_mapping_required_for_artifact_entry(self):
        r,d=self.fixture_release();d['plan']['entrypoints']=['artifact'];d['reviews'][0]['checks']['artifact_mapping']['verdict']='not_applicable'
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_chat_has_no_file_release(self):
        r,d=self.fixture_release();d['plan']['materials'][0]['path']=None
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_symlink_material_rejected(self):
        r,d=self.fixture_release();(r/'other.md').write_text('Example only.\n');(r/'lesson.md').unlink();(r/'lesson.md').symlink_to(r/'other.md')
        with self.assertRaises(ContractError):check(d,'release',r)
    def test_partial_review_blocks(self):
        r,d=self.fixture_release();d['reviews'][0]['checks']['connections']['verdict']='partial'
        with self.assertRaises(ContractError):check(d,'release',r)
