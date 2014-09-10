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
``FRAME_COOKIES = ['__ac', '_ZopeId']``.

Your ``layout.html`` must extend ``"frame.html"`` in order to use the frame.

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

For each user that is authenticated on _eea.frame_, a
``django.contrib.auth.models.User`` instance is created.

For each of the roles the user has in _eea.frame_, a
``django.contrib.auth.models.Group`` instance is created, and you can assign
permissions to that group.
