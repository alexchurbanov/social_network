from rest_framework.mixins import RetrieveModelMixin
from rest_framework.schemas.openapi import AutoSchema


class PostsSchema(AutoSchema):

    def _get_pagination_parameters(self, path, method):
        view = self.view
        if view.action in ['favourite_posts', 'published_posts', 'analytics']:
            paginator = self._get_paginator()
            return paginator.get_schema_operation_parameters(view)

        return super(PostsSchema, self)._get_pagination_parameters(path, method)

    def _allows_filters(self, path, method):
        if self.view.action in ['favourite_posts', 'published_posts', 'analytics']:
            return True
        return super(PostsSchema, self)._allows_filters(path, method)

    def _get_request_body(self, path, method):
        if self.view.action in ['like', 'unlike']:
            return {}
        return super(PostsSchema, self)._get_request_body(path, method)

    def _get_responses(self, path, method):
        if self.view.action in ['like', 'unlike']:
            return {
                '200': {
                    'content': {
                        ct: {'schema': {'properties': {
                            'id': {'type': 'string', 'format': 'uuid', 'readOnly': True},
                            'status': {'type': 'string', 'readOnly': True},
                            'message': {'type': 'string', 'readOnly': True}}}}
                        for ct in self.response_media_types
                    },
                    'description': ""
                }
            }
        elif self.view.action == 'analytics':
            response = super(PostsSchema, self)._get_responses(path, method)
            response_schema = {
                'type': 'array',
                'items': response['200']['content']['application/json']['schema'],
            }
            paginator = self._get_paginator()
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

        return super(PostsSchema, self)._get_responses(path, method)

