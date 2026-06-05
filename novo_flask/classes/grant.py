from classes.gclass import Gclass
class Grant(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_title','_category']
    header = 'Grants'
    des = ['Id','Title','Category']

    def __init__(self, id, title, category, director_id):
        super().__init__()
        id = Grant.get_id(id)
        self._id = id
        self._director_id=director_id
        self._title=title
        self._category=category
        Grant.obj[id] = self
        Grant.lst.append(id)
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
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        self._title=title
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category):
        self._category = category

