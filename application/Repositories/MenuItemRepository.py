from .RepositoryBase import RepositoryBase
from Models import MenuItem, MenuItemSchema
from Validators import MenuItemValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class MenuItemRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of MenuItem."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(MenuItem, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(MenuItem).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = MenuItemSchema(many=True)
            return self.handle_success(result, schema, 'get', 'MenuItem')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(MenuItem).filter_by(id=id).first()
            schema = MenuItemSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'MenuItem')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                menu_item = MenuItem(
                    type = data['type'],
                    behavior = data['behavior'],
                    url = data['url'],
                    #target_id = data['target_id'],
                    title = data['title'],
                    order = data['order'],
                    #parent_id = data['parent_id'],
                    menu_id = data['menu_id']
                )
                session.add(menu_item)
                session.commit()
                return self.handle_success(None, None, 'create', 'MenuItem', menu_item.id)

            return self.validate_before(process, request.get_json(), MenuItemValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, menu_item):
                    menu_item.type = data['type']
                    menu_item.behavior = data['behavior']
                    menu_item.url = data['url']
                    #menu_item.target_id = data['target_id']
                    menu_item.title = data['title']
                    menu_item.order = data['order']
                    #menu_item.parent_id = data['parent_id']
                    menu_item.menu_id = data['menu_id']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'MenuItem', menu_item.id)

                return self.run_if_exists(fn, MenuItem, id, session)

            return self.validate_before(process, request.get_json(), MenuItemValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, menu_item):
                session.delete(menu_item)
                session.commit()
                return self.handle_success(None, None, 'delete', 'MenuItem', id)

            return self.run_if_exists(fn, MenuItem, id, session)

        return self.response(run, True)