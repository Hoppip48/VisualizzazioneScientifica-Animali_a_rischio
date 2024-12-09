import pandas as pd
import matplotlib.pyplot as plt

file_path = "conservation_needed_filtered.csv"
data = pd.read_csv(file_path)
unique_data = data.drop_duplicates(subset='internalTaxonId')

Traduzione
translation_dict = {
    "Site/area protection": "Protezione dell'habitat",
    "Resource & habitat protection": "Protezione delle risorse",
    "Habitat & natural process restoration": "Ripristino dei processi naturali",
    "Invasive/problematic species control": "Gestione delle specie invasive",
    "Awareness & communications": "Consapevolezza e comunicazione",
    "Captive breeding/artificial propagation": "Riproduzione in cattività",
    "Harvest management": "Gestione dell'agricoltura",
}
unique_data['name'] = unique_data['name'].replace(translation_dict)

category_counts = unique_data['name'].value_counts()

top_categories = category_counts.nlargest(7)

Creazione grafico
plt.figure(figsize=(10, 6))
bars = plt.bar(top_categories.index, top_categories.values, color='blue', edgecolor='black')
plt.ylabel('Numero di specie salvaguardate', fontsize=12, color='white')
plt.xticks(rotation=45, fontsize=10, color='white', ha='right')
plt.yticks(fontsize=10, color='white')

Grafico bianco
plt.gca().spines['bottom'].set_color('white')  # Bordo inferiore bianco
plt.gca().spines['left'].set_color('white')    # Bordo sinistro bianco
plt.gca().spines['top'].set_color('white')     # Bordo superiore bianco
plt.gca().spines['right'].set_color('white')   # Bordo destro bianco

Sfondo trasparente
plt.gca().set_facecolor('none')  # Colore di sfondo del grafico
plt.gcf().patch.set_facecolor('none')  # Colore di sfondo dell'intera figura

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=10, color='white')

plt.tight_layout()
plt.savefig("top_7_conservation_chart_translated.png", dpi=300, transparent=True)
plt.show()