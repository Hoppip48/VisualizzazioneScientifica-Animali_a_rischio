import pandas as pd
import matplotlib.pyplot as plt
import re

def estrai_data_solo(data_str):
    """
    Estrae la data (YYYY-MM-DD) da una stringa datetime.
    """
    if isinstance(data_str, str):  
        match = re.match(r'\d{4}-\d{2}-\d{2}', data_str)
        if match:
            return match.group(0)  
    return None 

def grafico_avvistamenti(file_paths, etichette):
    """
    Crea un grafico degli avvistamenti nel tempo per ciascuna fonte.
    """
    dataframes = []

    for file_path, etichetta in zip(file_paths, etichette):
        data = pd.read_csv(file_path)

        if 'created_at' in data.columns:
            data['data'] = data['created_at'].apply(estrai_data_solo)
            data['data'] = pd.to_datetime(data['data'], format='%Y-%m-%d', errors='coerce')
            righe_non_valide = data[data['data'].isna()]['created_at']
            if not righe_non_valide.empty:
                print(f"Righe con date non valide in {file_path}:\n{righe_non_valide}")
        else:
            raise KeyError(f"La colonna 'created_at' non è presente in {file_path}")

        data = data.dropna(subset=['data'])
        data['fonte'] = etichetta
        dataframes.append(data)

    dati_combinati = pd.concat(dataframes, ignore_index=True)
    dati_combinati['anno'] = dati_combinati['data'].dt.year
    dati_combinati = dati_combinati[dati_combinati['anno'] >= 2015]
    dati_aggregati = dati_combinati.groupby(['anno', 'fonte']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6), facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('none')
    for spine in ax.spines.values():
        spine.set_visible(False)

    for fonte in dati_aggregati.columns:
        plt.plot(dati_aggregati.index, dati_aggregati[fonte], label=fonte)

    plt.title("", fontsize=16, color='white')
    plt.xlabel("Anno", fontsize=12, color='white')
    plt.ylabel("Avvistamenti", fontsize=12, color='white')
    legenda = plt.legend(
        title="Specie a rischio",
        fontsize=10,
        title_fontsize=12,
        labelcolor='white',
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        frameon=False
    )
    legenda.get_title().set_color('white')
    plt.grid(alpha=0.5, color='white')
    plt.tick_params(axis='both', colors='white')
    plt.tight_layout()
    plt.show()

file_paths = [
    "observations-510092.csv",
    "observations-510078.csv",
    "observations-510121.csv",
    "observations-510068.csv"
]
etichette_file = ["Cervo volante", "Rospo comune", "Lucciola", "Salamandra"]

grafico_avvistamenti(file_paths, etichette_file)
