from flask_table import Table, Col, LinkCol

class FreeWorker:
    def __init__(self, fullname):
        self.fullname = fullname


class FreeWorkersTable(Table):
    fullname = Col('Fullname')

class IncompletedFuneral:
    def __init__(self, funeral_id, client, date, status, cemetery):
        self.funeral_id = funeral_id
        self.client = client
        self.date = date
        self.status = status
        self.cemetery = cemetery


class IncompletedFuneralsTable(Table):
    funeral_id = Col('FuneralId', show=False)
    date = Col('Date')
    status = Col('Status')
    client = Col('Client')
    cemetery = Col('Cemetery')

class ShortClient:
    def __init__(self, fullname, date):
        self.fullname = fullname
        self.deathdate = date

class ShortClientsTable(Table):
    fullname = Col('Fullname')
    deathdate = Col('Deathdate')