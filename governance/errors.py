"""Typed errors for deterministic governance-runtime input handling."""


class GovernanceError(Exception):
    """Base class for expected, user-actionable governance failures."""


class InputError(GovernanceError):
    """An input path, encoding, or serialization format is invalid."""


class SchemaValidationError(GovernanceError):
    """A mapping does not conform to its governance schema."""
