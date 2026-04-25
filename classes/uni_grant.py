from classes.gclass import Gclass
import datetime

class Uni_Grant(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_university_id', '_grant_id', '_amount', '_start_date']
    header = 'Uni_Grants'
    des = ['Id', 'University Id', 'Grant Id', 'Amount', 'Start Date']

    def __init__(self, id, university_id, grant_id, amount, start_date):  
        super().__init__()
        id = Uni_Grant.get_id(id)
        self._id = id
        self._university_id = university_id
        self._grant_id = grant_id
        self._amount = float(amount)
        self._start_date = datetime.date.fromisoformat(start_date)
        Uni_Grant.obj[id] = self
        Uni_Grant.lst.append(id)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def university_id(self):
        return self._university_id
    @university_id.setter
    def university_id(self, university_id):
        self._university_id = university_id

    @property
    def grant_id(self):
        return self._grant_id
    @grant_id.setter
    def grant_id(self, grant_id):
        self._grant_id = grant_id

    @property
    def amount(self):
        return self._amount
    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def start_date(self):
        return self._start_date
    @start_date.setter                     
    def start_date(self, start_date):
        self._start_date = start_date