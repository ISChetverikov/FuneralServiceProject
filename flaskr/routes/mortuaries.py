from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Mortuaries import Mortuary, MortuariesTable

CAR_TABLE_NAME = 'mortuary'

@routes.route('/mortuary/edit/<int:id>', methods=['GET'])
def edit_mortuary(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT * FROM mortuary WHERE mortuaryid=%s";
        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        return render_template("edit_mortuary.html", mortuary=Mortuary(*row))
    # except Exception as e:
        # return render_template("500.html", e=e)
    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/mortuary/update/', methods=['POST'])
def update_mortuary():
    conn = None
    cursor = None
    try:
        address = request.form['inputAddress']
        name = request.form['inputName']
        id = request.form['id']

        error_validation = ""
        if len(address) > 10 :
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(name) > 100:
            error_validation += "Name of car must be a string with number of symbols up to 100"

        if error_validation:
            mortuary = Mortuary(id, name, address)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_mortuary.html", mortuary=mortuary)

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM mortuary WHERE mortuaryid=%s";
        cursor.execute(sql, (id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("500.html", e="Server cannot find mortuary is being updated")

        sql = "UPDATE mortuary SET MortuaryAdress=%s, MortuaryName=%s WHERE mortuaryid=%s"
        cursor.execute(sql, (address, name, id));
        conn.commit()
        flash('Mortuary has been successfully updated');
        return redirect(url_for('.mortuaries'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()

@routes.route('/mortuaries/')
def mortuaries():
    cursor = mysql.get_db().cursor()
    sql = "SELECT * FROM mortuary"
    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    mortuaries = MortuariesTable(list(map(lambda x: Mortuary(*x), rows)))
    cursor.close()

    mortuaries.border = True
    return render_template('mortuaries.html', table=mortuaries)

@routes.route('/mortuary/delete/<int:id>')
def delete_mortuary(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM mortuary WHERE mortuaryid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Mortuary has been successfully deleted')
        return redirect(url_for('.mortuaries'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/mortuary/create/', methods=['POST'])
def create_mortuary():
    conn = None
    cursor = None
    try:
        address = request.form['inputAddress']
        name = request.form['inputName']

        error_validation = ""
        if len(address) > 10:
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(name) > 100:
            error_validation += "Name of car must be a string with number of symbols up to 100"

        if error_validation:
            mortuary = Mortuary(12, name, address)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_mortuary.html", mortuary=mortuary)

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO mortuary (MortuaryAdress, MortuaryName) VALUES(%s, %s)"
        cursor.execute(sql, (address, name))
        conn.commit()
        flash('Mortuary has been successfully created')
        return redirect(url_for('.mortuaries'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/mortuary/new/', methods=['GET'])
def show_create_mortuary_dialog():
    return render_template("new_mortuary.html")
