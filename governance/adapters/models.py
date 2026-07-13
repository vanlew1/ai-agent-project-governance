"""Stable, side-effect-free values returned by project adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionEvidence:
    adapter_id: str
    matched_markers: tuple[str, ...]
    score: int
    reasons: tuple[str, ...]

    def to_mapping(self) -> dict[str, object]:
        return {"adapter_id": self.adapter_id, "matched_markers": list(self.matched_markers),
                "score": self.score, "reasons": list(self.reasons)}


@dataclass(frozen=True)
class AdapterDetection:
    schema_version: str
    repository_root: str
    primary_adapter: str
    detected_adapters: tuple[str, ...]
    confidence: str
    evidence: tuple[DetectionEvidence, ...]
    conflicts: tuple[str, ...]
    status: str
    detected_at: str
    auxiliary_adapters: tuple[str, ...] = ()

    def to_mapping(self) -> dict[str, object]:
        return {"schema_version": self.schema_version, "repository_root": self.repository_root,
                "primary_adapter": self.primary_adapter, "detected_adapters": list(self.detected_adapters),
                "auxiliary_adapters": list(self.auxiliary_adapters), "confidence": self.confidence,
                "evidence": [item.to_mapping() for item in self.evidence], "conflicts": list(self.conflicts),
                "status": self.status, "detected_at": self.detected_at}
