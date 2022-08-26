# docker build  --network=host -t testfnd .

import requests
res = requests.get('http://localhost:5000/new')
print(res.text)