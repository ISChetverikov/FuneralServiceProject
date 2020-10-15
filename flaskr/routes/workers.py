from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Workers import Worker, WorkersTable

CAR_TABLE_NAME = 'worker'

@routes.route('/worker/edit/<int:id>', methods=['GET'])
def edit_worker(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT * FROM worker WHERE workerid=%s";
        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        return render_template("edit_worker.html", worker=Worker(*row))
    # except Exception as e:
        # return render_template("500.html", e=e)
    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/worker/update/', methods=['POST'])
def update_worker():
    conn = None
    cursor = None
    try:
        passport_number = request.form['inputPassportNumber']
        fullname = request.form['inputFullname']
        id = request.form['id']

        error_validation = ""
        if len(passport_number) > 10 :
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(fullname) > 100:
            error_validation += "Fullname of car must be a string with number of symbols up to 100"

        if error_validation:
            worker = Worker(id, fullname, passport_number)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_worker.html", worker=worker)

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM worker WHERE workerid=%s";
        cursor.execute(sql, (id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("500.html", e="Server cannot find worker is being updated")

        sql = "UPDATE worker SET WorkerPassportNumber=%s, WorkerFullName=%s WHERE workerid=%s"
        cursor.execute(sql, (passport_number, fullname, id));
        conn.commit()
        flash('Worker has been successfully updated');
        return redirect(url_for('.workers'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()

@routes.route('/workers/')
def workers():
    cursor = mysql.get_db().cursor()
    sql = "SELECT * FROM worker"
    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    workers = WorkersTable(list(map(lambda x: Worker(*x), rows)))
    cursor.close()

    workers.border = True
    return render_template('workers.html', table=workers)

@routes.route('/worker/delete/<int:id>')
def delete_worker(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM worker WHERE workerid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Worker has been successfully deleted')
        return redirect(url_for('.workers'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/worker/create/', methods=['POST'])
def create_worker():
    conn = None
    cursor = None
    try:
        passport_number = request.form['inputPassportNumber']
        fullname = request.form['inputFullname']

        error_validation = ""
        if len(passport_number) > 10:
            error_validation += "Passport number must be a string with number of symbols up to 10"

        if len(fullname) > 100:
            error_validation += "Fullname of car must be a string with number of symbols up to 100"

        if error_validation:
            worker = Worker(id, fullname, passport_number)
            flash("Server validation failed: " + error_validation)
            return render_template("edit_worker.html", worker=worker)

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO worker (WorkerPassportNumber, WorkerFullName) VALUES(%s, %s)"
        cursor.execute(sql, (passport_number, fullname))
        conn.commit()
        flash('Worker has been successfully created')
        return redirect(url_for('.workers'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/worker/new/', methods=['GET'])
def show_create_worker_dialog():
    return render_template("new_worker.html")
