from typing import List, Dict

def clean_texts(texts: List[str]) -> List[str]:
    return [t.strip() for t in texts if t and t.strip()]

def normalize_scores(items: List[Dict], key: str) -> List[Dict]:
    if not items:
        return items
    vals = [abs(float(i.get(key, 0))) for i in items]
    m = max(vals) or 1
    for i in items:
        i[key] = float(i.get(key, 0)) / m
    return items
