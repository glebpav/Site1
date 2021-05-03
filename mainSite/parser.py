from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class SeleniumParser:

    def parse_lenta(self, url):
        article_text = self.parse_site(url=url, className="js-topic__text")
        print(article_text)
        return article_text

    def parse_ria(self, url):
        print("Starting Ria parser")
        article_text = self.parse_site(url=url, className="article__block")
        print(article_text)
        return article_text

    def parse_meduza(self, url):
        print("Stating Meduza parser")
        article_text = self.parse_site(url=url, className="GeneralMaterial-article")
        print(article_text)
        return article_text

    def parse_site(self, url, className):
        print("Stating Default parser")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('srtart_maximized')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')

        driver = webdriver.Chrome(chrome_options=options)
        # driver = webdriver.Chrome()
        driver.get(url)
        try:
            all_text = driver.find_element_by_class_name(className).text
        except:
            all_text = ""
        driver.quit()
        return all_text
