from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, InventoryItemForm
from app.models import User, InventoryItem

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/inventory')
@login_required
def inventory():
    items = InventoryItem.query.filter_by(user_id=current_user.id).all()
    return render_template('inventory.html', title='Inventory', items=items)

@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = InventoryItemForm()
    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            quantity=form.quantity.data,
            price=form.price.data,
            user_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Item has been added!', 'success')
        return redirect(url_for('inventory'))
    return render_template('create_item.html', title='New Item',
                         form=form, legend='New Item')

@app.route('/item/<int:item_id>/update', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    form = InventoryItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.price = form.price.data
        db.session.commit()
        flash('Item has been updated!', 'success')
        return redirect(url_for('inventory'))
    elif request.method == 'GET':
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.price.data = item.price
    return render_template('create_item.html', title='Update Item',
                         form=form, legend='Update Item')

@app.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted!', 'success')
    return redirect(url_for('inventory'))
