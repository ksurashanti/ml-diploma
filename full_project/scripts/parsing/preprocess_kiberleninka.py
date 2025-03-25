import re
import pandas as pd
from nltk.corpus import stopwords
import pymorphy3
#from langdetect import detect


def get_user_input():
    file_name = input("Введите название файла без расширения (например, physical-sciences): ")
    return file_name

def fill_na(df_articles):
    df_articles = df_articles.dropna(subset='text') #строки без текста нет смысла хранить
    df_articles = df_articles.dropna(subset='authors') #строки без автора тоже
    df_articles['annotation'] = df_articles['annotation'].fillna('no annotation') #аннотацию заполняем текстом
    df_articles['article_level'] = df_articles['article_level'].fillna('-') #уровень статьи заполняем прочерком
    if df_articles.isna().any().any():
        print("Не все пропуски заполнены")
        return df_articles
    else:
        print("Пропуски успешно заполнены")
        return df_articles

def feature_udk(df_articles):
    """"извлечение УДК через
    регулярное выражение и запись
    в отдельный столбик"""
    udk = []
    for el in df_articles['text']:
        reg = re.search(r'УДК:?\s+\d{1,3}(\.\d{1,3})?(.?|:?)?(\d{1,3}(\.\d{1,3})?)?', el)
        try:
            udk.append(reg.group(0))
        except AttributeError:
            udk.append('None') #если нет УДК
    df_articles['UDK'] = udk
    print('УДК добавлены')
    return df_articles

def del_short_articles(df_articles, size=200):
    count_words = []
    #добавляем информацию о словах в отдельный столбец датафрейма
    for el in df_articles['text']:
        count_words.append(len(el.split()))
    df_articles['count_words'] = count_words
    #удаляем статьи где меньше size слов
    df_articles = df_articles.drop(df_articles[df_articles['count_words'] < size].index)
    print(f"Статьи с количеством слов меньше {size} удалены")
    return df_articles.reset_index(drop=True)

#приведение к нижнему регистру, лемматизация, удаление стоп-слов
def preproc_pymorhy(df_articles):
    m = pymorphy3.MorphAnalyzer()
    mystopwords = stopwords.words('russian') + ['удк',
                                                'это', 'наш', 'тыс', 'млн', 'млрд', 'также', 'т', 'д',
                                                'который', 'прошлый', 'сей', 'свой', 'наш', 'мочь', 'такой'
                                                ]
    ru_words = re.compile("[А-Яа-яЁё]+")

    def words_only(text):
        return " ".join(ru_words.findall(text))

    def lemmatize(text, mystem=m):
        try:
            return " ".join([m.parse(w)[0].normal_form for w in text.split(' ')]).strip()
        except:
            return " "

    def remove_stopwords(text, mystopwords=mystopwords):
        try:
            return " ".join([token for token in text.split() if not token in mystopwords])
        except:
            return ""

    def preprocess(text):
        return remove_stopwords(lemmatize(words_only(text.lower())))

    df_articles.text = df_articles.text.apply(preprocess)
    print("Статьи приведены к нижнему регистру, лемматизированы, стоп-слова удалены")
    return df_articles


def main():
    file_name = get_user_input()
    path = 'C:/Users/ksurashanti/PycharmProjects/netology_diploma/date/kiberleninka/'
    dateframe_from_file = pd.read_excel(f'{path}raw/{file_name}.xlsx', index_col = 0) #открытие файла
    dateframe_from_file = fill_na(dateframe_from_file) #обработка пустых значений
    dateframe_from_file = feature_udk(dateframe_from_file) #извлечение УДК
    dateframe_from_file = del_short_articles(dateframe_from_file) #удаление коротких текстов (до 200 слов)

    dateframe_from_file = preproc_pymorhy(dateframe_from_file)

    #сохранение, осторожно, не перезапиши файл, директория должна быть processed!
    dateframe_from_file.to_excel(f'{path}processed/{file_name}.xlsx')
    print("Файл сохранен")

if __name__ == "__main__":
    main()