import json


def build_create_dossier_event(
        marque_id,
        marque,
        modele_id,
        modele,
        genre_simplifie_id,
        now,
        vin,
        immatriculation,
        id_correlation_fourriere,
        id_correlation_autorite_fourriere,
        id_correlation_unite_fo,
):
    raw_body = {
        "class": "V1CreateEvent",
        "dateMiseAJour": "2021-03-15T14:00:19.292716Z",
        "ficheVehicule": {
            "vin": vin,
            "etat": {
                "id": "a275d415-88bd-44ab-85f9-fd876825f408",
                "etat": "BON_ETAT",
                "detail": None,
                "libelleCourt": None,
                "idCorrelation": "6a716316-abb6-42e1-94d4-e2922582aaec"
            },
            "genre": {
                "id": genre_simplifie_id,
                "dicem": False,
                "libelle": "VP"
            } if genre_simplifie_id else None,
            "marque": {
                "id": marque_id,
                "libelle": marque,
                "categorie": "Premium"
            } if marque_id else None,
            "modele": {
                "id": modele_id,
                "libelle": modele,
                "marqueId": "b3d213ea-6cb2-4bdf-8c0f-3566e780502c"
            } if modele_id else None,
            "numero": immatriculation,
            "portes": True,
            "coffres": True,
            "couleur": "ROUGE CLAIR",
            "sansPlaque": None,
            "observations": None,
            "paysEtranger": None,
            "nombreAntennes": None,
            "objetsVisibles": None,
            "posteCbVisible": None,
            "autoRadioVisible": None,
            "telephonePortable": None,
            "marqueNonReference": False,
            "modeleNonReference": False
        },
        "ficheFourriere": {
            "dateEntree": now,
            "dateEnlevement": now,
            "idCorrelationFourriere": id_correlation_fourriere
        },
        "ficheInfraction": {
            "nuit": None,
            "nigend": None,
            "motifMef": {
                "id": "ad52f8b0-8e8b-4ec9-a417-94a54ee845d4",
                "nature": "Procédure de droit commun – garanties de paiement",
                "motifMef": "Absence de paiement amende par conducteur non domicilié en France (L. 121-4-1) – droit commun",
                "brancheDto": {
                    "id": "99a823d6-4dbe-4be1-91b5-762c0a4e020c",
                    "nature": "Droit commun",
                    "branche": "NORMALE",
                    "idCorrelation": "7123d1b4-4b89-4a37-81c1-95d1e900418e"
                },
                "idCorrelation": "4c1aaec4-1131-4158-ad6d-75dec3f94e77",
                "natureLibelleCourt": "Droit commun"
            },
            "nomAgent": "Bob",
            "lieuPrive": False,
            "emailUnite": None,
            "pluieOuNeige": None,
            "dateRedaction": None,
            "lieuEnlevement": "Bourg-en-Bresse",
            "dateConstatation": "2021-03-10T14:18:22Z",
            "communeEnlevement": "Bourg-en-Bresse (01000)",
            "idCorrelationUniteFO": id_correlation_unite_fo,
            "nomAutoriteMainlevee": None,
            "nomAutoritePrescriptrice": "Bob",
            "qualiteAutoritePrescriptrice": "APJA",
            "idCorrelationAutoriteFourriere": id_correlation_autorite_fourriere
        }
    }

    return json.dumps(raw_body)
