# Messenger

Tämä on yksinkertainen keskustelu ohjelma. Messengerilla on seuravat ominaisuudet.

Käyttäjä voi registroida. Luo oma tili ja salasana joka on suojattu ja säilytetty.

Käyttäjä voi kirjautu sisään omilla tunnuksilla.

Käyttäjä voi muoka oma profili ja lisää profili kuva.

Käyttäjä voi ettiä muita käyttäji nimen perustella.

Käyttäjä voi lisää muitä käyttäji oman kontakti listan.

Käyttäjä voi lähetää ja vastanotta viestiä muilta käyttäjiltä. Muilla käytäjillä ei ole mahdolisuuksia päästä käsiks toisen käyttäjän viestiin.

Käyttäjä voi selaa koko viesti historia haluttaessa.

Tän hetkinen tilanne:

Sovellus on valmis. Kaikki tavoiteet saavuttettu ja koodi refaktoroitu pylintin mukaan.


# Käynnistysohjeet

Kloonaa repositorio koneellesi ja siirry sen juurihakemistoon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavasti:
```bash
DATABASE_URL=<"tietokannan-paikallinen-osoite">
SECRET_KEY=<"sainen-avain">
```

Aktivoi virtuaaliympäristö ja asenna riippuvuudet:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Sovellus käyttää PostgreSQL-tietokantaa. Tietokannan skeema määritetään komennolla:
```bash
psql < schema.sql
start-pg.sh
```

Sovellus käynnistetään komennolla
```bash
cd src/
flask run
```


