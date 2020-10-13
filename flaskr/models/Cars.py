from flask_table import Table, Col, LinkCol


class Car:
    def __init__(self, car_id, car_registration_number, car_type, car_model):
        self.car_id = car_id
        self.car_registration_number = car_registration_number
        self.car_type = car_type
        self.car_model = car_model


class CarsTable(Table):
    car_id = Col('CarId', show=False)
    car_registration_number = Col('RegistrationNumber')
    car_type = Col('CarType')
    car_model = Col('CarModel')
    edit = LinkCol('Edit', '.edit_car', url_kwargs=dict(id='car_id'))
    delete = LinkCol('Delete', '.delete_car', url_kwargs=dict(id='car_id'))
