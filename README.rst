EEA Frame
=========

Django integration middleware for EEA Zope websites.


Usage
-----

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
  
Also, usually in ``local_settings.py`` you need to define: ``FRAME_URL`` to an url pointing to a Zope frame instance.
