from rest_framework.schemas.openapi import AutoSchema


class UsersSchema(AutoSchema):
    def _get_responses(self, path, method):
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
        return super(UsersSchema, self)._get_responses(path, method)


class AuthSchema(AutoSchema):
    def _get_responses(self, path, method):
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
        return super(AuthSchema, self)._get_responses(path, method)
