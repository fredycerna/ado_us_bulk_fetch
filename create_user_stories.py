import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Cargar configuración
with open('settings.json', 'r') as config_file:
    config = json.load(config_file)

organization = config['organization']
project = config['project']
pat = config['personal_access_token']
api_version = config.get('api_version', '7.0')

# URL base
url_base = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User%20Story?api-version={api_version}"

# Autenticación
auth = HTTPBasicAuth('', pat)

# Headers necesarios
headers = {
    "Content-Type": "application/json-patch+json"
}

# Función para crear una User Story
def create_user_story(title, description, feature_id, acceptance_criteria):
    body = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        }
    ]

    if description:
        body.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        })

    if acceptance_criteria:
        body.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
            "value": acceptance_criteria
        })

    if feature_id:
        body.append({
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"https://dev.azure.com/{organization}/_apis/wit/workItems/{feature_id}",
                "attributes": {
                    "comment": "Linking User Story to Feature"
                }
            }
        })
    
    response = requests.post(url_base, 
                              auth=auth, 
                              headers=headers, 
                              data=json.dumps(body))
    
    if response.status_code in [200, 201]:
        print(f"✅ User Story creada: {title} (FeatureID: {feature_id})")
    else:
        print(f"❌ Error creando {title}: {response.status_code} - {response.text}")

# Leer y procesar CSV
def process_csv(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        created = 0
        for row in reader:
            title = row['Title'].strip()
            description = row.get('Description', '').strip()
            feature_id = row.get('FeatureID', '').strip()
            acceptance_criteria = row.get('AcceptanceCriteria', '').strip()

            if not title or not feature_id:
                print(f"⚠️  Skipping row with missing Title or FeatureID: {row}")
                continue

            create_user_story(title, description, feature_id, acceptance_criteria)
            created += 1
    print(f"\n🎯 {created} User Stories creadas exitosamente.")

# Ejecutar
if __name__ == "__main__":
    process_csv('test.csv')
