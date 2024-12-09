import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Lettura del file
data = pd.read_csv('LPD_2024_public.csv', encoding='latin1', low_memory=False)

# Filtra le colonne rilevanti e rimuovi valori mancanti
habitat_data = data[['Common_name', 'Latitude', 'Longitude', 'T_biome']].dropna()

# Crea la mappa 
animals_map = folium.Map(location=[0, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(bird_map)

# Aggiungi i dati sulla mappa
for _, row in habitat_data.iterrows():
    popup_info = f"<b>Specie:</b> {row['Common_name']}<br><b>Habitat:</b> {row['T_biome']}"
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_info,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)


animals_map.save('habitats_map.html')
animals_map
