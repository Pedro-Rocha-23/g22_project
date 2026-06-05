from classes.gclass import Gclass
import datetime
class Director(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_director_name','_dob']
    header = 'Directors'
    des = ['Id','director_name','Date of Birth']
    def __init__(self, id, director_name, dob):
        super().__init__()
        id = Director.get_id(id)
        self._id = id
        self._director_name = director_name
        try:
            self._dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        except:
            self._dob = datetime.date.fromisoformat(dob)
        Director.obj[id] = self
        Director.lst.append(id)
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id
    @property
    def director_name(self):
        return self._director_name
    @director_name.setter
    def director_name(self, director_name):
        self._director_name = director_name
    @property
    def dob(self):
        return self._dob
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    @property
    def age(self):
        tday = datetime.date.today()
        age = tday.year - self.dob.year
        if tday.month < self.dob.month or \
            (tday.month == self.dob.month and tday.day < self.dob.day):
            age -= 1
        return age

