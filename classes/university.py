from classes.gclass import Gclass
import datetime
class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name','_creation_date']
    header = 'Universities'
    des = ['Id','Name','Date of Creation']
    def __init__(self, id, name, creation_date):
        super().__init__()
        # Object attributes
        id = University.get_id(id)
        self._id = id
        self._name = name
        self._creation_date = datetime.datetime.strptime(creation_date, "%d/%m/%Y").date()
        University.obj[id] = self
        University.lst.append(id)
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id 
   
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
  
    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        self._creation_date = creation_date

    @property
    def age(self):
        tday = datetime.date.today()
        age = tday.year - self.creation_date.year
        if tday.month < self.creation_date.month or \
            (tday.month == self.creation_date.month and tday.day < self.creation_date.day):
            age -= 1
        return age

