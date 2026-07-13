"""Scope guard with optional adapter path classifications."""
from .path_matcher import classify, match


def check(contract, paths, sensitive_patterns=(), generated_patterns=(), test_patterns=()):
    groups={key:[] for key in ("allowed_changes","conditional_changes","denied_changes","unmatched_changes")}
    names={"allow":"allowed_changes","conditional":"conditional_changes","deny":"denied_changes","unmatched":"unmatched_changes"}
    explicit_deny=tuple(contract["write_scope"]["deny"])
    for path in paths:
        if match(path, explicit_deny) or match(path, sensitive_patterns):
            groups["denied_changes"].append(path)
        elif match(path, generated_patterns):
            continue
        elif match(path, test_patterns):
            groups["conditional_changes"].append(path)
        else:
            groups[names[classify(path,contract["write_scope"]["allow"],explicit_deny)]].append(path)
    return groups