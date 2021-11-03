from flask import Flask, render_template, request, redirect, url_for, session
import connection
from flask import Flask
import os.path

TEMPLATE_DIR = os.path.abspath('../templates')
STATIC_DIR = os.path.abspath('../static')

# app = Flask(__name__) # to make the app run without any
# app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


# static_path = os.path.join(project_root, '../client/static')
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/add_product/', methods=['POST'])
def add_product():
    if request.method == "POST":
        connection.add_product(request.form['name'], request.form['price'])
    return redirect('http://127.0.0.1:5000/admin')


@app.route('/add_user/', methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        if (len(request.form["name"]) > 4 and len(request.form["email"]) > 4 and len(request.form["password"]) > 3
                and request.form["password"] and not connection.user_exist(
                    request.form["email"])):
            name = request.form["name"]

            email = request.form["email"]
            psw = request.form["password"]
            print(name)
            print(email)
            print(request.form["password"])
            connection.add_user(name, email, psw)
            return redirect(url_for('admin'))
    return render_template("admin.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if (len(request.form["name"]) > 4 and len(request.form["email"]) > 4 and len(request.form["password"]) > 3
                and request.form["password"] == request.form["repeat_password"] and not connection.user_exist(
                    request.form["email"])):
            name = request.form["name"]
            email = request.form["email"]
            psw = request.form["password"]
            print(name)
            print(email)
            print(request.form["password"])

            connection.add_user(name, email, psw)
            return redirect('http://127.0.0.1:5000/login')
        else:
            print("Такой пользователь уже существует")
    return render_template("register.html", title="Register")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session['email'] = email
        if connection.login_user(email, password):
            # render_template("shop.html")
            if (email == "admin@gmail.com") and (password == "admin"):
                return redirect('http://127.0.0.1:5000/admin')
        return redirect('http://127.0.0.1:5000/shop')
    return render_template("login.html", title="Login")


@app.route('/add_cash/', methods=["POST"])
def add_cash():
    if request.method == "POST":
        print(session['email'], request.form['cash'])
        connection.add_cash(session['email'], request.form['cash'])
    return redirect(url_for('shop'))


@app.route('/add_product_to_busket/', methods=["POST"])
def add_product_to_busket():
    if request.method == "POST":
        print("айди", request.form['product_id'])
        email = session['email']
        connection.add_product_to_busket(connection.get_user_id_by_email(email), request.form.get('product_id'))
        return redirect(url_for('shop'))


@app.route('/delete_user/', methods=['POST'])
def delete_user():
    if request.method == "POST":
        connection.delete_user(request.form['id'])
    return redirect('http://127.0.0.1:5000/admin')


@app.route('/delete_product/', methods=['POST'])
def delete_product():
    if request.method == "POST":
        connection.delete_product(request.form['idproduct'])
    return redirect('http://127.0.0.1:5000/admin')


@app.route('/delete_product_from_busket/', methods=['POST'])
def delete_product_from_busket():
    if request.method == "POST":
        connection.delete_product_from_busket(request.form['delete'], connection.get_user_id_by_email(session['email']))
    return redirect(url_for('busket'))


@app.route('/buy/', methods=['POST'])
def buy():
    if request.method == "POST":
        connection.buy_product(connection.get_user_id_by_email(session['email']), request.form['buy'])
    return redirect(url_for('busket'))


@app.route('/shop', methods=["POST", "GET"])
def shop():
    email = session['email']
    return render_template("shop.html", products=connection.get_all_products(),
                           balans=connection.get_user_by_email(email)[4])


@app.route('/busket', methods=["POST", "GET"])
def busket():
    email = session['email']
    user_id = connection.get_user_id_by_email(email)
    return render_template("busket.html",
                           products=connection.get_products_from_busket(user_id),
                           balans=connection.get_user_by_email(email)[4])


@app.route("/admin", methods=["POST", "GET"])
def admin():
    return render_template("admin.html", products=connection.get_all_products(), users=connection.get_all_users())


@app.route("/")
def index():
    return "hello world"


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    # connection.add_user("admin","admin","makc@gmail.com","qwerty")
    # print(connection.get_user_by_email("makc@gmail.com"))
