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

Kloonaa repositorio
```
$ git clone git@github.com:meri573/score-tracker.git
```
Luo virtuaaliympäristö ja aktivoi se
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Asenna `flask`
```
$ pip install flask
```
Luo tietokanta ja lisää luokat siihen `init.sql` tiedostosta
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:
```
$ flask run
```

Sovelluksessa voi tällä hetkellä 
* luoda käyttäjän 
* kirjautua sisään 
* kirjautua ulos 
* lisätä tuloksen
* katsella tuloksia
* editoida omia tuloksia 
* poistaa omia tuloksia
* etsiä tuloksia
* vierailla käyttäjäsivulla
* lisätä kommentteja tulokselle

* loukittelujen oikein tekeminen on vielä työn alla, joten projekti ei välttämättä toimi oiken tällä hetkellä
* editoida kommentteja
* poistaa kommentteja
