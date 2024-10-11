from imports import *


class UniversityScraper:
    def __init__(self, web_url, search_text):
        self.web_url = web_url
        self.search_text = search_text
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.uni_name = ""
        self.csv_name = ""
        self.url = ""

    def open_page(self):
        # Web sayfasını aç
        self.driver.get(self.web_url)
        # Web sayfasının yüklenmesini bekle
        time.sleep(5)

    def perform_search(self):
        # Arama butonunu bul ve tıkla (aria-label kullanarak)
        search_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Arama']")
        search_button.click()

        # Arama kutusu tıklanınca açılıyorsa, burada arama kutusunu bulabilir ve arama yapabilirsiniz.
        time.sleep(10)  # Arama kutusunun açılması için bir süre bekle

        search_box = self.driver.find_element(By.XPATH, "//input[@type='text']")  # Arama kutusunu bul
        search_box.send_keys(self.search_text)  # Arama terimini gönder

        time.sleep(10)
        # Enter tuşuna basarak arama yap
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

    def click_search_button(self):
        # Butonu class'a göre bul ve tıkla (CSS Selector kullanarak)
        search_button = self.driver.find_element(By.CSS_SELECTOR,
                                                 ".MuiLoadingButton-root.MuiButton-containedPrimary.search-button")
        search_button.click()
        time.sleep(5)

    def navigate_to_details(self):
        # Yeni sayfada 'Künyesine Git' butonunu bul ve tıkla
        kunesine_git_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Künyesine Git')]")
        kunesine_git_button.click()
        time.sleep(5)
        self.url = self.driver.current_url

    def extract_university_name(self):
        # İlgili kısmı XPath ile bulun ve text içeriğini alın
        self.uni_name = self.driver.find_element(By.XPATH, "//div[@style='font-size: 32px; font-weight: 600;']").text
        print(f"Üniversite Adı: {self.uni_name}")

    def close_cookie_notice(self):
        try:
            tamam_button = self.driver.find_element(By.XPATH, "//button[text()='Tamam']")
            if tamam_button.is_displayed():
                tamam_button.click()
                time.sleep(2)
        except Exception as e:
            print("Çerez bildirimi bulunamadı veya kapatılamadı:", e)

    def click_mevzuat_button(self):
        try:
            mevzuat_button = self.driver.find_element(By.XPATH, "//button[@aria-controls='simple-tabpanel-4']")
            time.sleep(12)
            mevzuat_button.click()
            time.sleep(15)
        except Exception as e:
            print("Buton tıklanamadı:", e)

    def collect_pdf_links(self):
        try:
            pdf_links = self.driver.find_elements(By.XPATH, "//a[@class='a-hover']")

            pdf_data = []
            for link in pdf_links:
                pdf_name = link.get_attribute('aria-label').replace("yeni sekmede aç", "").strip()
                pdf_url = link.get_attribute('href')
                # URL formatını kontrol et ve ekle
                pdf_format = self.check_url_format(pdf_url)
                pdf_data.append({'PDF Name': pdf_name, 'PDF URL': pdf_url, 'Format': pdf_format})

            df = pd.DataFrame(pdf_data)
            # PDF-Name-Short sütununu ekle
            df = self.add_pdf_name_short_column(df)
            # .csv uzantısını ekleyerek dosya adını tamamla ve kaydet
            if not self.uni_name.endswith('.csv'):
                self.csv_name = self.uni_name + '.csv'
            df.to_csv(self.csv_name, index=False)
            print(f"DF HEAD: {df.head()}")
            print(f"DF SHAPE: {df.shape}")
            print(f"PDF isimleri, URL'leri ve formatları '{self.csv_name}' dosyasına kaydedildi.")
        except Exception as e:
            print("PDF'ler alınamadı:", e)

    def add_pdf_name_short_column(self, df):
        # PDF-Name-Short sütununu ekle ve sırasıyla PDF-1, PDF-2, ... olarak numaralandır
        df['PDF-Name-Short'] = ['PDF-' + str(i+1) for i in range(len(df))]
        return df

    def check_url_format(self, url):
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

    def close_browser(self):
        # Tarayıcıyı kapatmak için
        self.driver.quit()

    def run(self):
        self.open_page()
        self.perform_search()
        self.click_search_button()
        self.navigate_to_details()
        self.extract_university_name()
        self.close_cookie_notice()
        self.click_mevzuat_button()
        self.collect_pdf_links()
        self.close_browser()