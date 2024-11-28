#!/usr/bin/python3

import sys

class Loggable (object):
    def __init__(self, verbose=False, debug=False):
        self.verbose = verbose or debug
        self.debug   = debug

    def emit(self, message, debug=False):
        if self.debug or self.verbose and not debug:
            print(message)

class Field (Loggable):
    def __init__(self, field_name, field_type="text", field_default=None, field_hard_default=False, field_label=None, field_length=20, verbose=False, debug=False, ):

        #TODO:  Validate field_type
        #TODO:  Implement soft defaults
        
        super().__init__(self, verbose, debug)
        self.field_name         = field_name
        self.field_type         = field_type
        self.field_default      = field_default
        self.field_hard_default = field_hard_default
        self.field_label        = field_label
        self.field_length       = field_length
        self.field_value        = None
        
    def render(self):
        if self.field_hard_default:
            self.field_value = self.field_default

        properties = {
            'type'   : self.field_type,
            'name'   : self.field_name,
            'value'  : self.field_value,
            'length' : self.field_length
        }

        result = ""
        if self.field_label is not None:
            result += '<label for=' + self.field_name + '>' + self.field_label + '</label>'
        result += '<input ' + ' '.join(['%s="%s"' % (x, properties[x]) for x in properties if properties[x] is not None]) + ' />'
        return result

    def set_value(self, field_value):
        self.field_value = field_value

    def get_value(self):
        return self.field_value
    
class Form (Loggable):
    def __init__(self, action, fields=[], verbose=False, debug=False):
        super().__init__(verbose, debug)
        self.form_action = action
        self.form_fields = fields
        self.results     = None

    def add_field(self, field):
        #TODO:  Valideate that field is a Field
        self.form_fields += [field]

    def render(self):
        result = '<form action="' + self.form_action + '" method="post" enctype="text/plain">'
        for field in form_fields:
            result += field.render()
        result += '</form>'
        return result

    def parse(self):

        #Don't do anything if this form has already been parsed.
        if self.results is None:
            self.results = []
            for line in sys.stdin:
                (key, value) = line.split('=', 1)
                self.results += [
                    {
                        'name'  : key,
                        'value' : value
                    }
                ]

    def result_as_list(self):
        self.parse()
        return self.results

    def result_as_dict(self):
        result=dict()
        for entry in self.result_as_list():
            result[entry['name']] = entry['value']
        return result

    def result_as_dict_list(self):
        result=dict()
        for entry in self.result_as_list():
            if entry['name'] in result:
                result[entry['name']] += [entry['value']]
            else:
                result[entry['name']] = [entry['value']]
                
        return result

