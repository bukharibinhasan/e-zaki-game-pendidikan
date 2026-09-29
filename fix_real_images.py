import json
import os
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# 1. Senarai ID gambar MANUAL anda yang PERLU DIKEKALKAN
# (Kategori Haiwan ANM, Anggota Badan BDY, Pekerjaan JOB tidak akan disentuh)
PRESERVE_PREFIXES = ['ANM', 'BDY', 'JOB']

# 2. Baca fail vocab.js
with open('vocab.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.split('AZ_ZAKI_DATA =')[1].strip().rstrip(';')
data = json.loads(json_str)

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}


def get_real_image_url(keyword):
  """Mencari pautan gambar sebenar daripada Carian Imej Enjin."""
  query = urllib.parse.quote(f'{keyword} clipart png transparent')
  search_url = f'https://www.bing.com/images/async?q={query}&first=1&count=5'

  try:
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
      html = response.read().decode('utf-8', errors='ignore')
      # Ekstrak pautan gambar asal (murl)
      matches = re.findall(r'murl&quot;:&quot;(.*?)&quot;', html)
      if matches:
        return matches[0]
  except Exception as e:
    pass
  return None


def download_accurate_image(item):
  file_id = item['id']
  file_path = f'images/{file_id}.png'
  cat = (item.get('category') or '').lower()

  # Skip kategori Asmaul Husna, Nabi, dan Malaikat
  if any(
      k in cat for k in ['allah', 'asma', 'husna', 'nabi', 'rasul', 'malaikat']
  ):
    return

  # Semak jika ini gambar manual yang anda dah simpan
  prefix = ''.join([c for c in file_id if c.isalpha()])
  if prefix in PRESERVE_PREFIXES and os.path.exists(file_path):
    print(f'🛡️ Kekalkan gambar manual: {file_id}.png ({item["malay"]})')
    return

  # Cari gambar sebenar yang tepat mengikut perkataan Bahasa Melayu
  img_url = get_real_image_url(item['malay'])

  if not img_url:
    # Fallback carian kedua guna nama kategori jika perkataan khusus tidak jumpa
    img_url = get_real_image_url(f"{item['category']} {item['malay']}")

  if img_url:
    try:
      req = urllib.request.Request(img_url, headers=headers)
      with (
          urllib.request.urlopen(req, timeout=12) as response,
          open(file_path, 'wb') as out_file,
      ):
        out_file.write(response.read())
      print(f'✅ Gambar Tepat Berjaya: {file_id}.png -> {item["malay"]}')
    except Exception as e:
      print(f'⚠️ Gagal muat turun {file_id} ({item["malay"]}): {e}')
  else:
    print(f'❌ Tiada carian ditemui untuk: {item["malay"]}')


print(
    '🚀 Memulakan penggantian gambar rawak kepada GAMBAR TEPAT mengikut'
    ' perkataan...'
)

# Gunakan 3 thread serentak supaya carian selamat & tidak disekat
with ThreadPoolExecutor(max_workers=3) as executor:
  executor.map(download_accurate_image, data)

print(
    '🎉 SIAP! Kesemua gambar pemandangan rawak telah digantikan dengan gambar'
    ' objek/mufradat yang TEPAT.'
)