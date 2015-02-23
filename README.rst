EEA Frame
=========

Django integration middleware for EEA Zope websites.


Template and request
--------------------

``pip install eea.frame``

In your project's ``settings.py`` add::

  INSTALLED_APPS = (
  ... # django apps
  'frame'
  ... # your project's apps
  )
 
  MIDDLEWARE_CLASSES = (
    'frame.middleware.RequestMiddleware',
    'frame.middleware.UserMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  )
  
  TEMPLATE_LOADERS = (
    'frame.middleware.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
  )
  
Also, usually in ``local_settings.py`` you need to define: ``FRAME_URL`` to an
url pointing to a Zope frame instance, and
``FRAME_COOKIES = ['__ac', '_ZopeId', '__ginger_snap']``.

You can skip https with ``FRAME_VERIFY_SSL = False``.

Your ``layout.html`` must extend ``"frame.html"`` in order to use the frame.

You can set ``FRAME_EXTRA_SUBSTITUTIONS`` to a list of pairs to be replaced
in the frame html.

Authentication Backend
----------------------
If you want to use the Django groups and permissions settings with users from
_eea.frame_, you need to set::

  MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    ...
  )

  AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'frame.backends.FrameUserBackend',
  )

For each user that is authenticated on *eea.frame*, a
``django.contrib.auth.models.User`` instance is created.

For each of the roles the user has in *eea.frame*, a
``django.contrib.auth.models.Group`` instance is created, and you can assign
permissions to that group.

Seen Middleware
---------------
Use the seen middleware to keep for each user the datetime of the last visit
to the application.

Set (at the end of the middleware classes setting)::

  MIDDLEWARE_CLASSES = (
    ...
    'frame.middleware.SeenMiddleware',
  )

If you want to use the default view, add
``frame.utils.get_objects_from_last_seen_count`` to your url patterns, in a
location such as ``^/_lastseen/$``, then set the ``FRAME_SEEN_MODELS`` to a
list of pairs (model, field) for the objects to be counted.

You should exclude this view using ``FRAME_SEEN_EXCLUDE`` config setting.
