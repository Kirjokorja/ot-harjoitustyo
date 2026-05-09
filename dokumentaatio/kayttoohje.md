# Käyttöohje

Imuroi ohjelman viimeisin [julkaisu](https://github.com/Kirjokorja/ot-harjoitustyo/releases) valitsemalla haluamasi pakkaus Assets-osion alta. Pura pakkaus ja asenna se alta löytyvien ohjeiden mukaisesti.

## Asetusten määrittäminen

Ohjelman tallentamiseen käyttämän tietokannan nimeä voi muuttaa **.env**-tiesdostosta käsin. Tietokanta luodaan **data**-hakemistoon.

## Ohjelman asentaminen

1. Asenna riippuvuudet käskyllä:

```bash
poetry install
```

2. Alusta sovellus käskyllä:

```bash
poetry run invoke build
```

## Ohjelman kännistäminen

Käynnistä sovellus käskyllä:

```bash
poetry run invoke start
```

## Käyttäjän luonti

Aloitusnäkymästä painamalla _Rekisteröidy_-nappia pääsee luomaan käyttäjätunnuksen. Anna ensimmäiseen kenttään käyttäjänimi ja kahteen seuraavaan sama salasana. Paina lopuksi _Luo_-painiketta. Onnistuneen rekisteröitymisen jälkeen sovellus palauttaa aloitusnäkymän, jossa on myös mahdollista kirjautua sisään.

## Sisäänkirjautuminen

Alkunäkymästä löytyvät kirjautumiskentät. Täytä ylemään luomasi tunnuksen käyttäjänimi ja alempaan salasana. Napauta _Kirjaudu_-nappulaa. Sovellus ohjaa sinut etusivulle kirjauduttuasi sisään.

## Uloskirjautuminen

Kirjauduttuasi siään pääset uloskirjautumaan painamalla _Kirjaudu ulos_ -painiketta, joka löytyy näkymän yläreunalta."

## Maailman luonti

Etusivun yläriviltä löydät _Luo maailma_ -pinikkeen. Sitä painamalla pääset sovellus vie sinut sivulle, jonka ensimmäisessä kentässä voit nimetä maailman ja kolmanteen voit kirjoittaa kuvauksen. Muista myös valita maailmalle luokka. Tällä hetkellä niitä on vain yksi. Voit tallentaa maailman siirtymättä maailman katselunäkymään painamalla _Tallenna_-nappia. Kun olet tyytyväinen maailmaasi napauta _Tallenna ja näytä_ -nappulaa. Ohjelma siirtää sinut näkymään, jossa voit tarkastella maailmaa. Ohjelma tekee sinusta automaattisesti maailman haltijan.

## Maailman muokkaaminen

Maailman tarkastelunäkymän alareunalta löydät Muokkaa-näppäimen, jota painamalla pääset muokkausnäkymään. _Tallenna_- sekä _Tallenna ja näytä_ -näppäimet toimivat kuten maailman luonnissa. Takaisin maailmaan -nappula vie sinut takaisin katselemaan maailmaa tallentamatta muutoksia.

## Maailman hakeminen

Kirjautumisen jälkeen jokaisen näkymän yläreunassa näkyy hakukenttä, josta maailmaa voi hakea hakusanalla. Kirjoita hakusana tai lauseke kenttään ja paina _Hae_-nappia. Haku etsii sanaa tai lauseketta maailman/hankkeen nimestä ja kuvauksesta. Tulokset se esittää listana. Maailman voi avata tarkastelunäkymään kaksoisnapauttamalla sitä listassa. Tarkastelunäkymästä pääset muokkaamaan tai poistamaan maailman, jos olet sen haltija. Pääset tarkastelunäkymästä takaisin hakutuloksiin napauttamalla _Takaisin hakutuloksiin_ -nappulaa.
