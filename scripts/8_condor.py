import pandas as pd
import matplotlib.pyplot as plt

# Carica il CSV aggiornato
data = pd.read_csv('condor_population.csv')

# Crea la figura e l'asse del grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Aggiungi i punti e la linea
for i in range(1, len(df)):
    if df['Popolazione stimata'][i] > df['Popolazione stimata'][i-1]:
        ax.plot(df['Anno'][i-1:i+1], df['Popolazione stimata'][i-1:i+1], marker='o', color='lime', linestyle='-', linewidth=2, markersize=8)
    else:
        ax.plot(df['Anno'][i-1:i+1], df['Popolazione stimata'][i-1:i+1], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)

# Aggiungi titoli e etichette con testo bianco
ax.set_title('Popolazione del Condor della California (1970-2020)', fontsize=14, color='white')
ax.set_xlabel('Anno', fontsize=12, color='white')
ax.set_ylabel('Popolazione stimata', fontsize=12, color='white')

# Impostazioni per il grafico
fig.patch.set_facecolor('none')  
ax.set_facecolor('none')  
ax.grid(True, color='white', linestyle='--', linewidth=0.5)  
ax.tick_params(axis='both', colors='white')  
ax.set_yticks(range(0, 501, 50))  
ax.grid(True, which='both', axis='y', color='white', linestyle='-', linewidth=0.5)  # Linee orizzontali
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Salvataggio del grafico con sfondo trasparente
plt.savefig('condor_population_graph.png', transparent=True)

# Mostra il grafico
plt.show()
