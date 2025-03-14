# Challenge IA M2 SISE

## 📋 Description

Application d'analyse et d'optimisation de CV utilisant l'intelligence artificielle pour améliorer l'adéquation avec les offres d'emploi.
[Lien vers l'application en ligne](https://adjaro-challenge-ia-m2-sise-appapp-fcj59w.streamlit.app/)

## 🚀 Fonctionnalités

- Lecture et analyse de CV au format PDF
- Analyse des offres d'emploi
- Calcul de similarité entre CV et offres
- Génération de lettres de motivation/CV personnalisées
- Suivi de l'impact environnemental des requêtes IA

## 🛠 Technologies Utilisées

- **IA et ML**:
  - Mistral AI (API)
  - Sentence Transformers pour les embeddings via l'API HuggingFace
  - scikit-learn pour la similarité cosinus
- **Interface**: Streamlit
- **Traitement de Documents**:
  - PyPDF2
  - python-docx
  - BeautifulSoup pour le scrapping de FranceTravail
- **Monitoring**: Suivi écologique des requêtes IA

## 📦 Installation

### Prérequis

- Python 3.8+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration

1. Créer un fichier `.env` à la racine du projet
2. Ajouter les clés API :

```env
MISTRAL_API_KEY=votre_clé_mistral
HF_TOKEN=votre_token_huggingface
```

## 🚀 Démarrage

```bash
streamlit run app/app.py
```

## 📂 Structure du Projet

```
challenge_ia_m2_sise/
├── app/
│   ├── app.py              # Point d'entrée de l'application
│   ├── components.py       # Composants Streamlit
│   └── utils/
│       └── ia.py          # Fonctions IA
├── ia/
│   ├── monitoring_ecologie.py  # Suivi impact environnemental
│   └── read_cv.ipynb      # Notebook de développement
└── requirements.txt
```

## 🌍 Impact Environnemental

L'application intègre un suivi de l'impact environnemental :

- Consommation d'énergie par requête
- Émissions de CO2 équivalent

## 🤝 Contribution

- Fork du projet
- Créer une branche (`git checkout -b feature/AmazingFeature`)
- Commit (`git commit -m 'Add AmazingFeature'`)
- Push (`git push origin feature/AmazingFeature`)
- Ouvrir une Pull Request

## 📝 License

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
