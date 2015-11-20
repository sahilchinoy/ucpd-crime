ucpd-crime
========================

A Daily Californian analysis of crime in the UC Berkeley area.

This repository contains tools for parsing and visualizing UCPD daily report logs from 2010 to 2015. Much of the code and methodology can be adapted to fit other data sources.

Getting started
-------------

Clone the repo and install the requirements.

```
pip install -r requirements.txt
npm install
```

Set the following environment variables:

* `DB_NAME`: name of a PostGIS database
* `DB_USER`: username with access to said database

If you'd like to deploy to S3 using [django-bakery](https://github.com/datadesk/django-bakery), set these as well:

* `AWS_BUCKET_NAME`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

To get started from scratch, run `python manage.py load`, which will call:

* [`load_bins`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/load_bins.py), to import hexagonal bins from a shapefile in [`data`](https://github.com/sahilchinoy/ucpd-crime/tree/master/data/bins)
* [`load_ucpd`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/load_ucpd.py), to load historical UCPD crime data
* [`classify`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/classify.py), to collapse incident information into [one of three categories](https://github.com/sahilchinoy/ucpd-crime/blob/master/data/classification.csv): violent, property or quality-of-life
* [`locate`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/locate.py), to merge location information with the [address database](https://github.com/sahilchinoy/ucpd-crime/blob/master/data/addresses.csv) to assign each incident a latitude and longitude
* [`assign_bin`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/assign_bin.py), to locate each incident within a bin
* [`compute_stats`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/compute_stats.py), to compute some basic statistics about crime across bins, across categories and over time
* [`pack`](https://github.com/sahilchinoy/ucpd-crime/blob/master/ucpd/management/commands/pack.py), to serialize incident-level information using [Tamper](http://nytimes.github.io/tamper/)

Data
-------------

### Raw data

Incident-level reports come from a PRA filed with the UC Police Department. They cover January 2010 to September 2015. These raw data files are stored in [`data/ucpd`](https://github.com/sahilchinoy/ucpd-crime/tree/master/data/ucpd).

### Bins

Hexagonal bins were generate in QGIS. The shapefile is stored in [`data/bins`](https://github.com/sahilchinoy/ucpd-crime/tree/master/data/bins).

### Classification

[Simple spreadsheet](https://github.com/sahilchinoy/ucpd-crime/blob/master/data/classification.csv) that maps the codes in the raw data to category codes: `V` for violent crimes, `P` for property crimes and `Q` for quality-of-life crimes. `N` is reserved for crimes that we aren't interested in analyzing or displaying.

### Address database

[A spreadsheet](https://github.com/sahilchinoy/ucpd-crime/blob/master/data/addresses.csv) that maps the addresses in the raw data to geocoded points, which were manually corrected and checked. The address database lives in a Google spreadsheet [here](https://docs.google.com/spreadsheets/d/1z_n68MUS2c2QJFnzV4ol90Knx-KN9PfSMUKe9KAn4ZE/edit?usp=sharing).

Why bins?
-------------

[Tamper](http://nytimes.github.io/tamper/) is a New York Times library for efficient serialization of data. We use Tamper as opposed to sending raw JSON  in order to experiment with sending *all* incidents to the user's browser, then using [Pourover](https://github.com/NYTimes/pourover) to quickly sort and filter that data on the client-side.

This means we can't send coordinates for each individual incident. Instead, we assign incidents to a bin and then send only the incident's bin ID. With small enough bins, this gives a fairly detailed look at the spatial distribution of crime, and keeps the data file being sent remarkably light (41KB, in this case).

While it's more of an experiment than something of great use for data of this scale (~10 thousand incidents), it's an interesting model for scaling up to hundreds of thousands of incidents — something we've tried with historical data from the city police department.

Building and deploying
-------------

Build this site out as flat files by running `python manage.py build`.

If you've set the appropriate environment variables, publish to S3 using `python manage.py publish`.

Thanks [django-bakery](https://github.com/datadesk/django-bakery)!

Where is this going?
-------------

We want to try scaling up this binning methodology to bigger datasets. That would involve creating a new shapefile and coming up with new address and classification dictionaries, but the rest of the loading, binning and serialization code should work.

We tried a few Pourover filters other than our basic classification (violent, property, quality-of-life), but none of them ended up being interesting for this particular dataset. For categorical variables, though, this project can accomplish some very fast visualizations of geospatial data — without running a server.
