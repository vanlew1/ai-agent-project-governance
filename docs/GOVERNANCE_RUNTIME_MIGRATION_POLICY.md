# Governance Runtime Migration Policy

Schema version `1.0` is additive during the P0?P5 baseline: existing required fields, enum values, and strict extra-field rejection remain stable. Changes require a fixture-backed compatibility check and an explicit migration plan. Runtime phase advances only when the local release gate passes; P5 keeps multi-agent behavior disabled.


## V1 Close

Version 1.0.0 preserves prior schemas and phase enum values. Migration remains additive; external projects may adopt the runtime without enabling remote Agents, Git writes, or production access.
