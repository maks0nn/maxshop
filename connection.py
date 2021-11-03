import psycopg2
from werkzeug.security import generate_password_hash

connection = psycopg2.connect(
    host="localhost",
    database="shop",
    user="postgres",
    password="root"
)



def add_user(name, email, password):
    cursor = connection.cursor()
    request = f'''INSERT INTO "User" (name, email, password, cash) VALUES ('{name}', '{email}', '{password}', {0});'''
    print(request)
    cursor.execute(request)
    connection.commit()
    return connection, cursor


def login_user(email, password):
    cursor = connection.cursor()
    request = f'''SELECT * FROM "User" WHERE email = '{email}' AND password ='{password}';'''
    cursor.execute(request)
    print(request)
    return cursor.fetchall()


def get_user_id_by_email(user_email):
    cursor = connection.cursor()
    request = f'''SELECT id FROM "User" WHERE email = '{user_email}';'''
    print(request)
    cursor.execute(request)
    return cursor.fetchone()[0]


def get_user_by_email(user_email):
    cursor = connection.cursor()
    request = f'''SELECT * FROM "User" WHERE email = '{user_email}';'''
    print(request)
    cursor.execute(request)
    return cursor.fetchone()


def add_cash(email, cash):  # добовление денег на счет акканута
    cursor = connection.cursor()
    request = f'''UPDATE "User" SET cash = cash + {cash} WHERE email ='{email}';'''
    print(request)
    cursor.execute(request)
    connection.commit()


def add_product(name, price):
    cursor = connection.cursor()
    request = f'''INSERT INTO "Product" (name, price) VALUES ('{name}', {price});'''
    print(request)
    cursor.execute(request)
    connection.commit()
    return connection, cursor


def get_products_from_busket():
    cursor = connection.cursor()
    request = '''SELECT * FROM "Basket";'''
    cursor.execute(request)
    return cursor.fetchall()

def get_product():
    cursor = connection.cursor()
    request = '''SELECT * FROM "Product";'''
    cursor.execute(request)
    return cursor.fetchall()

def get_all_products():
    cursor = connection.cursor()
    request = '''SELECT * FROM "Product";'''
    cursor.execute(request)
    return cursor.fetchall()


def get_all_users():
    cursor = connection.cursor()
    request = '''SELECT * FROM "User";'''
    cursor.execute(request)
    return cursor.fetchall()


def add_product_to_busket(iduser, idproduct):
    cursor = connection.cursor()
    request = f'''INSERT INTO "Basket" (id_user, id_product) 
    VALUES ({iduser}, {idproduct});'''
    print(request)
    cursor.execute(request)
    connection.commit()
    return connection, cursor


def buy_product(user_id, product_id):
    cursor = connection.cursor()
    cursor.execute(f'''SELECT price FROM "Product" WHERE id = {product_id}''')
    price = cursor.fetchone()[0]
    cursor.execute(f'''SELECT cash FROM "User" WHERE id = {user_id}''')
    cash = cursor.fetchone()[0]
    if int(price) < int(cash):
        cursor.execute(f'''DELETE FROM "Basket" WHERE id_user = {user_id} AND id_product = {product_id};''')
        cursor.execute(f'''UPDATE "User" SET cash = cash - {price} WHERE id ='{user_id}';''')
        connection.commit()
    return connection, cursor


def get_products_from_busket(iduser):
    cursor = connection.cursor()
    request = f'''SELECT id_product FROM "Basket" WHERE id_user = {iduser};'''
    print(request)
    cursor.execute(request)
    busket_products = []
    busket_products_id = cursor.fetchall()
    for product_id in busket_products_id:
        cursor.execute(f'''SELECT * FROM "Product" WHERE id = {product_id[0]};''')
        busket_products.append(cursor.fetchall())
    print(busket_products)
    return busket_products



def delete_user(id):
    cursor = connection.cursor()
    request = f'''DELETE FROM "User" WHERE id = {id};'''
    print(request)
    cursor.execute(request)
    connection.commit()


def delete_product(idproduct):
    cursor = connection.cursor()
    request = f'''DELETE FROM "Product" WHERE id = {idproduct};'''
    print(request)
    cursor.execute(request)
    connection.commit()

def delete_product_from_busket(idproduct, user_id):
    cursor = connection.cursor()
    request = f'''DELETE FROM "Basket" WHERE id_product = {idproduct} AND id_user = {user_id};'''
    print(request)
    cursor.execute(request)
    connection.commit()

def user_exist(user_email):
    cursor = connection.cursor()
    request = f'''SELECT * FROM "User" WHERE 'email' = '{user_email}';'''
    cursor.execute(request)
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False