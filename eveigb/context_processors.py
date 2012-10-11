from eveigb import IGBHeaders

from .settings import EVEIGB_CONTEXT_VAR_NAME

def igb_headers(request):
    """ Returns the parsed IGB headers. """
    return { EVEIGB_CONTEXT_VAR_NAME : IGBHeaders(request)}