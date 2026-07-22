class PubMedError(Exception):
    """A user-actionable PubMed tool failure."""

    code = "pubmed_error"


class ConfigurationError(PubMedError):
    code = "configuration_error"


class TransportError(PubMedError):
    code = "transport_error"


class ResponseError(PubMedError):
    code = "response_error"


class CompletenessError(PubMedError):
    code = "completeness_error"


class SearchLimitError(PubMedError):
    code = "search_limit_exceeded"
