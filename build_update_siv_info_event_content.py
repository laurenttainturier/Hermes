import json


def build_update_siv_info_event(
        marque_id,
        modele_id,
        code_genre,
        carrosserie,
        vin,
        immatriculation,
        cnit,
        date_circulation,
        energie_id,
        nb_place,
        puissance_fiscale,
        now
):
    raw_body = {
        "class": "V2UpdateSivInformationEvent",
        "dateMiseAJour": now,
        "sivInformation": {
            "vehicule": {
                "descriptionVehicule": {
                    "marque": {
                        "id": marque_id,
                        "libelle": "FORD",
                        "categorie": None
                    } if marque_id else None,
                    "modele": {
                        "id": modele_id,
                        "libelle": "GALAXY",
                        "marqueId": "80fdac43-1ed1-4a85-b7a8-8e48315df602"
                    } if modele_id else None,
                    "couleur": None,
                    "energie": {
                        "id": energie_id,
                        "code": "ES",
                        "libelle": "Essence",
                        "libelleCourt": "Essence"
                    } if energie_id else None,
                    "codeGenre": code_genre,
                    "puissanceCv": puissance_fiscale,
                    "typeVariante": cnit,
                    "placesAssises": nb_place if nb_place else None,
                    "codeCarrosserieCe": carrosserie,
                    "codeCarrosserieNational": "CI"
                },
                "dateControleTechnique": None,
                "identificationVehicule": {
                    "vin": vin,
                    "cnit": "MFD1496A3128",
                    "numeroImmatriculation": immatriculation,
                    "datePremiereImmatriculation": date_circulation
                }
            },
            "documents": [],
            "personnesRattachees": [],
            "situationAdministrative": {
                "flags": {
                    "dvs": "False",
                    "ove": "False",
                    "pve": "False",
                    "gage": "False",
                    "otci": "False",
                    "suspendu": "true",
                    "vehiculeVole": "False"
                },
                "gages": [],
                "declarationPve": None,
                "dateDestruction": None
            }
        }
    }

    return json.dumps(raw_body)
