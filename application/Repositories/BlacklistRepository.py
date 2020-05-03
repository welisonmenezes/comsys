from Models import Blacklist, BlacklistSchema
from Validators import BlacklistValidator
from Utils import Paginate, ErrorHandler, Checker
from .RepositoryBase import RepositoryBase

class BlacklistRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            filter = ()
            page = 1
            limit = 10

            if (args['page'] and Checker.can_be_integer(args['page'])):
                page = int(args['page'])

            if (args['limit'] and Checker.can_be_integer(args['limit'])):
                limit = int(args['limit'])

            if (args['value']):
                filter += (Blacklist.value.like('%' + args['value'] + '%'),)

            if (args['type']):
                filter += (Blacklist.type == args['type'],)

            if (args['target']):
                filter += (Blacklist.target == args['target'],)

            schema = BlacklistSchema(many=True)
            query = session.query(Blacklist).filter(*filter)
            result = Paginate(query, page, limit)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        def fn(session):
            schema = BlacklistSchema(many=False)
            result = session.query(Blacklist).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Blacklist found.').response

        return self.response(fn, False)

    
    def create(self, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = BlacklistValidator(data)

                if (validator.is_valid()):
                    blacklist = Blacklist(
                        type = data['type'],
                        value = data['value'],
                        target = data['target']
                    )
                    session.add(blacklist)
                    session.commit()
                    last_id = blacklist.id

                    return {
                        'message': 'Blacklist saved successfully.',
                        'id': last_id
                    }, 200
                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def update(self, id, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = BlacklistValidator(data)

                if (validator.is_valid()):
                    blacklist = session.query(Blacklist).filter_by(id=id).first()

                    if (blacklist):
                        blacklist.type = data['type']
                        blacklist.value = data['value']
                        blacklist.target = data['target']
                        session.commit()

                        return {
                            'message': 'Blacklist updated successfully.',
                            'id': blacklist.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No Blacklist found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            blacklist = session.query(Blacklist).filter_by(id=id).first()

            if (blacklist):
                session.delete(blacklist)
                session.commit()

                return {
                    'message': 'Blacklist deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No Blacklist found.').response

        return self.response(fn, True)