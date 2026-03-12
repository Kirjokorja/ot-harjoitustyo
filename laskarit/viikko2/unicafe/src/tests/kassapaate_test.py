import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(500)

    def test_kassalla_on_tuhat_euroa_aloitusvaroja(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

    def test_luontihetkella_kassa_ei_ole_myynyt_maukkaita_lounaita(self):
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_luontihetkella_kassa_ei_ole_myynyt_edullisia_lounaita(self):
        self.assertEqual(self.kassa.edulliset, 0)

    def test_edullisen_lounaan_ostaminen_kateisella_kasvattaa_kassavaroja_hinnan_verran(self):
        self.kassa.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1002.4)
    
    def test_edullisen_lounaan_ostaminen_kateisella_kasvattaa_myytyjen_lounaiden_maaraa_yhdella(self):
        self.kassa.syo_edullisesti_kateisella(240)

        self.assertEqual(self.kassa.edulliset, 1)
    
    def test_edullisen_lounaan_ostaminen_kateisella_palauttaa_vaihtorahaa_oikean_maaran(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(300), 60)
    
    def test_edullisen_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_ei_kasvata_myytyjen_lounaiden_maaraa(self):
        self.kassa.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassa.edulliset, 0)

    def test_edullisen_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_ei_kasvata_kasssavaroja(self):
        self.kassa.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)
    
    def test_edullisen_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_palauttaa_ostorahat_vaihtorahana(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(200), 200)
    
    def test_maukkaan_lounaan_ostaminen_kateisella_kasvattaa_kassavaroja_hinnan_verran(self):
        self.kassa.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1004.0)
    
    def test_maukkaan_lounaan_ostaminen_kateisella_kasvattaa_myytyjen_lounaiden_maaraa_yhdella(self):
        self.kassa.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassa.maukkaat, 1)
    
    def test_maukkaan_lounaan_ostaminen_kateisella_palauttaa_vaihtorahaa_oikean_maaran(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(500), 100)
    
    def test_maukkaan_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_ei_kasvata_myytyjen_lounaiden_maaraa(self):
        self.kassa.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassa.maukkaat, 0)

    def test_maukkaan_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_ei_kasvata_kasssavaroja(self):
        self.kassa.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)
    
    def test_maukkaan_lounaaan_ostaminen_riittamattomilla_kateisvaroilla_palauttaa_ostorahat_vaihtorahana(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(100), 100)

    def test_edullisen_lounaan_osto_onnistuu_riittavilla_korttivaroilla(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)
    
    def test_edullisen_lounaan_osto_veloittaa_hinnan_kortilta(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo_euroina(), 2.6)
    
    def test_edullisen_lounaan_osto_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassa.edulliset, 1)
    
    def test_edullisen_lounaan_ostaminen_riittamattomalla_saldolla_ei_onnistu(self):
        kortti = Maksukortti(100)

        self.assertEqual(self.kassa.syo_edullisesti_kortilla(kortti), False)
    
    def test_edullisen_lounaan_ostaminen_riittamattomalla_saldolla_ei_veloita_rahaa_kortilta(self):
        kortti = Maksukortti(100)
        self.kassa.syo_edullisesti_kortilla(kortti)

        self.assertEqual(kortti.saldo_euroina(), 1.0)
    
    def test_edullisen_lounaan_ostaminen_riittamattomalla_saldolla_ei_muuta_myytyjen_lounaiden_maaraa(self):
        kortti = Maksukortti(100)
        self.kassa.syo_edullisesti_kortilla(kortti)

        self.assertEqual(self.kassa.edulliset, 0)
    
    def test_edullisen_lounaan_ostaminen_kortilla_ei_muuta_kassavaroja(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

    def test_maukkaan_lounaan_osto_onnistuu_riittavilla_korttivaroilla(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)
    
    def test_maukkaan_lounaan_osto_veloittaa_hinnan_kortilta(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo_euroina(), 1.0)
    
    def test_maukkaan_lounaan_osto_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassa.maukkaat, 1)
    
    def test_maukkaan_lounaan_ostaminen_riittamattomalla_saldolla_ei_onnistu(self):
        kortti = Maksukortti(100)

        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), False)
    
    def test_maukkaan_lounaan_ostaminen_riittamattomalla_saldolla_ei_veloita_rahaa_kortilta(self):
        kortti = Maksukortti(100)
        self.kassa.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo_euroina(), 1.0)
    
    def test_maukkaan_lounaan_ostaminen_riittamattomalla_saldolla_ei_muuta_myytyjen_lounaiden_maaraa(self):
        kortti = Maksukortti(100)
        self.kassa.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(self.kassa.maukkaat, 0)

    def test_maukkaan_lounaan_ostaminen_kortilla_ei_muuta_kassavaroja(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)
    
    def test_kortin_lataaminen_kasvattaa_korttivaroja_oikealla_summalla(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 2000)

        self.assertEqual(self.kortti.saldo_euroina(), 25.0)

    def test_kortin_lataaminen_kasvattaa_kassavaroja_oikealla_summalla(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 2000)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1020.0)
    
    def test_kortin_lataaminen_negatiivisella_summalla_ei_kasvata_korttisaldoa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -2000)

        self.assertEqual(self.kortti.saldo_euroina(), 5.0)
    
    def test_kortin_lataaminen_negatiivisella_summalla_ei_kasvata_kassavaroja(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -2000)

        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)
