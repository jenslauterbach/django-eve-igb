from django.test import TestCase
from django.http import HttpRequest

from eveigb import IGBHeaders


class IGBHeadersTestCase(TestCase):
    
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
        
        self.igbheaders_attributes = [
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
        """ Searches the given IGBHeaders instance for the given
        unexpected attributes. Under certain circumstances the IGBHeaders
        instance does not contain all possible attributes.
        
        Keyword arguments:
        instance -- The IGBHeaders instance
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
        Tests if 'TypeError' is thrown when IGBHeaders is initialized without
        a 'django.http.HttpRequest' instance.
        """
        with self.assertRaises(TypeError):
            IGBHeaders('Not django.http.HttpRequest')
        
        with self.assertRaises(TypeError):
            IGBHeaders(None)
    
    #--------------------------------------------------------------------------
    # Normal tests
    #--------------------------------------------------------------------------
    def test_none_igb_browser(self):
        """
        Test that 'is_igb' returns 'False' if the 'HTTP_EVE_TRUSTED' header
        is not present in the request. That usually means that the players
        browser is not IGB.
        """
        request = self.test_request
        del request.META['HTTP_EVE_TRUSTED']
        headers = IGBHeaders(request)
        
        self.assertFalse(headers.is_igb)
        
        unexpected_attributes = self.igbheaders_attributes
        unexpected_attributes.remove('is_igb')
        
        self._search_for_unexpected_attributes(headers, unexpected_attributes)
        
    def test_untrusted_request(self):
        """
        Tests that only 'is_igb' and 'trusted' attributes are set on the
        IGBHeaders object if the user does not trust the site.
        """
        request = self.test_request
        request.META['HTTP_EVE_TRUSTED'] = 'No'
        headers = IGBHeaders(request)
        
        self.assertTrue(headers.is_igb)
        self.assertFalse(headers.trusted)
        
        unexpected_attributes = self.igbheaders_attributes
        unexpected_attributes.remove('is_igb')
        unexpected_attributes.remove('trusted')
        
        self._search_for_unexpected_attributes(headers, unexpected_attributes)
        
    
    def test_with_all_headers_set(self):
        """
        This teset checks if all headers are correctly applied to their
        respective class attributes.
        """
        request = self.test_request
        headers = IGBHeaders(request)
        
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
        This test ensures that IGBHeaders.warfactionid is set when
        the 'HTTP_EVE_WARFACTIONID' header is set.
        """
        request = self.test_request
        headers = IGBHeaders(request)
        
        self.assertEquals(headers.warfactionid, 8)
        
    def test_warfactionid_not_set(self):
        """
        This test ensures that IGBHeaders.warfactionid == None when
        the user is not participating in Factional Warfare. In this
        case the 'HTTP_EVE_WARFACTIONID' won't be set.
        """
        request = self.test_request
        del request.META['HTTP_EVE_WARFACTIONID']
        headers = IGBHeaders(request)
        
        self.assertEquals(headers.warfactionid, 0)
    
    def test_player_on_station(self):
        """
        In this test we check if the attributes 'stationname' and 'stationid'
        are set correctly. When players are on station these values will be
        set.
        """
        request = self.test_request
        headers = IGBHeaders(request)
        
        self.assertEquals(headers.stationname, 'Test STATIONNAME')
        self.assertEquals(headers.stationid, 5)
    
    def test_player_not_on_station(self):
        """
        When the player is in space the value the IGB won't send the
        corresponding headers 'HTTP_EVE_STATIONNAME' and 'HTTP_EVE_STATIONID'.
        In that case IGBHeaders.stationname and IGBHeaders.stationid should
        return their defaults:
        
        stationname = '' (empty string)
        stationid = 0
        
        This test is going to ensure that behaviour.
        """
        request = self.test_request
        del request.META['HTTP_EVE_STATIONNAME']
        del request.META['HTTP_EVE_STATIONID']
        headers = IGBHeaders(request)
        
        self.assertEquals(headers.stationname, '')
        self.assertEquals(headers.stationid, 0)
        
    def test_corp_roles_set(self):
        """
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
        headers = IGBHeaders(request)
        
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
        Tests if attribute 'corprules' returns an empty list and
        attribute 'corprole' returns 0 when the player does not have
        any corp roles.
        """
        request = self.test_request
        del request.META['HTTP_EVE_CORPROLE']
        headers = IGBHeaders(request)
    
        self.assertEquals(headers.corproles, [])
        self.assertEquals(headers.corprole, 0)