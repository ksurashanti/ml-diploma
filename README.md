Дипломный проект.

Выявление релевантных пар исследователей и формирование команд для совместной научной работы на основе семантического анализа текстов научных статей.

Предполагаю сравнивать схожесть научных интересов путём анализа статей, которые пишет научный сотрудник. По результатам анализа можно рекомендовать совместную работу двух исследователей, рекомендовать научных руководителей аспирантам и собирать научные группы, специализирующиеся на определённом направлении.

Сделано:
1. Парсинг https://cyberleninka.ru/
2. Предобработка собранных данных: извлечение полезной информации (УДК, год написания, уровень научной публикации), лемматизация, удаление стоп-слов
3. Анализ данных по годам публикации, по уровням научной публикации
4. Классификации по 4 классам: ИТ, физика, медицина, математика. Точность полученной модели 98%

План:

5. Кластеризация с использованием небольших кластеров. Группируем статьи по более узким тематикам, чем предметная область -> понимаем, какие исследователи в какой области работают
6. Семантическая мера близости текстов, определяем пары исследователей
7. Соединяем кластеризацию и исследование семантической меры близости текстов, получаем рекомендательную систему для формирования пар исследователей и научных команд
