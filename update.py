import json
import os

# 1. Baca vocab.js secara selamat
if not os.path.exists('vocab.js'):
    print("❌ Ralat: Fail 'vocab.js' tidak dijumpai!")
    exit()

with open('vocab.js', 'r', encoding='utf-8') as f:
    content = f.read()

try:
    json_str = content.split('AZ_ZAKI_DATA =')[1].strip().rstrip(';')
    data = json.loads(json_str)
except Exception as e:
    print(f"❌ Ralat membaca struktur vocab.js: {e}")
    exit()

# 2. Kemaskini laluan gambar tempatan (Pelindung: Kekalkan gambar Base64 Admin)
updated_count = 0
for item in data:
    current_img = item.get('image', '')
    # Jangan timpa jika gambar muat naik manual dari Admin (Data URL Base64)
    if not current_img.startswith('data:image'):
        item['image'] = f"images/{item['id']}.png"
        updated_count += 1

# 3. Simpan semula ke vocab.js
new_content = f"const AZ_ZAKI_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};"
with open('vocab.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(
    f"✅ Berjaya! 'vocab.js' dikemaskini ({updated_count} mufradat dihubungkan"
    " ke folder images/)."
)