/**
 * @author Kate
 */
var foodCount = 0;
var Food = Vector.extend({
	init : function() {

		this._super();
		this.id = ++foodCount;
		this.mass = Math.random() * 60 + 4;
		this.radius = Math.pow(this.mass, .5) + 1;
		this.drawn = 0;
	},

	collide : function(boid) {
		boid.food++;
		this.destroyed = true;
	},

	draw : function(g) {
		g.fill(.4, 1, .7, .3);
		if (!this.destroyed)
			g.fill(.4, 1, .7);
		this.drawCircle(g, this.radius);
	},
	drawSpot : function(g) {
		this.drawn++;
		if (!this.destroyed && (this.drawn < 6 || time.frameCount % 30 === this.id % 30)) {
			g.fill(.45, 1, .7, .5);

			this.drawCircle(g, this.radius * 10 * this.drawn % 10 + 30);
		}
	}
});

var environment = {
	scale : .084,
	items : [],
	init : function() {
		for (var i = 0; i < 1200; i++) {
			this.spawnFood(-1000 + .01*i);
		}
	},

	getFoodAt : function(p) {
		if (!this.image)
			return 0;

		var x = p.x * this.scale + this.image.width / 2;
		var y = p.y * this.scale + this.image.height / 2;
		///	console.log(x + " " + y);
		var c = this.image.get(x, y);

		var g = (c >> 8) & 0xFF;

		//console.log(c + " " + g);
		if (c !== 0)
			return g / 255;
		return (0);

	},

	draw : function(g) {
		if (!this.image) {
			this.image = g.createGraphics(50, 50, g.P2D);

			this.image.background(0);
			this.image.colorMode(g.HSB, 1);
		}
		this.image.beginDraw();

		if (time.frameCount % 10 === 0) {
			this.image.fill(0, 0, 0, .1);
			this.image.rect(0, 0, this.image.width, this.image.height);
		}

		this.image.pushMatrix();
		this.image.translate(this.image.width / 2, this.image.height / 2);
		this.image.scale(this.scale);

		for (var i = 0; i < this.items.length; i++) {
			this.items[i].drawSpot(this.image);
		}

		this.image.popMatrix();
		this.image.endDraw();
		g.image(this.image, -300, -300, 600, 600);

		for (var i = 0; i < this.items.length; i++) {
			this.items[i].draw(g);
		}

		g.fill(1, 0, 1);
		app.mouse.drawCircle(g, this.getFoodAt(app.mouse) * 10 + 10);
	},

	spawnFood : function(t) {
		for (var i = 0; i < 1; i++) {
			if (Math.random() > .9 && this.items.length < 100) {
				var f = new Food();
				f.setToPolar(200 * utilities.noise(t * .15) + 100 + 30*Math.random(), 20 * utilities.noise(t * .03 + 100));
				this.items.push(f);
			}
		}
	},

	update : function(time) {
		this.spawnFood(time.current);

		this.items = this.items.filter(function(item) {
			return !item.destroyed;
		});
	}
};
