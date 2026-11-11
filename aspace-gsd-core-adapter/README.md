# A'Space adapter — gsd-core (référence du canonique, nouveau domicile)

**Adresse :** `fiber:a0:gsd-core` — D-N053 pas C (design Clara, design signé pas C D-C0..D-C3).
**Fork souverain :** `Amdkn/gsd-core` (parent `open-gsd/gsd-core`, branche `next`).
**Gel amont :** `cb15dcf13d99e0c24ce3bff7089ae02f9a6a6aaa` (« docs(#5307): list beads in the Community Capability Registry (#5384) »).
**Bind Cordis Fiber (4L) :** `d8c51c5e335d178e846beef34462e003b449673b` — `aspace-plugin.json` sur `aspace-v5-native` (parent = gel, patron D8 / pas A autogluon), re-appliqué VERBATIM sur `next` au-dessus de l'adapter (F8 D4).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron pas A/B.

## Ce que fait l'adapter

gsd-core est une référence du canonique MasterSpec `fiber:a0:superpowers` (§D5) :
monorepo Node/TypeScript — `gsd-core/bin/lib/` (registre de capacités),
`gsd-core/workflows/`, `skills/`, `agents/`, `commands/gsd`.

Surface : `validate()` (constate : gel, licence, 9 fichiers `bin/lib/`,
91 workflows à la racine + 18 sous-dossiers (187 fichiers), 72 skills / 72 SKILL.md, 64 agents, registre de capacités
8 518 lignes / 7 sections, commandes/plugins/runner, zéro appel réseau),
`doctor()` (liste de contrôles), `describe()` (manifeste machine).
**Aucun fichier amont touché, aucun appel réseau, aucun poids monté dans le fork.**

Mesures au gel : `bin/lib/` 9 .cjs + vendor/, 91 workflows à la racine
+ 18 sous-dossiers (187 fichiers), 72 skills,
64 agents. Suite amont bornée (D-C2) : `node scripts/run-tests.cjs
--suite unit` après `npm run build:lib` (pretest amont).

Nouveau domicile (§D4) : l'ancien fork `Amdkn/get-shit-done` n'est pas
touché (H-A7) — le gitlink V5 est re-pointé par renommage `get-shit-done`
→ `gsd-core` (D-C1 option (a)).

## Confinement

Aucun confinement commercial : code MIT. Usage B2B autorisé par la licence.

## Tests

```bash
python -m pytest aspace-gsd-core-adapter/tests/test_smoke.py -v
```

Suite amont bornée (Node 24, TMPDIR hors /tmp — /tmp tmpfs 512 Mo saturé
par les autres pistes) :

```bash
npm run build:lib
TMPDIR=$HOME/workspace/.tmp-pas-c node scripts/run-tests.cjs --suite unit
```
