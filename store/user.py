from utils import singleton, get, post, delete, put
from enum import Enum
from PySide6.QtCore import Signal, QObject

class Role(Enum):
    USER = 0
    ADMIN = 1

class UserError(Enum):
    PHONE_FORMAT_ERROR = 100
    USERNAME_FORMAT_ERROR = 101
    PASSWORD_FORMAT_ERROR = 102
    NOT_ALLOWED = 103
    PASSWORD_ERROR = 201
    USER_NOT_FOUND = 404
    USER_EXIST = 403

@singleton
class User(QObject):
    loginSignal = Signal()

    def __init__(self):
        super().__init__()
        self.not_login = True

    def check_phone(self, phone):
        if len(phone) != 11 or not phone.isdigit():
            return False
        return True
    
    def check_username(self, username):
        if len(username) < 3 or len(username) > 10:
            return False
        if not username.isalnum():
            for sub in username.split("_"):
                if not sub.isalnum():
                    return False
        return True
    
    def check_password(self, password):
        if len(password) < 6 or len(password) > 20:
            return False
        if not password.isalnum():
            for sub in password.split("@"):
                if not sub.isalnum():
                    return False
        return True

    def is_login(self):
        return not self.not_login
    
    def login(self, phone, password):
        if not self.check_phone(phone):
            return False, UserError.PHONE_FORMAT_ERROR
        if not self.check_password(password):
            return False, UserError.PASSWORD_FORMAT_ERROR
        data = {
            "phone": phone,
            "password": password
        }
        response = post('/user/login', data)
        if response['code'] != 200:
            return False, UserError(response['code'])
        self.not_login = False
        self.id = response['data']['id']
        self.username = response['data']['username']
        self.phone = response['data']['phone']
        self.role = Role(response['data']['isAdmin'])
        return True, response['data']
    
    def logout(self):
        self.not_login = True
        self.id = None
        self.username = None
        self.phone = None
        self.role = None
    
    def register(self, username, phone, password):
        if not self.check_username(username):
            return False, UserError.USERNAME_FORMAT_ERROR
        if not self.check_phone(phone):
            return False, UserError.PHONE_FORMAT_ERROR
        if not self.check_password(password):
            return False, UserError.PASSWORD_FORMAT_ERROR
        data = {
            "username": username,
            "phone": phone,
            "password": password
        }
        response = post('/user/signup', data)
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']
    
    def get_user_info(self, user_id):
        response = get('/user/info/' + user_id)
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']

    def rename(self, new_name):
        data = {
            "id": self.id,
            "newName": new_name
        }
        response = post('/user/modify/name', data)
        if response['code'] != 200:
            return False, UserError(response['code'])
        self.username = new_name
        return True, response['data']
    
    def change_password(self, old_password, new_password):
        if not self.check_password(new_password):
            return False, UserError.PASSWORD_FORMAT_ERROR
        data = {
            "id": self.id,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = post('/user/modify/pwd', data)
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']
    
    def delete_user(self, id):
        if self.role != Role.ADMIN:
            return False, UserError.NOT_ALLOWED
        response = delete('/user/delete' + f"?id={id}")
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']
    
    def get_all_users(self):
        if self.role != Role.ADMIN:
            return False, UserError.NOT_ALLOWED
        response = get('/user/all')
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']
    
    def add_admin(self, id):
        if self.role != Role.ADMIN:
            return False, UserError.NOT_ALLOWED
        response = put('/user/admin' + f"?id={id}")
        if response['code'] != 200:
            return False, UserError(response['code'])
        return True, response['data']