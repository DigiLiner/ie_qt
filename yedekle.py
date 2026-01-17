import zipfile
from datetime import datetime
import os

def yedekle():
    # Çalışılan dizin
    base_dir = os.getcwd()
    
    # Yedekler klasörünü oluştur
    yedekler_dir = os.path.join(base_dir, "yedekler")
    if not os.path.exists(yedekler_dir):
        os.makedirs(yedekler_dir)
        
    # Tarih-zaman damgası
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(yedekler_dir, f"yedek_{timestamp}.zip")
    
    # Zip dosyası oluştur
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # .py ve .ui dosyalarını ekle
        for file in os.listdir(base_dir):
            if file.endswith(".py") or file.endswith(".ui"):
                zipf.write(os.path.join(base_dir, file), file)
        
        # resources klasörünü ekle
        resources_dir = os.path.join(base_dir, "resources")
        if os.path.exists(resources_dir):
            for root, dirs, files in os.walk(resources_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Zip içindeki göreli yol
                    rel_path = os.path.relpath(full_path, base_dir)
                    zipf.write(full_path, rel_path)
    
    print(f"Yedekleme tamamlandı: {zip_filename}")