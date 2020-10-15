from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Funerals import FuneralsTable, Funeral
from flaskr.forms.new_funeral import FuneralForm


@routes.route('/funerals/')
def funerals():
    cursor = mysql.get_db().cursor()
    sql = "SELECT FuneralId, FuneralDate, FuneralStatus, cemetery.CemeteryName, funeral.cemeteryId, deceased.DeceasedFullName, funeral.DeceasedId " \
            "FROM funeral " \
            "LEFT JOIN cemetery ON funeral.cemeteryId = cemetery.cemeteryId " \
            "LEFT JOIN deceased ON funeral.deceasedId = deceased.deceasedId "

    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    funerals = FuneralsTable(list(map(lambda x: Funeral(*x), rows)))
    cursor.close()

    funerals.border = True
    return render_template('funerals.html', table=funerals)


@routes.route('/funeral/new/', methods=['GET'])
def show_create_funeral_dialog():
    cursor = mysql.get_db().cursor()

    sql = "SELECT CemeteryId, CemeteryName FROM Cemetery"
    cursor.execute(sql)
    cemetery_rows = cursor.fetchall()  # tuples

    sql = "SELECT DeceasedId, DeceasedFullName FROM deceased"
    cursor.execute(sql)
    clients_rows = cursor.fetchall()

    cursor.close()

    form = FuneralForm(cemeteries_list=cemetery_rows, client_list=clients_rows);
    return render_template("new_funeral.html", form=form, url=url_for('.create_funeral'), action='creation')


@routes.route('/funeral/edit/<int:id>', methods=['GET'])
def edit_funeral(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT FuneralId, FuneralDate, FuneralStatus, cemetery.CemeteryName, funeral.cemeteryId, deceased.DeceasedFullName, funeral.DeceasedId" \
              " FROM funeral " \
              "LEFT JOIN cemetery ON funeral.cemeteryId = cemetery.cemeteryId " \
              "LEFT JOIN deceased ON funeral.deceasedId = deceased.deceasedId " \
              "WHERE funeralid=%s"

        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        sql = "SELECT CemeteryId, CemeteryName FROM Cemetery"
        cursor.execute(sql)
        cemetery_rows = cursor.fetchall()

        sql = "SELECT DeceasedId, DeceasedFullName FROM deceased"
        cursor.execute(sql)
        clients_rows = cursor.fetchall()

        funeral = Funeral(*row)
        form = FuneralForm(funeral=funeral, client_list=clients_rows, cemeteries_list=cemetery_rows, cemeteries=funeral.cemetery_id, clients=funeral.client_id)

        return render_template("new_funeral.html", form=form, url=url_for('.update_funeral'), action='edit')

    finally:
        if cursor is not None:
            cursor.close()


@routes.route('/funeral/update/', methods=['POST'])
def update_funeral():
    conn = None
    cursor = None
    try:
        print(request.form)
        status = request.form['status']
        date = request.form['date']

        cemetery_id = request.form['cemeteries']
        client_id = request.form['clients']
        id = request.form['id']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "UPDATE funeral SET " \
              "FuneralDate=%s, funeralstatus=%s, " \
              "CemeteryId=%s, DeceasedId=%s" \
              "WHERE funeralid=%s"
        cursor.execute(sql, (date, status, cemetery_id, client_id, id));
        conn.commit()
        flash('Funeral has been successfully updated');
        return redirect(url_for('.funerals'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/funeral/delete/<int:id>')
def delete_funeral(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM funeral WHERE funeralid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Funeral has been successfully deleted')
        return redirect(url_for('.funerals'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/funeral/create/', methods=['POST'])
def create_funeral():
    conn = None
    cursor = None
    try:
        status = request.form['status']
        date = request.form['date']

        client_id = request.form['clients']
        cemetery_id = request.form['cemeteries']
        id = request.form['id']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO funeral (" \
              "funeralDate, funeralstatus, " \
              "CemeteryId, DeceasedId ) " \
              "VALUES (%s, %s, %s, %s)"
        cursor.execute(sql,
                       (date, status, cemetery_id, client_id));
        conn.commit()
        flash('Funeral has been successfully updated');
        return redirect(url_for('.funerals'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()
