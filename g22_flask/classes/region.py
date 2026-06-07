from classes.gclass import Gclass

class Region(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    
    att = ['_id', '_name']
    

    header = 'Regions'

    des = ['Id', 'Region Name']
    
  
    def __init__(self, id, name):
        super().__init__()
       
        
        id = Region.get_id(id)
        self._id = id
        self._name = name
        

        Region.obj[id] = self
        Region.lst.append(id)
        

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

