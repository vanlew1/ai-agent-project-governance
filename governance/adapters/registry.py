"""Closed adapter registry; it never imports project supplied code."""
from .generic import GenericAdapter
from .node import NodeAdapter
from .python import PythonAdapter
from .wechat_miniprogram import WeChatMiniprogramAdapter

_ADAPTERS = (GenericAdapter(), PythonAdapter(), NodeAdapter(), WeChatMiniprogramAdapter())
_BY_ID = {adapter.adapter_id: adapter for adapter in _ADAPTERS}

def all_adapters(): return _ADAPTERS
def get(adapter_id: str): return _BY_ID.get(adapter_id)
def ids(): return tuple(adapter.adapter_id for adapter in _ADAPTERS)
