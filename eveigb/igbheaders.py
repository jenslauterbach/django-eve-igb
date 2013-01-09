from django.http import HttpRequest

from .constants import CORP_ROLES


class IGBHeaderParser(object):
    def __init__(self, request):
        if not isinstance(request, HttpRequest):
            raise TypeError("Argument 'request' must be of type django.http.HttpRequest!")

        self._parse_igb_headers(request)

    def _get_corp_roles(self, corp_roles_bit_mask=0):
        """Returns the list of corp roles the player with the given
        'corp_roles_bit_mask' has. If the player does not have any corp roles
        an empty list will be returned.

        Keyword arguments:
        corp_roles_bit_mask -- the corp role bitmask from 'HTTP_EVE_CORPROLE' (default: 0)

        """
        roles = [role for role in CORP_ROLES if (role['id'] & corp_roles_bit_mask) > 0]

        return roles

    def _parse_igb_headers(self, request):
        """ Parses the HTTP_EVE_* headers from IGB and sets the header values as class attributes.

        Keyword arguments:
        request -- Django HttpRequest object
        
        """
        # More information on the headers can be found in CCPs documentation:
        # http://wiki.eveonline.com/en/wiki/IGB_Headers
        self.is_igb = True if 'HTTP_EVE_TRUSTED' in request.META else False
        self.trusted = True if request.META.get('HTTP_EVE_TRUSTED', 'No') == 'Yes' else False

        # only if the user trusted the website the other HEADERS will be send by the IGB.
        #if self.trusted:
        self.serverip = request.META.get('HTTP_EVE_SERVERIP', '')
        self.charname = request.META.get('HTTP_EVE_CHARNAME', '')
        self.charid = int(request.META.get('HTTP_EVE_CHARID', 0))
        self.corpname = request.META.get('HTTP_EVE_CORPNAME', '')
        self.corpid = int(request.META.get('HTTP_EVE_CORPID', 0))
        self.regionname = request.META.get('HTTP_EVE_REGIONNAME', '')
        self.constellationname = request.META.get('HTTP_EVE_CONSTELLATIONNAME', '')
        self.solarsystemid = int(request.META.get('HTTP_EVE_SOLARSYSTEMID', 0))
        self.solarsystemname = request.META.get('HTTP_EVE_SOLARSYSTEMNAME', '')
        self.shipid = int(request.META.get('HTTP_EVE_SHIPID', 0))
        self.shipname = request.META.get('HTTP_EVE_SHIPNAME', '')
        self.shiptypeid = int(request.META.get('HTTP_EVE_SHIPTYPEID', 0))
        self.shiptypename = request.META.get('HTTP_EVE_SHIPTYPENAME', '')

        # The following headers don't have to be set by the IGB.
        # That's why they are read from the request.META dict with get.
        # If the header is not set, a sane default will be returned.

        # Only set if the player has roles
        self.corprole = int(request.META.get('HTTP_EVE_CORPROLE', 0))
        self.corproles = self._get_corp_roles(self.corprole)
        
        # Only set if the players corporation is part of an alliance
        self.alliancename = request.META.get('HTTP_EVE_ALLIANCENAME', '')
        self.allianceid = int(request.META.get('HTTP_EVE_ALLIANCEID', 0))

        # Only set if the player is on a station
        self.stationname = request.META.get('HTTP_EVE_STATIONNAME', '')
        self.stationid = int(request.META.get('HTTP_EVE_STATIONID', 0))

        # Only set if the player is participating in factional warfare
        self.warfactionid = int(request.META.get('HTTP_EVE_WARFACTIONID', 0))

        self.is_on_station = True if self.stationname != '' else False
        self.is_factionwarfare = True if self.warfactionid != 0 else False
        self.has_alliance = True if self.alliancename != '' else False
        self.has_corproles = False if not self.corproles else True
