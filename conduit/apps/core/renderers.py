import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            _data = json.loads(
                super(ConduitJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps({
                self.object_label_plural: _data
            })
        else:
            # If the view throws an error (such as the user can't be authenticated
            # or something similar), `data` will contain an `errors` key. We want
            # the default JSONRenderer to handle rendering errors, so we need to
            # check for this case.
            errors = data.get('errors', None)

            if errors is not None:
                # As mentioned about, we will let the default JSONRenderer handle
                # rendering errors.
                return super(ConduitJSONRenderer, self).render(data)

            return json.dumps({
                self.object_label: data
            })
