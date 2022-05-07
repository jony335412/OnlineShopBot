import sqlite3


def get_user_info():
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        print("Ma'lumotlar bazasi yaratildi!")

        sql = """CREATE TABLE Product(
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                description TEXT,
                price INTEGER NOT NULL,
                image TEXT NOT NULL,
                date DATETIME NOT NULL,
                cat_id INTEGER NOT NULL
                );"""
        cursor.execute(sql)
        connection.commit()
        print("Jadval yaratildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")

# get_user_info()


def cart_info():
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        print("Ma'lumotlar bazasi yaratildi!")

        sql = """CREATE TABLE Cart(
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                tg_id INTEGER NOT NULL
                );"""
        cursor.execute(sql)
        connection.commit()
        print("Jadval yaratildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")

# cart_info()

def add_user_info(tg_id, full_name, user_name):
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        # print("Connected!")

        sql = """INSERT INTO Users(tg_id, full_name, user_name) VALUES (?, ?, ?);"""
        data = (tg_id, full_name, user_name)
        cursor.execute(sql, data)
        connection.commit()
        print("Qo'shildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")

# add_user_info("12345678", "Javohir", None)


def add_product_info(product_name, quantity, tg_id):
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        # print("Connected!")

        sql1 = """SELECT * FROM Cart WHERE tg_id=? AND product_name=?;"""
        cursor.execute(sql1, (tg_id, product_name))
        total_rows = cursor.fetchall()
        print(total_rows)
        if total_rows:
            product = total_rows[0]
            sql_update_query = """Update Cart set quantity = ? where tg_id = ?"""
            data = (int(product[2]) + int(quantity), tg_id)
            cursor.execute(sql_update_query, data)
            connection.commit()
            print("Yangilandi")
        else:
            sql = """INSERT INTO Cart(product_name, quantity, tg_id) VALUES (?, ?, ?);"""
            data = (product_name, quantity, tg_id)
            cursor.execute(sql, data)
            connection.commit()
            print("Qo'shildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")

# add_product_info("DAMAS", 3, 1343692719)


def add_category(title):
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        # print("Connected!")

        sql = """INSERT INTO Category(title) VALUES (?);"""
        data = (title,)
        cursor.execute(sql, data)
        connection.commit()
        print("Qo'shildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")

# add_category(title="Telefon")


def add_product(title, description, price, image, date, cat_id):
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        # print("Connected!")

        sql = """INSERT INTO Product(title, description, price, image, date, cat_id) VALUES (?, ?, ?, ?, ?, ?);"""
        data = (title, description, price, image, date, cat_id)
        cursor.execute(sql, data)
        connection.commit()
        print("Qo'shildi!")
        cursor.close()
    except sqlite3.Error as error:
        print("Xatolik yuz berdi", error)
    finally:
        if connection:
            connection.close()
            print("Ma'lumotlar bazasi yopildi!")


# add_product(title="Mehrobdan chayon", description="„Mehrobdan chayon“ romanida xonliklar davri zugʻumi muayyan darajada sezilsa ham, adibda goho tarafkashlik mayllari koʻrinadi. Adib amalda realizm mavqeida turgan tarixiy haqiqatni mumkin qadar haqqoniy ifodalashga intilgan. Romanda muallif yengil hazil-mutoyiba, kulgi-yumor, piching, kinoya-kesatiq, hajv orqali Solix maxdum tabiatiga xos „maqtab boʻlmaydigan“ xususiyatlarni batafsil koʻrsatadi", price=20, image="https://assets.asaxiy.uz/product/items/desktop/678a1491514b7f1006d605e9161946b12021073115035538064RZZpHVnn0G.jpg", date="2022-05-05", cat_id=2)


def get_categories():
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from Category"""
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchall()    
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def get_cart_products(tg_id):
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT product_name, quantity from Cart WHERE tg_id=?"""
        cursor.execute(sqlite_select_query, (tg_id, ))
        total_rows = cursor.fetchall()    
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# prod = get_cart_products(tg_id=1343692719)
# print(prod)


def get_products():
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from Product"""
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchall()    
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# products = get_products()
# print(products)


def get_category_by_id(title):
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT id from Category WHERE title=?;"""
        data = (title, )
        cursor.execute(sqlite_select_query, data)
        total_rows = cursor.fetchone()
        cat_id = total_rows[0]
        sql = """SELECT title from Product WHERE cat_id=?;"""
        id = (cat_id, )
        cursor.execute(sql, id)
        total = cursor.fetchall()
        cursor.close()
        return total, cat_id

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# avto = get_category_by_id(title="Avtomobil")

# print(avto[0], avto[1])


def get_all_data(title):
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from Product WHERE title=?"""
        cursor.execute(sqlite_select_query, (title, ))
        total_rows = cursor.fetchone()    
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# product = get_all_data(title="DAMAS")
# print(product)


def get_product_by_id(cat_id):
    try:
        sqlite_connection= sqlite3.connect("main.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT title from Product WHERE cat_id=?"""
        cursor.execute(sqlite_select_query, (cat_id, ))
        total_rows = cursor.fetchall()    
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# all_data = get_product_by_id(cat_id=1)
# print(all_data)