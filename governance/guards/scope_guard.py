from .path_matcher import classify
def check(contract,paths):
    groups={key:[] for key in ('allowed_changes','conditional_changes','denied_changes','unmatched_changes')}
    names={'allow':'allowed_changes','conditional':'conditional_changes','deny':'denied_changes','unmatched':'unmatched_changes'}
    for path in paths: groups[names[classify(path,contract['write_scope']['allow'],contract['write_scope']['deny'])]].append(path)
    return groups
