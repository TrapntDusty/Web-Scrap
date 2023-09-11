import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import openpyxl
import time

headers = { #https://www.whatismybrowser.com/detect/what-is-my-user-agent/ }






#Amazon Section
urlamazon = "Amazon Link , beware amazon has lazy loading so wont load everything , use grid"
resp = requests.get(urlamazon, headers=headers)
soupamazon = BeautifulSoup(resp.text, "lxml")

elements = soupamazon.find_all("li",attrs={'data-id':' Some ID '}) # Change for the part that u need , or just add the ID from data-id of the product in ur grid amazon wishlist 
Costs = soupamazon.find_all("span",attrs={'class':'a-offscreen'}) # sames as elements
aria_labels = []
prices =[]

#finding the name of products
for element in elements:
    a_elements = element.find_all("a")
    
    for a in a_elements:
        aria_label = a.get("aria-label")
        if aria_label:
            aria_labels.append(aria_label)

#finding the cost of the products
for Cost in Costs:
    pricing = Cost.get_text()
    pricing = pricing.replace('$', '').replace(',', '')
    try:
        price_float = float(pricing)
        prices.append(price_float)
    except ValueError:
        print(f"Invalid Price: {pricing}")

if prices:
    total_cost = sum(prices)
    prices.append(total_cost)
else:
    print("No se encontro ninguno valido.")






#CYBERPUERTA section
# Here we just grabbing the price because we already got the name and price from amazon
urls = [
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Gabinetes/Gabinete-Balam-Rush-DragonFly-con-Ventana-Midi-Tower-ATX-Micro-ATX-Mini-ATX-USB-3-0-sin-Fuente-Rosa.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Fuentes-de-Poder-para-PC-s/Fuente-de-Poder-Corsair-RM850x-80-PLUS-Gold-24-pin-ATX-135mm-850W-cp2.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Fuentes-de-Poder-para-PC-s/Fuente-de-Poder-Corsair-RM850x-80-PLUS-Gold-24-pin-ATX-135mm-850W-cp2.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Fuentes-de-Poder-para-PC-s/Fuente-de-Poder-Corsair-RM850x-80-PLUS-Gold-24-pin-ATX-135mm-850W-cp2.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Procesadores/Procesadores-para-PC/Procesador-Intel-Core-i5-13600KF-S-1700-3-50GHz-14-Core-24MB-Smart-Cache-13va-Generacion-Raptor-Lake.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Memorias-RAM-y-Flash/Memorias-RAM-para-PC/Kit-Memoria-RAM-Corsair-Vengeance-DDR5-5600MHz-32GB-2-x-16GB-CL36-XMP-Gris.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Enfriamiento-y-Ventilacion/Disipadores-para-CPU/Disipador-CPU-DeepCool-AK500-ZERO-DARK-120mm-500-1850RPM-Negro.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Discos-Duros-SSD-NAS/SSD/SSD-Kingston-NV2-NVMe-1TB-PCI-Express-4-0-M-2.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Gigabyte-NVIDIA-GeForce-RTX-4070-GAMING-OC-12G-12GB-192-bit-GDDR6-PCI-Express-4-0.html',
    'https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-MSI-NVIDIA-GeForce-RTX-4070-Ti-VENTUS-3X-12G-OC-12GB-192-bit-GDDR6X-PCI-Express-4-0.html'
] # change for the links u desire , or remove if wanted

all_prices = []
positions_to_insert_zeros = [2, 3] # this is because some links from amazon dont exist on CYBERPUERTA so i copied one link just to put its data as 0 in price

# Iterate over the list of URLs and make requests
for url in urls:
    time.sleep(2)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soupcyber = BeautifulSoup(response.text, "lxml")
        pricecyber = soupcyber.find("span",attrs={'class':'priceText'}).get_text().replace('$', '').replace(',', '')
        try:
            price_float2 = float(pricecyber)
        except ValueError:
            print(f"Precio Invalido: {pricecyber}")
        if len(all_prices) in positions_to_insert_zeros:
            all_prices.append(0.0)  
        else:
            all_prices.append(price_float2)  
    else:
        print(f"Fallo encontrar datos de {url}")

total_costcyber = sum(all_prices)
all_prices.append(total_costcyber)







#EXCEL SECTION

#Fix that all columns need to have the same quantity 
max_length = max(len(aria_labels), len(prices),len(all_prices))

if len(aria_labels) < max_length:
    aria_labels.extend(["TOTAL"] * (max_length - len(aria_labels)))

if len(prices) < max_length:
    prices.extend([0.0] * (max_length - len(prices)))

if len(all_prices) < max_length:
    all_prices.extend([0.0] * (max_length - len(all_prices)))


#Saving excel
data = {'Nombres': aria_labels, 'PrecioAmazon': prices, 'PrecioCyber': all_prices} #the 2 sites and the names
df = pd.DataFrame(data)

current_date = datetime.now().strftime("%Y-%m-%d") # to save with the date

excel_file_path = f"D:/Desktop/amazon_webscraper-master/COMPONENTS_PRICE_{current_date}.xlsx" # saving on site , with current date to never modify an already existing save

with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    worksheet = writer.sheets['Sheet1']
    
    for column_name in df.columns: # to make colum fit properly
        max_length = df[column_name].astype(str).str.len().max()
        column_letter = openpyxl.utils.get_column_letter(df.columns.get_loc(column_name) + 1)
        column_width = max(max_length + 2, 10)  
        worksheet.column_dimensions[column_letter].width = column_width
