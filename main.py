from parser import get_countries, write_to_excel, write_to_db, write_to_csv

if __name__ == '__main__':
    write_to_excel(get_countries)
    write_to_db(get_countries)
    write_to_csv()