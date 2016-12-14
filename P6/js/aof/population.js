/**
 * @author Kate Compton
 * A population of individuals
 * Can be refreshed and refilled by various breeding mechanisms
 */

function Population(count, createDNA, dnaToIndividual) {
	this.individuals = [];
	// Create a fresh population with totally random DNA
	this.count = count;
	this.createDNA = createDNA;
	this.dnaToIndividual = dnaToIndividual;
};

Population.prototype.reroll = function() {
	for (var i = 0; i < this.count; i++) {
		this.individuals[i] = this.dnaToIndividual(this.createDNA());
	}

	updatePopulationUI();
};

