import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

"""
перед началом выполнения программы создайте 
файлы в формате эксель для тех категорий, которые вы планируете выгружать
со столбцами 'page','date','title','link','annotation',
'authors','article_level'"""

def get_user_input():
    """Запрос параметров у пользователя"""
    category = input("Введите категорию статей с киберленинки (например physical-sciences): ")
    start_page = 1
    end_page = int(input("Введите конечную страницу в этой категории: "))
    num_pages = int(input("Сколько страниц парсить? "))
    first_index = int(input("Первый индекс статьи для выгрузки текста: "))
    last_index = int(input("Последний индекс статьи для выгрузки текста: "))
    return category, start_page, end_page, num_pages, first_index, last_index

def parse_articles(category, pages, df):
    """Парсинг статей с CyberLeninka
    только та информация, что на страницах
    тексты статей сюда не входят"""
    already_pages =  df['page'].unique()
    articles_df_func = pd.DataFrame()

    for page in pages: #в pages список всех страниц случайный, для каждой страницы
        if page in already_pages:
            pass
        else:
            url = f'https://cyberleninka.ru/article/c/{category}/{page}'

            req = requests.get(url).text
            soup = BeautifulSoup(req, 'html.parser')

            articles = soup.find_all('li')

            for el in articles:
                try:
                    article_data = {
                            'page': page,
                            'date': el.find('span').text[0:4],
                            'title': el.find('div', 'title').text,
                            'link': el.find('a').get('href'),
                            'annotation': el.find('p').text,
                            'authors': el.find('span').text[7:],
                            'article_level': el.find('div', 'labels').get_text(separator=' ').strip()
                            } #сепаратором делаю пробел между словами, стрипом удаляю пробелы в начале и конце
                except AttributeError:
                        break
                articles_df_func = pd.concat([articles_df_func, pd.DataFrame([article_data])])
                time.sleep(random.uniform(0.01, 0.03)) #при выгрузке страниц длинный слип не нужен
    try:
        return articles_df_func
    except UnboundLocalError:
        print("Все значения в диапазоне страниц уже загружены, повторите запрос")

#парсинг текста статей (для него надо заходить внутрь по каждой ссылке)
def add_full_text(category, first_index, last_index):
    print("Прогресс:\n")
    articles_df = pd.read_excel(f'{category}.xlsx', index_col=0)
    i = first_index
    while i <= last_index:
        el = articles_df['link'].iloc[i]
        url = 'https://cyberleninka.ru' + el
        time.sleep(random.uniform(0.01, 0.6)) #здесь без слипа часто запрашивает капчу
        try:
            req = requests.get(url).text
            soup = BeautifulSoup(req, 'html.parser')
            full_text = soup.find('div', class_='ocr').text.strip()
            articles_df.loc[i, 'text'] = full_text
            i += 1
            print(i)
        except AttributeError: #в некоторых случаях достаточно просто повторно выполнить запрос, без перехода по ссылке
            print(f"Надо зайти на страницу и возможно ввести капчу по ссылке {el}, статья на {i} строчке")
            print("Продолжить парсинг? (y/n)")
            if input().lower() != 'y':
                return articles_df
            pass

    return articles_df #возвращает готовый датафрейм со статьями и номер строки, на которой остановился парсинг

def main():
    category, start_page, end_page, num_pages, first_index, last_index = get_user_input()
    random_pages = random.sample(range(start_page, end_page + 1), num_pages)

#улучшить: создавать файл на основании директории которую ввел пользователь, а не вручную
    dateframe_from_file = pd.read_excel(f'{category}.xlsx', index_col = 0)

#парсинг страниц
    articles_df = pd.concat([dateframe_from_file, parse_articles(category, random_pages, dateframe_from_file)])
    articles_df = articles_df.reset_index(drop=True)
    articles_df.to_excel(f'C:/Users/ksurashanti/PycharmProjects/netology_diploma/date/kiberleninka/raw/{category}.xlsx')

#парсинг текста
    df_with_text = add_full_text(category, first_index, last_index)
    df_with_text.to_excel(f'C:/Users/ksurashanti/PycharmProjects/netology_diploma/date/kiberleninka/raw/{category}.xlsx')

    print(f"\nФайл сохранён")

if __name__ == "__main__":
    main()