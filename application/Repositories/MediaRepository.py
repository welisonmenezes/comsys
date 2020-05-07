from Models import Media, MediaSchema
from Validators import MediaValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder, Helper
from .RepositoryBase import RepositoryBase
import base64
from flask import make_response
import filetype
from flask import send_file

class MediaRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            # filter params
            fb = FilterBuilder(Media, args)

            # TODO: implement Media filters

            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')
            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            query = session.query(Media).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = MediaSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        def fn(session):
            schema = MediaSchema(many=False)
            result = session.query(Media).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                if (id and args['return_file_data'] == '1'):
                    data['file_base64'] = str(base64.b64encode(result.file[2:]))

                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Media found.').response

        return self.response(fn, False)



    def get_file(self, id):
        def fn(session):
            result = session.query(Media).filter_by(id=id).first()
            if (result):
                return self.file_response(result, False)
            else:
                return ErrorHandler(404, 'Culd not load this file.').response

        return self.response(fn, False)


    def get_image_preview(self, id):
        def fn(session):
            result = session.query(Media).filter_by(id=id).first()
            image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/svg']
            if (result and result.type in image_types):
                return self.file_response(result, True)
            else:
                return self.image_not_found_response()

        return self.response(fn, False)


    def file_response(self, result, is_preview):
        saved_file = str(base64.b64encode(result.file))
        saved_file = saved_file[2:]
        imgdata = base64.b64decode(saved_file)
        file_ext = Helper.get_extension_by_type(result.type)
        response = make_response(imgdata)
        response.headers.set('Content-Type', result.type)
        if (not is_preview):
            response.headers.set('Content-Disposition', 'attachment; filename=' + result.name + '.' + file_ext)
        return response

    
    def image_not_found_response(self):
        notFoundImage = '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'
        imgdata = base64.b64decode(notFoundImage)
        response = make_response(imgdata)
        response.headers.set('Content-Type', 'image/png')
        return response
        
    
    def create(self, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = MediaValidator(data)

                if (validator.is_valid()):

                    # get file details from request
                    try:
                        type_and_data = Helper.get_file_type_and_data(data['file'])
                        file_type = type_and_data[0]
                        file_data = base64.b64decode(type_and_data[1])
                    except:
                        return ErrorHandler(400, 'Cannot get file details. Please, check if it is a valid file.').response

                    media = Media(
                        name = data['name'],
                        description = data['description'],
                        type = file_type,
                        file = file_data,
                        origin = data['origin'],
                        user_id = data['user_id']
                    )
                    session.add(media)
                    session.commit()
                    last_id = media.id

                    return {
                        'message': 'Media saved successfully.',
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
                validator = MediaValidator(data)

                if (validator.is_valid(id=id)):

                    # TODO: edit media

                    media = session.query(Media).filter_by(id=id).first()

                    if (Media):
                        media.name = data['name']
                        media.description = data['description']
                        media.type = data['type']
                        media.file = data['file']
                        media.origin = data['origin']
                        media.user_id = data['user_id']
                        session.commit()

                        return {
                            'message': 'Media updated successfully.',
                            'id': media.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No Media found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            media = session.query(Media).filter_by(id=id).first()

            if (media):

                # TODO: check if media can be deleted (if user has a file as avatar cannot delete)

                session.delete(media)
                session.commit()

                return {
                    'message': 'Media deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No Media found.').response

        return self.response(fn, True)