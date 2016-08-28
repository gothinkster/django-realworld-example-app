from conduit.apps.core.renderers import ConduitJSONRenderer


class ArticleJSONRenderer(ConduitJSONRenderer):
    object_label = 'article'
    object_label_plural = 'articles'
