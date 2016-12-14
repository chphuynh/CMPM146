/**
 * @author Kate Compton
 * Manages creating processing windows and time
 */

// control the processing view
function createProcessing(holder, onUpdate, onDraw) {
	var canvas = $("<canvas/>").appendTo(holder).css({
		width : "100%",
		height : "100%"
	});

	var processingInstance = new Processing(canvas.get(0), function(g) {

		// Set the size of processing so that it matches that size of the canvas element
		var w = canvas.width();
		var h = canvas.height();

		g.size(w, h);
		g.colorMode(g.HSB, 1);
		g.ellipseMode(g.CENTER_RADIUS);

		g.draw = function() {

			var preventDraw = onUpdate(time);

			if (!preventDraw) {
				g.background(.55, .1, 1);
				g.pushMatrix();
				g.translate(w / 2, h / 2);

				onDraw(g);
				g.popMatrix();
			}
		};
	});

}
