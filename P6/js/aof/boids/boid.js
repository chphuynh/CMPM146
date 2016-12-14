/**
 * @author Kate
 * Your behavior goes here
 */

var Boid = Particle.extend({
	init : function(flock) {

		// Be sure to keep this line, it sets up the Boid as a particle!
		this._super();
		this.food = 0;
		this.flock = flock;
		this.rotation = Math.random() * Math.PI * 2;
		this.forces = [];
		this.forces = [new Vector(), new Vector(), new Vector(), new Vector(), new Vector(), new Vector(), new Vector(), new Vector()];
		this.rebuild();
	},

	rebuild : function() {
		this.wingLength = this.flock.wingLength;
		this.length = this.flock.length;
		this.wingWidth = this.flock.wingWidth;
		this.drag = this.flock.drag;
		this.wingPower = this.flock.wingPower;
		this.separation = this.flock.separation;
	},

	compileNeighbors : function() {
		// Compute a shorter list of the neighbors, minus self?

		// Punt for now, just return the whole flock

		return this.flock.members;
	},

	/*
	 * This function sets all of the forces on
	 *   the boids before updating them
	 * 	 You can have up to 8 forces
	 */
	preUpdate : function(t, neighbors) {

		this.flapCycle = (.1 * t.current * (this.wingPower + 20) + this.id * .27) % 1;

		this.neighbors = this.compileNeighbors();

		// set all the forces from the flock

		// Separation
		// Go through the flock and move away from anyone who is too close
		this.forces[0].mult(0);
		var spacing = 65;
		var offset = new Vector();
		for (var i = 0; i < this.neighbors.length; i++) {

			offset.setToDifference(this.neighbors[i], this);
			//console.log(offset);
			var d = offset.magnitude();
			if (d === 0) {
				offset.setToPolar(2, 20 * Math.random());
				d = 2;
			}
			if (d < spacing) {

				offset.mult(Math.pow(spacing - d, 1.8) / d);
				this.forces[0].add(offset);
			}

		}
		this.forces[0].mult(-.5 * this.flock.dna.values[13]);

		// Alignment
		// Add up all the velocities of my neighbors.
		// Set them to the same magnitude as my velocity
		// Calculate the difference
		var avgDir = new Vector();
		for (var i = 0; i < this.neighbors.length; i++) {
			//	console.log(this.neighbors[i]);
			avgDir.add(this.neighbors[i].v);
		}

		avgDir.normalize();
		avgDir.mult(this.v.magnitude());
		this.forces[1].mult(0);
		this.forces[1].setToDifference(avgDir, this.v);
		this.forces[1].mult(9 * Math.pow(this.flock.dna.values[14], 1.4));
		// A little slowdown (keeps this force from making them move too fast)
		this.forces[1].addMultiple(this.v, -.4);

		// Cohesion
		// Calculate the center of the flock
		this.forces[2].mult(0);
		this.forces[2].setToDifference(this, this.flock.center);
		this.forces[2].mult(-(10 * (this.flock.dna.values[15] + 4)));

		// Propulsion force
		// A force to keep them moving forward (in whatever direction forward is)
		this.forces[3].setToPolar(4 * Math.pow(this.wingPower, 1.25), this.rotation);

		// Containment force, keeps the birds on screen
		this.forces[4].mult(0);
		var range = 280;
		var d = this.magnitude();
		if (d > range) {
			var f = d - range;
			this.forces[4].setToMultiple(this, -1.2 * Math.pow(f, 1.5) / d);
		}

		/*
		* TODO
		*  Custom forces (5-7)
		* Consider using this.flock.dna.values[16 - 19] to control new forces
		*/

		// EXAMPLE_WANDER: For example, this is a force that tells them to wander around
		this.forces[5].mult(1000 * this.flock.dna.values[16]);
		this.forces[5].setToPolar(160, 10 * utilities.noise(this.id, t.current * .8));

		// EXAMPLE_FOOD: This example force searches for food directly ahead, and,
		// if found, exerts a lunging force forward
		// Can you think of a better method?

		this.forces[6].setTo(this.v);
		this.forces[6].normalize();
		var sampleSpot = new Vector();
		var total = 0;
		for (var i = 0; i < Math.floor(this.flock.dna.values[17]*40); i++) {
			sampleSpot.setToAddMultiple(this, 1, this.v, i * .012 + .005);
			var amt = environment.getFoodAt(sampleSpot);
			total += amt;
		}
		this.forces[6].mult(200 * total);

		// EXAMPLE_MOUSE: Try making the boids CHASE or RUN FROM your mouse movement
		// Try controlling fearfulness/curiosity about 
		// the mouse with one of the unused DNA genes
		
		this.forces[7].setToDifference(this, app.mouse);
		// Reverse the behavior:
		this.forces[7].mult(2*this.flock.dna.values[18]);
		
		
		// Leave this line in!
		this._super(t);
		this.rotation = this.v.getAngle();

	},

	postUpdate : function() {
		for (var i = 0; i < environment.items.length; i++) {
			var d = this.getDistanceTo(environment.items[i]);
			if (d < 5)
				environment.items[i].collide(this);
		}
	},

	draw : function(g) {

		g.pushMatrix();
		g.translate(this.x, this.y);
		g.rotate(this.rotation);
		g.noStroke();

		this.drawBody(g);

		g.popMatrix();
	},

	drawThumbnail : function(g) {
		var temp = this.flapCycle;
		this.flapCycle = 0;
		g.pushMatrix();
		g.scale(2.2);
		g.rotate(this.id * 100 + 10);
		g.translate(10, 0);
		this.drawBody(g);
		g.popMatrix();
		this.flapCycle = temp;
	},

	drawBody : function(g) {

		/*
		 * TODO:
		 * There are several *unused* DNA elements,
		 * can you use them to make more interesting birds?
		 * The unused DNA is stored in "this.flock.dna.values[N]"
		 * where N is 6, 7, 8, 9
		 */
		var wx = (1 + .5 * Math.sin(-this.flapCycle * Math.PI * 2)) * this.wingWidth;
		var wy = (1 + .2 * Math.cos(-this.flapCycle * Math.PI * 2)) * this.wingLength;

		// Draw the body
		g.noStroke();
		g.fill(this.flock.hue0, 1, .9);
		g.beginShape(g.TRIANGLE_FAN);
		g.vertex(this.length * .4, 0);
		g.vertex(-wy, wx);
		g.vertex(-this.length * .6, 0);
		g.vertex(-wy, -wx);
		g.endShape();
		
		g.beginShape(g.TRIANGLE_FAN);
		g.vertex(this.flock.tail * 10 - 5, 0);
		g.vertex(-wy * 2 - 20, wx);
		g.vertex(-this.flock.tail * 10 - 5, 0);
		g.vertex(-wy * 2 - 20, -wx);
		g.endShape();
		
		g.fill(this.flock.hue1, 1.5 - 1.5 * this.flock.centerPastel, .25 + 1.5 * this.flock.centerPastel);
		g.beginShape(g.TRIANGLE_FAN);
		g.vertex(this.length * .4, 0);
		g.vertex(-wy * .6, wx * .4);
		g.vertex(-this.length * .6, 0);
		g.vertex(-wy * .6, -wx * .4);
		g.endShape();
		
		g.fill(this.flock.eyeHue,  1.5 - 1.5 * this.flock.centerPastel, .25 + 1.5 * this.flock.centerPastel);
		g.stroke(this.flock.eyeStroke,  1.5 - 1.5 * this.flock.centerPastel, .25 + 1.5 * this.flock.centerPastel);
		g.ellipse(0, 3, this.flock.eyeSize * 3, this.flock.eyeSize * 3);
		g.ellipse(0, -3, this.flock.eyeSize * 3, this.flock.eyeSize * 3);
		g.noStroke();
		
	},
});
