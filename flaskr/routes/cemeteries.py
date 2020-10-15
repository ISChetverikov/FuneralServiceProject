from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Cemeteries import Cemetery, CemeteriesTable

CAR_TABLE_NAME = 'cemetery'

@routes.route('/cemetery/edit/<int:id>', methods=['GET'])
def edit_cemetery(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT * FROM cemetery WHERE cemeteryid=%s";
        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        return render_template("edit_cemetery.html", cemetery=Cemetery(*row))
    # except Exception as e:
        # return render_template("500.html", e=e)
    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/cemetery/update/', methods=['POST'])
def update_cemetery():
    conn = None
    cursor = None
    try:
        address = request.form['inputAddress']
        name = request.form['inputName']
        places = request.form['inputPlaces']
        phone = request.form['inputPhone']
        id = request.form['id']

        error_validation = ""
        if len(name) > 45 :
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(address) > 100:
            error_validation += "Name of car must be a string with number of symbols up to 100"

        if len(phone) > 100:
            error_validation += "Phone must be a string with number of symbols up to 20"

        if error_validation:
            cemetery = Cemetery(id, name, address, places, phone)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_cemetery.html", cemetery=cemetery)

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM cemetery WHERE cemeteryid=%s";
        cursor.execute(sql, (id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("500.html", e="Server cannot find cemetery is being updated")

        sql = "UPDATE cemetery SET CemeteryAdress=%s, CemeteryName=%s, CemeteryFreePlacesNumber=%s, CemeteryPhoneNumber=%s WHERE cemeteryid=%s"
        cursor.execute(sql, (address, name, places, phone, id));
        conn.commit()
        flash('Cemetery has been successfully updated');
        return redirect(url_for('.cemeteries'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()

@routes.route('/cemeteries/')
def cemeteries():
    cursor = mysql.get_db().cursor()
    sql = "SELECT * FROM cemetery"
    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    cemeteries = CemeteriesTable(list(map(lambda x: Cemetery(*x), rows)))
    cursor.close()

    cemeteries.border = True
    return render_template('cemeteries.html', table=cemeteries)

@routes.route('/cemetery/delete/<int:id>')
def delete_cemetery(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM cemetery WHERE cemeteryid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Cemetery has been successfully deleted')
        return redirect(url_for('.cemeteries'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/cemetery/create/', methods=['POST'])
def create_cemetery():
    conn = None
    cursor = None
    try:
        address = request.form['inputAddress']
        name = request.form['inputName']
        places = request.form['inputPlaces']
        phone = request.form['inputPhone']

        error_validation = ""
        if len(address) > 10:
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(name) > 100:
            error_validation += "Name of car must be a string with number of symbols up to 100"

        if len(phone) > 100:
            error_validation += "Phone must be a string with number of symbols up to 20"

        if error_validation:
            cemetery = Cemetery(12, name, address, places, phone)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_cemetery.html", cemetery=cemetery)

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO cemetery (CemeteryAdress, CemeteryName, CemeteryFreePlacesNumber, CemeteryPhoneNumber) VALUES(%s, %s, %s, %s)"
        cursor.execute(sql, (address, name, places, phone))
        conn.commit()
        flash('Cemetery has been successfully created')
        return redirect(url_for('.cemeteries'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/cemetery/new/', methods=['GET'])
def show_create_cemetery_dialog():
    return render_template("new_cemetery.html")
