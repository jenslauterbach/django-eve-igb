**Please feel free to write feature requests and bug reports!**

[![Build Status](https://secure.travis-ci.org/jenslauterbach/django-eve-igb.png)](http://travis-ci.org/jenslauterbach/django-eve-igb)

# django-eve-igb
-------------------

This project is first and foremost a simple to use Django wrapper around the HTTP headers that are send by [EVE Onlines](http://eveonline.com "EVE Online website") ingame browser (IGB).
When a player visits a website with the IGB it will send a "wealth of additional information in its HTTP header". A full list of those headers can be found here: [List of IGB HTTP headers](http://wiki.eveonline.com/en/wiki/IGB_Headers).

At the moment the project is in its early stages and only contains the following:

* A Django template context processor that exposes the data from the IGB HTTP headers to your templates.
* HttpRequest parser that parses the EVE Online IGB HTTP headers.

# Requirements
-------------------

* Python >= 2.6
* Django >= 1.3.1

django-eve-igb might work with older versions of Python and Django but I won't support them officially. If you want to run bundled tests read the section "How to run tests".

# Setup instructions
-------------------

Basically you do have three options how you can install django-eve-igb:

1. [Download](https://github.com/jenslauterbach/django-eve-igb/zipball/master "Direct download link") the latest version and run `python setup.py install`
2. Clone repository and run `python setup.py install` 
3. Run `pip install git+https://github.com/jenslauterbach/django-eve-igb.git`

# Quickstart
-------------------

After you installed django-eve-igb open your `settings.py` and do the following changes: 

1. Add `eveigb` to `INSTALLED_APPS`
2. Add `eveigb.context_processors.igb_headers` to  `TEMPLATE_CONTEXT_PROCESSORS`.

Now open one of your templates and add:

    {% if eveigb.is_igb %}
      I am looking at this page with the EVE Online IGB!
    {% endif %}

If you visit that page from within EVE Online using the IGB you should see this text: **I am looking at this page with the EVE Online IGB!**

# How to run tests
-------------------

1. Install test requirements with `pip install -r requirements_tests.txt`
2. Run tests with `python eveigb/tests/runtests.py eveigb.tests.tests:IGBHeadersTestCase`

Note: I want to make running tests easier but didn't found a way yet.

# Documentation
-------------------

You can find the documentation in the Wiki: [https://github.com/jenslauterbach/django-eve-igb/wiki/Documentation](https://github.com/jenslauterbach/django-eve-igb/wiki/Documentation)