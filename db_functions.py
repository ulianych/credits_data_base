import sqlite3

db_path = 'db/credits.db'

credit_queries = {'insert': "INSERT INTO CREDIT (INN, CREDIT_SUM, CREDIT_PERCENT, LOAN_DATE, TERM, CURRENCY, STATUS) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  'delete': "DELETE FROM CREDIT WHERE CREDITID=?",
                  'update': "UPDATE CREDIT SET {} = ? WHERE CREDITID = ?",
                  'order': "SELECT * FROM CREDIT ORDER BY {}"}

fine_queries =  {'insert': "INSERT INTO FINE (CREDITID, FINE_DATE, FINE_SUM, PAID, PAYMENT_METHOD) VALUES (?, ?, ?, ?, ?)",
                  'delete': "DELETE FROM FINE WHERE ID=?",
                  'update': "UPDATE FINE SET {} = ? WHERE ID = ?",
                  'order': "SELECT * FROM FINE ORDER BY {}"}

ul_queries =  {'insert': "INSERT INTO UL (INN, NAME, ADDRESS, FIELDOKAD, STATUS, CREATEDATE) VALUES (?, ?, ?, ?, ?, ?)",
                  'delete': "DELETE FROM UL WHERE INN=?",
                  'update': "UPDATE UL SET {} = ? WHERE INN = ?",
                  'order': "SELECT * FROM UL ORDER BY {}"}


def create_connection():
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"An error occurred while connection to {db_path}: {e}")

def close_connection(cursor, connection):
    try:
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"An error occurred while closing {db_path}: {e}")

def fetch_data(cursor, table_name):
    try:
        cursor.execute('SELECT * FROM {}'.format(table_name))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred while fetching data from {table_name}: {e}")

def insert_row(cursor, table_name, values):
    try:
        if table_name == 'CREDIT':
            query_str = credit_queries['insert']
        elif table_name == 'UL':
            query_str = ul_queries['insert']
        elif table_name == 'FINE':
            query_str = fine_queries['insert']
        
        cursor.execute(query_str, values)
    except Exception as e:
        print(f"An error occurred while inserting a row: {e}")

def update_field(cursor, table_name, field_name, new_value, id):
    try:
        if table_name == 'CREDIT':
            query_str = credit_queries['update'].format(field_name)
        elif table_name == 'UL':
            query_str = ul_queries['update'].format(field_name)
        elif table_name == 'FINE':
            query_str = fine_queries['update'].format(field_name)
        
        cursor.execute(query_str, (new_value, id))
    except Exception as e:
        print(f"An error occurred while updating the field: {e}")

def sort_by_field(cursor, table_name, field_name):
    try:
        if table_name == 'CREDIT':
            query_str = credit_queries['order'].format(field_name)
        elif table_name == 'UL':
            query_str = ul_queries['order'].format(field_name)
        elif table_name == 'FINE':
            query_str = fine_queries['order'].format(field_name)
        
        cursor.execute(query_str)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred while sorting the table: {e}")

def delete_row(cursor, table_name, id):
    try:
        if table_name == 'CREDIT':
            query_str = credit_queries['delete']
        elif table_name == 'UL':
            query_str = ul_queries['delete']
        elif table_name == 'FINE':
            query_str = fine_queries['delete']
        
        cursor.execute(query_str, (id,))
    except Exception as e:
        print(f"An error occurred while deleting a row: {e}")

def get_column_names(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    return column_names

def print_table(rows, header=None):
    if not rows:
        print("No data available")
        return

    if header:
        print(" | ".join(header))
        print("-" * 70)

    for row in rows:
        print(" | ".join(map(str, row)))

def fetch_credit_ids(cursor):
    cursor.execute("SELECT CREDITID FROM CREDIT")
    return [row[0] for row in cursor.fetchall()]

def fetch_inn(cursor):
    cursor.execute("SELECT INN FROM UL")
    return [row[0] for row in cursor.fetchall()]

# connection, cursor = create_connection()

# # Вставка записи в таблицу
# insert_row(cursor, 'UL', ('1789', 'Company ABC', '123 Main St', 5555, 1, '2024-12-15'))

# print(print_table(fetch_data(cursor, 'UL')))
# # Обновление поля в таблице
# update_field(cursor, 'UL', 'STATUS', 0, '1789')
# print(print_table(fetch_data(cursor, 'UL')))

# # Удаление записи из таблицы
# delete_row(cursor, 'UL', '1789')
# print(print_table(fetch_data(cursor, 'CREDIT')))

# close_connection(cursor, connection)