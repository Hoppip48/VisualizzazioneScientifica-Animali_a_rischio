import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("tassi.csv", encoding="latin1", low_memory=False)
data_sorted = data.sort_values(by="Tasso di Variazione (%)", ascending=True)

# Creare una mappa di colori per i tassi di variazione
colors = ['lime' if tasso >= 0 else 'red' for tasso in data_sorted['Tasso di Variazione (%)']]

# Creazione del grafico a barre orizzontali
plt.figure(figsize=(12, 8))
bars = plt.barh(data_sorted['Gruppo Animale'], data_sorted['Tasso di Variazione (%)'], 
                color=colors, edgecolor='black')  # Bordo bianco per le barre

# Personalizzazione del grafico
plt.title('Variazione delle Popolazioni Animali negli Ultimi 50 Anni', fontsize=14, color='white')
plt.xlabel('Tasso di Variazione (%)', fontsize=12, color='white')  
plt.ylabel('Gruppo Animale', fontsize=12, color='white') 
plt.xticks(color='white')  
plt.yticks(color='white')  
plt.gca().spines['bottom'].set_color('white')  
plt.gca().spines['left'].set_color('white')    
plt.gca().spines['top'].set_color('white')     
plt.gca().spines['right'].set_color('white')
plt.gca().set_facecolor('none')  
plt.gcf().patch.set_facecolor('none')
plt.grid(axis='y', linestyle='--', alpha=0.5, color='white')
# Aggiungere i valori all'interno delle barre
for bar in bars:
    tasso = bar.get_width()
    posizione_testo = bar.get_y() + bar.get_height() / 2
    if tasso >= 0:
        plt.text(tasso - 2, posizione_testo, f'{tasso:.1f}%', va='center', ha='right', fontsize=10, color='black')
    else:
        plt.text(tasso + 2, posizione_testo, f'{tasso:.1f}%', va='center', ha='left', fontsize=10, color='black')
 

# Mostra il grafico
plt.tight_layout()
plt.show()
