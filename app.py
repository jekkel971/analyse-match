import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse Matchs 1.5", page_icon="⚽", layout="centered")

st.title("⚽ Analyse semi-automatique des matchs avec cote ~1.5")
st.write("Colle ci-dessous tes matchs avec leurs cotes et forme récente (1 = victoire, 0 = défaite).")

# Exemple de format
st.code("""
PSG, Reims, 1.45, 1,1,1,1,0
Real Madrid, Valence, 1.55, 1,0,1,1,1
Chelsea, Brighton, 1.60, 0,1,1,0,1
Bayern, Leipzig, 1.50, 1,1,1,1,1
""", language="text")

# Entrée utilisateur
text_input = st.text_area("Entre tes matchs ici :", height=200)

if st.button("Analyser les matchs ⚡"):
    if not text_input.strip():
        st.warning("👉 Ajoute d'abord des matchs avant d'analyser.")
    else:
        # Transformation du texte en données
        lignes = [l.strip() for l in text_input.strip().splitlines() if l.strip()]
        matchs = []
        for ligne in lignes:
            try:
                parts = [p.strip() for p in ligne.split(",")]
                equipe, adversaire = parts[0], parts[1]
                cote = float(parts[2])
                forme = list(map(int, parts[3:]))
                matchs.append({"Equipe": equipe, "Adversaire": adversaire, "Cote": cote, "Forme": forme})
            except Exception as e:
                st.error(f"Erreur sur la ligne : {ligne} ({e})")

        if matchs:
            # Calcul des scores
            for match in matchs:
                forme_score = sum(match["Forme"]) / len(match["Forme"])
                proba_estimee = forme_score * (2 - (match["Cote"] / 2))
                match["Forme_moyenne"] = round(forme_score, 2)
                match["Probabilité_estimee"] = round(proba_estimee * 100, 1)
                match["Note_confiance"] = round(match["Probabilité_estimee"] / match["Cote"], 1)
                match["Recommandation"] = "✅ Oui" if match["Probabilité_estimee"] >= 75 else "❌ Non"

            df = pd.DataFrame(matchs)
            df = df.sort_values(by="Note_confiance", ascending=False)
            df["Classement"] = range(1, len(df) + 1)

            st.success("✅ Analyse terminée ! Voici le classement :")
            st.dataframe(df[["Classement", "Equipe", "Adversaire", "Cote", "Forme_moyenne", "Probabilité_estimee", "Note_confiance", "Recommandation"]],
                         use_container_width=True)

            st.download_button(
                "📥 Télécharger les résultats en CSV",
                df.to_csv(index=False).encode("utf-8"),
                "classement_matchs.csv",
                "text/csv"
            )
