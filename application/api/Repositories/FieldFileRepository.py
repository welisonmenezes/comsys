from .RepositoryBase import RepositoryBase
from Models import FieldFile, FieldFileSchema, Field, Media, Post, Grouper
from Validators import FieldFileValidator
from Utils import Paginate, FilterBuilder
from ErrorHandlers import BadRequestError

class FieldFileRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldFile."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(FieldFile, args)
        fb.set_equals_filters(['field_id', 'media_id', 'grouper_id', 'post_id'])
        self.set_protection_to_child_post(fb)
        query = self.session.query(FieldFile).join(*self.joins, isouter=True).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = FieldFileSchema(many=True)
        return self.handle_success(result, schema, 'get', 'FieldFile')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Post, {})
        self.set_protection_to_child_post(fb)
        fb.filter += (FieldFile.id == id,)
        result = self.session.query(FieldFile).join(*self.joins, isouter=True).filter(*fb.get_filter()).first()
        schema = FieldFileSchema(many=False)
        return self.handle_success(result, schema, 'get_by_id', 'FieldFile')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            field_file = FieldFile()
            self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
            self.add_foreign_keys_field_type('file', field_file, data, session, [('field_id', Field), ('media_id', Media), ('grouper_id', Grouper), ('post_id', Post)])
            session.add(field_file)
            session.commit()
            return self.handle_success(None, None, 'create', 'FieldFile', field_file.id)

        return self.validate_before(process, request.get_json(), FieldFileValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, field_file):
                self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                self.add_foreign_keys_field_type('file', field_file, data, session, [('field_id', Field), ('media_id', Media), ('grouper_id', Grouper), ('post_id', Post)], id)  
                session.commit()
                return self.handle_success(None, None, 'update', 'FieldFile', field_file.id)

            return self.run_if_exists(fn, FieldFile, id, session)

        return self.validate_before(process, request.get_json(), FieldFileValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, field_file):
            session.delete(field_file)
            session.commit()
            return self.handle_success(None, None, 'delete', 'FieldFile', id)

        return self.run_if_exists(fn, FieldFile, id, self.session)