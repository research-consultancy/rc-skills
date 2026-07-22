# Route PubMed retrieval by capability

Use the bundled CLI for evidence-grade retrieval and verification, and use an already-connected PubMed MCP for bounded lookup, PMC full text, and copyright or licence status. The MCP reduces interaction cost and adds capabilities the CLI lacks, but its current contract does not expose the warnings, completeness checks, durable provenance, or missing-record accounting required for evidence-grade work; routing by capability preserves those guarantees without discarding the connector's strengths.
