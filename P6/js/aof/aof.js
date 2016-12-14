/**
 * @author Kate
 */
function randomSign() {
	return Math.random() < 0.5 ? -1 : 1;
}

function setDivToValue(div, value) {

	var color = new KColor((.3 + .7 * Math.pow(value, 1.7)) % 1, 1, 1);

	div.fill.css({
		backgroundColor : color.toCSS(),
		width : Math.round(value * 100) + "%"
	});
};

function randomValue() {
	// Lightly push the value to .5 (regress to the mean?)
	var v = Math.pow(Math.random(), 1.5);
	v = randomSign() * .5 * v + .5;
	return v;

	// Or just return a random value
	//return Math.random();
}

// Create an array of floats the size
function AOF(size) {
	this.values = [];
	for (var i = 0; i < size; i++) {
		this.values[i] = randomValue();

	}
}

/*
 * Mutations and crossover
 * An AOF is a "thing you can modify"
 */
AOF.prototype.clone = function() {
	var clone = new AOF(this.values.length);
	for (var i = 0; i < this.values.length; i++) {
		clone.values[i] = this.values[i];
	}
	return clone;
};

// Create a variant, amt is the amount to vary,
// chance is the chance that any given value will change
AOF.prototype.createMutant = function(amt, chance) {
	var child = this.clone();
	child.mutate(amt, chance);
	return child;
};

AOF.prototype.mutate = function(amt, chance) {
	console.log("mutate " + this + " amt: " + amt + " chance:" + chance);
	for (var i = 0; i < this.values.length; i++) {
		if (Math.random() < chance) {
			// Distance to move (max of amt, but more likely to move less)
			var d = Math.pow(Math.random(), 2) * amt * randomSign();
			this.values[i] += d;
			this.values[i] = Math.max(0, Math.min(1, this.values[i]));

		}
	}
	if (this.onChange)
		this.onChange();
};

AOF.prototype.refreshHTML = function() {
	for (var i = 0; i < this.divValues.length; i++) {
		setDivToValue(this.divValues[i], this.values[i]);
	}
};

AOF.prototype.toHTML = function(holder) {

	// Remove pre-existing html (unlikely!)
	if (this.div)
		this.div.remove();
	this.divValues = [];

	var aof = this;

	var valueHolder = $("<div/>", {
		class : "aof-value-holder"
	}).appendTo(holder);

	$.each(this.values, function(index, value) {

		var dragStart = 0;

		var bg = $("<div/>", {
			class : "aof-value-bg"
		}).appendTo(valueHolder).css({
			height : Math.floor(100 / aof.values.length) + "%"
		}).draggable({
			cursorAt : {
				left : 0,
				top : 0
			},

			helper : function() {
				return "<div></div>";
			},
			start : function() {
				dragStart = event.clientX;
			},
			drag : function(ev, ui) {

				var value = Math.min(1, Math.max(0, ui.position.left / bg.width()));
				aof.values[index] = value;
				setDivToValue(bg, value);

				if (aof.onChange)
					aof.onChange(index, value);
			}
		});

		bg.fill = $("<div/>", {
			class : "aof-value-fill",
			width : Math.random() * 100 + "%"
		}).appendTo(bg);

		bg.label = $("<div/>", {
			class : "aof-value-label",
			html : dnaLabels[index]
		}).appendTo(bg);
		aof.divValues[index] = bg;

	});

	this.refreshHTML();
};
