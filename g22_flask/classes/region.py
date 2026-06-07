from classes.gclass import Gclass

class Region(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    
    # Atributos privados, o ID tem de ser o primeiro
    att = ['_id', '_name']
    
    # Título do cabeçalho
    header = 'Regions'
    
    # Descrição para formulários
    des = ['Id', 'Region Name']
    
    # Construtor
    def __init__(self, id, name):
        super().__init__()
        # Usar o método get_id da Gclass (tal como no Director)
        id = Region.get_id(id)
        self._id = id
        self._name = name
        
        # Adicionar aos dicionários e listas da classe
        Region.obj[id] = self
        Region.lst.append(id)
        
    # Getter e Setter para o ID
    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, id):
        self._id = id
        
    # Getter e Setter para o Nome
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name

