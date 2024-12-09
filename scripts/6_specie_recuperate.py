import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caricamento del dataset con specifiche di encoding
file_path = 'LPD_2024_public.csv'
data = pd.read_csv(file_path, encoding='latin1', low_memory=False)

# Lista delle specie di interesse (nomi scientifici con underscore)
species_of_interest = [
    "Gorilla_beringei",  # Mountain gorilla
    "Haliaeetus_leucocephalus",  # Bald eagle
    "Oryx_leucoryx",  # Arabian oryx
    "Bison_bison",  # American bison
    "Falco_peregrinus", # Peregrine falcon
    "Rhinoceros_unicornis", # Greater one-horned rhino
    "Eubalaena_glacialis", # North Antlantic right whale
    "Eretmochelys_imbricata" # Hawktuah turtle
]

# Dizionario per mappare i nomi scientifici alle specie in italiano
species_translation = {
    "Gorilla_beringei": "Gorilla \ndi montagna",
    "Haliaeetus_leucocephalus": "Aquila \ndi mare \ntestabianca",
    "Oryx_leucoryx": "Orice \nd'Arabia",
    "Bison_bison": "Bisonte \namericano",
    "Falco_peregrinus": "Falco \npellegrino",
    "Rhinoceros_unicornis": "Rinoceronte \nindiano",
    "Eubalaena_glacialis": "Balena franca \nnordatlantica",
    "Eretmochelys_imbricata": "Tartaruga \nembricata"
}

# Filtrare il dataset per le specie elencate
selected_species_data = data[data['Binomial'].isin(species_of_interest)]

# Riempi righe con tutti valori nulli nelle colonne degli anni
years = [str(year) for year in range(1950, 2021)]
selected_species_data[years] = selected_species_data[years].fillna(method='bfill', axis=1).fillna(method='ffill', axis=1)

# Estrarre i dati di popolazione per il 1950 e il 2020
pop_1950 = selected_species_data[['Binomial', 'Common_name', '1950']].rename(columns={'1950': 'Population_1950'})
pop_2020 = selected_species_data[['Binomial', 'Common_name', '2020']].rename(columns={'2020': 'Population_2020'})

# Unire i dati per creare un confronto tra il 1950 e il 2020
pop_comparison = pop_1950.merge(pop_2020, on='Binomial', how='inner')
pop_comparison['Common_name'] = pop_comparison['Common_name_x'].fillna(pop_comparison['Common_name_y'])
pop_comparison = pop_comparison.drop(columns=['Common_name_x', 'Common_name_y'])
pop_comparison = pop_comparison.drop_duplicates(subset=['Binomial'])
pop_comparison['Common_name'] = pop_comparison['Common_name'].apply(lambda x: x.split('/')[0].strip())
pop_comparison['Common_name'] = pop_comparison['Binomial'].map(species_translation).fillna(pop_comparison['Common_name'])
pop_comparison = pop_comparison.sort_values(by='Population_1950', ascending=False)

# Creazione del grafico a barre
x = np.arange(len(pop_comparison['Binomial']))
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_ylim(0, 3000) 

# Creazione delle barre
ax.bar(x - width/2, pop_comparison['Population_1950'], 0.35, label='1950', color='red')
ax.bar(x + width/2, pop_comparison['Population_2020'], 0.35, label='2020', color='lime')
ax.set_xlabel('Specie', fontsize=12, color='white')  # Etichetta asse X bianca
ax.set_ylabel('Popolazione', fontsize=12, color='white')  # Etichetta asse Y bianca

# Personalizzazione grafico
ax.set_xticks(x)
ax.set_xticklabels([f"{common}" for common in pop_comparison['Common_name']], rotation=45, ha='right', color='white')  
ax.tick_params(axis='y', colors='white')  
for spine in ax.spines.values():
    spine.set_edgecolor('white')
legend = ax.legend(title='Anno', fontsize=12, title_fontsize=14, labelcolor='white', frameon=False)
legend.get_title().set_color('white') 
ax.grid(False)  
fig.patch.set_alpha(0.0)  
ax.set_facecolor('none') 

# Layout compatto
plt.tight_layout()
plt.show()
