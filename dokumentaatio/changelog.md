# Changelog

## Viikko 3

- Käyttäjä pystyy rekisteröitymään sovellukseen.
- Sovellukseen on lisätty luokat: 
    - DatabaseInterface-luokka, joka halinnoi tietokantakutsuja.
    - Users-luokka, joka määrittelee käyttäjäolion.
    - UserRepository-luokka, joka hallitsee käyttäjiin liittyviä tietokantatoimintoja.
    - Repositories-luokka, joka kokoaa eri tietokantatoimintopalvelut yhdeksi.
    - UserService-luokka, joka vastaa käyttäjiin liittyvästä sovelluslogiikasta.
    -  PasswordService-luokka, joka tarjoaa metodeja salasanojen käsittelyyn.
    - Services-luokka, joka kokoaa eri palvelut yhdeksi.
- DatabaseInterface-luokkasta on testattu, että sen query-metodi palauttaa listan.
