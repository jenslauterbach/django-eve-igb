from django.test import TestCase
from django.http import HttpRequest

from eveigb import IGBHeaderParser


class IGBHeaderParserTestCase(TestCase):
    
    #-------------------------------------------------------------------------
    # Test set up
    #-------------------------------------------------------------------------
    def setUp(self):
        # Create a test request that contains ALL headers
        # Modify this request to your needs in your test.
        request = HttpRequest()
        request.META['HTTP_EVE_TRUSTED'] = 'Yes'
        request.META['HTTP_EVE_SERVERIP'] = '0.0.0.0:26000'
        request.META['HTTP_EVE_CHARNAME'] = 'Test CHARNAME'
        request.META['HTTP_EVE_CHARID'] = '1'
        request.META['HTTP_EVE_CORPNAME'] = 'Test CORPNAME'
        request.META['HTTP_EVE_CORPID'] = '2'
        request.META['HTTP_EVE_ALLIANCENAME'] = 'Test ALLIANCENAME'
        request.META['HTTP_EVE_ALLIANCEID'] = '3'
        request.META['HTTP_EVE_REGIONNAME'] = 'Test REGIONNAME'
        request.META['HTTP_EVE_CONSTELLATIONNAME'] = 'Test CONSTELLATIONNAME'
        request.META['HTTP_EVE_SOLARSYSTEMID'] = '4'
        request.META['HTTP_EVE_SOLARSYSTEMNAME'] = 'Test SOLARSYSTEMNAME'
        request.META['HTTP_EVE_STATIONNAME'] = 'Test STATIONNAME'
        request.META['HTTP_EVE_STATIONID'] = '5'
        request.META['HTTP_EVE_CORPROLE'] = '0'
        request.META['HTTP_EVE_SHIPID'] = '6'
        request.META['HTTP_EVE_SHIPNAME'] = 'Test SHIPNAME'
        request.META['HTTP_EVE_SHIPTYPEID'] = '7'
        request.META['HTTP_EVE_SHIPTYPENAME'] = 'Test SHIPTYPENAME'
        request.META['HTTP_EVE_WARFACTIONID'] = '8'
        
        self.test_request = request
        
        self.IGBHeaderParser_attributes = [
            'is_igb',
            'trusted',
            'serverip',
            'charname',
            'charid',
            'corpname',
            'corpid',
            'alliancename',
            'allianceid',
            'regionname',
            'constellationname',
            'solarsystemid',
            'solarsystemname',
            'stationname',
            'stationid',
            'corprole',
            'shipid',
            'shipname',
            'shiptypeid',
            'shiptypename',
            'warfactionid'
        ]
    
    #-------------------------------------------------------------------------
    # Test utilities
    #-------------------------------------------------------------------------
    def _search_for_unexpected_attributes(self, instance, unexpected_attributes):
        """ Searches the given IGBHeaderParser instance for the given
        unexpected attributes. Under certain circumstances the IGBHeaderParser
        instance does not contain all possible attributes.
        
        Keyword arguments:
        instance -- The IGBHeaderParser instance
        unexpected_attributes -- List of the attributes that are not allowed
          to be part of the instances attributes.
          
        """
        for attribute in unexpected_attributes:
            self.assertNotIn(attribute, instance.__dict__)
    
    #--------------------------------------------------------------------------
    # Exception tests
    #--------------------------------------------------------------------------
    def test_init_with_none_request(self):
        """
        test_init_with_none_request
        
        Tests if 'TypeError' is thrown when IGBHeaderParser is initialized without
        a 'django.http.HttpRequest' instance.
        """
        with self.assertRaises(TypeError):
            IGBHeaderParser('Not django.http.HttpRequest')
        
        with self.assertRaises(TypeError):
            IGBHeaderParser(None)
    
    #--------------------------------------------------------------------------
    # Normal tests
    #--------------------------------------------------------------------------
    def test_none_igb_browser(self):
        """
        test_none_igb_browser
        
        Test that 'is_igb' returns 'False' if the 'HTTP_EVE_TRUSTED' header
        is not present in the request. That usually means that the players
        browser is not IGB.
        """
        request = self.test_request
        del request.META['HTTP_EVE_TRUSTED']
        headers = IGBHeaderParser(request)
        
        self.assertFalse(headers.is_igb)
        
    def test_untrusted_request(self):
        """
        test_untrusted_request
        
        Tests that only 'is_igb' and 'trusted' attributes are set on the
        IGBHeaderParser object if the user does not trust the site.
        """
        request = self.test_request
        request.META['HTTP_EVE_TRUSTED'] = 'No'
        headers = IGBHeaderParser(request)
        
        self.assertTrue(headers.is_igb)
        self.assertFalse(headers.trusted)
    
    def test_with_all_headers_set(self):
        """
        test_with_all_headers_set
        
        This test checks if all headers are correctly applied to their
        respective class attributes.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        self.assertTrue(headers.trusted)
        self.assertTrue(headers.is_igb)
        self.assertEquals(headers.serverip, '0.0.0.0:26000')
        self.assertEquals(headers.charname, 'Test CHARNAME')
        self.assertEquals(headers.charid, 1)
        self.assertEquals(headers.corpname, 'Test CORPNAME')
        self.assertEquals(headers.corpid, 2)
        self.assertEquals(headers.alliancename, 'Test ALLIANCENAME')
        self.assertEquals(headers.allianceid, 3)
        self.assertEquals(headers.regionname, 'Test REGIONNAME')
        self.assertEquals(headers.constellationname, 'Test CONSTELLATIONNAME')
        self.assertEquals(headers.solarsystemid, 4)
        self.assertEquals(headers.solarsystemname, 'Test SOLARSYSTEMNAME')
        self.assertEquals(headers.stationname, 'Test STATIONNAME')
        self.assertEquals(headers.stationid, 5)
        self.assertEquals(headers.corprole, 0)
        self.assertEquals(headers.shipid, 6)
        self.assertEquals(headers.shipname, 'Test SHIPNAME')
        self.assertEquals(headers.shiptypeid, 7)
        self.assertEquals(headers.shiptypename, 'Test SHIPTYPENAME')
        self.assertEquals(headers.warfactionid, 8)
    
    def test_warfactionid_is_set(self):
        """
        test_warfactionid_is_set
        
        This test ensures that IGBHeaderParser.warfactionid is set when
        the 'HTTP_EVE_WARFACTIONID' header is set.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        self.assertEquals(headers.warfactionid, 8)
        
    def test_warfactionid_not_set(self):
        """
        test_warfactionid_not_set
        
        This test ensures that IGBHeaderParser.warfactionid == None when
        the user is not participating in Factional Warfare. In this
        case the 'HTTP_EVE_WARFACTIONID' won't be set.
        """
        request = self.test_request
        del request.META['HTTP_EVE_WARFACTIONID']
        headers = IGBHeaderParser(request)
        
        self.assertEquals(headers.warfactionid, 0)
    
    def test_player_on_station(self):
        """
        test_player_on_station
        
        In this test we check if the attributes 'stationname' and 'stationid'
        are set correctly. When players are on station these values will be
        set.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        self.assertEquals(headers.stationname, 'Test STATIONNAME')
        self.assertEquals(headers.stationid, 5)
    
    def test_player_not_on_station(self):
        """
        test_player_not_on_station
        
        When the player is in space the value the IGB won't send the
        corresponding headers 'HTTP_EVE_STATIONNAME' and 'HTTP_EVE_STATIONID'.
        In that case IGBHeaderParser.stationname and IGBHeaderParser.stationid should
        return their defaults:
        
        stationname = '' (empty string)
        stationid = 0
        
        This test is going to ensure that behaviour.
        """
        request = self.test_request
        del request.META['HTTP_EVE_STATIONNAME']
        del request.META['HTTP_EVE_STATIONID']
        headers = IGBHeaderParser(request)
        
        self.assertEquals(headers.stationname, '')
        self.assertEquals(headers.stationid, 0)
        
    def test_corp_roles_set(self):
        """
        test_corp_roles_set
        
        This test will check if the bitmask '1039225405767189504' will be
        resolved to the following set of roles:
        
        1024 ---> Factory Manager
        32768 ---> Hangar Can Take Division 3
        1048576 ---> Hangar Can Query Division 1
        4194304 ---> Hangar Can Query Division 3
        536870912 ---> Account Can Take Division 3
        2199023255552 ---> Equipment Config
        17592186044416 ---> Container Can Take Division 3
        1125899906842624 ---> Can Rent Factory Slot
        2251799813685248 ---> Can Rent Research Slot
        9007199254740992 ---> Starbase Config
        18014398509481984 ---> Trader
        """
        request = self.test_request
        request.META['HTTP_EVE_CORPROLE'] = '1039225405767189504'
        headers = IGBHeaderParser(request)
        
        expected_corp_role_ids = [1024, 32768, 1048576, 4194304,
            536870912, 2199023255552, 17592186044416, 1125899906842624,
            2251799813685248, 9007199254740992, 18014398509481984
        ]
        
        corproles = headers.corproles
        
        # check that the lenghts match
        self.assertEquals(len(corproles), len(expected_corp_role_ids))
        
        for corprole in corproles:
            self.assertIn(corprole['id'], expected_corp_role_ids)
    
    def test_corp_roles_not_set(self):
        """
        test_corp_roles_not_set
        
        Tests if attribute 'corprules' returns an empty list and
        attribute 'corprole' returns 0 when the player does not have
        any corp roles.
        """
        request = self.test_request
        del request.META['HTTP_EVE_CORPROLE']
        headers = IGBHeaderParser(request)
    
        self.assertEquals(headers.corproles, [])
        self.assertEquals(headers.corprole, 0)

    def test_is_on_station(self):
        """
        test_is_on_station
        
        If the player is in space the station name will not be set
        (empty String). So 'headers.is_on_station' should return False. If the
        player is on a station 'headers.is_on_station' should return True.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        # Station name is set so headers.is_on_station has to return True
        self.assertTrue(headers.is_on_station)
        
        # Remove the station name from the headers and parse the headers again.
        # This time headers.is_on_station must return False
        del request.META['HTTP_EVE_STATIONNAME']
        headers = IGBHeaderParser(request)
        
        self.assertFalse(headers.is_on_station)

    def test_has_alliance(self):
        """
        test_has_alliance
        
        If the player is not in an alliance the property should be set to False,
        otherwise True.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        # The alliance name is set, therefor the player is in an alliance and
        # the property should return True.
        self.assertTrue(headers.has_alliance)
        
        # Now the alliance name is removed from the request headers. That means
        # that 'has_alliance' should return False.
        request = self.test_request
        del request.META['HTTP_EVE_ALLIANCENAME']
        headers = IGBHeaderParser(request)
        
        self.assertFalse(headers.has_alliance)

    def test_has_corproles(self):
        """
        test_has_corproles
        
        If the player has corproles the property 'has_corproles' must be set to
        'True'. If the player hs no corproles it must be set to False.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        # In the default test headers the corp role bitmask is set
        # to 0 (no roles). Therefor 'has_corproles' must be set to False.
        self.assertFalse(headers.has_corproles)
        
        # Now change the corprole header to '1' (director). The property
        # 'has_corproles' must have the value 'True' now.
        request = self.test_request
        request.META['HTTP_EVE_CORPROLE'] = '1'
        headers = IGBHeaderParser(request)
        
        self.assertTrue(headers.has_corproles)

    def test_is_factionwarefare(self):
        """
        test_is_factionwarefare
        
        Tests if 'is_factionwarfare' is set to 'True' if the player attends
        faction warfare. If the player is not engaged in faction warfare the
        property has to be set to 'False'.
        """
        request = self.test_request
        headers = IGBHeaderParser(request)
        
        # In the default request (test_request) faction warfare id is set to '8'.
        # The player is engaged in faction warfare and therefor the property
        # 'is_factionwarfare' must be set to 'True'.
        self.assertTrue(headers.is_factionwarfare)
        
        # Now the faction warfare id is deleted from the request and the headers
        # are parsed again. Now the propert 'is_factionwarfare' must be 'False'.
        request = self.test_request
        del request.META['HTTP_EVE_WARFACTIONID']
        headers = IGBHeaderParser(request)
        
        self.assertFalse(headers.is_factionwarfare)
        