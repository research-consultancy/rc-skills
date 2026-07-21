---
name: pubmed
description: Search and verify biomedical literature in PubMed. Use when a medical research question needs papers, PMIDs, MeSH-aware queries, evidence mapping, citation verification, related studies, or a reproducible PubMed search.
---

# PubMed

Use PubMed as a reproducible evidence lookup, not a title generator.

## Define the search

Clarify the information need and whether the search is a rapid lookup, scoping search, citation check, or systematic-search contribution. Translate clinical questions into PICO/PECO/PICOS concepts where useful.

For each concept, combine:

- controlled vocabulary, including current MeSH terms;
- title/abstract synonyms, spelling variants, acronyms, and older terminology;
- study-design terms only when they serve the stated purpose.

Build Boolean blocks explicitly. Inspect PubMed's query translation or Search Details when available. Treat field tags as exact constraints because they turn off Automatic Term Mapping for the tagged term.

The search definition is complete when another researcher could rerun the exact query and understand every applied limit.

## Retrieve and verify

Use an available PubMed connector first. Otherwise use NCBI E-utilities according to [references/eutils.md](references/eutils.md).

Retrieve full PubMed records for candidate PMIDs. Verify title, authors, journal, publication year, abstract, publication type, MeSH terms, DOI, correction/retraction links, and PMID from the record itself. Deduplicate by PMID first, then DOI and normalized title.

For topic refinement, first locate recent systematic reviews and protocols, then use their terminology and included studies to find landmark and newer primary reports. For claim verification, read enough of the abstract or accessible full text to determine whether the cited paper actually supports the claim.

Retrieval is complete only when every reported paper has a verified PMID and the result set's coverage limits are stated.

## Report reproducibly

Return:

1. the exact PubMed query;
2. search date, result count, sort order, and applied limits;
3. a concise synthesis answering the research need;
4. a table or list with title, first author, year, journal, study type, PMID, DOI when present, and `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`;
5. caveats about indexing, unavailable abstracts/full text, retractions or corrections, and likely missed terminology.

Label inference as inference. A PubMed-only search is not an exhaustive systematic search; recommend additional databases and information sources when the user is conducting a systematic review or meta-analysis.
