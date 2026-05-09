# Käyttöohje

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

Aloitusnäkymästä painamalla Rekisteröidy-nappia pääsee luomaan käyttäjätunnuksen. Anna ensimmäiseen kenttään käyttäjänimi ja kahteen seuraavaan sama salasana. Paina lopuksi Luo-painiketta. Onnistuneen rekisteröitymisen jälkeen sovellus palauttaa aloitusnäkymän, jossa on myös mahdollista kirjautua sisään.

## Sisäänkirjautuminen

Alkunäkymästä löytyvät kirjautumiskentät. Täytä ylemään luomasi tunnuksen käyttäjänimi ja alempaan salasana. Napauta Kirjaudu-nappulaa. Sovellus ohjaa sinut etusivulle kirjauduttuasi sisään.

## Uloskirjautuminen

Kirjauduttuasi siään pääset uloskirjautumaan painamalla Kirjaudu ulos -painiketta, joka löytyy näkymän yläreunalta."

## Maailman luonti

Etusivun yläriviltä löydät Luo maailma -pinikkeen. Sitä painamalla pääset sovellus vie sinut sivulle, jonka ensimmäisessä kentässä voit nimetä maailman ja kolmanteen voit kirjoittaa kuvauksen. Muista myös valita maailmalle luokka. Tällä hetkellä niitä on vain yksi. Voit tallentaa maailman siirtymättä maailman katselunäkymään painamalla Tallenna-nappia. Kun olet tyytyväinen maailmaasi napauta Tallenna ja näytä -nappulaa. Ohjelma siirtää sinut näkymään, jossa voit tarkastella maailmaa. Ohjelma tekee sinusta automaattisesti maailman haltijan.

## Maailman muokkaaminen

Maailman tarkastelunäkymän alareunalta löydät Muokkaa-näppäimen, jota painamalla pääset muokkausnäkymään. Tallenna- sekä Tallenna ja näytä -näppäimet toimivat kuten maailman luonnissa. Takaisin maailmaan -nappula vie sinut takaisin katselemaan maailmaa tallentamatta muutoksia.

## Maailman hakeminen

Kirjautumisen jälkeen jokaisen näkymän yläreunassa näkyy hakukenttä, josta maailmaa voi hakea hakusanalla. Kirjoita hakusana tai lauseke kenttään ja paina Hae-nappia. Haku etsii sanaa tai lauseketta maailman/hankkeen nimestä ja kuvauksesta. Tulokset se esittää listana. Maailman voi avata tarkastelunäkymään kaksoisnapauttamalla sitä listassa. Tarkastelunäkymästä pääset muokkaamaan tai poistamaan maailman, jos olet sen haltija. Pääset tarkastelunäkymästä takaisin hakutuloksiin napauttamalla Takaisin hakutuloksiin -nappulaa.
