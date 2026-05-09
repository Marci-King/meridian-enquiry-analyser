"""Lightweight keyword retrieval for the Meridian V2 proof artifact.

This module uses local Markdown files, simple chunking, and keyword-overlap
scoring. It is a deterministic proof layer, not a production retrieval system.
It uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


DEFAULT_KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent / "knowledge_base"

STOPWORDS = {
    "a",
    "about",
    "all",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "by",
    "can",
    "do",
    "does",
    "for",
    "from",
    "have",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "or",
    "our",
    "say",
    "should",
    "the",
    "this",
    "to",
    "what",
    "whether",
    "with",
    "you",
    "your",
}


@dataclass(frozen=True)
class GuidanceChunk:
    """One searchable chunk from the local Markdown guidance."""

    source_filename: str
    chunk_id: str
    text: str
    keywords: set[str]


def tokenize(text: str) -> set[str]:
    """Return normalized keywords for deterministic overlap scoring."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


def split_markdown_into_chunks(source_filename: str, markdown: str) -> list[GuidanceChunk]:
    """Split Markdown into small heading-aware chunks."""
    chunks: list[GuidanceChunk] = []
    current_heading = "overview"
    current_lines: list[str] = []
    chunk_number = 1

    def flush() -> None:
        nonlocal chunk_number, current_lines
        text = "\n".join(line.strip() for line in current_lines).strip()
        if not text:
            current_lines = []
            return
        chunk_id = f"{Path(source_filename).stem}:{chunk_number:02d}"
        chunk_text = f"{current_heading}\n{text}"
        chunks.append(
            GuidanceChunk(
                source_filename=source_filename,
                chunk_id=chunk_id,
                text=chunk_text,
                keywords=tokenize(chunk_text),
            )
        )
        chunk_number += 1
        current_lines = []

    for line in markdown.splitlines():
        if line.startswith("#"):
            flush()
            current_heading = line.lstrip("#").strip() or "section"
            continue
        if line.strip():
            current_lines.append(line)
        else:
            flush()

    flush()
    return chunks


class KeywordGuidanceRetriever:
    """Load local Markdown guidance and return top keyword-overlap snippets."""

    def __init__(self, knowledge_base_dir: Path | None = None) -> None:
        self.knowledge_base_dir = knowledge_base_dir or DEFAULT_KNOWLEDGE_BASE_DIR
        self.chunks = self._load_chunks()

    def _load_chunks(self) -> list[GuidanceChunk]:
        chunks: list[GuidanceChunk] = []
        for path in sorted(self.knowledge_base_dir.glob("*.md")):
            chunks.extend(split_markdown_into_chunks(path.name, path.read_text(encoding="utf-8")))
        return chunks

    def retrieve(self, query: str, limit: int = 3) -> list[dict[str, object]]:
        """Return the best matching snippets for a query.

        Results include the source filename, chunk ID, overlap score, matched
        keywords, and snippet text. Chunks with zero overlap are omitted.
        """
        query_keywords = tokenize(query)
        scored: list[tuple[int, str, GuidanceChunk, list[str]]] = []

        for chunk in self.chunks:
            matches = sorted(query_keywords & chunk.keywords)
            if not matches:
                continue
            scored.append((len(matches), chunk.chunk_id, chunk, matches))

        scored.sort(key=lambda item: (-item[0], item[1]))

        results: list[dict[str, object]] = []
        for score, _, chunk, matches in scored[:limit]:
            snippet = re.sub(r"\s+", " ", chunk.text).strip()
            results.append(
                {
                    "source_filename": chunk.source_filename,
                    "chunk_id": chunk.chunk_id,
                    "score": score,
                    "matched_keywords": matches,
                    "snippet": snippet[:360],
                }
            )

        return results


def retrieve_guidance(query: str, limit: int = 3) -> list[dict[str, object]]:
    """Convenience wrapper for local keyword guidance retrieval."""
    return KeywordGuidanceRetriever().retrieve(query, limit=limit)


if __name__ == "__main__":
    sample_query = "JFades PRP guarantee outcome consultation"
    for result in retrieve_guidance(sample_query):
        print(f"{result['source_filename']} {result['chunk_id']} score={result['score']}")
        print(result["snippet"])
