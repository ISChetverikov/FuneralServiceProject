from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.db import mysql
from flaskr.models.Clients import ClientsTable, Client
from flaskr.forms.new_client import ClientForm

@routes.route('/clients/')
def clients():
    cursor = mysql.get_db().cursor()
    sql = "SELECT DeceasedId, DeceasedFullName, DeceasedPassportNumber, DeceasedBirthDate, DeceasedDeathDate, DeceasedSizeMeasurements," \
          "DeceasedWeight, CemeteryName, MortuaryName, deceased.cemeteryId, deceased.mortuaryId" \
          " FROM deceased " \
            "LEFT JOIN cemetery ON deceased.cemeteryId = cemetery.cemeteryId " \
            "LEFT JOIN mortuary ON deceased.mortuaryId = mortuary.mortuaryId"

    cursor.execute(sql)
    rows = cursor.fetchall() # tuples
    clients = ClientsTable(list(map(lambda x: Client(*x), rows)))
    cursor.close()

    clients.border = True
    return render_template('clients.html', table=clients)

@routes.route('/client/new/', methods=['GET'])
def show_create_client_dialog():
    cursor = mysql.get_db().cursor()
    sql = "SELECT MortuaryId, MortuaryName FROM Mortuary"
    cursor.execute(sql)
    mortuary_rows = cursor.fetchall()  # tuples

    sql = "SELECT CemeteryId, CemeteryName FROM Cemetery"
    cursor.execute(sql)
    cemetery_rows = cursor.fetchall()  # tuples

    cursor.close()

    form = ClientForm(mortuaries_list=mortuary_rows, cemeteries_list=cemetery_rows);
    return render_template("new_client.html", form=form, url=url_for('.create_client'), action='creation')

@routes.route('/client/edit/<int:id>', methods=['GET'])
def edit_client(id):
    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT DeceasedId, DeceasedFullName, DeceasedPassportNumber, DeceasedBirthDate, DeceasedDeathDate, DeceasedSizeMeasurements," \
              "DeceasedWeight, CemeteryName, MortuaryName, deceased.cemeteryId, deceased.mortuaryId" \
              " FROM deceased " \
              "LEFT JOIN cemetery ON deceased.cemeteryId = cemetery.cemeteryId " \
              "LEFT JOIN mortuary ON deceased.mortuaryId = mortuary.mortuaryId " \
              "WHERE deceasedid=%s"

        cursor.execute(sql,(id,))
        row = cursor.fetchone()  # tuples
        if row is None:
            return render_template("404.html")

        sql = "SELECT MortuaryId, MortuaryName FROM Mortuary"
        cursor.execute(sql)
        mortuary_rows = cursor.fetchall()  # tuples

        sql = "SELECT CemeteryId, CemeteryName FROM Cemetery"
        cursor.execute(sql)
        cemetery_rows = cursor.fetchall()

        client = Client(*row)
        form = ClientForm(client=client, mortuaries_list=mortuary_rows, cemeteries_list=cemetery_rows,
                          cemeteries=client.cemetery_id, mortuaries=client.mortuary_id)

        return render_template("new_client.html", form=form, url=url_for('.update_client'), action='edit')

    finally:
        if cursor is not None:
            cursor.close()


@routes.route('/client/update/', methods=['POST'])
def update_client():
    conn = None
    cursor = None
    try:
        print(request.form)
        fullname = request.form['fullname']
        passport_number = request.form['passport_number']
        birthday = request.form['birthday']
        deathday = request.form['deathday']
        size = request.form['size']
        weight = request.form['weight']
        cemetery_id = request.form['cemeteries']
        mortuary_id = request.form['mortuaries']
        id = request.form['id']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "UPDATE deceased SET " \
              "DeceasedFullName=%s, DeceasedPassportNumber=%s, " \
              "DeceasedBirthDate=%s, DeceasedDeathDate=%s, " \
              "DeceasedSizeMeasurements=%s, DeceasedWeight=%s, " \
              "CemeteryId=%s, MortuaryId=%s " \
              "WHERE deceasedid=%s"
        cursor.execute(sql, (fullname, passport_number, birthday, deathday, size, weight, cemetery_id, mortuary_id, id));
        conn.commit()
        flash('Client has been successfully updated');
        return redirect(url_for('.clients'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/client/delete/<int:id>')
def delete_client(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "DELETE FROM deceased WHERE deceasedid=%s"
        cursor.execute(sql, (id))
        conn.commit()
        flash('Client has been successfully deleted')
        return redirect(url_for('.clients'))

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()


@routes.route('/client/create/', methods=['POST'])
def create_client():
    conn = None
    cursor = None
    try:
        fullname = request.form['fullname']
        passport_number = request.form['passport_number']
        birthday = request.form['birthday']
        deathday = request.form['deathday']
        size = request.form['size']
        weight = request.form['weight']
        cemetery_id = request.form['cemeteries']
        mortuary_id = request.form['mortuaries']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO deceased (" \
              "DeceasedFullName, DeceasedPassportNumber, " \
              "DeceasedBirthDate, DeceasedDeathDate, " \
              "DeceasedSizeMeasurements, DeceasedWeight, " \
              "CemeteryId, MortuaryId ) " \
              "VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (fullname, passport_number, birthday, deathday, size, weight, cemetery_id, mortuary_id));
        conn.commit()
        flash('Client has been successfully updated');
        return redirect(url_for('.clients'));

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            cursor.close()
