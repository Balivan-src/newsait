from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Товары (в реальном проекте используйте базу данных)
products = [
    {"id": 1, "name": "1 день", "price": 220},
    {"id": 2, "name": "7 дней", "price": 610},
    {"id": 3, "name": "30 дней", "price": 1320},
    {"id": 3, "name": "Lifetime", "price": 2250},
]

# Главная страница
@app.route('/')
def home():
    return render_template('index.html', products=products)

# Добавление товара в корзину
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Проверяем, есть ли товар уже в корзине
    for item in session['cart']:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        # Если товара нет в корзине, добавляем его
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            session['cart'].append({"id": product_id, "name": product['name'], "price": product['price'], "quantity": 1})

    flash('Товар добавлен в корзину!', 'success')
    return redirect(url_for('home'))

# Корзина
@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []

    # Подсчёт общей суммы
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)

# Оформление заказа
@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Ваша корзина пуста!', 'danger')
        return redirect(url_for('cart'))

    # Очищаем корзину после оформления заказа
    session.pop('cart', None)
    flash('Заказ успешно оформлен! Спасибо за покупку.', 'success')
    return render_template('checkout.html')

if __name__ == "__main__":
    app.run(debug=True)