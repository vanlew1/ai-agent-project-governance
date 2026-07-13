AUTO={'test_failed','compile_failed','lint_failed','import_failed','fixture_missing','mock_missing','path_location_changed','first_attempt_failed','local_compatibility_issue'}
HUMAN={'new_permission_required','production_write_required','irreversible_operation_required','secret_required','material_requirement_conflict','scope_expansion_required','core_architecture_change_required'}
def classify(code): return 'AUTONOMOUS_ENGINEERING' if code in AUTO else 'HUMAN_CHECKPOINT' if code in HUMAN else 'UNKNOWN'
