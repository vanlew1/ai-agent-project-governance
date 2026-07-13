from fnmatch import fnmatch
def match(path,patterns): return any(path==p or path.startswith(p.rstrip('/')+'/') or fnmatch(path,p) for p in patterns)
def classify(path,allow,deny):
    if match(path,deny): return 'deny'
    if match(path,allow): return 'allow'
    if path.startswith('tests/') and any('/' in p for p in allow): return 'conditional'
    return 'unmatched'
