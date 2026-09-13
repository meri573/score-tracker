# Tetris score tracker

## Sovelluksen toiminnot

* käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* käyttäjä pystyy lisäämään muokkaamaan ja poistamaan tetriksessä saamiaan tuloksia
* käyttäjä pystyy lisäämään kuvan tai videon todisteaineistoksi tuloksestaan
* käyttäjä voi lisätä kuvauksen tulokseensa
* käyttäjä näkee sovellukseen lisätyt tulokset
* käyttäjä pystyy etsimään tuloksia hakusanalla, pistemäärällä, tuloksen lisääjän tunnuksella, etc.
* sovelluksesa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tulokset
* käyttäjä pystyy valitsemaan tulokselle yhden tai useamman luokittelun (esim. tetris versio, pelimoodi, erikoisasetukset)
* käyttäjä voi lisätä kommentteja tuloksiin

## Sovelluksen asennus

Asenna `flask`
```
$ pip install flask
```
Luo tietokanta
```
$sqlite3 database.db < schema.sql
´´´

Käynnistä sovellus:
```
$flask run
```

Sovelluksessa voi tällä hetkellä luoda käyttäjän , kirjautua sisään, kirjautua ulos. Tulosten lisääminen melkein toimii.