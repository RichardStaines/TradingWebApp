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
        self.driver.get(url)
        table = self.driver.find_elements(By.TAG_NAME, "table")[0]  # 1st table
        for i, row in enumerate(table.find_elements(By.TAG_NAME, 'tr')):
            for j, cell in enumerate(row.find_elements(By.TAG_NAME, 'td')):
                if j == 2 and row_meanings[i] in interesting_rows:
                    out_dict[row_meanings[i]] = cell.text
                    # print(f"{i},{j} {cell.text} {row_meanings[i]}")

        return out_dict



