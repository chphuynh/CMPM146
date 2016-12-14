/**
 * @author Kate
 * A panel to display all the dna of the individuals
 */

function DNAPanel() {
	// Create slots for all the population

	this.setPopulation();

};

DNAPanel.prototype.setPopulation = function() {
	var div = $("#population");
	div.html("");
	var tiles = [];
	$.each(app.population.individuals, function(index, ind) {
		var tile = $("<div/>", {
			class : "pop-tile"
		}).appendTo(div).click(function() {
			select(ind);
		}).dblclick(function() {
			app.evoPanel.addToWinners(ind, index);
		});

		var thumbDiv = $("<div/>", {
			class : "pop-tile-thumb"
		}).appendTo(tile);

		var scoreDiv = $("<div/>", {
			class : "pop-tile-score"
		}).appendTo(tile);

		var dnaDiv = $("<div/>", {
			class : "pop-tile-dna"
		}).appendTo(tile);

		ind.dna.toHTML(dnaDiv);
		ind.slot = tile;
	});
};

function select(ind) {
	if (selected) {
		selected.deselect();
	}
	selected = ind;
	if (selected) {
		selected.select();
	}
	$(".pop-tile").removeClass("selected");
	if (selected && selected.slot)
		selected.slot.addClass("selected");
}
