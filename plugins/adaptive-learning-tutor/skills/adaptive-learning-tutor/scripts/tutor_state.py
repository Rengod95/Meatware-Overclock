#!/usr/bin/env python3
"""Local, consent-based state storage for adaptive-learning-tutor (inherited SLT schema 0.1.0).

Python 3.10+, standard library only. This is NOT an LLM, assessment engine,
background scheduler, or universal JSON Schema implementation. The validator
implements only the schema keywords used in this package and checks additional
reference/evidence invariants. It cannot verify the truth of supplied evidence.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Any, Iterator

SKILL_ROOT = Path(__file__).resolve().parent.parent


class StateError(ValueError):
    """A state contract, permission, or revision constraint was violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    def bad_constant(value: str) -> None:
        raise StateError(f"유효하지 않은 JSON 숫자: {value}")

    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=bad_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StateError(f"JSON을 읽지 못했습니다: {path}: {exc}") from exc


def _is_type(value: Any, expected: str) -> bool:
    types = {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "boolean": lambda: isinstance(value, bool),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value),
        "null": lambda: value is None,
    }
    if expected not in types:
        raise StateError(f"지원하지 않는 스키마 type: {expected}")
    return types[expected]()


def _validate(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> None:
    """Validate the limited set of JSON Schema keywords used by our own schema."""
    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/$defs/"):
            raise StateError(f"지원하지 않는 스키마 참조: {reference}")
        return _validate(value, root["$defs"][reference.rsplit("/", 1)[1]], root, path)
    if "anyOf" in schema:
        for option in schema["anyOf"]:
            try:
                _validate(value, option, root, path)
                return
            except StateError:
                pass
        raise StateError(f"{path}: 허용된 형태 중 어느 것에도 맞지 않습니다.")
    expected = schema.get("type")
    if expected is not None:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(_is_type(value, item) for item in choices):
            raise StateError(f"{path}: type은 {choices}여야 합니다.")
    if "const" in schema and value != schema["const"]:
        raise StateError(f"{path}: 값은 {schema['const']!r}여야 합니다.")
    if "enum" in schema and value not in schema["enum"]:
        raise StateError(f"{path}: 허용되지 않은 값 {value!r}")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - set(value)
        if missing:
            raise StateError(f"{path}: 필수 항목 누락 {sorted(missing)}")
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, item in value.items():
            if key in props:
                _validate(item, props[key], root, f"{path}.{key}")
            elif extra is False:
                raise StateError(f"{path}: 정의하지 않은 항목 {key!r}")
            elif isinstance(extra, dict):
                _validate(item, extra, root, f"{path}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise StateError(f"{path}: 항목 수가 부족합니다.")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise StateError(f"{path}: 항목 수가 너무 많습니다.")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(x, ensure_ascii=False, sort_keys=True) for x in value]
            if len(set(encoded)) != len(encoded):
                raise StateError(f"{path}: 중복 항목이 있습니다.")
        for index, item in enumerate(value):
            _validate(item, schema.get("items", {}), root, f"{path}[{index}]")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise StateError(f"{path}: 문자열이 너무 짧습니다.")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            raise StateError(f"{path}: 문자열이 너무 깁니다.")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise StateError(f"{path}: 문자열 형식이 맞지 않습니다.")
        if schema.get("format") == "date-time":
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise StateError(f"{path}: 날짜·시간 형식이 맞지 않습니다.") from exc
            if dt.tzinfo is None:
                raise StateError(f"{path}: 시간대가 포함된 날짜·시간이 필요합니다.")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", -math.inf):
            raise StateError(f"{path}: 최소값보다 작습니다.")


def _index(records: list[dict[str, Any]], name: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        key = record["id"]
        if key in result:
            raise StateError(f"{name}: 중복 ID {key}")
        result[key] = record
    return result


def _refs(values: list[str], target: dict[str, Any], label: str) -> None:
    missing = set(values) - set(target)
    if missing:
        raise StateError(f"{label}: 존재하지 않는 참조 {sorted(missing)}")


def validate_state(state: Any) -> None:
    schema = read_json(SKILL_ROOT / "assets/state.schema.json")
    _validate(state, schema, schema)
    authorization = state["authorization"]
    if authorization["persistent_storage"] and not authorization["consent_record"]:
        raise StateError("지속 저장을 켜려면 consent_record가 필요합니다.")
    if state["profile"]["instruction_mode"] == "read_only" and state["profile"]["preferences"]["mandatory_exercises"]:
        raise StateError("read_only에서 필수 실습을 켤 수 없습니다.")

    nodes = _index(state["curriculum"]["nodes"], "nodes")
    paths = _index(state["curriculum"]["reading_paths"], "reading_paths")
    claims = _index(state["claims"], "claims")
    evidence = _index(state["evidence"], "evidence")
    sources = _index(state["sources"], "sources")
    _index(state["artifacts"], "artifacts")
    materials = _index(state["materials"], "materials")
    _index(state["deliveries"], "deliveries")

    for node in nodes.values():
        _refs(node["source_ids"], sources, f"node {node['id']}")
    for path in paths.values():
        _refs(path["node_ids"], nodes, f"reading_path {path['id']}")
    for entry in state["curriculum"]["glossary"]:
        _refs([entry["node_id"]], nodes, "glossary")
    for entry in state["curriculum"]["foundations_backlog"]:
        _refs([entry["node_id"]], nodes, "foundations_backlog")
        _refs(entry["linked_material_ids"], materials, "foundations_backlog")

    # Only prerequisite edges must be acyclic; other relations can be cyclic.
    graph: dict[str, set[str]] = {key: set() for key in nodes}
    indegree = {key: 0 for key in nodes}
    seen_edges: set[tuple[str, str, str]] = set()
    for edge in state["curriculum"]["edges"]:
        _refs([edge["from"], edge["to"]], nodes, "edge")
        key = (edge["from"], edge["to"], edge["relation"])
        if key in seen_edges:
            raise StateError(f"중복 관계: {key}")
        seen_edges.add(key)
        if edge["relation"] == "prerequisite":
            graph[edge["from"]].add(edge["to"])
            indegree[edge["to"]] += 1
    ready = [key for key, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        key = ready.pop()
        visited += 1
        for target in graph[key]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    if visited != len(nodes):
        raise StateError("엄격한 선수 관계에 순환이 있습니다. 임시 모형이나 supports 관계로 설계를 수정하세요.")

    for item in evidence.values():
        _refs([item["claim_id"]], claims, f"evidence {item['id']}")
        if item["id"] not in claims[item["claim_id"]]["evidence_ids"]:
            raise StateError(f"evidence {item['id']}: claim의 evidence_ids에도 등록해야 합니다.")
        if item["kind"] == "self_report" and (item["outcome"] != "not_scored" or item["unassisted_on_this_item"]):
            raise StateError(f"evidence {item['id']}: 자기보고는 정답 평가나 무지원 수행 증거가 아닙니다.")
        if item["unassisted_on_this_item"]:
            a = item["assistance"]
            if (item["kind"] != "learner_response" or item["authorship"] != "learner"
                or a["task_help"] != "none" or a["solution_seen"] or a["ai_assistance"] != "none"):
                raise StateError(f"evidence {item['id']}: 도움·정답 노출·작성자 조건과 무지원 주장이 충돌합니다.")
    for claim in claims.values():
        if not claim["concept_ids"]:
            raise StateError(f"claim {claim['id']}: 하나 이상의 concept_id가 필요합니다.")
        _refs(claim["concept_ids"], nodes, f"claim {claim['id']}")
        _refs(claim["evidence_ids"], evidence, f"claim {claim['id']}")
        items = [evidence[key] for key in claim["evidence_ids"]]
        if any(item["claim_id"] != claim["id"] for item in items):
            raise StateError(f"claim {claim['id']}: 다른 주장에 속한 증거를 참조합니다.")
        assessment = claim["assessment"]
        label = assessment["label"]
        direct = [item for item in items if item["kind"] == "learner_response" and item["authorship"] == "learner"]
        supporting = [item for item in direct if item["outcome"] == "correct"]
        if label == "self_report_only" and (not items or any(item["kind"] != "self_report" for item in items)):
            raise StateError(f"claim {claim['id']}: self_report_only는 자기보고 증거만을 전제합니다.")
        if label == "supported_in_context" and not supporting:
            raise StateError(f"claim {claim['id']}: 사용자 자신의 실제 응답 근거가 없으므로 지식 지지를 주장할 수 없습니다.")
        if label == "mixed_in_context" and not direct:
            raise StateError(f"claim {claim['id']}: 혼합 판정에도 실제 사용자 반응이 필요합니다.")
        if label in {"supported_in_context", "mixed_in_context"}:
            if not assessment["limits"] or not assessment["reviewed_at"]:
                raise StateError(f"claim {claim['id']}: 해석의 한계와 검토 시점을 남기세요.")
        if label == "supported_in_context":
            supported_contexts = {item["context_id"] for item in supporting}
            if not assessment["supported_contexts"] or not set(assessment["supported_contexts"]) <= supported_contexts:
                raise StateError(f"claim {claim['id']}: 지지되는 맥락이 실제 증거 범위를 벗어납니다.")
        if label in {"unknown", "self_report_only"} and assessment["supported_contexts"]:
            raise StateError(f"claim {claim['id']}: 미확인·자기보고 상태에서 확인된 맥락을 만들지 마세요.")

    for source in sources.values():
        if source["verification_level"] == "opened" and not source["checked_at"]:
            raise StateError(f"source {source['id']}: 실제 열어 확인한 시점이 필요합니다.")
    for artifact in state["artifacts"]:
        _refs(artifact["source_ids"], sources, f"artifact {artifact['id']}")
    for material in materials.values():
        path = PurePosixPath(material["path"])
        if (path.is_absolute() or ".." in path.parts or "\\" in material["path"]
            or ":" in material["path"] or len(path.parts) < 2 or path.parts[0] != "materials"):
            raise StateError(f"material {material['id']}: materials/ 아래의 안전한 상대 경로가 필요합니다.")
        _refs(material["concept_ids"], nodes, f"material {material['id']}")
        _refs(material["source_ids"], sources, f"material {material['id']}")
        if set(material["source_versions"]) != set(material["source_ids"]):
            raise StateError(f"material {material['id']}: source_versions는 모든 source_id와 일치해야 합니다.")
        if material["status"] == "reviewed":
            for source_id in material["source_ids"]:
                current = sources[source_id]["version"]
                if current is not None and material["source_versions"][source_id] != current:
                    raise StateError(f"material {material['id']}: 출처 버전이 바뀌었습니다. 재검토하거나 needs_recheck로 표시하세요.")
    for delivery in state["deliveries"]:
        _refs([delivery["material_id"]], materials, f"delivery {delivery['id']}")
        if delivery["event"] == "user_reported_read" and not delivery["source_locator"]:
            raise StateError("읽었다는 자기보고에는 실제 발언 위치가 필요합니다.")
    if state["last_session"]:
        _refs(state["last_session"]["material_ids"], materials, "last_session")
        _refs(state["last_session"]["claim_ids"], claims, "last_session")


def _root(workspace: str | Path) -> Path:
    original = Path(workspace).expanduser()
    if original.is_symlink():
        raise StateError("작업 공간 자체의 심볼릭 링크는 허용하지 않습니다.")
    root = original.resolve()
    if not root.is_dir() or (root / "state.json").is_symlink():
        raise StateError("유효한 작업 공간과 일반 state.json 파일이 필요합니다.")
    return root


def load_workspace(workspace: str | Path) -> tuple[Path, dict[str, Any]]:
    root = _root(workspace)
    state = read_json(root / "state.json")
    validate_state(state)
    return root, state


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=".state-", suffix=".json.tmp", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, allow_nan=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


@contextmanager
def workspace_lock(root: Path) -> Iterator[None]:
    lock = root / ".state.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise StateError("다른 변경이 진행 중이거나 잠금 파일이 남아 있습니다. 상태를 확인하세요.") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(f"pid={os.getpid()}\ncreated_at={utc_now()}\n")
        yield
    finally:
        lock.unlink(missing_ok=True)


def init_workspace(workspace: str | Path, consent: bool) -> dict[str, Any]:
    if not consent:
        raise StateError("저장 위치와 보존에 대한 사용자 동의 후 --consent를 사용하세요. 아무 파일도 만들지 않았습니다.")
    original = Path(workspace).expanduser()
    if original.exists() or original.is_symlink():
        raise StateError("기존 폴더를 덮어쓰지 않습니다. 새 작업 공간 경로를 지정하세요.")
    root = original.resolve()
    if not root.parent.is_dir():
        raise StateError("상위 폴더가 없습니다. 존재하는 상위 폴더 아래의 새 경로를 지정하세요.")
    state = read_json(SKILL_ROOT / "assets/default-state.json")
    state["updated_at"] = utc_now()
    state["authorization"] = {
        "persistent_storage": True,
        "consent_record": f"CLI init --consent; {state['updated_at']}; local directory: {root}",
    }
    validate_state(state)
    root.mkdir(mode=0o700)
    (root / "materials").mkdir(mode=0o700)
    (root / "designs").mkdir(mode=0o700)
    atomic_write(root / "state.json", state)
    return {"status": "initialized", "workspace": str(root), "revision": 0,
            "note": "상태 저장소만 초기화했습니다. 튜터 서버·자동 기록·외부 연동은 실행하지 않습니다."}


def _collections(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result = {key: state[key] for key in ("claims", "evidence", "sources", "artifacts", "materials", "deliveries")}
    result.update({f"curriculum.{key}": state["curriculum"][key] for key in ("nodes", "reading_paths")})
    return result


def _change_summary(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {}
    for name, previous in _collections(old).items():
        following = _collections(new)[name]
        old_map, new_map = {x["id"]: x for x in previous}, {x["id"]: x for x in following}
        changes[name] = {
            "added": sorted(new_map.keys() - old_map.keys()),
            "removed": sorted(old_map.keys() - new_map.keys()),
            "changed": sorted(k for k in old_map.keys() & new_map.keys() if old_map[k] != new_map[k]),
        }
    changes["profile_changed"] = old["profile"] != new["profile"]
    changes["curriculum_changed"] = old["curriculum"] != new["curriculum"]
    changes["last_session_changed"] = old["last_session"] != new["last_session"]
    return changes


def commit_candidate(workspace: str | Path, candidate_path: Path, expected_revision: int,
                     apply: bool = False, allow_removals: bool = False) -> dict[str, Any]:
    candidate = read_json(candidate_path)
    validate_state(candidate)
    root, _ = load_workspace(workspace)

    def prepare() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        _, old = load_workspace(root)
        if not old["authorization"]["persistent_storage"]:
            raise StateError("이 작업 공간에는 지속 저장 권한이 없습니다.")
        if old["revision"] != expected_revision or candidate["revision"] != expected_revision:
            raise StateError(f"revision 충돌: 현재={old['revision']}, 후보={candidate['revision']}, 기대={expected_revision}. 다시 읽고 합치세요.")
        if candidate["authorization"] != old["authorization"]:
            raise StateError("commit은 저장 권한·최초 동의 기록을 변경하지 않습니다.")
        summary = _change_summary(old, candidate)
        removed = {key: value["removed"] for key, value in summary.items()
                   if isinstance(value, dict) and value.get("removed")}
        result = {"status": "validated_not_written", "revision": old["revision"],
                  "changes": summary, "removals_require_flag": bool(removed)}
        if apply and removed and not allow_removals:
            raise StateError("삭제되는 ID가 있습니다. 사용자 요청과 변경안을 확인한 뒤 --allow-removals를 추가하세요: " + json.dumps(removed, ensure_ascii=False))
        return old, summary, result

    if not apply:
        return prepare()[2]
    with workspace_lock(root):
        old, summary, result = prepare()
        updated = copy.deepcopy(candidate)
        updated["revision"] = old["revision"] + 1
        updated["updated_at"] = utc_now()
        validate_state(updated)
        atomic_write(root / "state.json", updated)
        result.update({"status": "written", "revision": updated["revision"], "changes": summary})
        return result


def summarize(state: dict[str, Any]) -> dict[str, Any]:
    labels: dict[str, int] = {}
    for claim in state["claims"]:
        label = claim["assessment"]["label"]
        labels[label] = labels.get(label, 0) + 1
    return {"revision": state["revision"], "mode": state["profile"]["instruction_mode"],
            "domain": state["profile"]["domain"], "concept_count": len(state["curriculum"]["nodes"]),
            "claim_labels": labels, "evidence_count": len(state["evidence"]),
            "material_count": len(state["materials"]), "delivery_event_count": len(state["deliveries"]),
            "note": "개수는 기록 통계이며 이해도·숙련 점수가 아닙니다."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="동의한 새 로컬 작업 공간 만들기")
    init.add_argument("workspace"); init.add_argument("--consent", action="store_true")
    check = commands.add_parser("check", help="상태의 구조와 증거 연결 검증")
    check.add_argument("workspace")
    summary = commands.add_parser("summary", help="원문 반응 없이 상태 통계 보기")
    summary.add_argument("workspace")
    commit = commands.add_parser("commit", help="상태 변경안 검증; --apply일 때만 저장")
    commit.add_argument("workspace"); commit.add_argument("candidate", type=Path)
    commit.add_argument("--expected-revision", required=True, type=int)
    commit.add_argument("--apply", action="store_true")
    commit.add_argument("--allow-removals", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_workspace(args.workspace, args.consent)
        elif args.command == "commit":
            result = commit_candidate(args.workspace, args.candidate, args.expected_revision, args.apply, args.allow_removals)
        else:
            _, state = load_workspace(args.workspace)
            result = summarize(state)
            if args.command == "check":
                result["status"] = "structurally_valid"
                result["limits"] = "사실·저작자·실제 이해·문서 내용·권한의 진실성은 자동 검증하지 않습니다."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (StateError, OSError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
