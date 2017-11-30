# Message Flashing on Web Server
from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
               newitem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
               session.add(newitem)
               session.commit()
               return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
         return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    edititem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
               if request.form['name']:
                          edititem.name = request.form['name']
               session.add(edititem)
               session.commit()
               return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
         return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, i=edititem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    delitem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
               session.delete(delitem)
               session.commit()
               return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
         return render_template('deletemenuitem.html', i = delitem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

