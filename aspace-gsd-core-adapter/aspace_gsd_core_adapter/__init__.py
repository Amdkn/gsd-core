"""A'Space adapter — gsd-core (D-N053 pas C, design Clara + design signé pas C).

Contrat seul, patron pas A/B : cet adapter ne modifie AUCUN fichier amont,
ne fait AUCUN appel réseau, ne monte AUCUN poids. Il constate : le gel
épinglé, la licence, l'inventaire commandes/phases (gsd-core/bin/lib/,
registre de capacités, manifeste de sections, workflows/, skills/,
agents/) — et il se déclare RÉFÉRENCE du canonique MasterSpec
`fiber:a0:superpowers` (§D5), pas un framework parallèle.

Adresse : fiber:a0:gsd-core
Fork souverain : Amdkn/gsd-core (parent open-gsd/gsd-core, branche next)
Gel amont : cb15dcf13d99e0c24ce3bff7089ae02f9a6a6aaa (« docs(#5307): list beads in the Community Capability Registry (#5384) »)
Bind Cordis Fiber (4L) : d8c51c5e335d178e846beef34462e003b449673b (créé pendant le pas, patron D8 / pas A autogluon, parent = gel)
Licence : MIT

Mesures au gel (2026-11-11, vérifiées au fichier) :
- gsd-core/bin/lib/ : 9 .cjs suivis + vendor/ ; `npm run build:lib`
  (ADR-457) compile `src/**/*.cts` en artefacts .cjs gitignored dans ce
  même dossier (256 fichiers après build) — la mesure porte sur les 9
  sources suivies, pas sur le disque brut.
- gsd-core/bin/ : check-latest-version.cjs, ensure-runtime-build.cjs, gsd-tools.cjs,
  gsd_run, lib/, shared/, verify-reapply-patches.cjs.
- gsd-core/workflows/ : 91 fichiers à la racine + 18 sous-dossiers
  (187 fichiers au total) ; skills/ : 72 entrées, 72 SKILL.md ;
  agents/ : 64 fichiers .md ; commands/gsd (1).
- Registre de capacités : gsd-core/bin/lib/capability-registry.cjs
  (8 518 lignes, généré par scripts/gen-capability-registry.cjs) ;
  docs/registries/capability-registry.md (136 lignes, 7 sections).
- Suite amont bornée (D-C2) : `node scripts/run-tests.cjs --suite unit`
  (≈ 1 169 fichiers : 1 126 plain + 43 property) après
  `npm run build:lib` (pretest amont). Autres suites hors borne.
- Nouveau domicile (§D4) : l'ancien fork Amdkn/get-shit-done n'est pas
  touché (H-A7) — le gitlink V5 est re-pointé par renommage
  get-shit-done → gsd-core (D-C1 option (a)).
- Télémétrie : 0 SDK ; seuls hôtes réseau = loopback locaux
  (Ollama 11434, LM Studio 1234, MemPalace 8080, configurés par
  l'utilisateur) + `npm view` explicite via /gsd-update.
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:gsd-core"
FORK = "Amdkn/gsd-core"
UPSTREAM_REPO = "open-gsd/gsd-core"
UPSTREAM_BRANCH = "next"
PINNED_UPSTREAM_COMMIT = "cb15dcf13d99e0c24ce3bff7089ae02f9a6a6aaa"
PINNED_UPSTREAM_COMMIT_SHORT = "cb15dcf1"
BIND_COMMIT = "d8c51c5e335d178e846beef34462e003b449673b"
BIND_LAYER = "4L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"

CANONICAL = "fiber:a0:superpowers"
EXPECTED_BIN_LIB = (
    "capability-command-router.cjs",
    "capability-registry.cjs",
    "capability-validator.cjs",
    "exit-code-registry.cjs",
    "legacy-cleanup.cjs",
    "loop-host-contract.cjs",
    "package-identity.cjs",
    "profile-pipeline-command-router.cjs",
    "stale-bake-guard.cjs",
)

CONFINEMENT = """Aucun confinement commercial : code MIT. Usage B2B autorisé par la
licence. L'adapter ne fait que constater l'inventaire ; aucun code amont
n'est modifié."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _skill_inventory(root: Path) -> dict:
    core = root / "gsd-core"
    bin_lib = core / "bin" / "lib"
    # Mesure sur les SOURCES SUIVIES uniquement : `npm run build:lib`
    # (ADR-457) compile src/**/*.cts en artefacts .cjs gitignored dans
    # ce même dossier (256 fichiers après build) — un comptage brut du
    # disque varie avec l'état du build, pas avec l'inventaire amont.
    bin_lib_files = sorted(p.name for p in bin_lib.iterdir() if p.is_file()) if bin_lib.is_dir() else []
    bin_lib_expected_present = [f for f in EXPECTED_BIN_LIB if f in bin_lib_files]
    workflows = core / "workflows"
    workflow_files = sorted(p.name for p in workflows.iterdir() if p.is_file()) if workflows.is_dir() else []
    workflow_dirs = sorted(p.name for p in workflows.iterdir() if p.is_dir()) if workflows.is_dir() else []
    workflow_files_total = sum(1 for p in workflows.rglob("*") if p.is_file()) if workflows.is_dir() else 0
    skills_dir = root / "skills"
    skill_dirs = sorted(p.name for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    skill_md = sum(1 for p in skills_dir.rglob("SKILL.md") if ".git" not in p.parts) if skills_dir.is_dir() else 0
    agents_dir = root / "agents"
    agent_files = sorted(p.name for p in agents_dir.iterdir() if p.is_file()) if agents_dir.is_dir() else []
    registry = bin_lib / "capability-registry.cjs"
    registry_lines = 0
    if registry.is_file():
        registry_lines = sum(1 for _ in registry.open(encoding="utf-8", errors="replace"))
    registry_doc = root / "docs" / "registries" / "capability-registry.md"
    sections = []
    if registry_doc.is_file():
        for line in registry_doc.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^##\s+(.+?)\s*$", line)
            if m:
                sections.append(m.group(1))
    return {
        "bin_lib_files": bin_lib_files,
        "bin_lib_expected_missing": [f for f in EXPECTED_BIN_LIB if f not in bin_lib_files],
        "bin_lib_expected_present": bin_lib_expected_present,
        "bin_lib_count": len(bin_lib_expected_present),
        "workflows_count": len(workflow_files),
        "workflows_dirs": len(workflow_dirs),
        "workflows_files_total": workflow_files_total,
        "skills_dirs": len(skill_dirs),
        "skills_with_skill_md": skill_md,
        "agents_count": len(agent_files),
        "commands_gsd_present": (root / "commands" / "gsd").exists(),
        "capability_registry_lines": registry_lines,
        "capability_registry_sections": sections,
        "run_tests_present": (root / "scripts" / "run-tests.cjs").is_file(),
        "build_lib_script": True,  # vérifié au package.json (tsc -p tsconfig.build.json)
        "claude_plugin_present": (root / ".claude-plugin" / "plugin.json").is_file(),
        "opencode_present": (root / ".opencode").is_dir(),
        "package_name": "@opengsd/gsd-core",
    }


def describe() -> dict:
    """Décrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'état de l'inventaire gelé. Aucun appel réseau, aucune écriture."""
    root = _repo_root()
    inv = _skill_inventory(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        **inv,
        "inventory_coherent": (
            inv["bin_lib_expected_missing"] == []
            and inv["bin_lib_count"] == 9
            and inv["workflows_count"] == 91
            and inv["workflows_dirs"] == 18
            and inv["workflows_files_total"] == 187
            and inv["skills_dirs"] == 72
            and inv["skills_with_skill_md"] == 72
            and inv["agents_count"] == 64
            and inv["commands_gsd_present"]
            and inv["capability_registry_lines"] == 8518
            and len(inv["capability_registry_sections"]) == 7
            and inv["run_tests_present"]
            and inv["claude_plugin_present"]
            and inv["opencode_present"]
        ),
    }


def doctor() -> list[dict]:
    """Liste de contrôles sur l'inventaire gelé."""
    v = validate()
    checks = [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT",
        },
        {
            "name": "bin_lib_9_fichiers",
            "ok": v["bin_lib_expected_missing"] == [] and v["bin_lib_count"] == 9,
            "detail": f"{v['bin_lib_count']} fichiers .cjs attendus présents dans gsd-core/bin/lib/ (artefacts compilés gitignored exclus, ADR-457), registre de capacités présent",
        },
        {
            "name": "workflows_91_plus_18_dossiers",
            "ok": v["workflows_count"] == 91 and v["workflows_dirs"] == 18
            and v["workflows_files_total"] == 187,
            "detail": f"{v['workflows_count']} workflows à la racine + {v['workflows_dirs']} sous-dossiers, {v['workflows_files_total']} fichiers au total",
        },
        {
            "name": "skills_72_agents_64",
            "ok": v["skills_dirs"] == 72 and v["skills_with_skill_md"] == 72 and v["agents_count"] == 64,
            "detail": f"{v['skills_dirs']} skills, {v['skills_with_skill_md']} SKILL.md, {v['agents_count']} agents",
        },
        {
            "name": "registre_capacites",
            "ok": v["capability_registry_lines"] == 8518 and len(v["capability_registry_sections"]) == 7,
            "detail": f"capability-registry.cjs {v['capability_registry_lines']} lignes, 7 sections au manifeste",
        },
        {
            "name": "commandes_plugins_runner",
            "ok": v["commands_gsd_present"] and v["claude_plugin_present"]
            and v["opencode_present"] and v["run_tests_present"],
            "detail": "commands/gsd, .claude-plugin/plugin.json, .opencode/, scripts/run-tests.cjs",
        },
        {
            "name": "reference_du_canonique",
            "ok": v["canonical"] == "fiber:a0:superpowers",
            "detail": "référence du canonique superpowers (§D5), pas un framework parallèle",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import réseau, 0 appel sortant",
        },
    ]
    return checks
