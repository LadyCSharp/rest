import sqlite3
def query():
    # Подключение к базе данных
    conn = sqlite3.connect('subject.db')
    # Создаем курсор
    cursor = conn.cursor()

    query = 'select "Полное название", Семестр, Наименование, Факультет from Специальность s, ' \
            'Дисциплина d ' \
            'where d.Специальность = s.шифр'

    cursor.execute(query)

    result = cursor.fetchall()
    return result

