import django.dispatch

post_save_user_signal_handler = django.dispatch.Signal(providing_args=["blog"])