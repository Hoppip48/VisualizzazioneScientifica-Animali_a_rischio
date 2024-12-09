import pandas as pd
import matplotlib.pyplot as plt

# Carica il dataset
data = pd.read_csv("habitats.csv", encoding="latin1", low_memory=False)

# Filtra dataset per habitats
main_habitats = ['Foresta', 'Zone Umide (interne)', 'Marino Neritico', 'Pianura', 
                 'Prateria', 'Artificiale/Terrestre', 'Aree Rocciose']
habitat_counts = data['name'].value_counts()
filtered_habitats = habitat_counts[main_habitats]
other_count = habitat_counts.drop(main_habitats).sum()
filtered_habitats["Altro"] = other_count
habitat_percentages = filtered_habitats / filtered_habitats.sum() * 100
colors = [
    '#005f00', '#4287f5', '#5ed0f3', '#7df35e', 
    '#f3f95e', '#d3d3d3', 
    '#a6622d', '#808080'   
]

# Configura il grafico
fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')
wedges, texts, autotexts = plt.pie(
    habitat_percentages, 
    labels=habitat_percentages.index, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors
)
for text in texts + autotexts:
    text.set_color("white")
plt.gca().set_facecolor('none')

# Mostra il grafico
plt.tight_layout()
plt.show()
