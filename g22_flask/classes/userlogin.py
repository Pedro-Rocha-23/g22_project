import bcrypt
from classes.gclass import Gclass


class Userlogin(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''

    att = ['_id', '_user', '_usergroup', '_password']

    header = 'Users'

    des = ['Id', 'User', 'User group', 'Password']

    username = ''
    user_id = 0

    def __init__(self, id, user, usergroup, password):
        super().__init__()

        id = Userlogin.get_id(id)
        self._id = id
        self._user = user
        self._usergroup = usergroup
        self._password = password

        Userlogin.obj[id] = self
        Userlogin.lst.append(id)

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def usergroup(self):
        return self._usergroup

    @usergroup.setter
    def usergroup(self, usergroup):
        self._usergroup = usergroup

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @classmethod
    def get_user_id(cls, user):
        user_id = 0
        lsobj = Userlogin.find(user, 'user')

        if len(lsobj) == 1:
            obj = lsobj[0]
            user_id = obj.id

        return user_id

    @classmethod
    def chk_password(cls, user, password):
        for id in cls.lst:
            obj = cls.obj[id]

            if obj.user == user:
                if obj.password == password:
                    cls.user_id = obj.id
                    cls.username = obj.user
                    return "Valid"
                else:
                    return "Invalid password"

        return "Invalid user"

    @classmethod
    def set_password(cls, password):
        passencrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return passencrypted.decode()

    def __str__(self):
        return f'Id:{self.id}, User:{self.user}, Usergroup:{self.usergroup}'