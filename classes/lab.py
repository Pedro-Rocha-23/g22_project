from classes.gclass import Gclass

class Lab(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_extra_info','_university_id']
    header = 'Labs'
    des = ['Id','Extra info','University Id']

    def __init__(self, id, extra_info, university_id):
        super().__init__()
        id = Lab.get_id(id)
        self._id = id
        self._extra_info = extra_info
        self._university_id = int(university_id)
        Lab.obj[id] = self
        Lab.lst.append(id)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id 
   
    @property
    def extra_info(self):
        return self._extra_info
    @extra_info.setter
    def extra_info(self, extra_info):
        self._extra_info = extra_info
  
    @property
    def university_id(self):
        return self._university_id

    @university_id.setter
    def university_id(self, university_id):
        self._university_id = int(university_id)