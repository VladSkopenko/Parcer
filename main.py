import csv
import requests
from lxml import html
import os

def login(session, login_url, login_data):
    """Логин в систему."""
    response = session.post(login_url, data=login_data)
    if response.status_code == 200 and "error" not in response.text.lower():
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False


def fetch_home_page(session, home_page_url):
    """Получение защищенной страницы после логина."""
    response = session.get(home_page_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve the protected page. Status code: {response.status_code}")
        return None


def parse_rows(page_content):
    """Парсинг данных с страницы."""
    tree = html.fromstring(page_content)
    xpath_path = '/html/body/div/div[3]/div/table/tbody/tr'
    rows = tree.xpath(xpath_path)
    return rows


def extract_data(rows):
    """Извлечение данных из строк таблицы."""
    header_for_csv = ['Artikelnummer', 'Beschreibung', 'Farbe', 'EAN', 'VPE', 'Status']
    data = []

    for row in rows:
        cells = row.xpath('.//td')
        cleaned_cells = []

        for cell in cells:
            text = cell.xpath('./text()')
            cleaned_text = text[0].strip() if text else 'Unknown'
            cleaned_cells.append(cleaned_text)

        img_src = row.xpath('.//td[6]/img/@src')
        status_number = 'Unknown'

        if img_src:
            img_src_value = img_src[0].lower()
            if 'green.gif' in img_src_value:
                status_number = '1'
            elif 'yellow.gif' in img_src_value:
                status_number = '2'
            elif 'red.gif' in img_src_value:
                status_number = '3'

        if len(cleaned_cells) == 6:
            cleaned_cells[5] = status_number
        data.append(cleaned_cells)

    return header_for_csv, data


def write_to_csv(filename, header, data):
    """Запись данных в CSV файл."""
    with open(filename, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Data successfully written to '{filename}'")


def main():
    login_url = "https://zac.zillnet.de/Login.php"
    home_page_url = "https://zac.zillnet.de/index.php"
    login_data = {
        'Customer_Number_Clear': os.getenv("USERNAME"),
        'password': os.getenv("PASSWORD"),
        'submit': 'Login'
    }

    session = requests.Session()

    if login(session, login_url, login_data):
        page_content = fetch_home_page(session, home_page_url)
        if page_content:
            rows = parse_rows(page_content)
            header, data = extract_data(rows)
            write_to_csv('home_page_zill.csv', header, data)


if __name__ == "__main__":
    main()
