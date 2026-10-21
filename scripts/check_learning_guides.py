from pathlib import Path
import re,csv
root=Path(__file__).resolve().parents[1]
ids=[r['id'] for r in csv.DictReader((root/'CURRICULUM_INDEX.csv').open(encoding='utf-8'))]
s=(root/'assets/learning-guides.js').read_text()
assert len(ids)==613 and len(set(ids))==613
assert s.count('"subtitle":')==613 and s.count('"verification":')==613 and s.count('"worked":')==613
assert s.count('"review":')==613
assert 'SNOMED CT' not in s and 'MedDRA' not in s
print('PASS 613 unique lessons each has full guide sections and review question; no restricted terminology embedded')
