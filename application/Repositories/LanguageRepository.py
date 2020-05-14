from .RepositoryBase import RepositoryBase
from Models import Language, LanguageSchema
from Validators import LanguageValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class LanguageRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Language."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Language, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Language).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = LanguageSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Language')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Language).filter_by(id=id).first()
            schema = LanguageSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Language')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                language = Language(
                    name = data['name'],
                    code = data['code'],
                    status = data['status'],
                    datetime_format = data['datetime_format']
                )
                session.add(language)
                session.commit()
                return self.handle_success(None, None, 'create', 'Language', language.id)

            return self.validate_before(process, request.get_json(), LanguageValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                language = session.query(Language).filter_by(id=id).first()

                if (language):
                    language.name = data['name']
                    language.code = data['code']
                    language.status = data['status']
                    language.datetime_format = data['datetime_format']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Language', language.id)

                else:
                    return ErrorHandler().get_error(404, 'No Language found.')

            return self.validate_before(process, request.get_json(), LanguageValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            language = session.query(Language).filter_by(id=id).first()

            if (language):
                session.delete(language)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Language', id)

            else:
                return ErrorHandler().get_error(404, 'No Language found.')

        return self.response(run, True)