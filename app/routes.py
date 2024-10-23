import bcrypt
from flask import render_template, url_for, flash, redirect

from app import app, bcrypt, db
from app.forms import RegistrationForm, InventoryItemForm
from app.models import User, InventoryItem


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Password Hashing using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/item/new", methods=['GET', 'POST'])
def new_item():
    form = InventoryItemForm()
    if form.validate_on_submit():
        item = InventoryItem(name=form.name.data, quantity=form.quantity.data, price=form.price.data, user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been added to Inventory', 'success')
        return redirect(url_for('inventory'))
    return render_template('create_item.html', form=form)

@app.route("/inventory")
def inventory():
    items = InventoryItem.query.all()
    return render_template('inventory.html', items=items)