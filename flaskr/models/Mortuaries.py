from flask_table import Table, Col, LinkCol

class Mortuary:
    def __init__(self, worker_id, name, address):
        self.mortuary_id = worker_id
        self.address = address
        self.name = name


class MortuariesTable(Table):
    mortuary_id = Col('MortuaryId', show=False)
    name = Col('Name')
    address = Col('Address')
    edit = LinkCol('Edit', '.edit_mortuary', url_kwargs=dict(id='mortuary_id'))
    delete = LinkCol('Delete', '.delete_mortuary', url_kwargs=dict(id='mortuary_id'))
