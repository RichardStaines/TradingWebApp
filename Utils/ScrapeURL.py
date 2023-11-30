from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class ScrapeURL:

    def __init__(self):
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True  # if we miss this line, we can't make Edge headless
        edge_options.add_argument('headless')
        # edge_options.add_argument('disable-gpu')
        self.driver = webdriver.Edge(options=edge_options)

    def get_div(self, url):
        row_meanings = ["headings", "status", "type", "Per Share", "decl_date", "ex_div", "payment_date", ]
        interesting_rows = ["Per Share", "ex_div", "payment_date"]
        out_dict = {}
        prev_div_dict = {}
        self.driver.get(url)
        tables = self.driver.find_elements(By.TAG_NAME, "table")
        if len(tables) == 0:
            return [out_dict, prev_div_dict]

        table = tables[0]
        for i, row in enumerate(table.find_elements(By.TAG_NAME, 'tr')):
            for j, cell in enumerate(row.find_elements(By.TAG_NAME, 'td')):
                if j == 1 and row_meanings[i] in interesting_rows:
                    if row_meanings[i] == "Per Share":
                        prev_div_dict[row_meanings[i]] = self.extract_price(cell.text)
                    else:
                        prev_div_dict[row_meanings[i]] = cell.text
                if j == 2 and row_meanings[i] in interesting_rows:
                    if row_meanings[i] == "Per Share":
                        out_dict[row_meanings[i]] = self.extract_price(cell.text)
                    else:
                        out_dict[row_meanings[i]] = cell.text
                    # print(f"{i},{j} {cell.text} {row_meanings[i]}")

        return [out_dict, prev_div_dict]

    def extract_price(self, s):
        """
        extract the price in pence
        :param s: <price>p [(<cents-price>c)]
        :return: price value
        """
        return 0 if s.lower() == 'sign up required' else s[:s.find('p')]
