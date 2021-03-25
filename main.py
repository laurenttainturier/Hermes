import datetime
import json
import os
import time
import uuid

import requests
import yaml

from build_update_siv_info_event_content import build_update_siv_info_event
from connect_to_db import connect_to_db
from build_create_dossier_event_content import build_create_dossier_event

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

dossiers_ids = {}


def get_current_time():
    return datetime.datetime.now().isoformat()[:-3] + 'Z'


@connect_to_db(config["fourriere-refentiels"])
def get_id_from_id_correlation(con, table: str, id_correlation: str) -> str:
    cursor = con.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE id_correlation='{id_correlation}' AND valid")
    return cursor.fetchone()


@connect_to_db(config["fourriere-refentiels"])
def get_id_from_libelle(con, table: str, libelle: str):
    cursor = con.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE libelle='{libelle}'")
    result = cursor.fetchone()
    if result and len(result) > 0:
        return result[0]

    return None


@connect_to_db(config['fourriere-dossiers'])
def insert_fourriere_in_cache(con, id_corretion_fourriere):
    cursor = con.cursor()
    cursor.execute(
        f"INSERT INTO cache_ref_fourriere (id_correlation) VALUES ('{id_corretion_fourriere}') ON CONFLICT DO NOTHING ")
    con.commit()


@connect_to_db(config["fourriere-dossiers"])
def create_dossier(
        con,
        id,
        immatriculation,
        id_correlation_fourriere,
        id_correlation_autorite_fourriere,
        id_correlation_unite_fo
):
    with open('create_dossier.sql', 'r', encoding='utf-8') as create_dossier_file:
        create_dossier_raw_request = create_dossier_file.read()

    create_dossier_request = eval(f'f"""{create_dossier_raw_request}"""')
    print(create_dossier_request)

    cursor = con.cursor()
    cursor.execute(create_dossier_request)
    con.commit()


@connect_to_db(config["fourriere-dossiers"])
def add_dossier_event(con, dossier_id, content, type):
    with open('create_dossier_event.sql', 'r', encoding='utf-8') as create_dossier_event_file:
        create_dossier_event_raw_request = create_dossier_event_file.read()

    id = uuid.uuid4()
    now = get_current_time()
    create_dossier_request = eval(f'f"""{create_dossier_event_raw_request}"""')
    print(create_dossier_request)

    cursor = con.cursor()
    cursor.execute(create_dossier_request)
    con.commit()


def build_dossier_and_create(dossier):
    marque_id = get_id_from_libelle("marque", dossier["marque"])
    modele_id = get_id_from_libelle("modele", dossier["modele"])
    energie = get_id_from_libelle("energie", dossier["energie"])
    genre_simplifie_id = get_id_from_libelle("genre_simplifie", dossier['genre_simplifie'])

    insert_fourriere_in_cache(dossier['id_correlation_fourriere'])

    id = uuid.uuid4()
    create_dossier(
        id=id,
        immatriculation=dossier["immatriculation"],
        id_correlation_fourriere=dossier["id_correlation_fourriere"],
        id_correlation_autorite_fourriere=dossier["id_correlation_autorite_fourriere"],
        id_correlation_unite_fo=dossier["id_correlation_unite_fo"]
    )

    now = get_current_time()

    create_dossier_event_content = build_create_dossier_event(
        marque_id=marque_id,
        marque=dossier["marque"],
        modele_id=modele_id,
        modele=dossier["modele"],
        genre_simplifie_id=genre_simplifie_id,
        vin=dossier["vin"],
        immatriculation=dossier["immatriculation"],
        now=now,
        id_correlation_fourriere=dossier["id_correlation_fourriere"],
        id_correlation_autorite_fourriere=dossier["id_correlation_autorite_fourriere"],
        id_correlation_unite_fo=dossier["id_correlation_unite_fo"]
    )

    add_dossier_event(dossier_id=id, content=create_dossier_event_content, type="V1_CREATE_EVENT")

    update_siv_info_event_content = build_update_siv_info_event(
        marque_id=marque_id,
        modele_id=modele_id,
        code_genre=dossier["code_genre"],
        carrosserie=dossier["carrosserie"],
        vin=dossier["vin"],
        immatriculation=dossier["immatriculation"],
        cnit=dossier["cnit"],
        date_circulation=now,
        energie_id=energie,
        nb_place=dossier["nb_place"],
        puissance_fiscale=dossier["puissance_fiscale"],
        now=now
    )

    add_dossier_event(dossier_id=id, content=update_siv_info_event_content, type="V2_UPDATE_SIV_INFORMATION_EVENT")

    update_classement_event = json.dumps({
        "class": "V1UpdateClassementAutoEvent",
        "classement": "ALIENATION",
        "dateMiseAJour": get_current_time()
    })
    add_dossier_event(dossier_id=id, content=update_classement_event, type="V1_UPDATE_CLASSEMENT_AUTO_EVENT")

    pre_abandon_event = json.dumps({
        "class": "V1PreAbandonEvent",
        "dateMiseAJour": "2021-03-15T13:54:32.955835Z",
        "decisionAbandon": "2021-03-15T15:04:00Z"
    })
    add_dossier_event(dossier_id=id, content=pre_abandon_event, type="V1_PRE_ABANDON_EVENT")

    abandon_event = json.dumps({"class": "V1AbandonEvent", "dateMiseAJour": get_current_time()})
    add_dossier_event(dossier_id=id, content=abandon_event, type="V1_ABANDON_EVENT")

    dossiers_ids[dossier['immatriculation']] = str(id)


def create_all_dossiers():
    directory = 'dossiers'
    dossier_files = os.listdir(path=directory)
    for dossier_file in dossier_files:
        print("## Creating dossier from:", dossier_file)

        dossier = extract_dossier_from_file(f"{directory}/{dossier_file}")

        build_dossier_and_create(dossier)


def create_dossiers_from_template():
    dossier = extract_dossier_from_file('remise_en_masse/dossier_template.env')

    for i in range(1, 41):
        dossier['immatriculation'] = f"RM-0{str(i).zfill(2)}-DM"
        build_dossier_and_create(dossier)


def extract_dossier_from_file(file):
    dossier = {}
    with open(file, 'r') as dossier_content:
        for line in dossier_content.readlines():
            key, value = line \
                .replace("\"", "") \
                .replace("'", "") \
                .replace("\n", "") \
                .split("=")
            dossier[key] = value

    return dossier


def synchronize_dosiers():
    camunda_config = config['camunda']
    url = camunda_config['url']
    process_def_id = camunda_config['process_def_id']
    r = requests.get(url + camunda_config['show_instances'])

    cam_instance_ids = []
    for cam in r.json():
        if cam['businessKey'] in dossiers_ids.values():
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
                "activityId": "id_pre_siv",
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
    create_all_dossiers()
    create_dossiers_from_template()

    print("## dossiers ids")
    for key, id in dossiers_ids.items():
        print(key, id)

    print("\n## waiting for some time to ensure synchronization")
    time.sleep(30)
    synchronize_dosiers()
