# ucpd-crime

UC Berkeley crime analysis (a universe away from [the original](http://berkeleycrime.org))

This repository contains tools for parsing and visualizing daily report logs from 2010 to 2015.

# Workflow

To get started from scratch, run `python manage.py load

* `load_bins`, to import hexagonal bins from a shapefile (which I generated in QGIS)
* `load_ucpd`, to load historical UCPD crime data
* `classify`, to collapse incident information into a custom severity index
* `assign_bin`, to locate each incident within a hexagonal bin
* `pack`, to serialize incident-level information using Tamper