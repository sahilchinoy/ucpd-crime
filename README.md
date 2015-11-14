ucpd-crime
========================

Analysis of crime in the UC Berkeley area. This repository contains tools for parsing and visualizing daily report logs from 2010 to 2015.

Getting started
-------------

Clone the repo and install the requirements.

```
pip install -r requirements.txt
```

Set the following environment variables:

* `DB_NAME`: name of a PostGIS database
* `DB_USER`: username with access to said database

If you'd like to deploy to S3 using [django-bakery](https://github.com/datadesk/django-bakery), set these as well:

* `AWS_BUCKET_NAME`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

To get started from scratch, run `python manage.py load`, which will call:

* `load_bins`, to import hexagonal bins from a shapefile in `data`
* `load_ucpd`, to load historical UCPD crime data
* `classify`, to collapse incident information into one of three categories: violent, property or quality-of-life
* `locate`, to merge address information with the address database to assign each incident a latitude and longitude
* `assign_bin`, to locate each incident within a bin
* `compute_stats`, to compute some basic statistics about crime across bins, across categories and over time
* `pack`, to serialize incident-level information using [Tamper](http://nytimes.github.io/tamper/)

Data
-------------

### Raw data

Incident-level comes from a PRA filed with the UC Police Department. It encompasses January 2010 to September 2015, one CSV for each year. These raw data files are stored in `data/ucpd`.

### Bins

Hexagonal bins were generate in QGIS. The shapefile is stored in `data/bins`.

### Classification

Simple spreadsheet that maps the codes in the raw data to category codes: `V` for violent crimes, `P` for property crimes and `Q` for quality-of-life crimes. `N` is reserved for crimes that we aren't interested in analyzing or displaying.

### Address database

A spreadsheet that maps the addresses in the raw data to geocoded points, which were manually corrected and checked. The address database lives in a Google spreadsheet [here](https://docs.google.com/spreadsheets/d/1z_n68MUS2c2QJFnzV4ol90Knx-KN9PfSMUKe9KAn4ZE/edit?usp=sharing).

Serializing
-------------

[Tamper](http://nytimes.github.io/tamper/) is a magical New York Times library for efficient serialization of data. We use Tamper as opposed to sending JSON compressed in a more standard way in order to experiment with sending *all* incidents to the user's browser, then using [Pourover](https://github.com/NYTimes/pourover) to quickly sort and filter that data on the client-side.

This means we can't send coordinates for each individual incident. Instead, we assign incidents to a bin and then send only the incident's bin ID. With small enough bins, this gives a fairly detailed look at the spatial distribution of crime, and keeps the data file being sent remarkably light. While it's more of an experiment than something of great use for this scale of data (~10 thousand incidents), it's an interesting model for scaling up to hundreds of thousands of incidents -- something we plan to try with historical data from the city police department.

Building and deploying
-------------

A wise man once said, "Running servers is for suckers."" Build this site out as flat files by running `python manage.py build`, and publish to S3 using `python manage.py publish`.

Thanks [django-bakery](https://github.com/datadesk/django-bakery)!
