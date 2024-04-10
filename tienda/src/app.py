from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session,jsonify
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from models.ModelUsers import ModelUsers, User
from models.ModelProduct import ModelProducts, Product
from models.ModelCategories import ModelCategories,Categories
from models.ModelShopping_cart import ShoppingCartModel
from models.ModelOrder import ModelOrder

app = Flask(__name__)

mysql = MySQL(app)
app.secret_key = '123456789'
app.config.from_object(config['development'])
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return ModelUsers.get_by_id(mysql, id)

# Variable global para almacenar los datos del usuario actual
current_user_data = None

# Decorador para requerir autenticación de administrador
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario está autenticado y es un administrador (tipo 1 o 3)
        if not current_user.is_authenticated or current_user.usertype not in [1, 3]:
            abort(403)  # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view


def root_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 3:
            abort(403)  # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User(0, request.form['username'], request.form['password'], 0, 0)
            print("Intento de inicio de sesión para el usuario:", user.username,user.usertype)
            logged_user = ModelUsers.login(mysql, user)
            print("Usuario autenticado:", logged_user)

            if logged_user is not None:
                login_user(logged_user)
                flash("¡Inicio de sesión exitoso!", 'success')
                if logged_user.usertype in [1, 3]:
                    return redirect(url_for("admin"))  # Redirige a la página de administrador
                elif logged_user.usertype == 0:
                    return redirect(url_for("todo"))
            else:
                print("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                flash("Acceso rechazado. Verifica tu nombre de usuario y contraseña.", 'error')  
                return render_template("auth/login.html")

        except ValueError as ve:
            print("Contraseña incorrecta:", ve)
            flash("Contraseña incorrecta. Verifica tu nombre de usuario y contraseña.", 'error')
            return render_template("auth/login.html")

        except Exception as e:
            print("Error al interactuar con la base de datos:", e)
            flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo nuevamente.", 'error')
            return render_template("auth/login.html")

    else:
        # Aquí estás renderizando el template login.html
        return render_template("auth/login.html", current_user=current_user)


@app.route("/admin")
@login_required
@admin_required
def admin():
    global current_user_data

    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=0)
    
    # Obtener todas las categorías
    categorias = ModelCategories.get_all_categories(mysql)

    user_type = current_user_data.usertype if current_user_data else None  # Obtener el tipo de usuario
    
    # Obtener el ID del producto más alto
    if productos:  # Verificar si la lista no está vacía
       max_product_id = max([producto.id for producto in productos])
    else:
        max_product_id = 1  # Establecer un valor predeterminado si la lista está vacía

    return render_template("admin.html", productos=productos, usertype=user_type, categorias=categorias, max_product_id=max_product_id)

@app.route("/ventas")
@login_required
@admin_required
def ventas():
    try:
        orders_info = ModelOrder.get_all_orders_details(mysql)  # Obtener información de todas las órdenes

        # Extraer datos individuales de orders_info
        order_ids = []
        user_ids = []
        order_dates = []
        total_amounts = []
        items = []

        for order in orders_info:
            order_ids.append(order['id'])
            user_ids.append(order['user_id'])
            order_dates.append(order['order_date'])
            total_amounts.append(order['total_amount'])
            
            # Extraer los productos para cada orden
            order_items = []
            for item in order['items']:
                order_items.append({
                    'name': item['name'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'image_url': item['image_url']
                })
            items.append(order_items)

        return render_template("ventas.html", order_ids=order_ids, user_ids=user_ids, order_dates=order_dates, total_amounts=total_amounts, items=items)
        
    except Exception as ex:
        print("Error en la vista de ventas:", ex)
        # Manejar el error adecuadamente, por ejemplo, redirigiendo a una página de error o mostrando un mensaje al usuario



@app.route("/root")
@login_required
@root_required
def root():
    try:
        usuarios = ModelUsers.get_all_users(mysql)
        return render_template("root.html", usuarios=usuarios)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        flash("Ocurrió un error al obtener usuarios. Por favor, inténtalo nuevamente.", "error")
        return redirect(url_for("login"))


@app.route("/shop")
@login_required
def shop():
    return render_template("shop.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/login2')
def login2():
    # Renderiza la plantilla login2.html
    return render_template('login2.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
             # Obtener los datos del formulario
            ddi=1
            usuario = request.form['username']
            contra = request.form['password']
            nombre = request.form['full_name']
            tipo = 0

            nuevo_usuario = User(id=ddi,username=usuario,password=contra,fullname=nombre,usertype= tipo)
 
            nuevo_usuario = ModelUsers.add_user(mysql,nuevo_usuario)

            # Retornar algún mensaje de éxito o redireccionar a otra página
            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print("Error al registrar usuario:", e)
            flash("Ocurrió un error al registrar el usuario. Por favor, inténtalo nuevamente.", "error")
            return redirect(url_for('register'))
    else:
        # Redirigir a alguna página en caso de que la solicitud no sea POST
        return redirect(url_for('index'))

@app.route("/agregar_producto", methods=["POST"])
@login_required
@admin_required
def agregar_producto():
    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            precio = float(request.form["precio"])
            imagen_url = request.form["imagen_url"]
            cantidad = int(request.form["cantidad"])
            categoria_id = int(request.form["categoria_id"])  # Asegúrate de obtener el ID de la categoría desde el formulario

            # Crear un nuevo objeto Product
            nuevo_producto = Product(id=None, name=nombre, price=precio, image_url=imagen_url)
            ModelProducts.add_product_with_inventory_and_category(mysql, product_name=nombre, price=precio, image_url=imagen_url, quantity=cantidad, category_id=categoria_id)
            # Llamar a ModelProducts.add_product con el objeto Product y la cantidad
            nuevo_producto = ModelProducts.add_product(mysql, nuevo_producto, cantidad)

            # Obtener la lista de productos del inventario
            productos = ModelProducts.get_all_products2(mysql)
          

            flash("Producto agregado exitosamente.", "success")
            return redirect(url_for("admin"))
        except Exception as e:
            print("Error al agregar producto:", e)
            flash("Ocurrió un error al agregar el producto. Por favor, inténtalo nuevamente.", "error")
            return redirect(url_for("admin"))
    else:
        # Redirigir al panel de administrador si la solicitud no es POST
        return redirect(url_for("admin"))

# Ruta para agregar una nueva categoría
@app.route('/agregar_categoria', methods=['POST'])
@login_required
@admin_required
def agregar_categoria():
    if request.method == "POST":
        try:
            name = request.form["nombre"]
            description = request.form["descripcion"]

            # Crear un nuevo objeto Categories
            nueva_categoria = Categories(id=None, name=name, description=description)

            # Llamar al método add_category con el objeto Categories
            ModelCategories.add_category(mysql, nueva_categoria)

            flash("Categoría agregada exitosamente.", "success")
            return redirect(url_for("admin"))
        except Exception as e:
            print("Error al agregar categoría:", e)
            flash("Ocurrió un error al agregar la categoría. Por favor, inténtalo nuevamente.", "error")
            return redirect(url_for("admin"))
    else:
        # Redirigir al panel de administrador si la solicitud no es POST
        return redirect(url_for("admin"))

@app.route('/update_category/<int:category_id>', methods=['POST'])
def update_category(category_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = Categories(id=category_id, name=name, description=description)
        ModelCategories.update_category(mysql, category)
        return redirect(url_for('admin'))

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        ModelCategories.delete_category(mysql, category_id)
        return redirect(url_for('admin'))

# Ruta para actualizar un producto
@app.route('/modificar_producto/<int:product_id>', methods=['POST'])
def update_product(product_id):
    # Obtener los datos del formulario
    name = request.form['nombre']
    price = request.form['precio']
    image_url = request.form['imagen_url']
    quantity = request.form['cantidad']
    categoria_id = int(request.form['categoria_id'])  # Asegúrate de obtener el ID de la categoría desde el formulario

    # Crear un objeto Product con los datos actualizados
    updated_product = Product(id=product_id, name=name, price=price, image_url=image_url)

    # Actualizar el producto en la base de datos
    ModelProducts.update_product(mysql, updated_product, quantity)

    # Actualizar la categoría del producto
    ModelProducts.update_category(mysql, product_id, categoria_id)

    # Redireccionar a la página de administrador
    return redirect(url_for('admin'))

# Ruta para borrar un producto
@app.route('/borrar_producto/<int:product_id>', methods=['POST'])
def borrar_producto(product_id):
    try:
        ModelProducts.delete_product(mysql, product_id)
        return redirect(url_for('admin'))
    except Exception as ex:
        print("Error al borrar producto:", ex)
        # Aquí puedes redirigir a una página de error o manejar el error de otra manera
        return "Error al borrar producto", 500


@app.route("/admin/usuarios/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_usuario():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            fullname = request.form["fullname"]
            usertype = request.form["usertype"]

            nuevo_usuario = User(id=None, username=username, password=password, fullname=fullname, usertype=usertype)
            ModelUsers.add_user(mysql, nuevo_usuario)

            flash("Usuario creado exitosamente.", "success")
            return redirect(url_for("listar_usuarios"))

        except Exception as e:
            print("Error al crear usuario:", e)
            flash("Ocurrió un error al crear el usuario. Por favor, inténtalo nuevamente.", "error")
            return redirect(url_for("crear_usuario"))
    else:
        return render_template("admin/usuarios/crear_usuario.html")

@app.route("/admin/usuarios")
@login_required
@admin_required
def listar_usuarios():
    try:
        usuarios = ModelUsers.get_all_users(mysql)
        return render_template("root.html", usuarios=usuarios)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        flash("Ocurrió un error al obtener usuarios. Por favor, inténtalo nuevamente.", "error")
        return redirect(url_for("root"))

@app.route('/sobres')
def sobres():

    category_id = 19  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)

    return render_template('sobres.html', productos=productos)


@app.route('/cajasdesobres')
def cajasdesobres():

    category_id = 20  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)
    return render_template('cajasdesobres.html', productos=productos)
@app.route('/elite')
def elite():

    category_id = 21  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)
    return render_template('elite.html', productos=productos)
@app.route('/tematicas')
def tematicas():

    category_id = 22  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)
    return render_template('tematicas.html', productos=productos)
@app.route('/misteriosas')
def misteriosas():

    category_id = 23  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)
    return render_template('misteriosas.html', productos=productos)
@app.route('/todo')
def todo():

    category_id =0  # ID de la categoría que quieres mostrar
    # Obtener la lista de productos del inventario
    productos = ModelProducts.get_all_products(mysql,category_id=category_id)
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)
    return render_template('todo.html', productos=productos)



@app.route('/update_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_user(user_id):
    if request.method == 'POST':
        try:
            username = request.form["username"]
            fullname = request.form["fullname"]
            usertype = request.form["usertype"]

            # Crear un objeto User con los datos actualizados
            updated_user = User(id=user_id, username=username, password='', fullname=fullname, usertype=usertype)

            # Actualizar el usuario en la base de datos
            ModelUsers.update_user(mysql, updated_user)

            flash("Usuario actualizado exitosamente.", "success")
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            print("Error al editar usuario:", e)
            flash("Ocurrió un error al editar el usuario. Por favor, inténtalo nuevamente.", "error")
            return redirect(url_for("listar_usuarios"))
    else:
        # Redirigir al panel de administrador si la solicitud no es POST
        return redirect(url_for("root"))


@app.route("/admin/usuarios/eliminar/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def eliminar_usuario(user_id):
    try:
        ModelUsers.delete_user(mysql, user_id)
        flash("Usuario eliminado exitosamente.", "success")
    except Exception as e:
        print("Error al eliminar usuario:", e)
        flash("Ocurrió un error al eliminar el usuario. Por favor, inténtalo nuevamente.", "error")
    return redirect(url_for("listar_usuarios"))


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    if request.method == "POST":
        try:
            user_id = current_user.id  # Obtener el ID del usuario actual
            product_id = request.json["product_id"]
            quantity = int(request.json["quantity"])

            # Llamar al método add_to_cart del modelo ShoppingCartModel
            success = ShoppingCartModel.add_to_cart(mysql, user_id, product_id, quantity)
            
            if success:
                return jsonify({"success": True, "message": "Producto agregado al carrito exitosamente."})
            else:
                return jsonify({"success": False, "message": "Error: Cantidad solicitada no disponible en el inventario."})

        except Exception as e:
            print("Error al agregar al carrito:", e)
            return jsonify({"success": False, "message": "Ocurrió un error al agregar el producto al carrito. Por favor, inténtalo nuevamente."})
    else:
        # Redirigir a la página principal si la solicitud no es POST
        return redirect(url_for("index"))

@app.route('/update_cart_item_quantity', methods=['POST'])
@login_required
def update_cart_item_quantity():
    if request.method == "POST":
        try:
            cart_item_id = int(request.json["cart_item_id"])
            new_quantity = int(request.json["new_quantity"])
            product_id = int(request.json["product_id"])
            # Llama al método update_cart_item_quantity del modelo ShoppingCartModel
            success = ShoppingCartModel.update_cart_item_quantity(mysql, cart_item_id,product_id, new_quantity)
       
            if success:
                return jsonify({"success": True, "message": "Cantidad actualizada exitosamente en el carrito."})
            else:
                return jsonify({"success": False, "message": "Error: Cantidad solicitada no disponible en el inventario."})

        except Exception as e:
            print("Error al actualizar la cantidad del artículo en el carrito:", e)
            return jsonify({"success": False, "message": "Ocurrió un error al actualizar la cantidad del artículo en el carrito. Por favor, inténtalo nuevamente."})
    else:
        # Redirigir a la página principal si la solicitud no es POST
        return redirect(url_for("index"))


@app.route('/shopping_cart')
def shopping_cart():
    # Obtener los productos del carrito de compras del usuario actual
    user_id = current_user.id  # Debes implementar esta función
    cart_items = ShoppingCartModel.get_cart_items(mysql, user_id)

    # Crear una lista de diccionarios con los datos de los elementos del carrito
    cart_data = []
    for item in cart_items:
        cart_data.append({
             'cart_item_id' : item.cart_item_id,
             'product_id' : item.product_id,
            'product_name': item.product_name,
            'image_url': item.image_url,
            'unit_price': item.unit_price,
            'quantity': item.quantity
        })

    # Devolver los datos del carrito como JSON
    return jsonify(cart_data)

@app.route("/get_order_products", methods=["GET"])
def get_order_products():
    # Obtener el ID de la orden de la solicitud GET
    order_id = request.args.get("order_id")
    
    # Aquí puedes usar la función que proporcionaste para obtener los detalles de la orden según el ID
    order_info = ModelOrder.get_order_details(mysql, order_id)
    
    if order_info:
        products = order_info["items"]
        print("Productos para la orden:", order_id)
        for product in products:
            print("Producto:", product)
        return jsonify({"products": products})
    else:
        return jsonify({"products": []})  # Enviar una lista vacía si no se encuentra la orden





@app.route('/remove_cart_item/<int:cart_item_id>', methods=['POST'])
def remove_cart_item(cart_item_id):
    # Aquí puedes usar cart_item_id directamente para eliminar el artículo del carrito
    ShoppingCartModel.remove_cart(mysql, cart_item_id)
    return jsonify(success=True)

@app.route('/realizar_venta', methods=['POST'])
@login_required
def realizar_venta():
    if request.method == "POST":
        try:
            user_id = current_user.id  # Obtener el ID del usuario actual

            # Llamar al método realizar_venta del modelo ShoppingCartModel
            ShoppingCartModel.realizar_venta(mysql, user_id)
            
            # Limpiar el carrito después de realizar la venta
            ShoppingCartModel.clear_cart_for_user(mysql, user_id)
            
            return jsonify({"success": True, "message": "Venta realizada con éxito."})

        except Exception as e:
            print("Error al realizar la venta:", e)
            return jsonify({"success": False, "message": "Ocurrió un error al realizar la venta. Por favor, inténtalo nuevamente."})
    else:
        # Redirigir a la página principal si la solicitud no es POST
        return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=False)
