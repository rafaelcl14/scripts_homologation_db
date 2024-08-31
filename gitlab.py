import requests
import json

url = 'https://gitlab.com/api/v4/projects'

privatetoken = 'glpat-swd1LHMtYPx9gchzNitr'

page = 1

per_page = 100

projects = []

while True:
    r = requests.get(url, params={'private_token': privatetoken, 'page':page, 'per_page': per_page})
    if r.status_code == 200:
        projects.extend(r.json())
        if len(r.json()) < per_page:
            break
        page += 1
    else:
        break


while open('projects.json', 'w'):
    json.dump(projects)

print(projects)

