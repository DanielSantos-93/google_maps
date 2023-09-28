from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class CustomWebDriver(webdriver.Firefox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def opcional_wait(self, by, value, timeout=3):
        try:
            wait = WebDriverWait(self, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except:
            return None

    def opcional_element(self, by, value, element_base, method_name=None, method_arg=None):
        try:
            if method_name == None:
                return element_base.find_element(by, value)
            else:
                method = getattr(element_base.find_element(by, value), method_name)
                if method_arg == None:
                    return method()
                else:
                    return method(method_arg)
        except:
            return None
class Maps():
    driver = None

    def __init__(self, headless = False):
        super(Maps, self).__init__()
        options = Options()
        options.headless = headless
        self.driver = CustomWebDriver()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.excel = ''

    def quit(self):
        self.driver.quit()
    def maximilize(self):
        self.driver.maximize_window()
    def minimize(self):
        self.driver.minimize_window()
    def opcional_element(self,type,value,wait=True,object=None):
        try:
            if wait:
                return self.wait.until(EC.visibility_of_element_located((type, value)))
            else:
                if object == None:
                    return self.driver.find_element(type, value)
                else:
                    return object.find_element(type, value)
        except:
            return None

    def main(self,search, quantity):
        self.driver.get(f'https://www.google.com.br/maps/search/{search}')
        total_elements = -1
        finish_list = False
        itens = []
        while total_elements < quantity or not finish_list:
            tabela_nomes = self.wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='hfpxzc']")))
            itens = []
            last_index = -1
            total_elements = len(tabela_nomes)

            for indice, row in enumerate(tabela_nomes, start=1):
                row_attr = row.get_attribute('outerHTML').split('aria-label="')[1]
                row_name = row_attr.split('" href="')[0]
                row_attr = row_attr.split('" href="')[1]
                row_link = row_attr.split('" jsaction="')[0]
                list_row = [indice,row_name,row_link]
                itens.append(list_row)
                if (total_elements < quantity or quantity == 0) and indice == total_elements -1:
                    try:
                        self.wait = WebDriverWait(self.driver, 1)
                        footer = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'HlvSq')))
                        if footer.text == 'Você chegou ao final da lista.':
                            finish_list = True
                            break
                    except:
                        pass
                    self.wait = WebDriverWait(self.driver, 20)
                    js_code = "arguments[0].scrollIntoView();"
                    self.driver.execute_script(js_code, row)
                if quantity > 0 and total_elements >= quantity and indice == quantity:
                    finish_list = True
                    break

        if len(itens) > 0:
            lojas = []
            for item in itens:
                linha_loja = {}
                linha_loja['indice'] = item[0]
                linha_loja['loja'] = item[1]
                self.driver.get(item[2])
                self.wait = WebDriverWait(self.driver, 3)

                stars = self.driver.opcional_wait(By.CLASS_NAME, 'F7nice ')
                if stars != None:
                    linha_loja['stars'] = self.driver.opcional_element(By.XPATH, "//span[contains(@aria-label,'estrelas')]", element_base=stars, method_name='get_attribute', method_arg='aria-label')

                type = self.driver.opcional_wait(By.XPATH, '//button[contains(@class,"DkEaL ")]')
                if type != None:
                    linha_loja['type'] = type.text

                info = self.driver.opcional_wait(By.XPATH, '//div[contains(@aria-label,"Informações")]')
                if info != None:
                    address = self.driver.opcional_element(By.XPATH, "//button[contains(@aria-label,'Endereço')]", element_base=info, method_name='get_attribute', method_arg='aria-label')
                    if address != None:
                        linha_loja['address'] = address

                    open_hours =  self.driver.opcional_element(By.XPATH, "//div[contains(@class,'t39EBf ') and contains(@class,'GUrTXd')]", element_base=info, method_name='get_attribute', method_arg='aria-label')
                    if open_hours != None:
                        linha_loja['open_hours'] = open_hours

                    website =  self.driver.opcional_element(By.XPATH, "//a[contains(@data-tooltip,'Abrir website')]", element_base=info, method_name='get_attribute', method_arg='href')
                    if website != None:
                        linha_loja['website'] = website

                    telephone = self.driver.opcional_element(By.XPATH, "//button[contains(@aria-label,'Telefone')]", element_base=info, method_name='get_attribute', method_arg='aria-label')
                    if telephone != None:
                        linha_loja['telephone'] = telephone

                lojas.append(linha_loja)

            for loja in lojas:
                for key, value in loja.items():
                    print(f'{key}: {value}',end='    ')
                print()
