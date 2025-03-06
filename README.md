Дипломный проект

<h1>Выявление релевантных пар исследователей и формирование команд для совместной научной работы на основе семантического анализа текстов научных статей.</h1>

Предполагаю сравнивать схожесть научных интересов путём анализа статей, которые пишет научный сотрудник. По результатам анализа можно рекомендовать совместную работу двух исследователей, рекомендовать научных руководителей аспирантам и собирать научные группы, специализирующиеся на определённом направлении.

Сделано:
1. Парсинг https://cyberleninka.ru/
2. Предобработка собранных данных: извлечение полезной информации (автор, аннотация, УДК, год написания, уровень научной публикации, текст статьи), лемматизация, удаление стоп-слов
3. Анализ данных по годам публикации, по уровням научной публикации
4. Классификации по 4 классам: ИТ, физика, медицина, математика. Точность полученной модели 98%
5. Кластеризация с использованием небольших кластеров на основе семантического анализа текстов. Группируем статьи по более узким тематикам, чем предметная область -> понимаем, какие исследователи в какой области работают
6. Рекомендательная система:
   
   6.1 Если ищем пару, то смотрим публикации одного человека и выводим список схожих авторов публикаций.

   План:
   
   6.1 Попробовать разные способы векторизации

   <p>6.2 Если надо сформировать научную группу, задаём параметры (область научных интересов, количество человек, требуемый уровень публикаций), выводим всех подходящих под запрос людей.</p> 
