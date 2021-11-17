import json

with open('backup.json', 'r') as f:
    data = json.load(f)

with open('backup.json', 'w') as f:
    data['age'] += 1
    json.dump(data, f)
