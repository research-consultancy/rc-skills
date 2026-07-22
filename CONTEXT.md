# Research Consultancy Skills

This repository defines repeatable agent practices for rigorous medical research. Its language distinguishes retrieval guarantees from the transport used to obtain evidence.

## Language

**Evidence-grade retrieval**:
A literature retrieval whose completeness boundaries, identifiers, query interpretation, and provenance are explicit enough to audit and rerun.
_Avoid_: exhaustive search, robust search

**Bounded lookup**:
A deliberately limited literature lookup of at most 200 records that makes no claim of exhaustiveness.
_Avoid_: quick search, complete search

**Capability routing**:
Selecting a retrieval path from the guarantees and capabilities the task requires, rather than from ambient tool availability alone.
_Avoid_: connector-first, automatic fallback
