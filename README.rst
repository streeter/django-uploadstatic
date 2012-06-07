===================
django-uploadstatic
===================

This is a Django app that provides helpers for uploading static files.

It is based off of `github.com/jezdez/django-staticfiles`_
but only uploads all the files in the collected `STATIC_ROOT` to S3 using
the ``storages.backends.s3boto.S3BotoStorage`` storage backend in the
``django-storages`` app.

Installation
------------

- Use your favorite Python packaging tool to install ``uploadstatic``
  from `PyPI`_, e.g.::

    pip install django-uploadstatic

- Added ``"uploadstatic"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # ...
        "uploadstatic",
    ]

- Set your ``STATIC_URL`` setting to the URL that handles serving
  static files from S3::

    STATIC_URL = "https://s3.amazonaws.com/some-domain/"

- Once you are ready to upload all static files that have been collecte in your
  site's ``STATIC_ROOT``, use the ``uploadstatic`` management
  command::

    python manage.py uploadstatic

  Then your files will be accessible from the ``STATIC_URL`` setting.

.. _github.com/jezdez/django-staticfiles: http://github.com/jezdez/django-staticfiles
.. _PyPI: http://pypi.python.org/pypi/django-uploadstatic
