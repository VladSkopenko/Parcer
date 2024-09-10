import csv
from database.models import Items
from database.db import session


def fix_text(text):
    return (text.replace('Â®', '®')
            .replace('Ã¼', 'ü').replace('Ã¶', 'ö')
            .replace("Ã¼n", 'ü').replace("Ã¶n", 'ö')
            .replace("Ã\x9f", 'ß'))


def fill_db():
    with open('home_page.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if index > 0:
                row = [fix_text(element) for element in row]
                item = Items(supplier="Zill", artikelnummer=row[0], beschreibung=row[1], farbe=row[2], ean=row[3], vpe=row[4],
                             status=row[5])
                session.add(item)
        session.commit()


if __name__ == '__main__':
    fill_db()
