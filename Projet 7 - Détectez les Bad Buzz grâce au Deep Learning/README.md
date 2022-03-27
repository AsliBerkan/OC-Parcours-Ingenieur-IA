# OC - Parcours Ingénieur IA - Projet 7 - BERKAN Asli Ceren

## Résumé du projet
Air Paradis souhaite avoir un prototype d'un produit IA permettant de présire le sentiment associé à un tweet, dans le but de détecter les Bad Buzz. Plusieurs approches sont testés :
- API sur étagère : utilisation de l'API du service cognitif proposé par Microsoft Azure pour l'analyse de sentiment
- Modèle sur-mesure simple : utilisation du service Azure Machine Learning Studio (classic)
- Modèle sur-mesure avancé : utilisation du service Azure Machine Learning pour développer un modèle basé sur les réseaux de neurones profonds (plusieurs modèles sont testés) :
    * Un modèle Keras de base avec embedding
    * Un modèle Keras avec embedding et couche LSTM
    * Un modèle BERT

## Le jeu de données
Sentiment140 dataset with 1.6 million tweets :
https://www.kaggle.com/datasets/kazanova/sentiment140

## Les compétences acquises
- Entraîner un modèle Deep Learning sur des données textuelles
- Évaluer la performance d’un modèle de Deep Learning sur des données textuelles
- Choisir la méthode de plongement de mots pertinente pour un modèle de Deep Learning
- Sélectionner les méthodes de prétraitement du texte pour un modèle de Deep Learning

## Mot-clés
- Prétraitement (lemmatization, stemming), prolongement de mots / word embeddings (word2vec, glove), Keras, LSTM, BERT 