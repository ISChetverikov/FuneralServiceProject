from flask_table import Table, Col, LinkCol


class Funeral:
    def __init__(self, funeral_id, date, status, cemetery_name, cemetery_id, client_name, client_id):
        self.funeral_id = funeral_id
        self.date = date
        self.status = status
        self.cemetery_name = cemetery_name
        self.cemetery_id = cemetery_id
        self.client_name = client_name
        self.client_id = client_id


class FuneralsTable(Table):
    funeral_id = Col('FuneralId', show=False)
    date = Col('Date')
    status = Col('Status')
    client_name = Col('Client')
    cemetery_name = Col('Cemetery')

    edit = LinkCol('Edit', '.edit_funeral', url_kwargs=dict(id='funeral_id'))
    delete = LinkCol('Delete', '.delete_funeral', url_kwargs=dict(id='funeral_id'))
