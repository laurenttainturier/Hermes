import json

import requests
import yaml

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

with open("dossiers_ids.txt") as dossier_ids_file:
    dossiers_ids = []
    for line in dossier_ids_file.readlines():
        if line[0] != "#":
            dossiers_ids.append(line.split(' ')[-1].replace("\n", ""))
    print(dossiers_ids)


def synchronize_dosiers():
    camunda_config = config['camunda']
    url = camunda_config['url']
    process_def_id = camunda_config['process_def_id']
    r = requests.get(url + camunda_config['show_instances'])

    cam_instance_ids = []
    for cam in r.json():
        if cam['businessKey'] in dossiers_ids:
            cam_instance_ids.append(cam['id'])

    data = {
        "processDefinitionId": process_def_id,
        "instructions": [
            {
                "type": "startTransition",
                "transitionId": "Flow_0dl1008"
            },
            {
                "type": "cancel",
                "activityId": "id_siv_consultation",
                "cancelCurrentActiveActivityInstances": True
            }
        ],
        "processInstanceIds": cam_instance_ids,
        "processInstanceQuery": {
            "processDefinitionId": process_def_id
        },
        "skipCustomListeners": True,
        "annotation": "Move dossiers to remise au domaine"
    }

    r = requests.post(
        url + camunda_config['move_instances'],
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    print("response status:", r.status_code)
    print(r.text)


if __name__ == "__main__":
    synchronize_dosiers()
