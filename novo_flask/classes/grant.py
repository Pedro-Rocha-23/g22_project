
# Class Grant - generic version with inheritance
from classes.gclass import Gclass
class Grant(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # Attribute names list, identifier attribute must be the first one and callled 'id'
    att = ['_id','_title','_category']
    # Class header title
    header = 'Grants'
    # field description for use in, for example, input form
    des = ['Id','Title','Category']
    # Constructor: Called when an object is instantiated
    def __init__(self, id, title, category, director_id):
        super().__init__()
        # Object attributes
        id = Grant.get_id(id)
        self._id = id
        self._director_id=director_id
        self._title=title
        self._category=category
        # Add the new object to the dictionary of objects
        Grant.obj[id] = self
        # Add the id to the list of object ids
        Grant.lst.append(id)
    # id property getter method
    @property
    def director_id(self):
        return self._director_id
    @director_id.setter
    def director_id(self, director_id):
        self._director_id = director_id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id
    # title property getter method
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        self._title=title
    # category property getter method
    @property
    def category(self):
        return self._category
    # category property setter method
    @category.setter
    def category(self, category):
        self._category = category

