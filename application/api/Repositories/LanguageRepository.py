from .RepositoryBase import RepositoryBase
from Models import Language, LanguageSchema, Configuration, Post, Menu, Comment, Term
from Validators import LanguageValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class LanguageRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Language."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Language, args)
        fb.set_like_filters(['name', 'code'])
        fb.set_equals_filters(['status'])
        query = self.session.query(Language).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = LanguageSchema(many=True)
        return self.handle_success(result, schema, 'get', 'Language')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(Language).filter_by(id=id).first()
        schema = LanguageSchema(many=False)
        return self.handle_success(result, schema, 'get_by_id', 'Language')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            language = Language()
            Helper().fill_object_from_data(language, data, ['name', 'code', 'status', 'datetime_format'])
            session.add(language)
            session.commit()
            return self.handle_success(None, None, 'create', 'Language', language.id)

        return self.validate_before(process, request.get_json(), LanguageValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):

            def fn(session, language):
                Helper().fill_object_from_data(language, data, ['name', 'code', 'status', 'datetime_format'])
                session.commit()
                return self.handle_success(None, None, 'update', 'Language', language.id)

            return self.run_if_exists(fn, Language, id, session)

        return self.validate_before(process, request.get_json(), LanguageValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""
 
        if id == 1:
            raise BadRequestError('The Primary Language cannot be be deleted.')

        def fn(session, language):
            self.is_foreigners([
                (language, 'language_id', Configuration),
                (language, 'language_id', Post),
                (language, 'language_id', Menu),
                (language, 'language_id', Comment),
                (language, 'language_id', Term)
            ], session)

            session.delete(language)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Language', id)

        return self.run_if_exists(fn, Language, id, self.session)