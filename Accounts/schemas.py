from rest_framework.schemas.openapi import AutoSchema


class UsersSchema(AutoSchema):
    def allows_filters(self, path, method):
        if self.view.action in ['followers', 'followed', 'friends']:
            return True
        return super(UsersSchema, self).allows_filters(path, method)

    def get_pagination_parameters(self, path, method):
        view = self.view
        if view.action in ['followers', 'followed', 'friends']:
            paginator = self.get_paginator()
            return paginator.get_schema_operation_parameters(view)
        return super(UsersSchema, self).get_pagination_parameters(path, method)

    def get_request_body(self, path, method):
        if self.view.action in ['add_friend', 'remove_friend']:
            return {}
        return super(UsersSchema, self).get_request_body(path, method)

    def get_responses(self, path, method):
        if self.view.action == 'change_password':
            return {
                '200': {
                    'content': {
                        ct: {'schema': {'properties': {
                             'status': {'type': 'string', 'readOnly': True},
                             'message': {'type': 'string', 'readOnly': True}}}}
                        for ct in self.response_media_types
                    },
                    'description': ""
                }
            }
        elif self.view.action in ['add_friend', 'remove_friend']:
            return {
                '200': {
                    'content': {
                        'application/json': {'schema': {'properties': {
                            'status': {'type': 'string', 'readOnly': True},
                            'message': {'type': 'string', 'readOnly': True}}}}
                    },
                    'description': ""
                }
            }
        elif self.view.action in ['followers', 'followed', 'friends']:
            response = super(UsersSchema, self).get_responses(path, method)
            response_schema = {
                'type': 'array',
                'items': response['200']['content']['application/json']['schema'],
            }
            paginator = self.get_paginator()
            response_schema = paginator.get_paginated_response_schema(response_schema)
            return {
                '200': {
                    'content': {
                        ct: {'schema': response_schema}
                        for ct in self.response_media_types
                    },
                    'description': ""
                }
            }
        return super(UsersSchema, self).get_responses(path, method)


class AuthSchema(AutoSchema):
    def get_responses(self, path, method):
        if path in ['/api/v1/auth/login/', '/api/v1/auth/logout/']:
            return {
                '200': {
                    'content': {
                        'application/json': {'schema': {'properties': {
                             'status': {'type': 'string', 'readOnly': True},
                             'message': {'type': 'string', 'readOnly': True}}}}
                    },
                    'description': ""
                }
            }
        elif path == '/api/v1/auth/jwt/create/':
            return {
                '200': {
                    'content': {
                        'application/json': {'schema': {'properties': {
                            'refresh': {'type': 'string', 'readOnly': True},
                            'access': {'type': 'string', 'readOnly': True},
                            'exp_date': {'type': 'object', 'readOnly': True,
                                         'properties':
                                             {'refresh': {'type': 'integer', 'readOnly': True},
                                              'access': {'type': 'integer', 'readOnly': True}}},
                            'user': {'type': 'string', 'readOnly': True}}}}

                    },
                    'description': ""
                }
            }
        elif path == '/api/v1/auth/jwt/refresh/':
            return {
                '200': {
                    'content': {
                        'application/json': {'schema': {'properties': {
                            'access': {'type': 'string', 'readOnly': True},
                            'exp_date': {'type': 'object', 'readOnly': True,
                                         'properties':
                                             {'access': {'type': 'integer', 'readOnly': True}}},
                            }}}

                    },
                    'description': ""
                }
            }
        elif path == '/api/v1/auth/jwt/verify/':
            return {
                '200': {'content': {'application/json': {}}},
                '401': {
                    'content': {
                        'application/json': {'schema': {'properties': {
                            'detail': {'type': 'string', 'readOnly': True},
                            'code': {'type': 'string', 'readOnly': True},
                            }}}

                    },
                    'description': ""
                }
            }
        return super(AuthSchema, self).get_responses(path, method)
