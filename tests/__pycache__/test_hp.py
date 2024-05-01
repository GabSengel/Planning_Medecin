"""
Desccription : Tester les fonctions de lib_hp.py
"""
import re
import pytest
import pandas as pd
from planning_medecin.lib_hp import (
    PeriodeVacance, 
    Medecin, 
    jours_de_gardes,
    trouver_emploi_du_temps,
    dispo_medecin)

def test_init_periode():
    periode = PeriodeVacance(nom="1", debut=30, duree=7)
    assert isinstance(periode, PeriodeVacance)

def test_plantage_periode():
    with pytest.raises(ValueError):
        PeriodeVacance(nom="1", debut=10, duree=-7)
    with pytest.raises(ValueError):
        PeriodeVacance(nom="1", debut=10, duree=float("inf"))
    with pytest.raises(ValueError):
        PeriodeVacance(nom="1", debut=-10, duree=7)
    with pytest.raises(ValueError):
        PeriodeVacance(nom="1", debut=float("inf"), duree=7)
    with pytest.raises(TypeError):
        PeriodeVacance(nom="1", debut="10", duree=7)
    with pytest.raises(TypeError):
        PeriodeVacance(nom="1", debut=10, duree="7")

def test_init_medecin():
    medecin = Medecin(id="Dr.Cardio", disponibilites={2,7,88})
    assert isinstance(medecin,Medecin)

def test_plantage_medecin():
    with pytest.raises(ValueError):
        Medecin(id=1, disponibilites={2, 7, 88})
    with pytest.raises(ValueError):
        Medecin(id=float("inf"), disponibilites={2, 7, 88})
    with pytest.raises(ValueError):
        Medecin(id="1", disponibilites=set())
    with pytest.raises(ValueError):
        Medecin(id="1", disponibilites={-2, 7, 88})
    with pytest.raises(ValueError):
        Medecin(id="1", disponibilites=[2, 7, 88]) 
    with pytest.raises(ValueError):
        Medecin(id="1", disponibilites={"deux", "sept", "quatre-vingt-huit"})
    with pytest.raises(ValueError):
        Medecin(id="1", disponibilites={2.5, 7.1, 88.6})

def test_jours_de_gardes():
    vacances = [PeriodeVacance(nom="Noel",debut=4, duree=2), 
                PeriodeVacance(nom="Ete",debut=8, duree=3)]
    nb_jours= 10
    assert jours_de_gardes(vacances, nb_jours) == {1: '', 2: '', 3: '', 4: 'Noel', 5: 'Noel', 6:'',7:'',8:'Ete',9:'Ete',10:'Ete'}
    assert isinstance(jours_de_gardes(vacances, nb_jours),dict)

def test_plantage_jours_de_gardes():
    with pytest.raises(ValueError):
        vacances= []
        nb_jours = 10
        jours_de_gardes(vacances, nb_jours)
    with pytest.raises(ValueError):
        vacances= [PeriodeVacance(nom="1", debut=1, duree=5)]
        nb_jours = 0
        jours_de_gardes(vacances, nb_jours)
    with pytest.raises(ValueError):
        vacances= [PeriodeVacance(nom="1", debut=1, duree=5)]
        nb_jours = -1
        jours_de_gardes(vacances, nb_jours)
    with pytest.raises(ValueError):
        vacances= [PeriodeVacance(nom="1", debut=1, duree=5)]
        nb_jours = float("inf")
        jours_de_gardes(vacances, nb_jours)
    with pytest.raises(TypeError):
        jours_de_gardes(None)

def test_dispo_medecin():
    dispos =   [Medecin(id="1", disponibilites={3, 5, 6}),
                Medecin(id="2", disponibilites={2, 3, 7}),
                Medecin(id="3", disponibilites={1, 4, 8, 9}),
                Medecin(id="4", disponibilites={1, 2, 7, 10})]
    nb_jours = 10
    assert isinstance(dispo_medecin(dispos, nb_jours),dict)
    assert dispo_medecin(dispos, nb_jours) == {
    1: ["3", "4"],
    2: ["2", "4"],
    3: ["1", "2"],
    4: ["3"],
    5: ["1"],
    6: ["1"],
    7: ["2", "4"],
    8: ["3"],
    9: ["3"],
    10: ["4"]
}

def test_plantage_dispo_medecin():
    with pytest.raises(ValueError, match="La liste des médecins ne peut pas être vide"):
        dispo_medecin([], nb_jours=10)
    with pytest.raises(TypeError):
        dispo_medecin(None, nb_jours=10)
    with pytest.raises(AttributeError):
        dispo_medecin([object()],nb_jours=10)

def test_trouver_edt():
    medecins = [
    Medecin("Dr. MACHECOURT", {1, 2, 3, 4, 8, 9}),
    Medecin("Dr. SENGEL", {1, 2, 4, 5, 6, 7, 10}),
    Medecin("Dr. THEODORE", {2, 3, 5, 6, 7, 8}),
    Medecin("Dr. LECH", {3, 4, 6, 9, 10}),
    Medecin("Dr. VIDAL", {1, 5, 7, 8, 9, 10}),
    ]
    vacances = [PeriodeVacance("Noel", 3, 2), PeriodeVacance("Ete", 8, 2)]
    max_gardes = 3
    nb_jours = 10
    result_df = trouver_emploi_du_temps(medecins, vacances, nb_jours, max_gardes)

    expected_df = {
        "Dr. MACHECOURT": ["X", "-", "-", "-", "-", "-","-","X","-","-"],
        "Dr. SENGEL": ["-", "X", "-", "-", "-", "X","-","-","-","-"],
        "Dr. THEODORE": ["-", "-", "X", "-", "-", "-","X","-","-","-"],
        "Dr. LECH": ["-", "-", "-", "X", "-", "-","-","-","X","-"],
        "Dr. VIDAL": ["-", "-", "-", "-", "X", "-","-","-","-","X"]
    }
    expected_df = pd.DataFrame(expected_df, index=["Jour 1", "Jour 2", "Jour 3 Noel", "Jour 4 Noel", "Jour 5","Jour 6","Jour 7","Jour 8 Ete","Jour 9 Ete","Jour 10"])
    pd.testing.assert_frame_equal(result_df, expected_df)
    assert isinstance(result_df,pd.DataFrame)

def test_couverture_minimale():
    medecins = [Medecin("Dr. VIDAL", {1, 2, 3, 4, 5}),
                Medecin("Dr. SENGEL", {1, 2, 3, 4, 5})]
    vacances = [PeriodeVacance("Noel",1,2), PeriodeVacance("Ete",4,2)]
    max_gardes = 3
    nb_jours = 5
    result_df = trouver_emploi_du_temps(medecins, vacances, nb_jours, max_gardes)

    expected_df = {
        "Dr. VIDAL": ["X", "-", "X", "-", "X"],
        "Dr. SENGEL": ["-", "X", "-", "X", "-"]
    }
    expected_df = pd.DataFrame(expected_df, index=["Jour 1 Noel","Jour 2 Noel","Jour 3","Jour 4 Ete","Jour 5 Ete"])
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_plantage_trouver_edt():
    with pytest.raises(ValueError):
        medecins = [Medecin("Dr. VIDAL", {1, 2, 3, 4, 5, 6})]
        vacances = [PeriodeVacance("Noel", 1, 1), PeriodeVacance("Ete", 4, 2)]
        max_gardes = 6
        nb_jours = 6
        trouver_emploi_du_temps(medecins, vacances, nb_jours,max_gardes)
        assert re.search(r"Nombre de médecins insuffisant pour couvrir la plus longue période de vacances de \d+ jours.", str(excinfo.value))
    with pytest.raises(ValueError) as excinfo:
        medecins = [Medecin("Dr. MACHECOURT", {1,2,3,4}),
                    Medecin("Dr. SENGEL", {5,6})]
        vacances = [PeriodeVacance("Noel", 2, 3), PeriodeVacance("Ete", 8, 2)]
        max_gardes = 3
        nb_jours = 6
        trouver_emploi_du_temps(medecins, vacances,nb_jours, max_gardes)
        assert re.search(r"Aucun médecin disponible pour le jour \d+, impossible de compléter l'emploi du temps.", str(excinfo.value))
    with pytest.raises(ValueError) as excinfo:
        medecins = [Medecin("Dr. MACHECOURT", {1,2,3}),
                    Medecin("Dr. SENGEL", {4,5,6}),
                    Medecin("Dr. THEODORE", {7,8,9})]
        vacances = [PeriodeVacance("Noel", 2, 3), PeriodeVacance("Ete", 6, 2)]
        max_gardes = 4
        nb_jours = 10
        trouver_emploi_du_temps(medecins, vacances,nb_jours, max_gardes)
        assert re.search(r"Aucun médecin disponible pour le jour \d+, impossible de compléter l'emploi du temps.", str(excinfo.value))
    with pytest.raises(ValueError) as excinfo:
        medecins = [Medecin("Dr. VIDAL", {1, 2, 3}),
                    Medecin("Dr. SENGEL", {4, 5, 6})]
        vacances = [PeriodeVacance("Noel", 2, 2)]
        max_gardes = 3
        nb_jours = 6
        emploi_du_temps_df = trouver_emploi_du_temps(medecins, vacances, nb_jours, max_gardes)
        assert re.search(r"Les médecins disponibles pour \d+ ont déjà réalisé leur jours de gardes pour cette période et des jours sont encore sans médecins", str(excinfo.value))
