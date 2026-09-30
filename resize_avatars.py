import os
from PIL import Image

# Laluan folder avatar
folder_path = "avatars"

# Semak keberadaan folder
if not os.path.exists(folder_path):
    print(f"❌ Folder '{folder_path}' tidak dijumpai. Pastikan nama folder betul!")
else:
    processed_count = 0
    print("🚀 Memulakan proses optimasi gambar avatar...\n")

    for filename in os.listdir(folder_path):
        # Memproses format gambar PNG, JPG, JPEG
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(folder_path, filename)
            
            try:
                with Image.open(file_path) as img:
                    # Ambil saiz asal untuk rujukan
                    old_size = os.path.getsize(file_path) / 1024  # Saiz dalam KB
                    
                    # Kecilkan skala gambar ke maksimum 512x512 piksel (mengekalkan nisbah)
                    img.thumbnail((512, 512))
                    
                    # Simpan semula fail dengan optimasi mampatan
                    img.save(file_path, optimize=True, quality=85)
                    
                    new_size = os.path.getsize(file_path) / 1024  # Saiz baharu dalam KB
                    processed_count += 1
                    
                    print(f"✅ [{processed_count}] {filename}")
                    print(f"   └─ Saiz asal: {old_size:.1f} KB ➔ Saiz baharu: {new_size:.1f} KB")

            except Exception as e:
                print(f"❌ Gagal memproses {filename}: {e}")

    print(f"\n🎉 Selesai! Kesemua {processed_count} gambar avatar berjaya dioptimumkan.")