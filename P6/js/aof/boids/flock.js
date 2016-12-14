/**
 * @author Kate
 */
var dnaLabels = ["wingLength", "length", "wingWidth", "hue0", "hue2", "pastel", "eyeStroke", "eyeSize", "eyeHue", "tail", "drag", "power", "flapRate", "separation", "alignment", "cohesion", "noise", "foodRange", "mouseAvoidance", "behavior3"];

var IndividualFlock = Individual.extend({
	// these individuals are actually each individual *flocks*
	postInit : function() {
		this.count = app.boidsPerFlock;
		this.members = [];

		this.center = new Vector();
		this.rebuildFlock();
		for (var i = 0; i < this.count; i++) {
			var b = new Boid(this);
			b.setToPolar(Math.random() * 30, Math.random() * 100);
			this.members[i] = b;
		}
	},

	rebuildFlock : function() {

		this.wingLength = this.dna.values[0] * 17 + 4;
		this.length = this.dna.values[1] * 10 + 10;
		this.wingWidth = this.dna.values[2] * 5 + 15;
		this.drag = .04 * Math.pow(this.dna.values[10], 5) + .01;
		this.wingPower = 10 + Math.pow(this.dna.values[11], 2) * 15;

		this.hue0 = this.dna.values[3];
		this.hue1 = this.dna.values[4];
		this.centerPastel = this.dna.values[5];
		
		this.eyeStroke = this.dna.values[6];
		this.eyeSize = this.dna.values[7];
		this.eyeHue = this.dna.values[8];
		this.tail = this.dna.values[9];
		this.separation = this.dna.values[14];

		for (var i = 0; i < this.members.length; i++) {
			this.members[i].rebuild();
		}
	},

	onChange : function() {
		this.thumbnailURL = undefined;
		this.rebuildFlock();
	},

	setThumbnail : function(url) {
		if (this.slot) {
			this.thumbnailURL = url;
			var pic = "<div class='drag-pic'>" + "<img src='" + this.thumbnailURL + "'/>" + "</div>";
			//		this.slot.find(".pop-tile-thumb").append(pic);
			this.slot.find(".pop-tile-thumb").css({
				backgroundImage : "url(" + this.thumbnailURL + ")",
				backgroundSize : "100%"
			});
		}

	},

	update : function(t) {
		// Calculate the forces on the flock
		this.center.mult(0);
		for (var i = 0; i < this.members.length; i++) {
			this.center.add(this.members[i]);
		}
		this.center.div(this.members.length);

		// Set forces
		for (var i = 0; i < this.members.length; i++) {
			this.members[i].preUpdate(t, this);
		}
		for (var i = 0; i < this.members.length; i++) {
			this.members[i].update(t);
		}
		this.food = 0;
		for (var i = 0; i < this.members.length; i++) {
			this.members[i].postUpdate(t);
			this.food += this.members[i].food;
		}
		
		if (this.slot) {
			this.slot.find(".pop-tile-score").html(this.food);
		}
		
	},

	drawThumbnail : function(g) {
		g.pushMatrix();
		//g.translate(-this.center.x, -this.center.y);
		this.members[0].drawThumbnail(g);
		g.popMatrix();
	},

	draw : function(g) {
		if (this.isSelected) {
			g.fill(this.hue1, .3, 1, 1);
			this.center.drawCircle(g, 35);
		} else {
			g.fill(this.hue1, .3, 1, .5);
			this.center.drawCircle(g, 5);
		}

		for (var i = 0; i < this.members.length; i++) {
			if (app.showForces && this.isSelected)
				this.members[i].drawForces(g, .02);
			this.members[i].draw(g);

		}

	}
});
