import matplotlib.pyplot as plt
import pandas as pd

# Carica i file CSV
file_2013_path = 'ricerca_avanzata 2013.csv'
file_2018_path = 'ricerca_avanzata 2018.csv'

data_2013 = pd.read_csv(file_2013_path)
data_2018 = pd.read_csv(file_2018_path)

# Estrai le colonne relative ai trend
trend_columns_2013 = [col for col in data_2013.columns if "Trend" in col]
trend_columns_2018 = [col for col in data_2018.columns if "Trend" in col]

# "Sciogli" i DataFrame per prepararli al confronto
trends_2013_melted = data_2013[trend_columns_2013].melt(var_name="Zona", value_name="Trend")
trends_2018_melted = data_2018[trend_columns_2018].melt(var_name="Zona", value_name="Trend")

# Sostituisci le etichette dei trend
trend_replacement = {
    "Trend ALP": "Alpina",
    "Trend CON": "Continentale",
    "Trend MED": "Mediterranea",
    "Trend MMED": "Trend MED"
}
trends_2013_melted["Zona"] = trends_2013_melted["Zona"].str.strip().replace(trend_replacement, regex=True)
trends_2018_melted["Zona"] = trends_2018_melted["Zona"].str.strip().replace(trend_replacement, regex=True)

# Aggiungi la colonna dell'anno per il confronto
trends_2013_melted["Anno"] = 2013
trends_2018_melted["Anno"] = 2018

# Unisci i dati per l'analisi dei trend
combined_trends = pd.concat([trends_2013_melted, trends_2018_melted], ignore_index=True)

# Rimuovi le righe con dati mancanti
combined_trends.dropna(subset=["Trend"], inplace=True)

# Raggruppa e prepara i dati aggregati per il grafico
trend_summary = (
    combined_trends.groupby(["Zona", "Trend", "Anno"])
    .size()
    .reset_index(name="Conteggio")
)

# Prepara la tabella pivot per il grafico a barre impilate
pivot_trend_summary = trend_summary.pivot_table(
    index=["Zona", "Anno"],
    columns="Trend",
    values="Conteggio",
    fill_value=0
).reset_index()

# Calcola le percentuali per ciascuna zona
pivot_trend_summary[["Miglioramento", "Stabile", "Peggioramento"]] = pivot_trend_summary[["+", "-", "="]].div(
    pivot_trend_summary[["+", "-", "="]].sum(axis=1), axis=0
) * 100

# Riorganizza i tipi di trend
trend_types = ["Miglioramento", "Stabile", "Peggioramento"]

# Definisci la mappa dei colori per i trend
color_map = {
    "Miglioramento": "green",  # Verde per "aumento"
    "Stabile": "yellow",  # Giallo per "stabile"
    "Peggioramento": "r"  # Rosso per "diminuzione"
}

# Prepara i dati per il grafico
zones = pivot_trend_summary["Zona"].unique()
years = [2013, 2018]
bar_width = 0.35 
spacing = 0.4  
x_indexes = range(len(zones))

# Memorizza le posizioni per le etichette sull'asse X
x_ticks = []
x_labels = []

# Crea un grafico a barre impilate con sfondo trasparente
fig, ax = plt.subplots(figsize=(14, 8))

# Imposta il background trasparente per figura e assi
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

for year_idx, year in enumerate(years):
    year_data = pivot_trend_summary[pivot_trend_summary["Anno"] == year]
    cumulative_bottom = [0] * len(zones)

    # Regola la posizione delle barre per gli anni
    offset = year_idx * spacing

    for trend in trend_types:  # Itera sui trend riorganizzati
        values = year_data[trend].values if trend in year_data else [0] * len(zones)
        bars = ax.bar(
            [x + offset for x in x_indexes],  # Aggiungi offset per posizionare le barre
            values,
            width=bar_width,
            bottom=cumulative_bottom,
            color=color_map.get(trend, 'gray'),  # Colori personalizzati
        )

        # Aggiungi le etichette di percentuale all'interno delle barre
        for bar, value, bottom in zip(bars, values, cumulative_bottom):
            if value > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bottom + value / 2,
                    f'{value:.1f}%',  # Formatta la percentuale
                    ha="center", va="center", color="black", fontsize=10  # Colore del testo
                )

        # Aggiorna la posizione per lo stacking delle barre
        cumulative_bottom = [sum(x) for x in zip(cumulative_bottom, values)]

    # Memorizza le posizioni e le etichette per le zone
    for i, zone in enumerate(zones):
        x_ticks.append(x_indexes[i] + offset)
        x_labels.append(f"{zone}\n{year}")

# Personalizzazione del grafico
ax.set_title("", fontsize=16, color='white')
ax.set_xlabel("Zona e anno dell'osservazione", fontsize=14, color='white')
ax.set_ylabel("Trend di conservazione in percentuale(%)", fontsize=14, color='white')
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45, color='white')
handles = [plt.Line2D([0], [0], color=color_map[trend], lw=6) for trend in trend_types]
legend = ax.legend(handles, trend_types, title="Trend", fontsize=12, title_fontsize=14, loc='upper left', bbox_to_anchor=(1.05, 1), frameon=False, labelcolor='white')
legend.get_title().set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(False)
plt.tight_layout()

# Mostra il grafico con sfondo trasparente
plt.show()
