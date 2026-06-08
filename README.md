# Analisi e Profilazione Utenti: Dashboard Interattiva

Questo repository contiene l'intero applicativo sviluppato per l'estrazione, l'elaborazione e la visualizzazione di pattern di interesse a partire da un dataset di visioni Netflix. Il progetto ha l'obiettivo di generalizzare la descrizione degli interessi dei vari utenti, proponendo un formato architetturale standard per questa finalità.

## 🎯 Obiettivo del Progetto
L'obiettivo è trasformare i log di visione storici degli utenti in "profili di interesse" strutturati in formato JSON. Il sistema calcola l'intensità dell'interesse normalizzata per categoria, permettendo di individuare sia le preferenze del singolo utente (Analisi Micro) sia di estrarre molteplici utenti in base a specifici target (Analisi Macro).

## 🗂️ Struttura del Repository

* **`generazione_profili.py`**: Uno script Python basato su Pandas che si occupa del Data Preprocessing. Raggruppa le interazioni, calcola le metriche di intensità e genera massivamente i file JSON standardizzati a nodi.
* **`app.py`**: Il front-end di analisi. Una dashboard sviluppata in Streamlit che indicizza i file JSON in memoria e offre due strumenti:
  1. **Esplorazione Singolo Utente**: Visualizzazione delle metriche storiche e grafici temporali degli interessi principali.
  2. **Ricerca Avanzata Target**: Motore di ricerca globale con filtri per categoria, interesse, volume di interazioni e range temporale, con algoritmi di raggruppamento per l'estrazione di più utenti in formato CSV.

## 🛠️ Tecnologie Utilizzate
* **Linguaggio**: Python
* **Elaborazione Dati**: Pandas
* **Data Visualization & UI**: Streamlit
* **Gestione Dati**: JSON, CSV

## 🚀 Come avviare la Dashboard
1. Assicurarsi di aver attivato il proprio ambiente virtuale.
2. Installare le dipendenze necessarie (Streamlit, Pandas).
3. Lanciare l'applicazione da terminale con il comando:
   `streamlit run app.py`
