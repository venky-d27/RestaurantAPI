from flask import Flask, jsonify,request
from flask_uuid import FlaskUUID
from flask_sqlalchemy import SQLAlchemy
import uuid
app=Flask(__name__)
dishlist=[{"dish_id":uuid.uuid1(),"dish_name": "idly","dish_cost": "45.00"}]

@app.route('/dish',methods=["GET","POST","DELETE"])
def dish():
    if request.method=="GET":
        return jsonify(dishlist)
    if request.method=="POST":
        dish_id= uuid.uuid1()
        dish_name=request.form['dish_name']
        dish_cost=request.form['dish_cost']
        dishlist.append({'dish_id':dish_id,'dish_name':dish_name,'dish_cost':dish_cost})
        #dishlist.append({'dish_id':request.form['dish_id'],'dish_name':request.form['dish_name'],'dish_cost':request.form['dish_cost']})
        return "Posted"
    if request.method=="DELETE":
        dishlist.clear()
        return "deleted successfully"

@app.route('/dish/<uuid:dish_id>',methods=["GET","PUT","DELETE"])
def get_dish(dish_id):
    for i in range(len(dishlist)):
        if dishlist[i]['dish_id']==dish_id:
            id=i
            print(id)
            break
    if request.method=="GET":
        return jsonify(dishlist[id])
    if request.method=="PUT":
        dishlist[id]["dish_name"] = request.form['dish_name']
        dishlist[id]["dish_cost"] = request.form['dish_cost']
        return jsonify(dishlist[id])
    if request.method=="DELETE":
        dishlist.pop(id)
        return "Deleted Sucessfully"



if __name__=="__main__":
    app.run(debug=True)

