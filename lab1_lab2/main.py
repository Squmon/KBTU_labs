# !pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

class W3Schools:
    def __init__(self, from_page, to_page, output_dir):
        self.driver = webdriver.Firefox()
        self.from_page = from_page
        self.to_page = to_page
        self.output_dir = output_dir
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            pass

    def get_page(self, url):
        self.driver.get(url)

    def get_examples_from_current_page(self):
        examples = self.driver.find_elements(By.CLASS_NAME, "w3-example")
        output = []
        for example in examples:
            w = example.text
            if "w3-pale-red" in example.get_attribute("class"):
                print(w, "- is a error example, skipping")
                continue
            try:
                code = example.find_element(By.CLASS_NAME, "pythoncolor").text
                print(f'"{w}"', " - has python code")
                output.append(code)
            except:
                print(f'"{w}"', " - has no python code")
            print()
        return output

    def run(self):
        self.get_page("https://www.w3schools.com/python")
        el = self.driver.find_element(By.ID, "leftmenuinnerinner")
        el.find_element(By.LINK_TEXT, self.from_page).click()
        while (cn := self.driver.find_element(By.ID, "leftmenuinnerinner").find_elements(By.CLASS_NAME, "active")[-1].text) != self.to_page:
            print("finding all examples on page", cn)
            ex = self.get_examples_from_current_page()
            if len(ex) != 0:
                write_page(cn, self.output_dir, ex)
            else:
                print("no examples found on", cn)
            self.driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[1]/div[2]/a[2]").click()
            print()

    def close(self):
        self.driver.close()


def write_page(name, output_dir, examples, IGNORE=None):
    with open(output_dir + "/" + name + ".py", "w") as f:
        for n, example in enumerate(examples):
            if IGNORE is None or example not in IGNORE:
                f.write(f"# example {n + 1}\n")
                f.write(example)
                if n != len(examples) - 1:
                    f.write("\n"*2)
            if not IGNORE is None:
                IGNORE.add(example)

print("starting doing lab1")
lab1 = W3Schools("Python HOME", "Python Booleans", "lab1")
lab1.run()
lab1.close()

print("starting doing lab2")
lab2 = W3Schools("Python Booleans", "Python Functions", "lab2")
lab2.run()
lab2.close()
