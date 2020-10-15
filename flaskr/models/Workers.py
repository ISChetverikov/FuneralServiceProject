from flask_table import Table, Col, LinkCol

class Worker:
    def __init__(self, worker_id, fullname, passport_number):
        self.worker_id = worker_id
        self.passport_number = passport_number
        self.fullname = fullname


class WorkersTable(Table):
    worker_id = Col('WorkerId', show=False)
    fullname = Col('Fullname')
    passport_number = Col('PassportNumber')
    edit = LinkCol('Edit', '.edit_worker', url_kwargs=dict(id='worker_id'))
    delete = LinkCol('Delete', '.delete_worker', url_kwargs=dict(id='worker_id'))
