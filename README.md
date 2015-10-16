# berkeley-crime

Berkeley crime analysis (a universe away from [the original](http://berkeleycrime.org))

The general idea is to analyze incident-level data from the Berkeley Police Department, accessed through the Socrata API and Berkeley's [Open Data Portal](https://data.cityofberkeley.info). This repository contains tools for fetching, parsing, and performing some basic geospatial analysis on that data, including hexagonal binning.

# Workflow

The heart of this repository are the custom management commands. To get started from scratch, here are the commands you'd need to run:

* `load_bins`, to import hexagonal bins from a shapefile (which I generated in QGIS)
* `load_ucpd`, to load historical UCPD crime data
* `classify`, to collapse incident information into a custom severity index
* `assign_bin`, to locate each incident within a hexagonal bin
* `pack`, to serialize incident-level information using Tamper