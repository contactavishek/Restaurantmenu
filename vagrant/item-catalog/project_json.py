# Responding with JSON
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint(GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])


# ADDING JSON ENDPOINT HERE
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = menuitem.serialize)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
               newitem = MenuItem(name = request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
               session.add(newitem)
               session.commit()
               flash("New Menu Item Created !")
               return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
         return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    edititem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
               if request.form['name']:
                          edititem.name = request.form['name']
               if request.form['description']:
                          edititem.description = request.form['name']
               if request.form['price']:
                          edititem.price = request.form['price']
               if request.form['course']:
                          edititem.course = request.form['course']
               session.add(edititem)
               session.commit()
               flash("A Menu Item has been Edited!")
               return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
         return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, i=edititem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    delitem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
               session.delete(delitem)
               session.commit()
               flash("A Menu Item has been Deleted!")
               return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
         return render_template('deletemenuitem.html', i = delitem)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

