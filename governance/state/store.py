from __future__ import annotations
from pathlib import Path
import yaml
from ..schema_loader import load_mapping,validate_mapping
from ..serialization import dump_mapping
from . import layout
from .atomic_writer import write
def init(project_file:Path, force=False):
    if layout.PROJECT.exists() and not force: raise ValueError('state already exists; use --force')
    value=load_mapping(project_file); validate_mapping(value,'project_state.schema.json'); write(layout.PROJECT,dump_mapping(value,'yaml')); write(layout.APPROVALS,'[]\n')
def load_project(): return load_mapping(layout.PROJECT)
def activate(contract_file:Path):
    value=load_mapping(contract_file); validate_mapping(value,'task_contract.schema.json')
    if layout.ACTIVE.exists(): raise ValueError('active task exists; deactivate first')
    write(layout.ACTIVE,dump_mapping(value,'yaml'))
def active(): return load_mapping(layout.ACTIVE)
def deactivate():
    if layout.ACTIVE.exists(): layout.ACTIVE.unlink()


def save_p3(path, value, schema_name):
    validate_mapping(value, schema_name)
    if value.get("task_id") != active().get("task_id"):
        raise ValueError("P3 result task_id does not match active task")
    write(path, dump_mapping(value, "yaml"))

def load_p3(path):
    return load_mapping(path)


def orchestration_path(orchestration_id: str, name: str) -> Path:
    if not orchestration_id or "/" in orchestration_id or "\\" in orchestration_id: raise ValueError("invalid orchestration id")
    return layout.ORCHESTRATION / orchestration_id / name

def save_orchestration(orchestration_id: str, name: str, value, schema_name: str):
    validate_mapping(value, schema_name)
    write(orchestration_path(orchestration_id, name), dump_mapping(value, "yaml"))
