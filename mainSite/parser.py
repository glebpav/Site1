from selenium import webdriver


class SeleniumParser():

    def parseLenta(self, url):
        articleText = self.parseSite(url=url, className="js-topic__text")
        print(articleText)
        return articleText.text

    def parseMeduza(self, url):
        print("Stating Meduza parser")
        articleText = self.parseSite(url=url, className="GeneralMaterial-container")
        print(articleText)
        return articleText

    def parseSite(self, url, className):
        print("Stating Default parser")
        driver = webdriver.Chrome()
        driver.get(url)
        allText = driver.find_element_by_class_name(className).text
        driver.quit()
        return allText

