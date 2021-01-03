from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = "Blog"
    def ready(self):
        import blog.signals.handlers
