from Preparation_Dataframe import UniversityScraper
from Dir_Download import FileDownloader
from imports import *


def check_url_format(url):
    try:
        response = requests.head(url, allow_redirects=True)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')

            if content_type:
                if 'application/pdf' in content_type:
                    return "PDF"
                elif 'text/html' in content_type:
                    return "HTML"
                elif 'text/plain' in content_type:
                    return "Text"
                else:
                    return f"Bilinmeyen format: {content_type}"
            else:
                return "Bilinmiyor"
        else:
            return f"Başarısız istek: {response.status_code}"

    except requests.RequestException as e:
        return f"Hata: {str(e)}"


def convert_path_slashes(path):
    return path.replace("\\", "/")


# Dosya Yolunu Düzeltme
def create_full_path(base_path="C:/Users/Emirhan Denizyol/Desktop/", folder_name=""):
    # Dosya ismindeki ters slaşları normal slaşlara çevir
    folder_name = folder_name.replace("\\", "/")
    # Sabit yol ile dosya ismini birleştir
    full_path = base_path.rstrip("/") + "/" + folder_name
    return full_path


# İsimleri Düzeltme
def create_uni_name(name):
    return name + "-Mevzuat"


# Oluşturulan CSV dosyalarını silme
def delete_csv_files(folder_path):
    # Belirtilen klasör yolundaki tüm CSV dosyalarını bul
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    # Her bir CSV dosyasını sil
    for file in csv_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Failed to delete {file}. Reason: {e}")


# Dosyaları rarlama işlemi
def create_rar_from_directory(directory_path, rar_file_path):
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return  # WinRAR'ın yüklü olduğu tam yol

    if not os.path.exists(rar_executable):
        print(f"rar.exe not found at {rar_executable}")
        return

    try:
        # stdout ve stderr parametreleri ile çıktıyı gizliyoruz
        subprocess.run([rar_executable, 'a', rar_file_path, directory_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"Directory successfully archived as {rar_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the RAR file: {e}")


# İstenilen PDF'leri İndirme
def Run(rar_name="", web_url="", search_text=""):
    scraper = UniversityScraper(web_url=web_url, search_text=search_text)
    scraper.run()
    time.sleep(10)

    # Download
    downloader = FileDownloader(scraper.csv_name, create_full_path(folder_name=scraper.uni_name))
    downloader.process_files()
    print("İndirme Tamamlandı")

    time.sleep(10)
    # Preparing the XLSx File
    df = pd.read_csv(scraper.csv_name)
    file_name = scraper.uni_name + ".xlsx"
    file_path = os.path.join(create_full_path(folder_name=scraper.uni_name), file_name)
    df.to_excel(file_path, index=False)

    print(f'DataFrame {file_path} konumuna başarıyla kaydedildi.')

    time.sleep(10)

    # Dosyaları rarlama
    create_rar_from_directory(directory_path=create_full_path(folder_name=scraper.uni_name), rar_file_path=create_full_path(folder_name=scraper.uni_name))
    print("RAR Dosyası Oluşturuldu")

    # Oluşan CSV Dosyasını Silme, Oluşan Dosyayı Silme ve RAR Dosyasını silme
