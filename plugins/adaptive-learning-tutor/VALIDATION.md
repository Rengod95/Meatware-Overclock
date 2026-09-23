# Codex plugin distribution validation

Date: 2026-09-23. Plugin wrapper 0.3.1; preserved learning core 0.3.0.

## Executed locally

| Check | Result |
|---|---|
| Original package files compared byte-for-byte with the uploaded ZIP | 46/46 identical |
| Original core unit tests, rerun from the nested plugin layout | 88 passed |
| Core structural and SHA-256 inventory validation | passed, 45 checksum records |
| Standalone prompt synchronization check (default CLI mode) | passed |
| New distribution regression tests | 10 passed |
| Marketplace identity, local path containment, manifest and skills-only checks | passed |

The distribution tests cover valid packaging, missing or changed skill files, traversal, absolute paths, symlinks, unexpected MCP/hooks, duplicate marketplace entries, and changed preview settings. An initial wrapper check used the wrong settings key and a documentation command used an unsupported flag. Both wrapper errors were corrected before the successful rerun; the preserved core files were not changed.

## Not performed

No Codex desktop installation or UI activation was performed. No model behavior or human learning effect was measured. The 26 behavioral cases inside the original core remain designed-but-unexecuted cases. The previous logs inside the core are preserved upstream records, not new host validation.

The source branch is published separately through the connected GitHub service. A remote commit and read-back must be verified before claiming publication. Repository publication is not installation in the user's desktop app and is not approval for the public plugin directory.

This is a package-specific offline validator, not an official OpenAI plugin certification. No external server, OAuth application, automatic hook, learner state, or new open-source license was introduced.
