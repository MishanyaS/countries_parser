from parser import get_countries, write_to_excel, write_to_db

if __name__ == '__main__':
    write_to_excel(get_countries)
    write_to_db(get_countries)