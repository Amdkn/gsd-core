"""Smoke tests de l'adapter gsd-core (D-N053 pas C).

Roulés avec le venv du pas : `python -m pytest aspace-gsd-core-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel réseau. La validation complète
de la suite est celle de la suite amont bornée (`node scripts/run-tests.cjs
--suite unit` après `npm run build:lib`) ; le smoke vérifie les constantes,
les comptages mesurés par l'adapter et le statut de référence du canonique
(§D5).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_gsd_core_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:gsd-core"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/gsd-core"
    assert adapter.UPSTREAM_REPO == "open-gsd/gsd-core"
    assert adapter.UPSTREAM_BRANCH == "next"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "d8c51c5e335d178e846beef34462e003b449673b"
    assert adapter.BIND_LAYER == "4L"


def test_validate_counts():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["bin_lib_expected_missing"] == []
    assert v["bin_lib_count"] == 9
    assert v["workflows_count"] == 91
    assert v["workflows_dirs"] == 18
    assert v["workflows_files_total"] == 187
    assert v["skills_dirs"] == 72
    assert v["skills_with_skill_md"] == 72
    assert v["agents_count"] == 64
    assert v["commands_gsd_present"] is True
    assert v["capability_registry_lines"] == 8518
    assert len(v["capability_registry_sections"]) == 7
    assert v["run_tests_present"] is True
    assert v["claude_plugin_present"] is True
    assert v["opencode_present"] is True
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_validate_coherent():
    v = adapter.validate()
    assert v["inventory_coherent"] is True
    assert v["canonical"] == "fiber:a0:superpowers"


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp"):
        assert banned not in src, banned


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:gsd-core"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
    assert d["canonical"] == "fiber:a0:superpowers"
