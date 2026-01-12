# Gen_AI

Application Streamlit de recommandation litteraire basee sur un questionnaire et une analyse semantique.

## Fonctionnement

1) Questionnaire
- L'utilisateur renseigne des preferences libres et guidees (genre, periode, themes).
- Les reponses sont sauvegardees en JSON dans `app/data/user_responses/`.

2) Preparation des donnees
- Le referentiel `books_reference.csv` est charge et normalise.
- L'annee de publication est extraite si possible et une periode est deduite.
- Des mots-cles sont derives a partir du titre, auteur, genres et resume.

3) Matching semantique
- Les reponses sont concatenees en segments textuels.
- Embeddings: SBERT (`all-MiniLM-L6-v2`) si dispo, sinon TF-IDF.
- Similarite cosinus entre chaque segment et chaque livre.

4) Scoring & personnalisation
- Score base = moyenne des similarites par livre.
- Bonus/malus fort selon les preferences explicites (genre, periode, auteur favori, themes, eviter).
- Classement final par score decroissant.

5) Resultats
- Tableau des livres recommandes + graphiques (scores, genres, annees).
- Carte de similarite pour visualiser la correspondance.
- Synthese GenAI via Gemini (1 clic, cache local).

## Demarrage

Etapes Windows (PowerShell):

1) Creer et activer le venv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Installer les dependances
```powershell
pip install -r requirements.txt
```

3) Definir la cle API Gemini (optionnel)
- Cree un fichier `.env` a la racine:
```
GEMINI_API_KEY=ta_cle
```

4) Lancer l'app
```powershell
streamlit run app\main.py
```

Alternative:
```powershell
python tasks.py run
```

## GenAI (Gemini)

Definis la variable d'environnement `GEMINI_API_KEY` pour activer la synthese.

## Commandes utiles

```bash
python tasks.py run
python tasks.py build-books
python tasks.py check-ref
python tasks.py test
```

## Structure

- `app/main.py`: entree Streamlit
- `app/pages`: pages Questionnaire, Resultats, Referentiel
- `app/nlp`: embeddings, similarite, pipeline
- `app/domain`: scoring et recommendation
- `app/data/referential`: `questions.json` + `books_reference.csv`

## GenAI (Gemini)

La synthese est generee via Gemini sur demande et mise en cache.
Definis `GEMINI_API_KEY` dans `.env` pour activer la fonctionnalite.
