"""Synthetic regression tests. Test records are NOT real learner observations."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from tutor_state import (StateError, commit_candidate, init_workspace, load_workspace,
                         read_json, validate_state)  # noqa: E402

AT = '2026-09-19T12:00:00+09:00'


def initial():
    return read_json(ROOT / 'assets/default-state.json')


def with_claim():
    state = initial()
    state['curriculum']['nodes'].append({
        'id': 'toy.observation', 'label': '관찰과 상태의 차이', 'domain': 'synthetic-test',
        'layer': 'foundation', 'source_ids': [], 'scope_note': '가상 시험용 노드'})
    state['claims'].append({
        'id': 'claim.toy', 'concept_ids': ['toy.observation'],
        'statement': '가상 문제에서 관찰과 상태를 구분한다.', 'dimension': 'mechanism',
        'evidence_ids': [], 'assessment': {'label': 'unknown', 'supported_contexts': [],
                                        'limits': [], 'reviewed_at': None},
        'next_instruction_change': None})
    return state


def with_response():
    state = with_claim()
    state['evidence'].append({
        'id': 'evidence.synthetic', 'claim_id': 'claim.toy', 'kind': 'learner_response',
        'authorship': 'learner', 'context_id': 'synthetic-context', 'observed_at': AT,
        'response_summary': '합성 시험 데이터. 실제 사용자가 말한 내용이 아니다.',
        'source_locator': 'test-fixture://synthetic-response',
        'assistance': {'task_help': 'none', 'solution_seen': False,
                       'reference_access': 'allowed', 'ai_assistance': 'none'},
        'outcome': 'correct', 'unassisted_on_this_item': True,
        'alternative_explanations': ['실제 사람의 수행에 대한 증거가 아니다.'],
        'limits': ['테스트에서 자료구조만 검사한다.']})
    state['claims'][0]['evidence_ids'] = ['evidence.synthetic']
    state['claims'][0]['assessment'] = {
        'label': 'supported_in_context', 'supported_contexts': ['synthetic-context'],
        'limits': ['가상 테스트 데이터의 한 맥락에만 해당.'], 'reviewed_at': AT}
    return state


def with_material():
    state = with_claim()
    state['sources'].append({
        'id': 'source.toy', 'title': '설명용 가상 모형', 'locator': 'test-fixture://toy',
        'version': 'v1', 'checked_at': AT, 'verification_level': 'opened', 'kind': 'project_policy'})
    state['materials'].append({
        'id': 'material.toy', 'path': 'materials/toy.md', 'title': '가상 사례',
        'genre': 'reading_chapter', 'concept_ids': ['toy.observation'],
        'source_ids': ['source.toy'], 'source_versions': {'source.toy': 'v1'},
        'status': 'reviewed', 'version': 'v1'})
    return state


class StateContractTests(unittest.TestCase):
    def test_initial_has_preferences_but_no_knowledge_claims(self):
        state = initial()
        validate_state(state)
        self.assertFalse(state['authorization']['persistent_storage'])
        self.assertEqual([], state['claims'])
        self.assertEqual([], state['evidence'])
        self.assertIsNone(state['profile']['domain'])

    def test_unknown_status_mastered_is_rejected(self):
        state = with_claim(); state['claims'][0]['assessment']['label'] = 'mastered'
        with self.assertRaises(StateError): validate_state(state)

    def test_revision_boolean_is_not_integer(self):
        state = initial(); state['revision'] = True
        with self.assertRaises(StateError): validate_state(state)

    def test_undeclared_mastery_score_is_rejected(self):
        state = initial(); state['mastery_score'] = 98
        with self.assertRaises(StateError): validate_state(state)

    def test_duplicate_node_id_is_rejected(self):
        state = with_claim(); state['curriculum']['nodes'] *= 2
        with self.assertRaises(StateError): validate_state(state)

    def test_dangling_evidence_reference_is_rejected(self):
        state = with_claim(); state['claims'][0]['evidence_ids'] = ['does.not.exist']
        with self.assertRaises(StateError): validate_state(state)

    def test_evidence_requires_back_reference(self):
        state = with_response(); state['claims'][0]['evidence_ids'] = []
        with self.assertRaises(StateError): validate_state(state)

    def test_support_claim_requires_actual_response(self):
        state = with_claim(); state['claims'][0]['assessment']['label'] = 'supported_in_context'
        with self.assertRaises(StateError): validate_state(state)

    def test_self_report_cannot_be_scored_as_correct(self):
        state = with_response(); state['evidence'][0]['kind'] = 'self_report'
        with self.assertRaises(StateError): validate_state(state)

    def test_self_report_cannot_support_ability_claim(self):
        state = with_response(); item = state['evidence'][0]
        item.update(kind='self_report', outcome='not_scored', unassisted_on_this_item=False)
        with self.assertRaises(StateError): validate_state(state)
        state['claims'][0]['assessment'].update(label='self_report_only', supported_contexts=[])
        validate_state(state)

    def test_reference_access_does_not_equal_task_help(self):
        state = with_response()
        self.assertEqual('allowed', state['evidence'][0]['assistance']['reference_access'])
        validate_state(state)

    def test_helped_response_can_support_limited_context(self):
        state = with_response(); item = state['evidence'][0]
        item['unassisted_on_this_item'] = False
        item['assistance']['task_help'] = 'hint'
        validate_state(state)

    def test_solution_seen_cannot_be_unassisted(self):
        state = with_response(); state['evidence'][0]['assistance']['solution_seen'] = True
        with self.assertRaises(StateError): validate_state(state)

    def test_unknown_ai_help_cannot_be_unassisted(self):
        state = with_response(); state['evidence'][0]['assistance']['ai_assistance'] = 'unknown'
        with self.assertRaises(StateError): validate_state(state)

    def test_ai_artifact_cannot_support_learner_claim(self):
        state = with_response(); item = state['evidence'][0]
        item['authorship'] = 'ai_assisted'; item['unassisted_on_this_item'] = False
        with self.assertRaises(StateError): validate_state(state)

    def test_supported_context_cannot_generalize_to_other_context(self):
        state = with_response(); state['claims'][0]['assessment']['supported_contexts'] = ['all-contexts']
        with self.assertRaises(StateError): validate_state(state)

    def test_assessment_requires_limits(self):
        state = with_response(); state['claims'][0]['assessment']['limits'] = []
        with self.assertRaises(StateError): validate_state(state)

    def test_prerequisite_cycle_rejected(self):
        state = with_claim()
        state['curriculum']['nodes'].append({**state['curriculum']['nodes'][0], 'id': 'toy.other'})
        state['curriculum']['edges'] = [
            {'from': 'toy.observation', 'to': 'toy.other', 'relation': 'prerequisite', 'note': 'A before B'},
            {'from': 'toy.other', 'to': 'toy.observation', 'relation': 'prerequisite', 'note': 'B before A'}]
        with self.assertRaises(StateError): validate_state(state)
        for edge in state['curriculum']['edges']: edge['relation'] = 'supports'
        validate_state(state)

    def test_material_path_escape_rejected(self):
        for value in ('../outside.md', '/absolute.md', 'materials/../../out.md', r'materials\out.md', 'C:/out.md'):
            with self.subTest(path=value):
                state = with_material(); state['materials'][0]['path'] = value
                with self.assertRaises(StateError): validate_state(state)

    def test_source_version_change_requires_recheck(self):
        state = with_material(); state['sources'][0]['version'] = 'v2'
        with self.assertRaises(StateError): validate_state(state)
        state['materials'][0]['status'] = 'needs_recheck'
        validate_state(state)

    def test_opened_source_requires_time(self):
        state = with_material(); state['sources'][0]['checked_at'] = None
        with self.assertRaises(StateError): validate_state(state)

    def test_read_report_requires_locator(self):
        state = with_material()
        state['deliveries'].append({'id':'delivery.toy','material_id':'material.toy',
                                    'event':'user_reported_read','at':AT,'source_locator':None})
        with self.assertRaises(StateError): validate_state(state)

    def test_delivery_does_not_promote_knowledge(self):
        state = with_material()
        state['deliveries'].append({'id':'delivery.toy','material_id':'material.toy',
                                    'event':'delivered','at':AT,'source_locator':None})
        validate_state(state)
        self.assertEqual('unknown', state['claims'][0]['assessment']['label'])
        self.assertEqual([], state['evidence'])

    def test_timestamp_requires_timezone(self):
        state = with_response(); state['evidence'][0]['observed_at'] = '2026-09-19T12:00:00'
        with self.assertRaises(StateError): validate_state(state)

    def test_read_only_rejects_mandatory_exercises(self):
        state = initial(); state['profile']['preferences']['mandatory_exercises'] = True
        with self.assertRaises(StateError): validate_state(state)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        self.candidate = self.root / 'candidate.json'

    def tearDown(self):
        self.temp.cleanup()

    def save_candidate(self, state):
        self.candidate.write_text(json.dumps(state, ensure_ascii=False), encoding='utf-8')

    def init(self):
        init_workspace(self.workspace, consent=True)
        return load_workspace(self.workspace)[1]

    def test_no_consent_creates_nothing(self):
        with self.assertRaises(StateError): init_workspace(self.workspace, consent=False)
        self.assertFalse(self.workspace.exists())

    def test_existing_workspace_not_overwritten(self):
        self.init(); before = (self.workspace/'state.json').read_bytes()
        with self.assertRaises(StateError): init_workspace(self.workspace, consent=True)
        self.assertEqual(before, (self.workspace/'state.json').read_bytes())

    def test_dry_run_does_not_write(self):
        state = self.init(); before = (self.workspace/'state.json').read_bytes()
        state['profile']['domain'] = 'synthetic-test'; self.save_candidate(state)
        result = commit_candidate(self.workspace, self.candidate, 0)
        self.assertEqual('validated_not_written', result['status'])
        self.assertEqual(before, (self.workspace/'state.json').read_bytes())

    def test_apply_increments_revision(self):
        state = self.init(); state['profile']['domain'] = 'synthetic-test'; self.save_candidate(state)
        result = commit_candidate(self.workspace, self.candidate, 0, apply=True)
        self.assertEqual(1, result['revision'])
        self.assertEqual('synthetic-test', load_workspace(self.workspace)[1]['profile']['domain'])
        self.assertFalse((self.workspace/'.state.lock').exists())

    def test_stale_revision_cannot_overwrite(self):
        state = self.init(); self.save_candidate(state)
        commit_candidate(self.workspace, self.candidate, 0, apply=True)
        before = (self.workspace/'state.json').read_bytes()
        with self.assertRaises(StateError): commit_candidate(self.workspace, self.candidate, 0, apply=True)
        self.assertEqual(before, (self.workspace/'state.json').read_bytes())

    def test_candidate_revision_must_match(self):
        state = self.init(); state['revision'] = 7; self.save_candidate(state)
        with self.assertRaises(StateError): commit_candidate(self.workspace, self.candidate, 0, apply=True)

    def test_authorization_cannot_be_changed_by_commit(self):
        state = self.init(); state['authorization']['consent_record'] = 'new'; self.save_candidate(state)
        with self.assertRaises(StateError): commit_candidate(self.workspace, self.candidate, 0, apply=True)

    def test_removal_requires_additional_flag(self):
        state = self.init()
        state['curriculum']['nodes'] = with_claim()['curriculum']['nodes']
        self.save_candidate(state); commit_candidate(self.workspace, self.candidate, 0, apply=True)
        state = load_workspace(self.workspace)[1]; state['curriculum']['nodes'] = []
        self.save_candidate(state)
        result = commit_candidate(self.workspace, self.candidate, 1)
        self.assertTrue(result['removals_require_flag'])
        with self.assertRaises(StateError): commit_candidate(self.workspace, self.candidate, 1, apply=True)
        result = commit_candidate(self.workspace, self.candidate, 1, apply=True, allow_removals=True)
        self.assertEqual(2, result['revision'])

    def test_existing_lock_blocks_apply(self):
        state = self.init(); self.save_candidate(state)
        (self.workspace/'.state.lock').write_text('synthetic lock')
        with self.assertRaises(StateError): commit_candidate(self.workspace, self.candidate, 0, apply=True)
        self.assertTrue((self.workspace/'.state.lock').exists())

    def test_nonfinite_json_number_rejected(self):
        self.candidate.write_text('{"value": NaN}')
        with self.assertRaises(StateError): read_json(self.candidate)


if __name__ == '__main__':
    unittest.main()
