from imports import *


class FileDownloader:
    def __init__(self, csv_path, output_dir):
        self.df = pd.read_csv(csv_path)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_html_as_txt(self, url, txt_filename):
        try:
            response = requests.get(url)
            response.encoding = 'ISO-8859-9'  # Türkçe karakterler için uygun kodlama
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text(separator='\n', strip=True)

            # Dosya kaydetme
            os.makedirs(os.path.dirname(txt_filename), exist_ok=True)
            with open(txt_filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_content)

            print(f"{txt_filename} olarak kaydedildi.")
        except Exception as e:
            print(f"{txt_filename} kaydedilemedi, hata: {e}")
            # Hata durumunda dosyayı pas geçiyoruz

    def download_pdfs(self, pdf_files):
        for index, row in tqdm(pdf_files.iterrows(), total=pdf_files.shape[0]):
            pdf_name = row['PDF-Name-Short']
            pdf_url = row['PDF URL']

            try:
                response = requests.get(pdf_url)
                response.raise_for_status()

                pdf_path = os.path.join(self.output_dir, f"{pdf_name}.pdf")
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)

                print(f"İndirildi: {pdf_name}")

            except requests.exceptions.RequestException as e:
                print(f"İndirilemedi: {pdf_name}, Hata: {e}")
                # Hata durumunda dosyayı pas geçiyoruz

    def process_files(self):
        # HTML olanları işleme
        html_urls = self.df[self.df['Format'] == 'HTML']
        for index, row in html_urls.iterrows():
            url = row['PDF URL']
            filename = f"{row['PDF-Name-Short']}.txt"
            txt_filename = os.path.join(self.output_dir, filename)
            self.save_html_as_txt(url, txt_filename)

        # PDF olanları indirme
        pdf_files = self.df[self.df['Format'] == 'PDF']
        self.download_pdfs(pdf_files)
