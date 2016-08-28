from conduit.apps.core.renderers import ConduitJSONRenderer


class ArticleJSONRenderer(ConduitJSONRenderer):
    object_label = 'article'
    object_label_plural = 'articles'


class CommentJSONRenderer(ConduitJSONRenderer):
    object_label = 'comment'
    object_label_plural = 'comments'
