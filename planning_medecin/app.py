import streamlit as st
from planning_medecin.lib_hp import Medecin, PeriodeVacance, trouver_emploi_du_temps

st.title("Planification des gardes de médecins")

nb_jours = st.number_input("Nombre total de jours dans la période concernée", min_value=1, value=10, step=1)

nb_medecins = st.number_input("Nombre de médecins", min_value=1, value=5, step=1)
medecins = []
for i in range(int(nb_medecins)):
    with st.expander(f"Information du médecin {i+1}"):
        nom = st.text_input(f"Nom du médecin {i+1}", value=f"Médecin {i+1}")
        disponibilites = st.text_input(f"Jours de disponibilité pour le médecin {i+1} (séparer les jours par une virgule)", value="1,2,3")
        jours_dispos = set(map(int, disponibilites.split(',')))
        medecins.append(Medecin(nom, jours_dispos))

nb_vacances = st.number_input("Nombre de périodes de vacances", min_value=0, value=2, step=1)
vacances = []
for i in range(int(nb_vacances)):
    with st.expander(f"Information sur la période de vacances {i+1}"):
        nom_vacance = st.text_input(f"Nom de la période de vacances {i+1}", value=f"Vacances {i+1}")
        debut_vacance = st.number_input(f"Jour de début pour {nom_vacance}", min_value=1, value=10*(i+1), step=1)
        duree_vacance = st.number_input(f"Durée de {nom_vacance} (en jours)", min_value=1, value=5, step=1)
        vacances.append(PeriodeVacance(nom_vacance, debut_vacance, duree_vacance))

max_gardes = st.number_input("Nombre maximal de gardes par médecin pendant la période", min_value=1, value=5, step=1)

if st.button('Générer le planning'):
    planning = trouver_emploi_du_temps(medecins, vacances, nb_jours, max_gardes)
    st.dataframe(planning)



