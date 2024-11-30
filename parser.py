import requests
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter
import sqlite3

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9" }

def get_countries():
        url = f'https://www.scrapethissite.com/pages/simple/'
        response = requests.get(url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='col-md-4 country')

        counter = 0
        for i in data:
            name = str.strip(i.find('h3', class_='country-name').text)
            capital = str.strip(i.find('span', class_='country-capital').text)
            population = str.strip(i.find('span', class_='country-population').text)
            area = str.strip(i.find('span', class_='country-area').text)
            counter = counter + 1

            print(f"Country №{counter}. Name: {name}, Capital: {capital}, Population: {population}, Area: {area}\n\n")

            yield name, capital, population, area

def write_to_excel(param):
    print("----------WRITING DATA TO XLSX----------")
    book = xlsxwriter.Workbook('countries.xlsx')
    page = book.add_worksheet('countries')

    row=0
    column=0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 20)
    page.set_column("D:D", 20)

    for item in param():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        page.write(row, column+3, item[3])
        row+=1

    print("Data about countries successfully written to file countries.xlsx")

    book.close()

def write_to_db(param):
    print("----------WRITING DATA TO DB----------")
    connection = sqlite3.connect('countries.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS countries
                  (id INTEGER PRIMARY KEY, name TEXT, capital TEXT, population REAL, area REAL)''')
    cursor.executemany('INSERT INTO countries (name, capital, population, area) VALUES (?, ?, ?, ?)', param())

    connection.commit()

    print("Data about countries successfully written to DB countries.db")

    connection.close()

