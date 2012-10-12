from eveigb import IGBHeaderParser

from .settings import EVEIGB_CONTEXT_VAR_NAME

def igb_headers(request):
    """ Returns the parsed IGB headers. """
    return { EVEIGB_CONTEXT_VAR_NAME : IGBHeaderParser(request)}