from flask import Flask, jsonify,request
from flask_uuid import FlaskUUID
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db=SQLAlchemy(app)
dishlist=[{"dish_id":uuid.uuid1(),"dish_name": "idly","dish_cost": "45.00"}]
class User(db.Model):
    __tablename__ = 'User'
    username = db.Column(db.String(50),primary_key=True)
    password = db.Column(db.String(100),unique=True)
    def __init__(self,username,password):
        self.username=username
        self.password=password

class Dish(db.Model):
    __tablename__='Dish'

    dish_id = db.Column(db.String(500),primary_key=True)
    dish_name = db.Column(db.String(80),index=True,unique=True,nullable=False)
    dish_cost = db.Column(db.String(80))
    dish_image = db.Column(db.String(200))
    def __init__(self,dish_id,dish_name,dish_cost,dish_image):
        self.dish_id=dish_id
        self.dish_name=dish_name
        self.dish_cost = dish_cost
        self.dish_image=dish_image

db.create_all()


@app.route('/dish',methods=["GET","POST","DELETE"])
def dish():
    username = request.headers.get('username')
    password = request.headers.get('password')
    if db.session.query(db.exists().where(User.username == username)).scalar():
        result=User.query.filter_by(username=username).first()
        if result.password==password:
            pass
        else:
            return "Password Wrong"
    else:
        result = User(username,password)
        db.session.add(result)
        db.session.commit()
    if request.method=="GET":
        result=Dish.query.all()
        l=[]
        for i in result:
            l.append({'dish_id':i.dish_id,'dish_name':i.dish_name,'dish_cost':i.dish_cost,'dish_image':i.dish_image})
        return jsonify(l)
    if request.method=="POST":
        dish_id= str(uuid.uuid1().int)
        dish_name=request.form['dish_name']
        dish_cost=request.form['dish_cost']
        dish_image = request.files["dish_image"]
        dish_image.save(os.path.join(dish_image.filename))
        dish = Dish(dish_id,dish_name, dish_cost, dish_image.filename)
        db.session.add(dish)
        db.session.commit()
        return jsonify(dish.dish_id)
    #dishlist.append({'dish_id':request.form['dish_id'],'dish_name':request.form['dish_name'],'dish_cost':request.form['dish_cost']})

    if request.method=="DELETE":
        Dish.query.delete()
        db.session.commit()
        return "Deleted successfully"

@app.route('/dish/<string:dish_id>',methods=["GET","PUT","DELETE"])
def get_dish(dish_id):
    username = request.headers.get('username')
    password = request.headers.get('password')
    if db.session.query(db.exists().where(User.username == username)).scalar():
        result = User.query.filter_by(username=username).first()
        if result.password == password:
            pass
        else:
            return "Password Wrong"
    else:
        result = User(username, password)
        db.session.add(result)
        db.session.commit()
    if request.method=="GET":
        result = Dish.query.filter_by(dish_id=dish_id).first()
        return jsonify({'dish_id':result.dish_id,'dish_name':result.dish_name,'dish_cost':result.dish_cost,'dish_image':result.dish_image})
    if request.method=="PUT":
        result = Dish.query.get(dish_id)
        result.dish_name=request.form['dish_name']
        result.dish_cost=request.form['dish_cost']
        result.dish_image = request.files["dish_image"].filename
        db.session.commit()
        return jsonify(result.dish_id)
    if request.method=="DELETE":
        Dish.query.filter_by(dish_id=dish_id).delete()
        db.session.commit()
        return "Deleted Sucessfully"



if __name__=="__main__":
    app.run(debug=True)



