from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Any

from .errors import ResponseError


def _text(element: ET.Element | None) -> str | None:
    if element is None:
        return None
    value = "".join(element.itertext())
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def _date(article: ET.Element) -> dict[str, str]:
    node = article.find(".//ArticleDate")
    if node is None:
        node = article.find(".//PubDate")
    if node is None:
        return {}
    return {
        tag.lower(): value
        for tag in ("Year", "Month", "Day", "MedlineDate")
        if (value := _text(node.find(tag)))
    }


def parse_pubmed_xml(data: bytes) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as error:
        raise ResponseError(f"Malformed PubMed XML: {error}") from error
    records: list[dict[str, Any]] = []
    for citation in root.findall(".//PubmedArticle"):
        medline = citation.find("MedlineCitation")
        article = citation.find(".//Article")
        if medline is None or article is None:
            continue
        pmid_node = medline.find("PMID")
        pmid = _text(pmid_node)
        if not pmid:
            continue
        authors = []
        for author in article.findall(".//AuthorList/Author"):
            collective = _text(author.find("CollectiveName"))
            name = collective or " ".join(
                filter(
                    None,
                    [_text(author.find("ForeName")), _text(author.find("LastName"))],
                )
            )
            if name:
                authors.append(name)
        identifiers: dict[str, list[str]] = {}
        # ReferenceList entries also contain ArticleIdList nodes. Only PubmedData's
        # direct list identifies the record being parsed.
        for node in citation.findall("PubmedData/ArticleIdList/ArticleId"):
            if value := _text(node):
                identifiers.setdefault(node.attrib.get("IdType", "unknown"), []).append(
                    value
                )
        abstracts = []
        for node in article.findall(".//Abstract/AbstractText"):
            value = _text(node)
            if value:
                label = node.attrib.get("Label")
                abstracts.append(f"{label}: {value}" if label else value)
        relations = []
        for comment in citation.findall(".//CommentsCorrections"):
            relations.append(
                {
                    "type": comment.attrib.get("RefType"),
                    "pmid": _text(comment.find("PMID")),
                    "citation": _text(comment.find("RefSource")),
                }
            )
        records.append(
            {
                "pmid": pmid,
                "pmid_version": pmid_node.attrib.get("Version")
                if pmid_node is not None
                else None,
                "status": medline.attrib.get("Status"),
                "title": _text(article.find("ArticleTitle")),
                "abstract": "\n".join(abstracts) or None,
                "authors": authors,
                "journal": _text(article.find(".//Journal/Title")),
                "journal_abbreviation": _text(
                    medline.find("MedlineJournalInfo/MedlineTA")
                ),
                "publication_date": _date(article),
                "publication_types": [
                    _text(node)
                    for node in article.findall(
                        ".//PublicationTypeList/PublicationType"
                    )
                    if _text(node)
                ],
                "mesh_terms": [
                    _text(node)
                    for node in medline.findall(".//MeshHeading/DescriptorName")
                    if _text(node)
                ],
                "identifiers": identifiers,
                "corrections_retractions": relations,
            }
        )
    deleted = [
        _text(node) for node in root.findall(".//DeleteCitation/PMID") if _text(node)
    ]
    return records, deleted
