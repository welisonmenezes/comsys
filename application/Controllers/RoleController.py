from .ControllerBase import ControllerBase
from Repositories import RoleRepository

class RoleController(ControllerBase):
    """This flask_restful API's Resource works like a controller to RoleRepository"""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved"""

        super(RoleController, self).__init__()
        self.repo = RoleRepository()

    
    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder"""

        self.parser.add_argument('get_capabilities')
        self.parser.add_argument('name')
        self.parser.add_argument('description')
        self.parser.add_argument('can_access_admin')
        self.parser.add_argument('capability_description')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)