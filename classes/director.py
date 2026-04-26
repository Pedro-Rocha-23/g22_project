"""
"""
# Class Director - generic version with inheritance
from classes.gclass import Gclass
import datetime
class Director(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # Attribute director_director_names list, identifier attribute must be the first one and callled 'id'
    att = ['_id','_director_name','_dob']
    # Class header title
    header = 'Directors'
    # field description for use in, for example, input form
    des = ['Id','director_name','Date of Birth']
    # Constructor: Called when an object is instantiated
    def __init__(self, id, director_name, dob):
        super().__init__()
        # Object attributes
        id = Director.get_id(id)
        self._id = id
        self._director_name = director_name
        try:
            self._dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        except:
            self._dob = datetime.date.fromisoformat(dob)
        # Add the new object to the dictionary of objects
        Director.obj[id] = self
        # Add the id to the list of object ids
        Director.lst.append(id)
    # id property getter method
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id
    # director_name property getter method
    @property
    def director_name(self):
        return self._director_name
    @director_name.setter
    def director_name(self, director_name):
        self._director_name = director_name
    # dob property getter method
    @property
    def dob(self):
        return self._dob
    # dob property setter method
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    # salary property getter method
    @property
    def age(self):
        tday = datetime.date.today()
        age = tday.year - self.dob.year
        if tday.month < self.dob.month or \
            (tday.month == self.dob.month and tday.day < self.dob.day):
            age -= 1
        return age

