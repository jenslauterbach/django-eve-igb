**Please feel free to write feature requests and bug reports!**

[![Build Status](https://secure.travis-ci.org/jenslauterbach/django-eve-igb.png)](http://travis-ci.org/jenslauterbach/django-eve-igb)

# django-eve-igb
------------------

A collection of helpers to handle the [EVE Online](http://eveonline.com "EVE Online website") ingame browser (IGB) within your Django views and templates.

At the moment the project is in its early stages and only contains the following:

* Template context processor
* HttpRequest parser that parses the EVE Online IGB HTTP headers

# Setup instructions
------------------

Basically you do have three options how you can install django-eve-igb:

1. [Download](https://github.com/jenslauterbach/django-eve-igb/zipball/master "Direct download link") the latest version and run `python setup.py install`
2. Clone repository and run `python setup.py install` 
3. Run `pip install git+https://github.com/jenslauterbach/django-eve-igb.git`

# Quickstart
------------------

After you installed django-eve-igb open your `settings.py` and do the following changes: 

1. Add `eveigb` to `INSTALLED_APPS`
2. Add `eveigb.context_processors.igb_headers` to  `TEMPLATE_CONTEXT_PROCESSORS`.

Now open one of your templates and add:

    {% if eveigb.is_igb %}
      I am looking at this page with the EVE Online IGB!
    {% endif %}

If you visit that page from within EVE Online using the IGB you should see this text.

# What's missing
------------------

Documentation, documentation and documentation.