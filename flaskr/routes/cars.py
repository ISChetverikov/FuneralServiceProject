from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Cars import CarsTable, Car

CAR_TABLE_NAME = 'car'

@routes.route('/car/edit/<int:id>', methods=['GET'])
def edit_car(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT * FROM car WHERE carid=%s";
        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        return render_template("edit_car.html", car=Car(*row))
    # except Exception as e:
        # return render_template("500.html", e=e)
    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/car/update/', methods=['POST'])
def update_car():
    conn = None
    cursor = None
    try:
        registration_number = request.form['inputRegistrationNumber']
        type = request.form['inputType']
        model = request.form['inputModel']
        id = request.form['id']

        error_validation = ""
        if len(registration_number) > 20 or len(registration_number)<5 :
            error_validation += "Registration number must be a string with number of symbols from 5 to 20"

        if len(type) > 45:
            error_validation += "Type of car must be a string with number of symbols up to 45"

        if len(model) > 45:
            error_validation += "Type of car must be a string with number of symbols up to 45"

        if error_validation:
            car = Car(id, registration_number, type, model)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_car.html", car=car)

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM car WHERE carid=%s";
        cursor.execute(sql, (id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("500.html", e="Server cannot find car is being updated")

        sql = "UPDATE car SET RegistrationNumber=%s, CarType=%s, CarModel=%s WHERE carid=%s"
        cursor.execute(sql, (registration_number, type, model, id));
        conn.commit()
        flash('Car has been successfully updated');
        return redirect(url_for('.cars'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()

@routes.route('/cars/')
def cars():
    cursor = mysql.get_db().cursor()
    sql = "SELECT * FROM car"
    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    cars = CarsTable(list(map(lambda x: Car(*x), rows)))
    cursor.close()

    cars.border = True
    return render_template('cars.html', table=cars)

@routes.route('/car/delete/<int:id>')
def delete_car(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM CAR WHERE carid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Car has been successfully deleted')
        return redirect(url_for('.cars'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/car/create/', methods=['POST'])
def create_car():
    conn = None
    cursor = None
    try:
        registration_number = request.form['inputRegistrationNumber']
        type = request.form['inputType']
        model = request.form['inputModel']

        error_validation = ""
        if len(registration_number) > 20 or len(registration_number) < 5:
            error_validation += "Registration number must be a string with number of symbols from 5 to 20"

        if len(type) > 45:
            error_validation += "Type of car must be a string with number of symbols up to 45"

        if len(model) > 45:
            error_validation += "Type of car must be a string with number of symbols up to 45"

        if error_validation:
            car = Car(id, registration_number, type, model)
            flash("Server validation failed: " + error_validation)
            return render_template("new_car.html", car=car)

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO car (RegistrationNumber, CarType, CarModel) VALUES(%s, %s, %s)"
        cursor.execute(sql, (registration_number, type, model))
        conn.commit()
        flash('Car has been successfully created')
        return redirect(url_for('.cars'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()

@routes.route('/car/new/', methods=['GET'])
def show_create_car_dialog():
    return render_template("new_car.html")
