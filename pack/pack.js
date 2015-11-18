var createTamp = require('tamp');
var jQuery = require('jquery');
var _ = require('lodash');
var fs = require('fs');

function packIt(incidents){
	console.log("Packing...")

	incidents.forEach(function(incident, index){
		incident.id = index;
	});

	var possibilities = {
		bin: incidents.map(function(a){
			return a.bin;
		}).filter(function(a, index, list){
			return a && !~list.indexOf(a, index + 1);
		}).sort(),
		category: incidents.map(function(a){
			return a.category;
		}).filter(function(a, index, list){
			return !~list.indexOf(a, index + 1);
		}).sort(),
		month_year: incidents.map(function(a){
			return a.month_year;
		}).filter(function(a, index, list){
			return !~list.indexOf(a, index + 1);
		}).sort(),
		day: incidents.map(function(a){
			return a.day;
		}).filter(function(a, index, list){
			return !~list.indexOf(a, index + 1);
		}).sort(),
		hour: incidents.map(function(a){
			return a.hour;
		}).filter(function(a, index, list){
			return !~list.indexOf(a, index + 1);
		}).sort()
	}

	var tamp = createTamp();

	tamp.addAttribute({
		attrName: 'bin',
		possibilities: possibilities.bin,
		maxChoices: 1
	});

	tamp.addAttribute({
		attrName: 'category',
		possibilities: possibilities.category,
		maxChoices: 1
	});

	tamp.addAttribute({
		attrName: 'month_year',
		possibilities: possibilities.month_year,
		maxChoices: 1
	});

	tamp.addAttribute({
		attrName: 'day',
		possibilities: possibilities.day,
		maxChoices: 1
	});

	tamp.addAttribute({
		attrName: 'hour',
		possibilities: possibilities.hour,
		maxChoices: 1
	});

	tamp.pack(incidents.map(function(a){
		return {
			id: a.id,
			bin: a.bin,
			category: a.category,
			month_year: a.month_year,
			day: a.day,
			hour: a.hour
		}
	}));

	fs.writeFile("./ucpd/static/json/packed.json", tamp.toJSON())
	console.log("Successfully packed.")
}

var data = require('./incidents.json');

packIt(data.incidents);