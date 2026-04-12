# Changelog

## Viikko 3

- Käyttäjä pystyy rekisteröitymään sovellukseen.
- Sovellukseen on lisätty luokat: 
    - DatabaseInterface-luokka, joka halinnoi tietokantakutsuja.
    - Users-luokka, joka määrittelee käyttäjäolion.
    - UserRepository-luokka, joka hallitsee käyttäjiin liittyviä tietokantatoimintoja.
    - Repositories-luokka, joka kokoaa eri tietokantatoimintopalvelut yhdeksi.
    - UserService-luokka, joka vastaa käyttäjiin liittyvästä sovelluslogiikasta.
    - PasswordService-luokka, joka tarjoaa metodeja salasanojen käsittelyyn.
    - Services-luokka, joka kokoaa eri palvelut yhdeksi.
- DatabaseInterface-luokkasta on testattu, että sen query-metodi palauttaa listan.

## Viikko 4

- Käyttäjä pystyy kirjautumaan sovellukseen
- PasswordService-luokka on varsinaiseti käytössä
- UserRepository-luokka sai uusia metodeita:
    - _get_user_from_row
    - _get_users_from_rows
- UserRepository-luokan julkiset metodit palauttavat User-olioita tietokannan rivien sijaan
- UserService-luokka sai kirjautumistoiminnallisuutta:
    - login-metodi
    - get_current_user-metodi
- Käyttäjä voi säätä fontin kokoa Ctrl+ArrowUp ja Ctrl+ArrowDown komennoilla
