from conduit.apps.core.renderers import ConduitJSONRenderer


class ArticleJSONRenderer(ConduitJSONRenderer):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'


class CommentJSONRenderer(ConduitJSONRenderer):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'


class CategoryJSONRenderer(ConduitJSONRenderer):
    object_label = 'category'
    pagination_object_label = 'categories'
    pagination_count_label = 'categoriesCount'
