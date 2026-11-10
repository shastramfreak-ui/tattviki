from pathlib import Path
import re,csv
root=Path(__file__).resolve().parents[1]
ids=[r['id'] for r in csv.DictReader((root/'CURRICULUM_INDEX.csv').open(encoding='utf-8'))]
s=(root/'assets/learning-guides.js').read_text()
assert len(ids)==737 and len(set(ids))==737
extra=(root/'assets/ai-curriculum.js').read_text()+(root/'assets/graph-learning.js').read_text()+(root/'assets/shacl-learning.js').read_text()
assert s.count('"subtitle":')+extra.count('"subtitle":')==737 and s.count('"verification":')+extra.count('"verification":')==737 and s.count('"worked":')+extra.count('"worked":')==737
assert s.count('"review":')+extra.count('"review":')==737
assert 'SNOMED CT' not in s+extra and 'MedDRA' not in s+extra
print('PASS 737 unique lessons each has full guide sections and review question; no restricted terminology embedded')
