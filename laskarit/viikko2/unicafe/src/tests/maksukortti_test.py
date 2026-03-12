import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_konstruktori_asettaa_saldon(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_rahaa_voi_ladata_kortille(self):
        self.maksukortti.lataa_rahaa(200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 12.0)
    
    def test_rahaa_voi_nostaa_kortilta(self):
        self.maksukortti.ota_rahaa(500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)
    
    def test_rahaa_ei_voi_nostaa_jos_varoja_ei_ole_riittavasti(self):
        self.maksukortti.ota_rahaa(2000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_metodi_palauttaa_true_jos_varat_riittavat_rahannostossa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_metodi_palauttaa_false_jos_varat_eivat_riita_rahannostossa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(2000), False)

    def test_tulostusmetodi_tulostaa_halutun_merkkijonon(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")