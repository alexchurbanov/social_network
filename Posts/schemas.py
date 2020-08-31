from rest_framework.schemas.openapi import AutoSchema


class PostsSchema(AutoSchema):

    def get_tags(self, path, method):
        view = self.view
        if view.action == 'analytics':
            return ['analytics']
        return super(PostsSchema, self).get_tags(path, method)

    def get_pagination_parameters(self, path, method):
        view = self.view
        if view.action in ['favourite_posts', 'published_posts', 'analytics']:
            paginator = self.get_paginator()
            return paginator.get_schema_operation_parameters(view)

        return super(PostsSchema, self).get_pagination_parameters(path, method)

    def allows_filters(self, path, method):
        if self.view.action in ['favourite_posts', 'published_posts', 'analytics']:
            return True
        elif self.view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return False
        return super(PostsSchema, self).allows_filters(path, method)

    def get_request_body(self, path, method):
        if self.view.action in ['like', 'unlike']:
            return {}
        return super(PostsSchema, self).get_request_body(path, method)

    def get_responses(self, path, method):
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
        elif self.view.action in ['favourite_posts', 'published_posts', 'analytics']:
            response = super(PostsSchema, self).get_responses(path, method)
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

        return super(PostsSchema, self).get_responses(path, method)

