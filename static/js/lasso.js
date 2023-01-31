// Lasso functions
var lasso_start = function() {
    lasso.items()
        .attr("r",3.5) // reset size
        .classed("not_possible",true)
        .classed("selected",false);
};

var lasso_draw = function() {

    // Style the possible dots
    lasso.possibleItems()
        .classed("not_possible",false)
        .classed("possible",true);

    // Style the not possible dot
    lasso.notPossibleItems()
        .classed("not_possible",true)
        .classed("possible",false);
};

//lasso_end defined separately for circles and rect in drawer.js


//lasso ends