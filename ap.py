import streamlit as st
import pandas as pd

st.title("Analyse de Matchs ⚽")

st.write("Exemple d'analyse semi-automatique de matchs.")

# Exemple de données (tu pourras les remplacer par de vraies plus tard)
data = {
    "Équipe A": ["PSG", "Real Madrid", "Bayern Munich"],
    "Équipe B": ["Marseille", "Barcelone", "Dortmund"],
    "Cote moyenne": [1.45, 1.52, 1.49],
    "Probabilité estimée de gain (%)": [78, 73, 69]
}

df = pd.DataFrame(data)
df = df.sort_values(by="Probabilité estimée de gain (%)", ascending=False)

st.dataframe(df)

st.success("Matchs classés du plus sûr au moins sûr ✅")
