from flask_table import Table, Col, LinkCol


class Client:
    def __init__(self, client_id, fullname, passport_number, birthdate, deathdate, size, weight, cemetery_name, mortuary_name, cemetery_id, mortuary_id):
        self.client_id = client_id
        self.fullname = fullname
        self.passport_number = passport_number
        self.birthdate = birthdate
        self.deathdate = deathdate

        self.size = size
        self.weight = weight
        self.cemetery_name = cemetery_name
        self.mortuary_name = mortuary_name

        self.cemetery_id = cemetery_id
        self.mortuary_id = mortuary_id

class ClientsTable(Table):
    client_id = Col('ClientId', show=False)
    fullname = Col('Fullname')
    passport_number = Col('PassportNumber')
    birthdate = Col('Birthday')
    deathdate = Col('Deathday')

    size = Col('Size')
    weight = Col('Weight')
    cemetery_name = Col('Cemetery')
    mortuary_name = Col('Mortuary')

    edit = LinkCol('Edit', '.edit_client', url_kwargs=dict(id='client_id'))
    delete = LinkCol('Delete', '.delete_client', url_kwargs=dict(id='client_id'))
