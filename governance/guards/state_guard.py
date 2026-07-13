from ..state import layout
def check(): return ('OK',[]) if layout.PROJECT.exists() and layout.ACTIVE.exists() else ('BLOCKED_STATE_INVALID',['missing state or active task'])
