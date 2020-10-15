from flask_table import Table, Col, LinkCol


class Cemetery:
    def __init__(self, cemetery_id, name, address, places, phone):
        self.cemetery_id = cemetery_id
        self.address = address
        self.name = name
        self.places = places
        self.phone = phone


class CemeteriesTable(Table):
    cemetery_id = Col('CemeteryId', show=False)
    name = Col('Name')
    address = Col('Address')
    phone = Col('Phone')
    places = Col('Places')

    edit = LinkCol('Edit', '.edit_cemetery', url_kwargs=dict(id='cemetery_id'))
    delete = LinkCol('Delete', '.delete_cemetery', url_kwargs=dict(id='cemetery_id'))
