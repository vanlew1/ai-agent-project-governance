def check(contract,paths):
    text=' '.join(contract.get('objective',[])).casefold()
    bad=any(word in text for word in ('force push','release','production database','delete')) or any('secret' in path or 'data/production/' in path for path in paths)
    return ('BLOCKED' if bad else 'PASS'), (['forbidden operation evidence'] if bad else [])
