import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('LPD_2024_public.csv', encoding='latin1', low_memory=False)
sns.set_context("talk")

class_name_map = {
    'Mammalia': 'Mammiferi',
    'Aves': 'Uccelli',
    'Reptilia': 'Rettili',
    'Amphibia': 'Anfibi',
}

# Funzione per calcolare il numero di specie ogni anno
def plot_class_species_count(class_name, class_data, class_name_ita):
    years = [str(year) for year in range(1970, 2021)]
    # Calcola il numero di specie per ogni anno
    species_count_per_year = class_data[years].apply(lambda x: x.notnull().sum(), axis=0)
    # Riempire i valori nulli
    species_count_filled = species_count_per_year.fillna(method='bfill')
    species_count_filled = species_count_filled.fillna(method='ffill')
    # Inserisci nel grafico
    plt.plot(years, species_count_filled, label=class_name_ita, linewidth=2)

plt.figure(figsize=(12, 9)) 

# Calcolo del trend per ogni classe 
for class_name in class_name_map.keys():
    class_data = data[data['Class'] == class_name]
    plot_class_species_count(class_name, class_data, class_name_map[class_name])

# Personalizzazione del grafico
plt.xlabel('Anno', fontsize=14, color='white')
plt.ylabel('Numero di specie in pericolo', fontsize=14, color='white')
plt.xticks([str(year) for year in range(1970, 2021, 10)], fontsize=12, color='white', rotation=45)
plt.yticks(fontsize=12, color='white')
plt.tick_params(axis='both', colors='white')  
plt.gca().set_facecolor('none')  
plt.gcf().patch.set_alpha(0)  
ax = plt.gca()  
for spine in ax.spines.values():
    spine.set_edgecolor('white')  
    spine.set_linewidth(1.5)  
legend = plt.legend(title='Classi', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=12, title_fontsize=14, frameon=False, labelcolor='white')
legend.get_title().set_color('white')  
plt.subplots_adjust(right=0.78, bottom=0.2)

# Mostra il grafico
plt.show()
