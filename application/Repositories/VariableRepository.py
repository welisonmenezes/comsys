from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from flask import  request
from app import errorHandler

from Models import Session, Variable, VariableSchema

class VariableRepository():
    
    def get(self):

        session = Session()
        schema = VariableSchema(many=True)
        
        try:
            result = session.query(Variable).all()
            data = schema.dump(result)
            return {
                'data': data
            }, 200

        except SQLAlchemyError as e:
            return errorHandler.error_500_handler(e)

        except HTTPException as e:
            return errorHandler.error_500_handler(e)

        finally:
            session.close()


    def get_by_id(self, id):

        session = Session()
        schema = VariableSchema(many=False)

        try:

            result = session.query(Variable).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return errorHandler.error_404_handler('No Variable found.')

        except SQLAlchemyError as e:
            return errorHandler.error_500_handler(e)

        except HTTPException as e:
            return errorHandler.error_500_handler(e)

        finally:
            session.close()

    
    def create(self, request):

        data = request.get_json()

        if (data):

            session = Session()

            try:
                variable = Variable(
                    key = data['key'],
                    value = data['value']
                )
                session.add(variable)
                session.commit()
                last_id = variable.id

                return {
                    'message': 'Variable saved successfully.',
                    'id': last_id
                }, 200
                
            except SQLAlchemyError as e:
                session.rollback()
                return errorHandler.error_500_handler(e)

            except HTTPException as e:
                session.rollback()
                return errorHandler.error_500_handler(e)
                
            finally:
                session.close()

        else:
            return {'message': 'No data send.'}, 400