from dataclasses import dataclass
from typing import Mapping, Any

@dataclass(frozen=True)
class TestResult:
    data: Mapping[str, Any]
    @classmethod
    def from_mapping(cls, value): return cls(dict(value))
    def to_mapping(self): return dict(self.data)
