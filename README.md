# Ohjelmistotekniikka, harjoitustyö

Sovellus on trakoitettu **maailmanrakentamiseen** _tarinan kirjoittamista ja roolipelaamista_ varten.

## Python-versio

Sovellusta on testattu `Python`-versioilla `3.12` ja `3.14`.

## Dokumentaatio

- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)

## Sovelluksen asennus

### Alkutoimet

1. Varmista, että koneellasi on asennettuna vähintään `Python`-versio `3.12`.
2. Varmista, että koneellasi on asennettuna vähintään `Poetry`-versio `2.0.0`. 

### Asennus

1. Asenna riippuvuudet käskyllä:

```bash
poetry install
```

2. Käynnistä sovellus käskyllä*:

```bash
poetry run invoke build-start
```

*Jos haluat alustaa ja ajaa sovelluksen erikseen, voit käyttää käskyä `poetry run invoke build` alustamiseen ja `poetry run invoke start`käynnistämiseen.

### Test
