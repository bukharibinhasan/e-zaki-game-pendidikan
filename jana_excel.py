import json
import urllib.parse
import csv

# 1. Baca data daripada vocab.js
with open('vocab.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.split('AZ_ZAKI_DATA =')[1].strip().rstrip(';')
data = json.loads(json_str)

# 2. Bina fail Excel CSV
filename = 'Carian_Gambar_AzZaki.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    # Header Excel
    writer.writerow(['ID', 'Kategori', 'Bahasa Melayu', 'Bahasa Arab', 'Nama Fail Img', 'Link Carian Google', 'Status'])
    
    for item in data:
        img_name = f"{item['id']}.png"
        query = urllib.parse.quote(f"{item['malay']} icon transparent png")
        search_url = f"https://www.google.com/search?tbm=isch&q={query}"
        
        writer.writerow([
            item['id'],
            item['category'],
            item['malay'],
            item['arabic'],
            img_name,
            search_url,
            'PENDING'
        ])

print(f"✅ Fail '{filename}' berjaya dijana! Buka fail ini menggunakan Microsoft Excel.")