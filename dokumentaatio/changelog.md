# Changelog

## Viikko 3

- Käyttäjä pystyy rekisteröitymään sovellukseen.
- Sovellukseen on lisätty luokat: 
    - DatabaseInterface-luokka, joka halinnoi tietokantakutsuja.
    - Users-luokka, joka määrittelee käyttäjäolion.
    - UserRepository-luokka, joka hallitsee käyttäjiin liittyviä tietokantatoimintoja.
    - UserService-luokka, joka vastaa käyttäjiin liittyvästä sovelluslogiikasta.
    - PasswordService-luokka, joka tarjoaa metodeja salasanojen käsittelyyn.
    - Services-luokka, joka kokoaa eri palvelut yhdeksi.
- DatabaseInterface-luokkasta on testattu, että sen query-metodi palauttaa listan.

## Viikko 4

- Käyttäjä pystyy kirjautumaan sovellukseen.
- PasswordService-luokka on varsinaiseti käytössä.
- UserRepository-luokka sai uusia metodeita:
    - _get_user_from_row
    - _get_users_from_rows
- UserRepository-luokan julkiset metodit palauttavat User-olioita tietokannan rivien sijaan.
- UserService-luokka sai kirjautumistoiminnallisuutta:
    - login-metodi
    - get_current_user-metodi
- Käyttäjä voi säätä fontin kokoa Ctrl+ArrowUp ja Ctrl+ArrowDown komennoilla.

## Viikko 5

- Käyttäjä pystyy kirjautumaan ulos.
- Käyttäjä pystyy luomaan maailman/hankkeen.
- Sovellukseen lisätyt luokat:
    - Projects, joka määrittelee hankeolion.
    - TypeClass, joka määrittelee tietokohteiden luokkaolion.
    - RepositoryBase, joka toimii emoluokkana erikoistuneimmille tietokantatoimintaluokille
    - ProjectRepository, joka vastaa hankkeiden tietokantatoiminnoista
    - ServiceBase, joka toimii emoluokkana erikoistuneemmille sovelluslogiikan luokille
    - ProjectService, joka vastaa hankkeiden toiminnoista sovelluksessa

## Viikko 6

- Käyttäjä pystyy muokkaamaan maailmaa/hanketta.
- Käyttäjä pystyy poistamaan maailman/hankkeen.
- Kaikki luokat on testattu.
