from .ControllerBase import ControllerBase
from Repositories import UserRepository

class UserController(ControllerBase):

    def __init__(self):
        self.repo = UserRepository()
        super(UserController, self).__init__()
        

    def get(self, id=None):
        self.parser.add_argument('name')
        self.parser.add_argument('email')
        self.parser.add_argument('registered')
        self.parser.add_argument('status')
        self.parser.add_argument('role_id')
        self.parser.add_argument('get_children')
        self.args = self.parser.parse_args()

        if id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)

    
    def post(self):
        return self.repo.create(self.request)


    def put(self, id=None):
        return self.repo.update(id, self.request)


    def delete(self, id=None):
        return self.repo.delete(id)