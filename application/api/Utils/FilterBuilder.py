from sqlalchemy import desc, asc, not_, or_, and_
from app import app
from Utils import Checker, Helper

class FilterBuilder():
    """Builds the filter tuple. Puts into the given context the
        corresponding arguments given by parameters."""

    def __init__(self, context, args):
        """Gets the context (the Model) and applies the given arguments."""

        self.filter = ()
        self.context = context
        self.args = args
        self.page = 1
        self.limit = app.config['DEFAULT_LIMIT_PAGINATION_RESULTS']


    def get_context_attr(self, key, kwa):
        """Returns the correct context. If has the parameters joined
            and joined_key returns this correctly."""

        if ('joined' in kwa and 'joined_key' in kwa):
            return getattr(kwa['joined'], kwa['joined_key'])
        else:
            return getattr(self.context, key)

    
    def set_equals_filter(self, key, *args, **kwargs):
        """Sets filter that checks if the field with a given key is equals to the args with same key."""

        if (key in self.args and self.args[key]):
            self.filter += (self.get_context_attr(key, kwargs) == self.args[key], )


    def set_equals_filters(self, keys, *args, **kwargs):
        """Sets filter that checks if the field with a given list of keys is equals to the args with same key."""

        for key in keys:
            self.set_equals_filter(key, args, kwargs)

    
    def set_like_filter(self, key, *args, **kwargs):
        """Sets filter that checks if the field with a given key is like to the args with same key."""

        if (key in self.args and self.args[key]):
            self.filter += (self.get_context_attr(key, kwargs).like('%' + self.args[key] + '%'), )


    def set_like_filters(self, keys, *args, **kwargs):
        """Sets filter that checks if the field with a given list of keys is like to the args with same key."""

        for key in keys:
            self.set_like_filter(key, args, kwargs)

    
    def set_and_or_filter(self, key, modifier, configurations, *args, **kwargs):
        """Sets filter witch applies the and_ or or_ SqlAchemy method on 
            the given configuration array of dictionary"""

        try:
            list_or = ()
            list_and = ()

            if (key in self.args and self.args[key] and isinstance(configurations, list)):

                for config in configurations:

                    kwa = kwargs
                    if 'kwargs' in config:
                        kwa = config['kwargs']
                        kwa.update({'joined':kwa['joined'], 'joined_key': config['field']})

                    if config['type'] == 'like' and modifier == 'or':
                        list_or += (self.get_context_attr(config['field'], kwa).like('%' + self.args[key] + '%'),)
                    elif config['type'] == 'like' and modifier == 'and':
                        list_and += (self.get_context_attr(config['field'], kwa).like('%' + self.args[key] + '%'),)
                    elif config['type'] == 'equal' and modifier == 'or':
                        list_or += (self.get_context_attr(config['field'], kwa) == self.args[key],)
                    elif config['type'] == 'equal' and modifier == 'and':
                        list_and += (self.get_context_attr(config['field'], kwa) == self.args[key],)

                self.filter += (or_(*list_or),)
                self.filter += (and_(*list_and),)

        except Exception as e:
            raise Exception(str(e)) 
        
    
    def set_date_filter(self, key, *args, **kwargs):
        """Sets filter that checks fields and args by same key, appling the date_modifier filter.
           The field and the arg must be an datetime data."""
        
        if (key in self.args and self.args[key]):
            try:
                date_time = Helper().get_date_from_string(self.args[key])

                date_modifier = 'greater_or_equal'
                if ('date_modifier' in kwargs and kwargs['date_modifier']):
                        date_modifier = kwargs['date_modifier']

                if (date_modifier == 'greater'):
                    self.filter += (self.get_context_attr(key, kwargs) > date_time,)
                elif (date_modifier == 'less'):
                    self.filter += (self.get_context_attr(key, kwargs) < date_time,)
                elif (date_modifier == 'greater_or_equal'):
                    self.filter += (self.get_context_attr(key, kwargs) >= date_time,)
                elif (date_modifier == 'less_or_equal'):
                    self.filter += (self.get_context_attr(key, kwargs) <= date_time,)
                elif (date_modifier == 'equal'):
                    self.filter += (self.get_context_attr(key, kwargs) == date_time,)
                elif (date_modifier == 'different'):
                    self.filter += (self.get_context_attr(key, kwargs) != date_time,)
                else:
                    raise Exception('The parameter \'date_modifier\' must be one of these:[greater, less, greater_or_equal, less_or_equal, equal or different]')

            except Exception as e:
                raise Exception(str(e))


    def set_between_dates_filter(self, key, *args, **kwargs):
        """Sets filter that checks if key field is between two dates given dates.
           The date comparators must be passed by the args compare_date_time_one and compare_date_time_two.
           An other modfier can be the arg not_between."""

        try:
            if ('compare_date_time_one' in kwargs and 'compare_date_time_two' in  kwargs 
                and kwargs['compare_date_time_one'] and kwargs['compare_date_time_two']):
                date_time_one = Helper().get_date_from_string(kwargs['compare_date_time_one'])
                date_time_two = Helper().get_date_from_string(kwargs['compare_date_time_two'])

                if ('not_between' in kwargs and kwargs['not_between'] == '1'):
                    self.filter += (not_(self.get_context_attr(key, kwargs).between(date_time_one, date_time_two)),)
                else:
                    self.filter += (self.get_context_attr(key, kwargs).between(date_time_one, date_time_two),)

        except Exception as e:
            raise Exception(str(e))


    def set_range_of_dates_filter(self, *args, **kwargs):
        """Sets filter that get items whose current date fit with publish_on and expire_on dates."""

        try:
            today = Helper().get_current_datetime()

            exp_kwargs = kwargs
            if 'joined_key' in kwargs:
                exp_kwargs = {
                    'joined': kwargs['joined'],
                    'joined_key': 'expire_on'
                }

            self.filter += (or_( and_(self.get_context_attr('publish_on', kwargs) <= today, self.get_context_attr('expire_on', exp_kwargs) >= today, ), or_(self.get_context_attr('publish_on', kwargs) == None, self.get_context_attr('expire_on', exp_kwargs) == None),),)

        except Exception as e:
            raise Exception(str(e))

    
    def get_filter(self):
        """Returns the tuple of the configured filter."""

        return self.filter


    def get_page(self):
        """Returns the current page."""

        if ('page' in self.args and self.args['page'] and Checker().can_be_integer(self.args['page'])):
            self.page = int(self.args['page'])
        return self.page


    def get_limit(self):
        """Returns the configured limit."""

        if ('limit' in self.args and self.args['limit'] and Checker().can_be_integer(self.args['limit'])):
            self.limit = int(self.args['limit'])
        return self.limit


    def get_order_by(self):
        """Returns the correct order_by configuration.
            The args order_by and order determine how it will behave."""

        if ('order_by' in self.args and self.args['order_by'] and self.args['order_by'] != ''):
            if ('order' in self.args and self.args['order'] and self.args['order'] == 'desc'):
                order_by = [desc(getattr(self.context, self.args['order_by']))]
            else:
                order_by = [asc(getattr(self.context, self.args['order_by']))]
        else:
            order_by = [desc(self.context.id)]
        return order_by