import os
import json
import pandas as pd

# =====================================================================
# 1. FUNZIONE UNIVERSALE DI MODELLAZIONE
# =====================================================================
def aggiungi_nodi_al_profilo(profilo, df, dominio, categoria_nome, colonna_valore, colonna_data, colonna_conteggio):
    """
    Trasforma una tabella dati in nodi JSON standardizzati per il profilo utente,
    calcolando l'intensità dell'interesse normalizzata per dominio.
    """
    # Calcolo dei totali per il periodo (per ricavare la percentuale/intensità)
    totali_periodo = df.groupby(colonna_data)[colonna_conteggio].sum().reset_index(name='Totale_Periodo')
    df_unito = pd.merge(df, totali_periodo, on=colonna_data)

    # Calcolo dell'intensità (da 0.0 a 1.0) all'interno del dominio
    df_unito['Intensita'] = (df_unito[colonna_conteggio] / df_unito['Totale_Periodo']).round(2)

    # Creazione e inserimento dei singoli nodi
    for index, row in df_unito.iterrows():
        nodo = {
            "dominio": dominio,
            "categoria": categoria_nome,
            "valore": row[colonna_valore],
            "intensita_interesse": row['Intensita'],
            "finestra_temporale": {
                "tipo_intervallo": "Mensile",
                "valore_intervallo": row[colonna_data]
            },
            "magic_box": {
                "interazioni_totali": int(row[colonna_conteggio])
            }
        }
        profilo["nodi_interesse"].append(nodo)

    return profilo


# =====================================================================
# 2. AVVIO ESPORTAZIONE PROFILI JSON
# =====================================================================
def main():
    print("\n--- AVVIO ESPORTAZIONE MASSIVA PROFILI JSON ---")
    print("Preparazione dei dati globali in corso...")

    # watch_history_pulito e movies_pulito sono tabelle precaricate
    # Uniamo la storia delle visioni pulita con i dati dei film
    visioni_globali = pd.merge(watch_history_pulito, movies_pulito, on='movie_id', how='left')

    # Convertiamo la data in Mese_Anno
    visioni_globali['Data_Ora'] = pd.to_datetime(visioni_globali['watch_date'])
    visioni_globali['Mese_Anno'] = visioni_globali['Data_Ora'].dt.to_period('M').astype(str)

    # Creiamo una cartella dedicata
    cartella_export = "Profili_Utenti_JSON"
    if not os.path.exists(cartella_export):
        os.makedirs(cartella_export)

    # Estraiamo la lista di tutti gli ID utente unici
    lista_utenti = visioni_globali['user_id'].unique()
    totale_utenti = len(lista_utenti)

    print(f"Trovati {totale_utenti} utenti unici. Inizio generazione...\n")

    conteggio_salvati = 0

    for utente_corrente in lista_utenti:
        # Filtriamo i dati solo per questo specifico utente
        dati_utente = visioni_globali[visioni_globali['user_id'] == utente_corrente]

        # Prepariamo le 3 tabelle aggregate
        # 1. Generi (top 4)
        top_generi = dati_utente['genre_primary'].value_counts().head(4).index.tolist()
        dati_generi = dati_utente[dati_utente['genre_primary'].isin(top_generi)]
        evoluzione_generi = dati_generi.groupby(['Mese_Anno', 'genre_primary']).size().reset_index(name='Conteggio')

        # 2. Paesi (top 5)
        top_paesi = dati_utente['country_of_origin'].value_counts().head(5).index.tolist()
        dati_paesi = dati_utente[dati_utente['country_of_origin'].isin(top_paesi)]
        evoluzione_paesi = dati_paesi.groupby(['Mese_Anno', 'country_of_origin']).size().reset_index(name='Conteggio')

        # 3. Formati
        evoluzione_formato = dati_utente.groupby(['Mese_Anno', 'content_type']).size().reset_index(name='Conteggio')

        # Costruiamo il JSON per l'utente
        profilo_corrente = {
            "id_profilo_univoco": utente_corrente,
            "piattaforma_origine": "Netflix_Data_Export",
            "nodi_interesse": []
        }

        # Popoliamo i nodi chiamando la nostra funzione 3 volte
        if not evoluzione_generi.empty:
            profilo_corrente = aggiungi_nodi_al_profilo(profilo_corrente, evoluzione_generi, "Intrattenimento Video", "Genere", "genre_primary", "Mese_Anno", "Conteggio")

        if not evoluzione_paesi.empty:
            profilo_corrente = aggiungi_nodi_al_profilo(profilo_corrente, evoluzione_paesi, "Intrattenimento Video", "Paese di Origine", "country_of_origin", "Mese_Anno", "Conteggio")

        if not evoluzione_formato.empty:
            profilo_corrente = aggiungi_nodi_al_profilo(profilo_corrente, evoluzione_formato, "Intrattenimento Video", "Formato Contenuto", "content_type", "Mese_Anno", "Conteggio")

        # Salviamo il file nella cartella
        json_formattato = json.dumps(profilo_corrente, indent=4, ensure_ascii=False)
        nome_file = os.path.join(cartella_export, f"profilo_{utente_corrente}.json")

        with open(nome_file, 'w', encoding='utf-8') as f:
            f.write(json_formattato)

        conteggio_salvati += 1

        if conteggio_salvati % 500 == 0:
            print(f"Elaborati {conteggio_salvati} / {totale_utenti} utenti...")

    print(f"\n[!] OPERAZIONE COMPLETATA! {conteggio_salvati} profili salvati in '{cartella_export}'.")

if __name__ == "__main__":
    main()
