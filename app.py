from flask import Flask, render_template, request, jsonify, session as login_session,redirect, url_for, flash
from database import Base, User, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_google_auth',methods=['GET'])
def processGoogleAuth():
    name = request.args.get('name')
    email = request.args.get('email')
    if session.query(User).filter_by(email=email).count() != 0:
        user = session.query(User).filter_by(email=email).one()
    else:
        user = User(name=name, email=email)
    session.add(user)
    session.commit()
    login_session['name'] = user.name
    login_session['email'] = user.email
    login_session['user_id'] = user.id
    return jsonify(success=True)

@app.route('/logout')
def logout():
    login_session.clear()
    return jsonify(success=True)

@app.route('/category/create')
def categoryCreatePage():
    if(isGuestUser()):
        return redirect(url_for('index'))
    return render_template('category/create.html')

@app.route('/category/save',methods=['POST'])
def saveCategory():
    categoryName = request.form.get('c_name')
    if session.query(Category).filter_by(name=categoryName).count() != 0:
        flash("Category already added, you can add items to it.",'info')
    else:
        category = Category(name=categoryName, user_id=login_session.get('user_id'))
        session.add(category)
        session.commit()
        flash("Category %s successfully added." % (categoryName),'success')
    return redirect(url_for('index'))

@app.route('/categories')
def showAllCategories():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])

@app.route('/category/<int:category_id>/items')
def showAllItemsGivenCategoryId(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])

@app.route('/category/<int:category_id>/item')
def addItemToCategoryPage(category_id):
    if(isGuestUser()):
        return redirect(url_for('index'))
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('item/create.html',category=category)

@app.route('/category/<int:category_id>/item/save',methods=['POST'])
def saveItemToCategory(category_id):
    itemName = request.form.get('i_name')
    itemDescription = request.form.get('i_description')
    category = session.query(Category).filter_by(id=category_id).one()
    item = Item(name=itemName,description=itemDescription,category_id=category.id,user_id=login_session.get('user_id'))
    session.add(item)
    session.commit()
    flash("Item %s successfully added for the category %s" % (item.name,category.name),'success')
    return redirect(url_for('index'))

@app.route('/item/<int:item_id>/delete',methods=['POST'])
def deleteItem(item_id):
    if(isGuestUser()):
        return redirect(url_for('index'))
    item = session.query(Item).filter_by(id=item_id,user_id=login_session.get('user_id')).one()
    session.delete(item)
    session.commit()
    return jsonify(success=True)

@app.route('/item/<int:item_id>/edit')
def editItemPage(item_id):
    if(isGuestUser()):
        return redirect(url_for('index'))
    item = session.query(Item).filter_by(id=item_id,user_id=login_session.get('user_id')).one()
    categories = session.query(Category).all()
    return render_template('item/edit.html',item=item,categories=categories)

@app.route('/item/<int:item_id>/edit/apply',methods=['POST'])
def applyItemChanges(item_id):
    newItemName = request.form.get('i_name')
    newItemDescription = request.form.get('i_description')
    newCategoryId = request.form.get('i_category_id')
    item = session.query(Item).filter_by(id=item_id,user_id=login_session.get('user_id')).one()
    item.name = newItemName
    item.description = newItemDescription
    item.category_id = newCategoryId
    session.add(item)
    session.commit()
    flash('The item has been successfully edited!','success')
    return redirect(url_for('index'))

def isGuestUser():
      if login_session.get('user_id') is None:
        flash('You must login to use this feature!','danger')
        return True
      return False

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)