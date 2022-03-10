x = [
    ['Marco',30],
    ['Marco',28],
    ['Matteo',30]
]

import json
with open('file.json','w') as f:
    json.dump(x,f)
