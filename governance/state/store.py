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
