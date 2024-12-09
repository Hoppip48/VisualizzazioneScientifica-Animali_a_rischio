import pandas as pd
import matplotlib.pyplot as plt

# Carica il dataset
def load_data(file_path):
    try:
        return pd.read_csv(file_path, encoding="latin1", low_memory=False)
    except FileNotFoundError:
        print(f"Errore: Il file {file_path} non è stato trovato.")
        return None

# Analizza le minacce principali
def analyze_threats(data, top_n=8):
    if 'name' not in data.columns:
        print("Errore: La colonna richiesta 'name' è assente.")
        return None

    # Conta le occorrenze delle minacce e seleziona le prime
    threat_counts = data['name'].value_counts().head(top_n)
    top_threats = pd.DataFrame({'Threat_Type': threat_counts.index, 'Species_Count': threat_counts.values})

    # Combina categorie simili
    if 'Named species' in top_threats['Threat_Type'].values and 'Unspecified species' in top_threats['Threat_Type'].values:
        named_count = top_threats.loc[top_threats['Threat_Type'] == 'Named species', 'Species_Count'].values[0]
        unspecified_count = top_threats.loc[top_threats['Threat_Type'] == 'Unspecified species', 'Species_Count'].values[0]
        top_threats = top_threats[~top_threats['Threat_Type'].isin(['Named species', 'Unspecified species'])]
        combined_count = named_count + unspecified_count
        combined_category = pd.DataFrame({'Threat_Type': ['Predatori e specie dannose'], 'Species_Count': [combined_count]})
        top_threats = pd.concat([top_threats, combined_category], ignore_index=True)

    # Rinomina le categorie
    name_mapping = {
        "Small-holder farming": "Agricolura intensiva",
        "Small-holder grazing, ranching or farming": "Allevamento intensivo",
        "Unintentional effects: (subsistence/small scale) [harvest]": "Pesticidi",
        "Mining & quarrying": "Habitat danneggiato",
        "Soil erosion, sedimentation": "Habitat danneggiato",
        "Droughts": "Siccità",
        "Housing & urban areas": "Inquinamento",
        "Scale Unknown/Unrecorded": "InTeoriaèDiNuovoAgricoltura",
        "Type Unknown/Unrecorded": "Urbanizzazione",
        "Motivation Unknown/Unrecorded": "Caccia e pesca eccessiva"
    }
    top_threats['Threat_Type'] = top_threats['Threat_Type'].replace(name_mapping)
    return top_threats

# Crea un grafico a torta
def create_pie_chart(data, title):
    plt.figure(figsize=(8, 8))
    plt.pie(
        data['Species_Count'],
        labels=data['Threat_Type'],
        autopct='%1.1f%%',
        startangle=200,
        colors=['forestgreen', 'dimgrey', 'darkgrey', 'limegreen', 'orangered', 'slateblue', 'firebrick'],
        textprops={'color': 'white'}
    )
    plt.title(title, color='white')
    plt.savefig('pie.png', transparent=True, format='png')
    plt.show()

# Main
if __name__ == "__main__":
    file_path = 'threats.csv'
    data = load_data(file_path)
    if data is not None:
        top_threats = analyze_threats(data)
        if top_threats is not None:
            print("Principali minacce alle specie:")
            print(top_threats)
            create_pie_chart(top_threats, "")
