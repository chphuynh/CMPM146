/**
 * @author Kate
 */

var particleCount = 0;

var Particle = Vector.extend({
	init : function() {
		this.handForce = 0;
		this.drag = .01;
		this.id = particleCount;
		particleCount++;
		this._super(0, 0, 0);
		this.v = new Vector();
		this.v.setToSpherical(12, Math.random() * 100, 0);
		this.totalForce = new Vector();
		this.forces = [];
	},

	drawForces : function(g, mult) {

		for (var i = 0; i < this.forces.length; i++) {
			g.stroke(i * .2 + .2, 1, .7);
			this.drawArrow(g, this.forces[i], mult);
		}
		g.stroke(0, 1, .7);
		this.drawArrow(g, this.totalForce, mult);
	}
});

Particle.prototype.preUpdate = function(t) {

	this.totalForce.mult(0);

for (var i = 0; i < this.forces.length; i++) {
	this.totalForce.add(this.forces[i]);
}
};

Particle.prototype.update = function(t) {
	this.v.mult(1 - this.drag);
	this.v.addMultiple(this.totalForce, t.elapsed);

	this.addMultiple(this.v, t.elapsed);
};

Particle.prototype.postUpdate = function(t) {

	// Has a three.js mesh?  update its position
	if (this.mesh) {
		this.mesh.position.setTo(this);
		this.mesh.lookAt(Vector.addMultiples(this, 1, this.v, 10));
	}
};
