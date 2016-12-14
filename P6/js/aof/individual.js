/**
 * @author Kate Compton
 * Individuals
 * Each individual has its own DNA
 * Note that an "individual" can be a critter,
 *   an artwork, or even a flock!
 */

var individualCount = 0;
var Individual = Class.extend({
	init : function(dna) {
		if (!dna)
		throw("No DNA provided");
		var individual = this;
		this.id = ++individualCount;
		this.dna = dna;
		this.dna.onChange = function(index, value) {
			individual.onChange();
			if (index)
				console.log(dnaLabels[index] + " changed: " + value.toFixed(2));
			individual.dna.refreshHTML();

		};

		this.name = "Generic Individual " + this.id;

		this.postInit();

	},

	postInit : function() {
		// Shorthand, because we have to reference dna values *a lot* when drawing
		var dna = this.dna.values;

		this.color = new KColor(dna[0], dna[1], dna[2] * .5 + .5);
		this.secondaryColor = new KColor((dna[0] + dna[3] * .3 + .9) % 1, 1, 1);
		this.radius = dna[4] * 30 + 10;
		this.outerRadius = dna[5] * 30;
		this.p = new Vector(0, 0);
		this.p.setToPolar(Math.random() * 100, Math.random() * Math.PI * 2);
	},

	select : function() {
		this.isSelected = true;
	},
	deselect : function() {
		this.isSelected = false;
	},

	/*
	 * Sim mode
	 */
	draw : function(g) {

		g.noStroke();
		this.secondaryColor.fill(g);
		var w = this.radius + this.outerRadius;
		this.p.drawCircle(g, w);
		this.color.fill(g);

		this.p.drawCircle(g, this.radius);

	},

	/*
	* Thumbnail mode
	*/
	// Draw with Processing.js drawing commands
	drawThumbnail : function(g) {

		g.noStroke();
		this.secondaryColor.fill(g);
		var w = this.radius + this.outerRadius;

		g.ellipse(0, 0, w, w);
		this.color.fill(g);
		g.ellipse(0, 0, this.radius, this.radius);

	},
	updateThumbnail : function(t) {
		this.update(t);
	}
});

