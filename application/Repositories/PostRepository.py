from .RepositoryBase import RepositoryBase
from Models import Post, PostSchema, PostType, Language, User
from Validators import PostValidator
from Utils import Paginate, ErrorHandler, FilterBuilder, Helper

class PostRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Post."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Post, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Post).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Post')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Post).filter_by(id=id).first()
            schema = PostSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Post')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                post = Post(
                    name = data['name'],
                    title = data['title'],
                    description = data['description'],
                    status = data['status'],
                    is_protected = data['is_protected'],
                    has_comments = data['has_comments'],
                    publish_on = Helper().get_null_if_empty(data['publish_on']),
                    expire_on = Helper().get_null_if_empty(data['expire_on']),
                    created = Helper().get_current_datetime(),
                    edited = Helper().get_current_datetime()
                )

                fk_was_added = self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                if fk_was_added != True:
                    return fk_was_added

                session.add(post)
                session.commit()
                return self.handle_success(None, None, 'create', 'Post', post.id)

            return self.validate_before(process, request.get_json(), PostValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, post):
                    post.name = data['name']
                    post.title = data['title']
                    post.description = data['description']
                    post.status = data['status']
                    post.is_protected = data['is_protected']
                    post.has_comments = data['has_comments']
                    post.publish_on = Helper().get_null_if_empty(data['publish_on'])
                    post.expire_on = Helper().get_null_if_empty(data['expire_on'])
                    post.edited = Helper().get_current_datetime()

                    fk_was_added = self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                    if fk_was_added != True:
                        return fk_was_added

                    session.commit()
                    return self.handle_success(None, None, 'update', 'Post', post.id)

                return self.run_if_exists(fn, Post, id, session)

            return self.validate_before(process, request.get_json(), PostValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, post):
                session.delete(post)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Post', id)

            return self.run_if_exists(fn, Post, id, session)

        return self.response(run, True)