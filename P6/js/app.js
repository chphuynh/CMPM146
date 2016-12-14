/**
 * @author Kate
 */

var app = {
	popCount : 6,
	dnaSize : 20,
	simView : true,
	boidsPerFlock : 10,
	winnerSlots : 5,

	mutationAmt : .05,
	mutationChance : 1,
	mouse : new Vector(0, 0)
};

var selected;

$(document).ready(function() {
	// Start the time object
	time.start();
	environment.init();
	// Create the animated arena view

	var selectedDrawn = false;

	// Go through all boids checking to see if any
	createProcessing($("#selected-window"), function(t) {
	}, function(g) {
		var thumbnailCheckIndex = -1;
		var flocks = app.population.individuals;
		for (var i = 0; i < flocks.length; i++) {
			if (!flocks[i].thumbnailURL) {
				thumbnailCheckIndex = i;
			}
		}

		if (thumbnailCheckIndex >= 0 && selected !== flocks[thumbnailCheckIndex]) {
			selected = flocks[thumbnailCheckIndex];
			//console.log("selected " + thumbnailCheckIndex + " for thumbnail production");
			selectedDrawn = false;
		}

		if (selected)
			selected.drawThumbnail(g);

		if (selected && !selected.thumbnailURL && selectedDrawn) {
			//console.log("render thumbnail");
			var canvas = $("#selected-window canvas").get(0);
			selected.setThumbnail(canvas.toDataURL());

		}

		selectedDrawn = true;

	});

	// Create the animated arena view
	createProcessing($("#view-holder"), function(time) {
		// Update function
		var members = app.population.individuals;
		// Update
		time.update();
		environment.update(time);
		for (var i = 0; i < members.length; i++) {
			members[i].update(time);
		}

	}, function(g) {
		// Draw funciton
		var members = app.population.individuals;
		// Draw
		g.fill(.5, .03, .8);
		g.ellipse(0, 0, 260, 260);
		environment.draw(g);
		for (var i = 0; i < members.length; i++) {
			members[i].draw(g);
		}

	});

	// Create a population.
	// Pass in:
	//    the number of individuals, a function to create DNA,
	//    and a method to create the indiviudals from DNA
	app.population = new Population(app.popCount, function() {
		return new AOF(app.dnaSize);
	}, function(dna) {
		return new IndividualFlock(dna);
	});

	$("#view-holder").mousemove(function(e) {
		//console.log(e.offsetX, e.offsetY);
		//	console.log(e);
		app.mouse.setTo(e.offsetX - $(this).width() / 2, e.offsetY - $(this).height() / 2);
	});

	$("#evo-panel").draggable();
	$("#dna-panel").draggable();

	app.population.reroll();

	app.evoPanel = new EvoPanel();
	app.dnaPanel = new DNAPanel();

});

function updatePopulationUI() {
	selected = undefined;
	console.log("Update pop ui");

	// Updated population
	if (app.dnaPanel)
		app.dnaPanel.setPopulation(app.population);
}

/*
 * Time object: controls time, like framecount/rate and total time
 */

var time = {
	frameCount : 0,
	current : 0,
	elapsed : .01,
	frameCount : 0,
	startTime : 0,
	start : function() {
		this.startTime = Date.now() * .001;
		this.current = Date.now() * .001 - this.startTime;
	},
	update : function() {

		this.frameCount++;
		var last = this.current;
		this.current = Date.now() * .001 - this.startTime;
		this.elapsed = this.current - last;
		if (this.frameCount % 100 === 0) {
			//console.log(this.current.toFixed(2) + ": " + this.elapsed);
		}
	}
};
