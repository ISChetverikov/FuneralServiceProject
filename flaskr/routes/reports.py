from . import routes

from flask import request
from flask import flash
from flask import redirect, url_for
from flask import render_template
from flaskr.forms.select_form import SelectForm
from flaskr.db import mysql
from flaskr.models.Reports import FreeWorker, FreeWorkersTable, IncompletedFuneralsTable, IncompletedFuneral, ShortClient, ShortClientsTable

@routes.route('/freeworkers/')
def get_free_workers():
    cursor = mysql.get_db().cursor()
    sql = "CALL GetFreeWorkers()"
    cursor.execute(sql)
    rows = cursor.fetchall()
    workers = FreeWorkersTable(list(map(lambda x: FreeWorker(*x), rows)))
    cursor.close()

    workers.border = True
    return render_template('Reports.html', table=workers, name="FreeWorkers")

@routes.route('/incompletedfunerals/')
def get_incompleted_funerals():
    cursor = mysql.get_db().cursor()
    sql = "CALL GetIncompletedFunerals()"
    cursor.execute(sql)
    rows = cursor.fetchall()
    funerals = IncompletedFuneralsTable(list(map(lambda x: IncompletedFuneral(*x), rows)))
    cursor.close()

    funerals.border = True
    return render_template('Reports.html', table=funerals, name="IncompletedFunerals")

@routes.route('/freeplaces/', methods=['POST', 'GET'])
def get_freeplaces():

    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT CemeteryId, CemeteryName FROM cemetery"
        cursor.execute(sql)
        cemeteries_rows = cursor.fetchall()
        form = SelectForm("Cemetery", select_list=cemeteries_rows)

        if request.method == 'GET':
            return render_template("ReportsIntParam.html", form=form, url=url_for('.get_freeplaces'), name='Free places')

        id = request.form['select']
        sql = "CALL GetCemeteryFreePlacesNumber(%s)"
        cursor.execute(sql, id)
        rows = cursor.fetchone()

        return render_template('ReportsIntParam.html', form=form, url=url_for('.get_freeplaces'), name="Free places", table=rows[0])

    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/cemeteryclients/', methods=['POST', 'GET'])
def get_cemetery_clients():

    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT CemeteryId, CemeteryName FROM cemetery"
        cursor.execute(sql)
        cemeteries_rows = cursor.fetchall()
        form = SelectForm("Cemetery", select_list=cemeteries_rows)

        if request.method == 'GET':
            return render_template("ReportsIntParam.html", form=form, url=url_for('.get_cemetery_clients'), name='Clients in cemeteries')

        id = request.form['select']
        sql = "CALL GetCemeteryDeceased(%s)"
        cursor.execute(sql, id)
        rows = cursor.fetchall()

        clients = ShortClientsTable(list(map(lambda x: ShortClient(*x), rows)))
        clients.border = True

        return render_template('ReportsIntParam.html', form=form, url=url_for('.get_cemetery_clients'), name="Clients in cemeteries", table=clients)

    finally:
        if cursor is not None:
            cursor.close()

@routes.route('/mortuaryclients/', methods=['POST', 'GET'])
def get_mortuary_clients():

    cursor = None
    try:
        cursor = mysql.get_db().cursor()
        sql = "SELECT MortuaryId, MortuaryName FROM mortuary"
        cursor.execute(sql)
        mortuaries_rows = cursor.fetchall()
        form = SelectForm("Cemetery", select_list=mortuaries_rows)

        if request.method == 'GET':
            return render_template("ReportsIntParam.html", form=form, url=url_for('.get_cemetery_clients'), name='Clients in mourtaries')

        id = request.form['select']
        sql = "CALL GeMortuaryDeceased(%s)"
        cursor.execute(sql, id)
        rows = cursor.fetchall()

        clients = ShortClientsTable(list(map(lambda x: ShortClient(*x), rows)))
        clients.border = True

        return render_template('ReportsIntParam.html', form=form, url=url_for('.get_cemetery_clients'), name="Clients in mourtaries", table=clients)

    finally:
        if cursor is not None:
            cursor.close()