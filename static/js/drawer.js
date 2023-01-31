//for lasso selected item calculations
var cluster_id = [];
var xVals = [];
var yVals = [];
var xLabelMax;
var xLabelMin;

var groupNames;

var svg;

let brush;
let counter;
let numberOfGroup;
let barsInGroup;

var lasso_selection;

var columnArr = [];
var columnArrInString = [];


var JSONRequestURL = "static/task/active_summary_types.json";
var JSONRequest = new XMLHttpRequest();
JSONRequest.open('GET', JSONRequestURL);
JSONRequest.responseType = 'json';
JSONRequest.send();

JSONRequest.onload = function () {

    if (JSONRequest.status === 200) {
        var jsonObj = JSONRequest.response;
        var brush = jsonObj['brush']
        lasso_selection = brush !== true;
    }
}


function lineGraph(data) {
    //console.log("lineGraph function called");
    //console.log(data);

    var margin = {top: 30, right: 40, bottom: getBottomMargin(), left: 100},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("role", "img")
        .attr("aria-label", "This is a " + graphType + " chart. That represents " + title + ". ")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // gridlines in x axis function
    function make_x_gridlines() {
        return d3.axisBottom(x)
            .ticks(5);
    }

    // gridlines in y axis function
    function make_y_gridlines() {
        return d3.axisLeft(y)
            .ticks(5);
    }

    counter = 0;


    //Read the data
    //fix x axis values if it contains alpha chars
    if (isNumeric(data[0][xLabel])) {
        data.forEach(function (d) {
            d[xLabel] = parseInt(d[xLabel]) || parseFloat(d[xLabel]);
            d[yLabel] = +d[yLabel];
        });
    }

    // d3.scaleLinear constructs creates a scale with a linear relationship between input and output.
    var x = d3.scaleLinear()
        .domain(
            [d3.min(data, function (d) {
                counter++;
                columnArr.push(d[xLabel])
                return +d[xLabel];
            }), d3.max(data, function (d) {
                return +d[xLabel];
            })])
        .range([0, width]);

    var z = d3.scaleLinear()
        .domain([0, counter - 1])
        .range([0, width]);

    columnArr = columnArr.reverse()
    console.log("counter")
    console.log(counter)
    console.log("columnArr")
    console.log(columnArr)

    xLabelMin = d3.min(data, function (d) {
        return +d[xLabel];
    })

    xLabelMax = d3.max(data, function (d) {
        return +d[xLabel];
    })

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x)
            .ticks(data.length - 1)
            .tickFormat(d3.format("d")))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    // Add Y axis
    // check if min value is negative
    let min = d3.min(data, function (d) {
        return +d[yLabel];
    });
    // console.log("MIN -> " + min);
    if (min >= 0) {
        min = 0;
    }
    const max = d3.max(data, function (d) {
        return +d[yLabel];
    });
    // console.log("MAX -> " + max);

    var y = d3.scaleLinear()
        .domain([min, max])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<strong> " + yLabel + ":</strong> <span style='color:#ff0000'>" + d[yLabel] + "</span>";
        });

    svg.call(tip);

    // Add the line
    svg.append("path")
        .datum(data)
        .attr("id", "path1")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", d3.line()
            .x(function (d) {
                return x(d[xLabel]);
            })
            .y(function (d) {
                return y(d[yLabel]);
            })
        )

    var circles = svg.selectAll(".dot")
        .data(data)
        .enter().append("circle")
        .attr("class", "dot") // Assign a class for styling
        .attr('class', 'lassoable') //new for lasso selection
        .attr("xVal", function (d) {
            return d[xLabel];
        })
        .attr("yVal", function (d) {
            return d[yLabel];
        })
        .attr("cx", function (d) {
            return x(d[xLabel]);
        })
        .attr("cy", function (d) {
            return y(d[yLabel]);
        })
        .attr("r", 5)
        .attr("fill", "#2ba8fc")
        .attr("stroke", "black")
        .each(setId)
        .on('mouseover', function (d) {
            //id = this.getAttribute("id")
            //lineListenerOver(id)
            tip.show(d);
        })
        .on('mouseout', function (d) {
            //id = this.getAttribute("id")
            //lineListenerOut(id)
            tip.hide(d);
        })
        .attr('tabindex', 0)
        .on('focus', function (d) {
            var id = this.getAttribute("id");
            console.log("FOCUSED -> " + id);
            console.log(d[yLabel])
            console.log(d[xLabel])
            tip.show(d);
            d3.select(this)
                .attr('stroke', 'red')
                .attr('stroke-width', 3);
        })
        .on('blur', function (d, i) {
            d3.select(this).attr('stroke', 'black')
                .attr('stroke-width', 1);
            tip.hide(d);
        });

    svg.append("text")
        .attr("transform",
            "translate(" + (width / 2) + " ," +
            (height + margin.top - 40) + ")")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(xLabel)


    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2) - (margin.top + margin.bottom))
        .attr("dy", "1em")
        .attr("class", "label")
        .text(yLabel);

    // add the X gridlines
    svg.append("g")
        .attr("class", "gridX")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines()
            .tickSize(-height)
            .tickFormat("")
        );

    // add the Y gridlines
    svg.append("g")
        .attr("class", "gridY")
        .call(make_y_gridlines()
            .tickSize(-width)
            .tickFormat("")
        );

    if (lasso_selection === true) {
        lassoCircle();

    } else {
        brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on("brush", brushing)
            .on("end", brushed);

        var brushg = svg.append("g")
            .attr("class", "brush")
            .call(brush)

        function brushing() {
            for (let i = 0; i <= counter; i++) {
                resetDotColor("Column" + i)
            }
        }

        function brushed() {
            /*
            d3.select('#start-number')
              .text(Math.round(brush.extent()[0]));
            d3.select('#end-number')
              .text(Math.round(brush.extent()[1]));
            */
            let min_range;
            let max_range;
            let chartNumber;
            let chartType;

            let chart;
            if (d3.brushSelection(this) != null) {
                var range = d3.brushSelection(this)
                    .map(z.invert);

                console.log("range")
                console.log(range)
                min_range = Math.round(range[0])
                max_range = Math.round(range[1])
                // highlight_point("Column"+min_range)
                // highlight_point("Column"+max_range)


                console.log("From -> " + columnArr[min_range])
                console.log("To -> " + columnArr[max_range])
                let selectedPoints = []

                for (let i = min_range; i <= max_range; i++) {
                    console.log(i)
                    highlightDots("Column" + Math.abs((counter - 1) - i))
                    selectedPoints.push(columnArr[i])
                }

                console.log("selectedPoints")
                console.log(selectedPoints)

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                console.log(xLabel)
                console.log(yLabel)

                chartType = "single";
                console.log(chartType)
                chart = "line";
                console.log(chart)

                // construct an HTTP request

                var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
                // var theUrl = "https://infovis-userstudy.herokuapp.com/multiBarBrush";
                var theUrl = "https://127.0.0.1:8080/multiBarBrush";
                xmlhttp.open("POST", theUrl);

                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({
                    "chart": "" + chart + "",
                    "chartType": "" + chartType + "",
                    "barValues": "" + selectedPoints.join() + "",
                    "xLabel": "" + xLabel + "",
                    "yLabel": "" + yLabel + "",
                    "chartNumber": "" + chartNumber + ""
                }));

                xmlhttp.onloadend = function () {
                    console.log(xmlhttp.status)
                    if (xmlhttp.status = 200) {

                        const myObj = JSON.parse(xmlhttp.response);
                        var part_sum_arr = []
                        part_sum_arr = myObj.summary.split("+");
                        summary = partial_summary
                        // console.log(part_sum_arr);

                        partial_summary = part_sum_arr;

                        console.log(partial_summary);
                        set_partial_summary();
                        speakText("Summary Generated");
                        // narrateSummary();
                    }
                };
            }

        }
    }

}


function highlightDots(dataId) {
    // document.getElementById(dataId).style.fill = 'red'
    document.getElementById(dataId).style.fill = '#fc5c2b'
    document.getElementById(dataId).style.fillOpacity = '1'

}

function resetDotColor(dataId) {
    if (document.getElementById(dataId) != null) {
        document.getElementById(dataId).style.fill = '#3093cf'
        document.getElementById(dataId).style.fillOpacity = '.5'

    }
}


function unselectSelectedBrush() {

    var b = document.getElementsByClassName("brush")[0].childNodes
    var c = b[1].attributes;
    // console.log(c)


    // console.log(c.length)
    // console.log(c['style'])
    if (c['width'] === undefined) {
        console.log("NO BRUSH SELECTION FOUND THERE")
    } else {
        console.log("BRUSH SELECTION FOUND")
        // console.log(b[1])

        b[1].attributes.width.value = "0";

        // console.log(b[1].attributes.width)

        if (columnType === "two" && graphType === "line") {
            for (let i = 0; i <= counter; i++) {
                resetDotColor("Column" + i)
            }
        } else if (columnType === "multi" && graphType === "line") {
            for (let j = 0; j < numberOfGroup; j++) {
                for (let i = 0; i < counter; i++) {
                    // resetDotColor("Column["+i+"]["+j+"]")
                    document.getElementById("Column[" + j + "][" + i + "]").style.fill = null
                    document.getElementById("Column[" + j + "][" + i + "]").style.fillOpacity = '.5'
                }
            }
        } else if (columnType === "two" && graphType === "bar") {
            for (let i = 0; i <= counter; i++) {
                resetPointColor("Column" + i)
            }
        } else if (columnType === "multi" && graphType === "bar") {
            for (let i = 0; i <= counter; i++) {
                for (let j = 0; j <= barsInGroup; j++) {
                    resetPointColor("Column[" + i + "][" + j + "]")
                }
            }
        }
    }

}

function multiLineGraph() {
    // console.log(data);


    var margin = {top: 30, right: 40, bottom: getBottomMargin(), left: 100},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("role", "img")
        .attr("aria-label", "This is a " + graphType + " chart. That represents " + title + ". ")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    // gridlines in x axis function
    function make_x_gridlines() {
        return d3.axisBottom(x)
            .ticks(5)
    }

    // gridlines in y axis function
    function make_y_gridlines() {
        return d3.axisLeft(y)
            .ticks(5)
    }

    //convert string x values to int
    data.forEach(function (d) {
        //check for years in form of '2018/19'
        if (d[labelArr[0]].length = 7) {
            if (isNumeric(d[labelArr[0]].slice(0, 4)) && isNumeric(d[labelArr[0]].slice(5, 7))
                && d[labelArr[0]].slice(4, 5) === '/') {
                d[labelArr[0]] = parseInt(d[labelArr[0]].slice(0, 5));
            }
        }
    });
    //convert string y values to int
    data.forEach(function (d) {
        for (let n = 1; n < labelArr.length; n++)
            d[labelArr[n]] = parseFloat(d[labelArr[n]]);
    });
    //console.log(data);

    counter = 0;

    var xLabel = labelArr[0]
    const minX = d3.min(data, function (d) {
        counter++;
        columnArr.push(d[xLabel])
        return +d[xLabel];
    });
    const maxX = d3.max(data, function (d) {
        return +d[xLabel];
    });

    columnArr = columnArr.reverse()

    // console.log("counter")
    // console.log(counter)
    // console.log("columnArr")
    // console.log(columnArr)

    var xRange = d3.scaleLinear()
        .domain([0, counter - 1])
        .range([0, width]);

    // console.log("xLabel -> "+xLabel)
    // console.log("xLabel2 -> "+labelArr[1])


    var x = d3.scaleLinear()
        .domain([minX, maxX])
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x)
            .ticks(data.length - 1)
            .tickFormat(d3.format("d"))
        )
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    // Add Y axis
    var keys = Object.keys(data[0]).slice(1);

    groupNames = keys
    console.log("groupNames")
    console.log(groupNames)

    numberOfGroup = groupNames.length
    console.log("numberOfGroup")
    console.log(numberOfGroup)


    //check if graph has a negative min value
    let min = d3.min(data, function (d) {
        return d3.min(keys, function (key) {
            return d[key];
        });
    })
    if (min >= 0) {
        min = 0
    }
    const max = d3.max(data, function (d) {
        return d3.max(keys, function (key) {
            return d[key];
        });
    })
    var y = d3.scaleLinear()
        // Scale the range of the data
        .domain([min, max]).nice()
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            //console.log(d)
            return "<strong> " + lineValue + ' at ' + xValue + ":</strong> <span style='color:red'>" + yValue + "</span>";
        })
    svg.call(tip);

    var z = d3.scaleOrdinal()
        .range(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6']);

    //iterate through non xAxis data
    let count = 0;


    for (let n = 1; n < labelArr.length; n++) {
        // Add the lines
        svg.append("path")
            .datum(data)
            .attr("id", "path" + n)
            .attr("fill", "none")
            .attr("stroke", () => {
                return z(n - 1)
            })
            .attr("stroke-width", 4)
            .attr("d", d3.line()
                .x(function (d) {
                    return x(d[xLabel])
                })
                .y(function (d) {
                    return y(d[labelArr[n]])
                })
            );


        //console.log(data.length - 1)
        data.forEach(function (d, index) {
            svg.append("circle")
                .attr("lineIndex", count)
                .attr("dotIndex", index)
                .attr("class", "dot") // Assign a class for styling
                .attr('class', 'lassoable') //new for lasso selection
                .attr("xVal", d[xLabel])
                .attr("yVal", d[labelArr[n]])
                .attr("lineVal", labelArr[n])
                .attr("cx", x(d[xLabel]))
                .attr("cy", y(d[labelArr[n]]))
                .attr("r", 5)
                .attr("fill", function () {
                    const color = z(count)
                    return shadeColor(color, 40)
                })
                .attr("stroke", "black")
                .attr("stroke-width", "1")
                .each(mulitLineSetID)
                .on('mouseover', function () {
                    lineValue = labelArr[n];
                    xValue = d[xLabel]
                    yValue = d[labelArr[n]]
                    tip.show([lineValue, xValue, yValue])
                    // console.log("Hurrah" + [lineValue, xValue, yValue])
                })
                .on('mouseout', function () {
                    tip.hide(d[labelArr[n]])
                })
                .attr('tabindex', 0)
                .on('focus', function () {
                    var id = this.getAttribute("id");
                    console.log("FOCUSED -> " + id);
                    lineValue = labelArr[n];
                    xValue = d[xLabel]
                    yValue = d[labelArr[n]]
                    tip.show([lineValue, xValue, yValue])
                    d3.select(this)
                        .attr('stroke', 'red')
                        .attr('stroke-width', 3);
                })
                .on('blur', function () {

                    d3.select(this).attr('stroke', 'black')
                        .attr('stroke-width', 1);
                    tip.hide(d[labelArr[n]])
                });
            if (index === data.length - 1) {
                count += 1;
            }


        });
    }

    svg.append("text")
        .attr("transform",
            "translate(" + (width / 2) + " ," +
            (height + margin.top - 40) + ")")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(xLabel);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2) - (margin.top + margin.bottom))
        .attr("dy", "1em")
        .attr("class", "label")
        .text(yLabel);

    // add the X gridlines
    svg.append("g")
        .attr("class", "gridX")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines()
            .tickSize(-height)
            .tickFormat("")
        )

    // add the Y gridlines
    svg.append("g")
        .attr("class", "gridY")
        .call(make_y_gridlines()
            .tickSize(-width)
            .tickFormat("")
        )


    var legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(keys.slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("x", width - 19)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", function (d) {
            const labelIndex = labelArr.indexOf(d) - 1;
            return z(labelIndex);
        });

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function (d) {
            return d;
        });

    if (lasso_selection === true) {
        lassoCircle();

    } else {
        brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on("brush", brushing)
            .on("end", brushed);

        var brushg = svg.append("g")
            .attr("class", "brush")
            // .attr("id", "anID")
            .call(brush)

        function brushing() {
            for (let j = 0; j < numberOfGroup; j++) {
                for (let i = 0; i < counter; i++) {
                    // resetDotColor("Column["+i+"]["+j+"]")
                    document.getElementById("Column[" + j + "][" + i + "]").style.fill = null
                    document.getElementById("Column[" + j + "][" + i + "]").style.fillOpacity = '.5'
                }
            }
        }

        function brushed() {
            /*
            d3.select('#start-number')
              .text(Math.round(brush.extent()[0]));
            d3.select('#end-number')
              .text(Math.round(brush.extent()[1]));
            */
            let min_range;
            let max_range;
            let chartNumber;
            let chartType;
            let chart;

            if (d3.brushSelection(this) != null) {
                var range = d3.brushSelection(this)
                    .map(xRange.invert);

                console.log("range")
                min_range = Math.round(range[0])
                max_range = Math.round(range[1])

                console.log(min_range)
                console.log(max_range)

                let selectedGroups = []
                //
                for (let i = min_range; i <= max_range; i++) {
                    selectedGroups.push(columnArr[i])

                }
                for (let j = 0; j < numberOfGroup; j++) {
                    for (let i = min_range; i <= max_range; i++) {
                        // console.log("Column[" + j + "][" + Math.abs((counter - 1) - i)  + "]")
                        highlightDots("Column[" + j + "][" + Math.abs((counter - 1) - i) + "]")
                    }
                }

                console.log(selectedGroups)

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                console.log(xLabel)
                console.log(yLabel)

                chartType = "multi";
                console.log(chartType)

                chart = "line"

                // construct an HTTP request

                var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
                // var theUrl = "https://infovis-userstudy.herokuapp.com/multiBarBrush";
                var theUrl = "https://127.0.0.1:8080/multiBarBrush";
                xmlhttp.open("POST", theUrl);

                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({
                    "chart": "" + chart + "",
                    "chartType": "" + chartType + "",
                    "barValues": "" + selectedGroups.join() + "",
                    "groupNames": "" + groupNames.join() + "",
                    "xLabel": "" + xLabel + "",
                    "yLabel": "" + yLabel + "",
                    "chartNumber": "" + chartNumber + ""
                }));

                xmlhttp.onloadend = function () {
                    console.log(xmlhttp.status)
                    if (xmlhttp.status = 200) {

                        const myObj = JSON.parse(xmlhttp.response);
                        var part_sum_arr = []
                        part_sum_arr = myObj.summary.split("+");
                        summary = partial_summary
                        // console.log(part_sum_arr);

                        partial_summary = part_sum_arr;
                        console.log(partial_summary);
                        set_partial_summary();
                        speakText("Summary Generated");
                    }
                };
            }

        }

    }

}


function barGraph() {
    // console.log("Bar Graph was called");
    // console.log(data);

    var margin = {top: 30, right: 40, bottom: getBottomMargin(), left: 100},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // convert string y values to int
    data.forEach(function (d) {
        d[xLabel] = d[xLabel];
        d[yLabel] = parseInt(d[yLabel]) || parseFloat(d[yLabel]);
    });

    // const minX = d3.min(data, function (d) {
    //     return +d[xLabel];
    // });
    // const maxX = d3.max(data, function (d) {
    //     return +d[xLabel];
    // });
    //
    // console.log("minX -> "+minX)
    // console.log("maxX -> "+maxX)

    //

    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);

    var y = d3.scaleLinear()
        .range([height, 0]);

    tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<strong> " + yLabel + ":</strong> <span style='color:red'>" + d[yLabel] + "</span>";
        });

    d3.selectAll("g > *").remove();
    svg = d3.select("#chart").append("svg")
        .attr("role", "img")
        .attr("aria-label", "This is a " + graphType + " chart. That represents " + title + ". ")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.call(tip);

    counter = 0;

    x.domain(data.map(function (d) {
        // console.log(d[xLabel]);
        counter++;
        columnArr.push(d[xLabel])
        return d[xLabel];
    }));

    y.domain([0, d3.max(data, function (d) {
        return (d[yLabel]);
    })]);

    console.log(counter)
    console.log(columnArr)

    var z = d3.scaleLinear()
        .domain([0, counter - 1])
        .range([0, width]);

    svg.append("g")
        .call(d3.axisBottom(x))
        .attr("transform", "translate(0," + height + ")")
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end");

    var circles = svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "dot") // Assign a class for styling
        .attr('class', 'lassoable') //new for lasso selection
        .attr("class", "bar")
        .attr("x", function (d) {
            return x(d[xLabel]);
        })
        .attr("width", x.bandwidth())
        .attr("y", function (d) {
            return y(d[yLabel]);
        })
        .attr("height", function (d) {
            return height - y(d[yLabel]);
        })
        .attr("xVal", function (d) {
            return d[xLabel];
        })
        .attr("yVal", function (d) {
            return d[yLabel];
        })
        .each(setId)
        .attr("fill", "#3093cf")
        .on('mouseover', function (d) {
            //id = this.getAttribute("id")
            //barListenerOver(id)
            tip.show(d);
        })
        .on('mouseout', function (d) {
            //id = this.getAttribute("id")
            //barListenerOut(id)
            tip.hide(d);
        })
        .attr('tabindex', 0)
        .on('focus', function (d) {
            // var id = this.getAttribute("id");
            // console.log("FOCUSED -> " + id);
            tip.show(d);
            d3.select(this)
                .attr('stroke', 'black')
                .attr('stroke-width', 3);
        })
        .on('blur', function (d, i) {

            d3.select(this).attr('stroke', 'black')
                .attr('stroke-width', 0);
            tip.hide(d);
        });

    svg.append("text")
        .attr("transform",
            "translate(" + (width / 2) + " ," +
            (height + margin.top - 40) + ")")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(xLabel);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2) - (margin.top + margin.bottom))
        .attr("dy", "1em")
        .attr("class", "label")
        .text(yLabel);

    if (lasso_selection === true) {
        console.log("LASSO SELECTION WAS FOUND TRUE")
        lassoRect();
    } else {
        console.log("LASSO SELECTION WAS FOUND FALSE")
        var brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on("brush", brushing)
            .on("end", brushed);

        var brushg = svg.append("g")
            .attr("class", "brush")
            .call(brush)
            .selectAll("rect")
            .style({
                "fill": "#69f",
                "fill-opacity": "0.3"
            });

        function brushing() {
            for (let i = 0; i <= counter; i++) {
                resetPointColor("Column" + i)
            }
        }

        function brushed() {
            /*
            d3.select('#start-number')
              .text(Math.round(brush.extent()[0]));
            d3.select('#end-number')
              .text(Math.round(brush.extent()[1]));
            */

            let min_range;
            let max_range;
            let chartNumber;
            let chartType;
            let chart;
            if (d3.brushSelection(this) != null) {
                var range = d3.brushSelection(this)
                    .map(z.invert);

                console.log("range")
                min_range = Math.round(range[0])
                max_range = Math.round(range[1])
                // highlight_point("Column"+min_range)
                // highlight_point("Column"+max_range)
                console.log("From -> " + columnArr[min_range])
                console.log("To -> " + columnArr[max_range])
                let selectedBars = []

                for (let i = min_range; i <= max_range; i++) {
                    highlightPoints("Column" + i)
                    selectedBars.push(columnArr[i])
                }

                console.log(selectedBars)

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                console.log(xLabel)
                console.log(yLabel)

                chartType = "single";
                console.log(chartType)

                chart = "bar"

                // construct an HTTP request

                var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
                // var theUrl = "https://infovis-userstudy.herokuapp.com/multiBarBrush";
                var theUrl = "https://127.0.0.1:8080/multiBarBrush";
                xmlhttp.open("POST", theUrl);

                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({
                    "chart": "" + chart + "",
                    "chartType": "" + chartType + "",
                    "barValues": "" + selectedBars.join() + "",
                    "xLabel": "" + xLabel + "",
                    "yLabel": "" + yLabel + "",
                    "chartNumber": "" + chartNumber + ""
                }));

                xmlhttp.onloadend = function () {
                    console.log(xmlhttp.status)
                    if (xmlhttp.status = 200) {

                        const myObj = JSON.parse(xmlhttp.response);
                        var part_sum_arr = []
                        part_sum_arr = myObj.summary.split("+");
                        summary = partial_summary
                        // console.log(part_sum_arr);

                        partial_summary = part_sum_arr;
                        console.log(partial_summary);
                        set_partial_summary();
                        speakText("Summary Generated");
                    }
                };

            }

        }

    }


}

function highlightPoints(dataId) {
    // document.getElementById(dataId).style.fill = 'red'
    document.getElementById(dataId).style.fillOpacity = '1'

}

function resetPointColor(dataId) {
    if (document.getElementById(dataId) != null) {
        // document.getElementById(dataId).style.fill = '#3093cf'
        document.getElementById(dataId).style.fillOpacity = '.5'

    }
}

function multiBarGraph() {
    var margin = {top: 30, right: 40, bottom: getBottomMargin(), left: 100},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            //console.log(d)
            return "<strong> " + d.key + ' at ' + d.xValue + ":</strong> <span style='color:red'>" + d.value + "</span>";
        })

    var svg = d3.select("#chart").append("svg")
        .attr("role", "img")
        .attr("aria-label", "This is a " + graphType + " chart. That represents " + title + ". ")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.call(tip);

    var x0 = d3.scaleBand()
        .rangeRound([0, width])
        .paddingInner(0.2);

    var x1 = d3.scaleBand()
        .padding(0.05);

    var y = d3.scaleLinear()
        .rangeRound([height, 0]);

    var z = d3.scaleOrdinal()
        .range(["#8dd3c7",
            "#ffffb3",
            "#bebada",
            "#fb8072",
            "#80b1d3",
            "#fdb462",
            "#b3de69",
            "#fccde5",
            "#d9d9d9",
            "#bc80bd",
            "#ccebc5",
            "#ffed6f"]);

    //convert string y values to int
    data.forEach(function (d) {
        for (let n = 0; n < labelArr.length; n++) {
            if (n > 0) {
                if (isNaN(d[labelArr[n]])) {
                    d[labelArr[n]] = 0;
                } else if (isNumeric(d[labelArr[n]])) {
                    d[labelArr[n]] = parseInt(d[labelArr[n]]) || parseFloat(d[labelArr[n]]);
                }
            }
        }
    });

    let keys = (Object.keys(data[0]));
    let yValues = []
    data.forEach(function (d) {
        for (key of keys) {
            if (key !== xLabel)
                yValues.push(parseInt(d[key]) || parseFloat(d[key]))
        }
    })
    const max = yValues.reduce(function (a, b) {
        return Math.max(a, b);
    });
    let index = keys.indexOf(xLabel)
    keys.splice(index, 1)

    counter = 0;
    barsInGroup = labelArr.length - 1;

    x0.domain(data.map(function (d) {
        counter++;
        columnArr.push(d[xLabel])
        return d[xLabel];
    }));

    console.log("counter")
    console.log(counter)
    console.log("barsInGroup")
    console.log(barsInGroup)

    var xRange = d3.scaleLinear()
        .domain([0, counter - 1])
        .range([0, width]);

    x1.domain(keys).rangeRound([0, x0.bandwidth()]);
    y.domain([0, max]).nice();

    groupNames = x1.domain()
    console.log("groupNames")
    console.log(groupNames)

    // console.log(x0.domain())
    // console.log(x1.domain())
    // console.log(y.domain())
    svg.append("g")
        .selectAll("g")
        .data(data)
        .enter().append("g")
        .attr("transform", function (d) {
            return "translate(" + x0(d[xLabel]) + ",0)";
        })
        .selectAll("rect")
        .data(function (d) {
            return keys.map(function (key) {
                return {key: key, value: d[key], xValue: d[xLabel]};
            });
        })
        .enter().append("rect")
        .attr("class", "dot") // Assign a class for styling
        .attr('class', 'lassoable') //new for lasso selection
        .attr("x", function (d) {
            return x1(d.key);
        })
        .attr("y", function (d) {
            return y(d.value);
        })
        .attr("width", x1.bandwidth())
        .attr("height", function (d) {
            return height - y(d.value);
        })
        .attr("fill", function (d) {
            return z(d.key);
        })
        .attr("stroke", "black")
        .attr("barVal", function (d) {
            return d.key
        })
        .attr("xLabel", xLabel)
        .attr("xVal", function (d) {
            return d.xValue
        })
        .attr("yVal", function (d) {
            return d.value
        })
        .each(mulitBarSetID)
        .on('mouseover', function (d) {
            tip.show(d)
        })
        .on('mouseout', function (d) {
            tip.hide(d)
        })
        .attr('tabindex', 0)
        .on('focus', function (d) {
            var id = this.getAttribute("id");
            console.log("FOCUSED -> " + id);
            tip.show(d);
            d3.select(this)
                .attr('stroke', 'red')
                .attr('stroke-width', 4);
        })
        .on('blur', function (d, i) {

            d3.select(this).attr('stroke', 'black')
                .attr('stroke-width', 1);
            tip.hide(d);
        });

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x0))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    svg.append("g")
        .attr("class", "axis")
        .call(d3.axisLeft(y).ticks(null, "s"))
        .append("text")
        .attr("x", 2)
        .attr("y", y(y.ticks().pop()) + 0.5)
        .attr("dy", "0.32em")
        .attr("fill", "#000")
        .attr("font-weight", "bold")
        .attr("text-anchor", "start")

    var legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(keys.slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(40," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("x", width - 19)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", z)
        .attr("stroke", "black");

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function (d) {
            return d;
        });

    svg.append("text")
        .attr("transform",
            "translate(" + (width / 2) + " ," +
            (height + margin.top - 40) + ")")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(xLabel);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2) - (margin.top + margin.bottom))
        .attr("dy", "1em")
        .attr("class", "label")
        .text(yLabel);

    if (lasso_selection === true) {
        lassoRect();

    } else {
        var brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on("brush", brushing)
            .on("end", brushed);

        var brushg = svg.append("g")
            .attr("class", "brush")
            .call(brush)
            .selectAll("rect")
            .style({
                "fill": "#69f",
                "fill-opacity": "0.3"
            });

        function brushing() {
            for (let i = 0; i <= counter; i++) {
                for (let j = 0; j <= barsInGroup; j++) {
                    resetPointColor("Column[" + i + "][" + j + "]")
                }
            }
        }

        function brushed() {
            let min_range;
            let max_range;
            let chartNumber;
            let chartType;
            let chart;
            if (d3.brushSelection(this) != null) {
                var range = d3.brushSelection(this)
                    .map(xRange.invert);

                console.log(range[0])
                console.log(range[1])
                console.log("range")
                min_range = Math.round(range[0])
                if (Math.floor(range[1]) === counter - 2) {
                    max_range = Math.ceil(range[1])
                } else {
                    max_range = Math.floor(range[1])

                }

                console.log("From -> " + columnArr[min_range])
                console.log("To -> " + columnArr[max_range])
                let selectedGroups = []
                //
                for (let i = min_range; i <= max_range; i++) {
                    selectedGroups.push(columnArr[i])
                    for (let j = 0; j < barsInGroup; j++) {
                        highlightPoints("Column[" + i + "][" + j + "]")
                    }
                }
                //
                console.log(selectedGroups)

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                console.log(xLabel)
                console.log(yLabel)

                chartType = "multi";
                console.log(chartType)

                chart = "bar"
                // construct an HTTP request

                var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
                // var theUrl = "https://infovis-userstudy.herokuapp.com/multiBarBrush";
                var theUrl = "https://127.0.0.1:8080/multiBarBrush";
                xmlhttp.open("POST", theUrl);

                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({
                    "chart": "" + chart + "",
                    "chartType": "" + chartType + "",
                    "barValues": "" + selectedGroups.join() + "",
                    "groupNames": "" + groupNames.join() + "",
                    "xLabel": "" + xLabel + "",
                    "yLabel": "" + yLabel + "",
                    "chartNumber": "" + chartNumber + ""
                }));

                xmlhttp.onloadend = function () {
                    console.log(xmlhttp.status)
                    if (xmlhttp.status = 200) {

                        const myObj = JSON.parse(xmlhttp.response);
                        var part_sum_arr = []
                        part_sum_arr = myObj.summary.split("+");
                        summary = partial_summary
                        // console.log(part_sum_arr);

                        partial_summary = part_sum_arr;
                        console.log(partial_summary);
                        set_partial_summary();
                        speakText("Summary Generated");
                    }
                };

            }

        }

    }


}


function drawPieChart(data) {

    var margin = {top: 30, right: 40, bottom: 50, left: 400},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("role", "img")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //specific to pie chart

    var radius = 250;

    console.log(data);

    var g = svg.append("g") //we use .append to put a <g> element inside of our <svg> element. The g svg elemnt is a container to group other svg elements
        .attr("transform", "translate(" + radius + "," + radius + ")")


    var colors = ["#097392", "#83B4B3", "#FFF0CE", "#D55534", "#555555", "#9C6E4E", "#E9CCC3", "#C9DAD8", "#E0D9D2", "#9EB371", "#E6C570", "#4F766F"];

    //var numberOfColumn= data.length; //already there
    var color_list = []
    for (i = 0; i < numberOfColumn; i++) {
        color_list.push(colors[i]);
    }

    var color = d3.scaleOrdinal(color_list); //we use scaleOrdinal methos to give our graph colors

    var pie = d3.pie()
        .sort(null)
        .value(function (d) {
            return d[percentage];
        });

    // var path = d3.arc() //help us draw our path //used to draw parts of the pie chart
    //     .outerRadius(radius)
    //     .innerRadius(0);
    //
    // var arcOver = d3.arc()
    //     .outerRadius(radius + 20)
    //     .innerRadius(radius - 180);//for interaction
    // The arc generator

    var path = d3.arc()
        .innerRadius(radius * 0.5)         // This is the size of the donut hole
        .outerRadius(radius * 0.8)

// Another arc that won't be drawn. Just for labels positioning
    var arcOver = d3.arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9)

    var arc = g.selectAll() ////help us draw our arc //used to draw parts of the pie chart //each section of the pie chart will be selected here and will run our pie fucntion with the data in through it, and will append each one of those to our g svg element
        .data(pie(data))
        .enter()
        .append("g");


    arc.append("path")  //This fills each of the sections --> each element/section inside g svg element.
        .attr("d", path) //Each section is given an svg attribute d which means draw the "path"
        .attr("fill", function (d) {
            return color(d.data[percentage]);
        }) //fills each of those section with the desired color
        .attr("nameVal", function (d) {
            return d.data[labelName]
        }) //assigns nameVal attribute to path/ specific arc which returns the actual name of that specific arc retrived by the labelName of the dataset (e.g. If labelName= fruit, value returned can be orange, watermelon etc)
        .attr("percentVal", function (d) {
            return d.data[percentage]
        }) //assigns percentVal attribute to path/ specific arc which returns the avtual value of percentage for that specific arc (e.g. 50%, 25% etc)

        .on("mouseenter", function (d) {
            d3.select(this)
                .attr("stroke", "white")
                .transition()
                .duration(200)
                .attr("stroke", "orange")
                .attr("stroke-width", 3);

        })
        .on("mouseleave", function (d) {
            d3.select(this).transition()
                .duration(200)
                .attr("d", path)
                .attr("stroke", "none");

        })
        .each(pieSetId)
        .on('focus', function (d) {
            // var id = this.getAttribute("id");
            // console.log("FOCUSED -> " + id);
            d3.select(this)
                .attr('stroke', 'black')
                .attr('stroke-width', 3);
        })
        .on('blur', function (d, i) {

            d3.select(this).attr('stroke', 'black')
                .attr('stroke-width', 0);
        });
    // .on("click", function (d) {
    //      d3.select(this)
    //      var str= d.data[labelName] + ": " + d.data[percentage] + "%" ;
    //     textChange(str)

    //      })

    // .on('mouseover', function (d) {
    //     //id = this.getAttribute("id")
    //     //barListenerOver(id)
    //     tip.show(d);
    // })
    // .on('mouseout', function (d) {
    //     //id = this.getAttribute("id")
    //     //barListenerOut(id)
    //     tip.hide(d);
    // });


    /*
        var labels = d3.arc() //same thing as path but different variable name for text paths and arc.
            .outerRadius(radius)
            .innerRadius(0);

        arc.append('text') //appends text to each arc variable  //instead of g.selectAll()
            .attr("transform", function(d){return "translate(" + labels.centroid(d) + ")";  //ensures all text don't stay in the center of the pie chart //puts each text in their arc
            })
            .attr("text-anchor", "middle") //centers each text within an arc
            .text(function(d) { return d.data[labelName] + ": " + d.data[percentage] + "%" ;}); //specifies the content of the text using data
    */

    // Add the polylines between chart and labels:
    arc
        .selectAll('allPolylines')
        .data(pie(data))
        .enter()
        .append('polyline')
        .attr("stroke", "black")
        .style("fill", "none")
        .attr("stroke-width", 1)
        .attr('points', function (d) {
            var posA = path.centroid(d) // line insertion in the slice
            var posB = arcOver.centroid(d) // line break: we use the other arc generator that has been built only for that
            var posC = arcOver.centroid(d); // Label position = almost the same as posB
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
            posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
            return [posA, posB, posC]
        })

// Add the polylines between chart and labels:
    arc
        .selectAll('allLabels')
        .data(pie(data))
        .enter()
        .append('text')
        .text(function (d) {
            return d.data[labelName] + ": " + d.data[percentage] + "%";
        })
        .attr('transform', function (d) {
            var pos = arcOver.centroid(d);
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
            return 'translate(' + pos + ')';
        })
        .style('text-anchor', function (d) {
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            return (midangle < Math.PI ? 'start' : 'end')
        })


    //lasso selection//

    // // Create a rectangle in the background for lassoing
    // var bg = svg.append('rect')
    //     .attr('class','lassoable')
    //     .attr('x',0)
    //     .attr('y',0)
    //     .attr('width',width)
    //     .attr('height',height)
    //     .attr('opacity',0);

    // //lasso inialization
    // lasso = d3.lasso()
    //     .closePathDistance(75)
    //     .closePathSelect(true)
    //     .hoverSelect(true)
    //     .targetArea(svg.selectAll('.lassoable')) //new
    //     .items(arc)
    //     .on("start",lasso_start)
    //     .on("draw",lasso_draw)
    //     .on("end",lasso_end);


    // svg.call(lasso);

    lassoPie();

}

function drawScatterPlot(data) {

    // var margin = {top: 30, right: 80, bottom: 50, left: 40},
    //         width = 1300 - margin.left - margin.right,
    //         height = 700 - margin.top - margin.bottom;


    var margin = {top: 30, right: 200, bottom: 50, left: 100},
        width = 1000,
        height = 500;

    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("role", "img")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    // gridlines in x axis function
    function make_x_gridlines() {
        return d3.axisBottom(x)
            .ticks(5);
    }

    // gridlines in y axis function
    function make_y_gridlines() {
        return d3.axisLeft(y)
            .ticks(5);
    }


    // d3.scaleLinear constructs creates a scale with a linear relationship between input and output.
    var x = d3.scaleLinear()
        .domain(
            [d3.min(data, function (d) {
                return +d[xLabel];
            }), d3.max(data, function (d) {
                return +d[xLabel];
            })])
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        //.ticks(data.length - 1)
        //.tickFormat(d3.format("d")))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");


    // Add Y axis
    let min = d3.min(data, function (d) {
        return +d[yLabel];
    });
    const max = d3.max(data, function (d) {
        return +d[yLabel];
    });

    // console.log("MAX -> " + max);

    var y = d3.scaleLinear()
        .domain([min, max])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // setup fill color
    var cValue = function (d) {
            return d[classLabel];
        },
        color = d3.scaleOrdinal(d3.schemeCategory10);


    // var tip = d3.tip()
    //     .attr('class', 'd3-tip')
    //     .offset([-10, 0])
    //     .html(function (d) {
    //         return "<strong> " + yLabel + ":</strong> <span style='color:#ff0000'>" + d[yLabel] + "</span>";
    //     });

    // svg.call(tip);

    // //add the tooltip area to the webpage
    // var tooltip = d3.select("body").append("div")
    //     .attr("class", "tooltip")
    //     .style("opacity", 0);


    var circles = svg.selectAll(".dot")
        .data(data)
        .enter().append("circle")
        .attr("class", "dot") // Assign a class for styling
        .attr('class', 'lassoable') //new for lasso selection
        .attr("xVal", function (d) {
            return d[xLabel];
        })
        .attr("yVal", function (d) {
            return d[yLabel];
        })
        .attr("classVal", function (d) {
            return d[classLabel];
        })
        .attr("cx", function (d) {
            return x(d[xLabel]);
        })
        .attr("cy", function (d) {
            return y(d[yLabel]);
        })
        .attr("r", 5)
        .style("fill", function (d) {
            return color(cValue(d));
        })
        .style("fill-opacity", 1)
        .style("opacity", 1)
        .each(scatterSetId)
        .on("mouseenter", function (d) {
            d3.select(this)
                .attr("stroke", "red")
                .attr("stroke-width", 3);

        })
        .on("mouseleave", function (d) {
            d3.select(this)
                .attr("stroke", "none");

        })
        .on('focus', function (d) {
            var id = this.getAttribute("id");
            console.log("FOCUSED -> " + id);
            //tip.show(d);
            d3.select(this)
                .attr('stroke', 'red')
                .attr('stroke-width', 3);
        })
        .on('blur', function (d, i) {
            d3.select(this).attr('stroke', 'black')
                .attr('stroke-width', 1);
            //tip.hide(d);
        });

    svg.append("text")
        .attr("transform",
            "translate(" + (width / 2) + " ," +
            (height + margin.top - 40) + ")")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(xLabel);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2) - (margin.top + margin.bottom))
        .attr("dy", "1em")
        .attr("class", "label")
        .text(yLabel);

    // add the X gridlines
    svg.append("g")
        .attr("class", "gridX")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines()
            .tickSize(-height)
            .tickFormat("")
        );

    // add the Y gridlines
    svg.append("g")
        .attr("class", "gridY")
        .call(make_y_gridlines()
            .tickSize(-width)
            .tickFormat("")
        );


    // draw legend
    var legend = svg.selectAll(".legend")
        .data(color.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(0," + i * 20 + ")";
        });

    // draw legend colored rectangles
    legend.append("rect")
        .attr("x", width + 10)
        .attr("y", 5)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    // draw legend text
    legend.append("text")
        // .attr("x", width - 24)
        // .attr("y", 9)
        .attr("x", width + 40)
        .attr("y", 10)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .text(function (d) {
            return d;
        })

    lassoScatterCircle();

    // clsuters= d3.select('.lassoable selected').attr('id');

    // var attr = d3.select(this).attributes
    // var string = "";
    // var string = barValue + " is " + yValue + " at " + xLabel + " " + xValue;
    // string += attr.getNamedItem('xVal').value + " is " + attr.getNamedItem('yVal').value + ", at " + attr.getNamedItem('xLabel').value + " " + attr.getNamedItem('xVal').value;
    // console.log(d3.selectAll(".lassoable selected").attr("xVal"))


    // console.log(d3.mean(d3.selectAll('.lassoable selected')))
    // var lasso_end = function() {
    //
    //
    //     // Style the selected dots
    //
    //
    //     //const c = lasso.selectedItems().getNamedItem('fill').value;
    //     //console.log(d3.mean(lasso.selectedItems().getNamedItem("xVal").value));
    //
    //     // var txt = "";
    //     // var lasso_selected_items= lasso.selectedItems();
    //     // lasso_selected_items.each(myFunction);
    //     // function myFunction(t){
    //     // txt = txt + t.getNamedItem("xVal").value + "<br>";
    //     // }
    //     // console.log(txt);
    //     lasso.selectedItems().datum(function(){
    //         // return this.getAttribute('yVal');
    //         console.log(+d3.select(this).attr('cx'))
    //         return +d3.select(this).attr('cx');
    //     });
    //
    //
    //
    //
    //
    //
    //
    // };
    // lasso_end();


}

function drawHeatMap(chartData) {
    // var margin = {top: 30, right: 40, bottom: getBottomMargin(), left: 100},
    //     width = 1300 - margin.left - margin.right,
    //     height = 600 - margin.top - margin.bottom;

    var margin = {top: 30, right: 40, bottom: 80, left: 100},
        width = 1300 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;


    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("role", "img")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var myGroups = d3.map(data, function (d) {
        return d[xLabel];
    }).keys()
    var myVars = d3.map(data, function (d) {
        return d[yLabel];
    }).keys()
    console.log(myGroups);
    console.log(myVars);


    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([0, width])
        .domain(myGroups)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 15)
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove()

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([height, 0])
        .domain(myVars)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 15)
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

    // Build color scale
    // var myColor = d3.scaleSequential()
    //     .interpolator(d3.interpolateInferno)
    //     .domain([1,100])
    var myColor = d3.scaleLinear()
        .range(["white", "#69b3a2"])
        .domain([1, 100])

    // create a tooltip
    // var tooltip = d3.select("#chart")
    //     .append("div")
    //     .style("opacity", 0)
    //     .attr("class", "tooltip")
    //     .style("background-color", "white")
    //     .style("border", "solid")
    //     .style("border-width", "2px")
    //     .style("border-radius", "5px")
    //     .style("padding", "5px")
    //
    // // Three function that change the tooltip when user hover / move / leave a cell
    // var mouseover = function(d) {
    //     tooltip
    //         .style("opacity", 1)
    //     d3.select(this)
    //         .style("stroke", "black")
    //         .style("opacity", 1)
    // }
    // var mousemove = function(d) {
    //     tooltip
    //         .html("The exact value of<br>this cell is: " + d[valLabel])
    //         .style("left", (d3.mouse(this)[0]+70) + "px")
    //         .style("top", (d3.mouse(this)[1]) + "px")
    // }
    // var mouseleave = function(d) {
    //     tooltip
    //         .style("opacity", 0)
    //     d3.select(this)
    //         .style("stroke", "none")
    //         .style("opacity", 0.8)
    // }

    // add the squares

    svg.selectAll()
        .data(data, function (d) {
            return d[xLabel] + ':' + d[yLabel];
        })
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return x(d[xLabel])
        })
        .attr("y", function (d) {
            return y(d[yLabel])
        })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .attr("xVal", function (d) {
            return d[xLabel];
        })
        .attr("yVal", function (d) {
            return d[yLabel];
        })
        .attr("cellVal", function (d) {
            return d[valLabel];
        })
        .style("fill", function (d) {
            return myColor(d[valLabel])
        })
        .style("stroke-width", 4)
        // .attr("id", function(d){
        //     return "circle" + myGroups.indexOf( d[xLabel]) + myVars.indexOf( d[yLabel]);})
        .style("opacity", 0.8)
        .each(heatMapSetID)
        .on("mouseenter", function (d) {
            d3.select(this)
                .attr("stroke", "red")
                .attr("stroke-width", 3);

        })
        .on("mouseleave", function (d) {
            d3.select(this)
                .attr("stroke", "none");

        })
        .on('focus', function (d) {
            var id = this.getAttribute("id");
            console.log("FOCUSED -> " + id);
            //tip.show(d);
            d3.select(this)
                .attr('stroke', 'red')
                .attr('stroke-width', 3);
        })
        .on('blur', function (d, i) {
            d3.select(this).attr('stroke', 'none')
                .attr('stroke-width', 1);
            //tip.hide(d);
        });
    // .on("mouseover", mouseover)
    // .on("mousemove", mousemove)
    // .on("mouseleave", mouseleave);

    // Add title to graph
    // svg.append("text")
    //     .attr("x", 0)
    //     .attr("y", -50)
    //     .attr("text-anchor", "left")
    //     .style("font-size", "22px")
    //     .text("A d3.js heatmap");

    // Add subtitle to graph
    // svg.append("text")
    //     .attr("x", 0)
    //     .attr("y", -20)
    //     .attr("text-anchor", "left")
    //     .style("font-size", "14px")
    //     .style("fill", "grey")
    //     .style("max-width", 400)
    //     .text("A short description of the take-away message of this chart.");

    lassoRect();


}


//https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
//usage:
//shadeColor("#63C6FF",40); shadeColor("#63C6FF",-40);

function shadeColor(color, percent) {

    var R = parseInt(color.substring(1, 3), 16);
    var G = parseInt(color.substring(3, 5), 16);
    var B = parseInt(color.substring(5, 7), 16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R < 255) ? R : 255;
    G = (G < 255) ? G : 255;
    B = (B < 255) ? B : 255;

    var RR = ((R.toString(16).length == 1) ? "0" + R.toString(16) : R.toString(16));
    var GG = ((G.toString(16).length == 1) ? "0" + G.toString(16) : G.toString(16));
    var BB = ((B.toString(16).length == 1) ? "0" + B.toString(16) : B.toString(16));

    return "#" + RR + GG + BB;
}

function getCurrentChart() {
    //console.log("getCurrentChart was called. rootName -> " + rootName)
    document.getElementById('chartNumber').setAttribute('value', rootName);
    document.getElementById('numberLabel').innerText = 'Chart #: ' + rootName + ' / 1057'
}

function nextChart() {
    let next = parseInt(rootName) + 1
    document.getElementById('chartNumber').setAttribute('value', next.toString());
    refresh();
}

function previousChart() {
    let previous = parseInt(rootName) - 1
    document.getElementById('chartNumber').setAttribute('value', previous.toString());
    refresh();
}

function getBottomMargin() {
    const label = labelArr[0] || xLabel;
    //console.log(labelArr)
    let labelLengths = []
    data.forEach(function (d) {
        labelLengths.push(d[label].length)
    })
    const maxLabelLength = labelLengths.reduce(function (a, b) {
        return Math.max(a, b);
    });
    return 20 + (maxLabelLength * 10)
}

//lasso functions
function lassoCircle() {


    var lasso_end = function () {

        //reset all variables to empty set
        cluster_id = []; //reset clusters var to empty array every time user finishes drawing lasso
        xVals = [];
        yVals = [];
        var lineVals = [];
        var chartNumber;

        // Reset the color of all dots
        lasso.items()
            .classed("not_possible", false)
            .classed("possible", false);

        // Style the selected dots
        lasso.selectedItems()
            .classed("selected", true)
            .attr("r", 7)
            .attr('stroke', 'red')
            .attr('stroke-width', '3')
            .each(function (d) {
                var id = this.getAttribute("id");
                console.log("LassoSelected -> " + id);
                var xValue = this.getAttribute("xVal");
                var yValue = this.getAttribute("yVal");
                var lineVal = this.getAttribute("lineVal");
                cluster_id.push(id);
                xVals.push(xValue);
                yVals.push(yValue);
                lineVals.push(lineVal);

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                //tip.show(d);
                // d3.select(this)
                //     .attr('stroke', 'red')
                //     .attr('stroke-width', 3);
            });

        var data_str = '{"xValues": "' + xVals.join() + '","yValues":"' + yVals.join() + '","lineValues": ' + lineVals.join() + '}';

        // construct an HTTP request

        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        // var theUrl = "https://infovis-userstudy.herokuapp.com/multiLineLasso";
        var theUrl = "https://127.0.0.1:8080/multiLineLasso";
        xmlhttp.open("POST", theUrl);

        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "xValues": "" + xVals.join() + "",
            "yValues": "" + yVals.join() + "",
            "lineValues": "" + lineVals.join() + "",
            "xLabel": "" + xLabel + "",
            "yLabel": "" + yLabel + "",
            "chartNumber": "" + chartNumber + ""
        }));

        xmlhttp.onloadend = function () {
            console.log(xmlhttp.status)
            if (xmlhttp.status = 200) {
                // const res = xmlhttp.responseText;
                // console.log("res")
                // console.log(res)

                const myObj = JSON.parse(xmlhttp.response);
                var part_sum_arr = []
                part_sum_arr = myObj.summary.split("+");
                summary = partial_summary
                // console.log(part_sum_arr);

                partial_summary = part_sum_arr;
                console.log(partial_summary);
                set_partial_summary();
                speakText("Summary Generated");
            }
        };

        // const c = lasso.selectedItems().getNamedItem('fill').value;

        // Reset the style of the not selected dots
        lasso.notSelectedItems()
            .attr("r", 5)
            .attr('stroke', "#3093cf")
            .attr('stroke-width', '2');

        //lasso selected items calculation
        //mean of x axis values
        // var mean_xVal= d3.mean(xVals);
        // console.log(mean_xVal);

        //mean of y axis values
        var mean_yVal = d3.mean(yVals);
        console.log(mean_yVal);

        var string = "";
        string += "For the selected items, the mean of " + yLabel + " is " + mean_yVal.toFixed(2);
        console.log(string)
        textChange(string);

    };


    lasso = d3.lasso()
        .closePathDistance(75)
        .closePathSelect(true)
        .hoverSelect(false)
        .items(d3.selectAll("circle"))
        .targetArea(d3.select("#chart")) //new
        .on("start", lasso_start)
        .on("draw", lasso_draw)
        .on("end", lasso_end);


    d3.select("svg").call(lasso);

}

function lassoScatterCircle() {
    // var arr=[]
    //
    // var lassoCalc= function(){
    //     // arr.append(d3.select(this).attr('yVal'));
    // }
    // console.log(arr);
    var lasso_end = function () {

        //reset all variables to empty set
        cluster_id = []; //reset clusters var to empty array every time user finishes drawing lasso
        xVals = [];
        yVals = [];

        // Reset the color of all dots
        lasso.items()
            .classed("not_possible", false)
            .classed("possible", false);

        // Style the selected dots
        var selected = lasso.selectedItems()
            .classed("selected", true)
            .attr("r", 7)
            .attr('stroke', 'red')
            .attr('stroke-width', '3')
            .each(function (d) {
                var id = this.getAttribute("id");
                console.log("LassoSelected -> " + id);
                var xValue = this.getAttribute("xVal");
                var yValue = this.getAttribute("yVal");
                cluster_id.push(id);
                xVals.push(xValue);
                yVals.push(yValue);
                //tip.show(d);
                // d3.select(this)
                //     .attr('stroke', 'red')
                //     .attr('stroke-width', 3);
            });
        console.log(cluster_id);
        console.log(xVals);
        console.log(xVals);


        // Reset the style of the not selected dots
        lasso.notSelectedItems()
            .attr("r", 5)
            .attr('stroke', "#3093cf")
            .attr('stroke-width', '0');

        //lasso selected items calculation
        //mean of x axis values
        var mean_xVal = d3.mean(xVals);
        console.log(mean_xVal);

        //mean of y axis values
        var mean_yVal = d3.mean(yVals);
        console.log(mean_yVal);

        var string = "";
        string += "For the selected items, the mean of " + yLabel + " is " + mean_yVal.toFixed(2) + " and the mean of " + xLabel + " is " + mean_xVal.toFixed(2);
        console.log(string)
        textChange(string);


    };

    lasso = d3.lasso()
        .closePathDistance(75)
        .closePathSelect(true)
        .hoverSelect(false)
        .items(d3.selectAll("circle"))
        .targetArea(d3.select("#chart")) //new
        .on("start", lasso_start)
        .on("draw", lasso_draw)
        .on("end", lasso_end);


    d3.select("svg").call(lasso);

}

function lassoRect() {
    // idNum = d3.select(this).attr("id");
    // // elem= document.getElementById(idNum);
    // // clr = d3.select(this).attr("fill");
    // // clr= elem.getAttribute('fill')


    var lasso_end = function () {

        //reset all variables to empty set
        cluster_id = []; //reset clusters var to empty array every time user finishes drawing lasso
        xVals = [];
        yVals = [];
        var barvals = [];
        var chartNumber;

        // Reset the color of all dots
        lasso.items()
            .classed("not_possible", false)
            .classed("possible", false);

        // Style the selected dots
        lasso.selectedItems()
            .classed("selected", true)
            .attr('stroke', 'red')
            .attr('stroke-width', '3')
            .each(function (d) {
                var id = this.getAttribute("id");
                console.log("LassoSelected -> " + id);
                var xValue = this.getAttribute("xVal");
                var yValue = this.getAttribute("yVal");
                var lineVal = this.getAttribute("barVal");
                cluster_id.push(id);
                xVals.push(xValue);
                yVals.push(yValue);
                barvals.push(lineVal);

                chartNumber = document.getElementById('chartNumber').value;
                console.log("Chart Number")
                console.log(chartNumber)

                //tip.show(d);
                // d3.select(this)
                //     .attr('stroke', 'red')
                //     .attr('stroke-width', 3);
            });
        console.log("cluster_id");
        console.log(cluster_id);
        console.log("xVals");
        console.log(xVals);
        console.log("yVals");
        console.log(yVals);
        console.log("barvals");
        console.log(barvals);
        console.log("xLabel");
        console.log(xLabel);
        console.log("yLabel");
        console.log(yLabel);

        var data_str = '{"xValues": "' + xVals.join() + '","yValues":"' + yVals.join() + '","lineValues": ' + barvals.join() + '}';

        // construct an HTTP request

        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        // var theUrl = "https://infovis-userstudy.herokuapp.com/multiBarLasso";
        var theUrl = "https://127.0.0.1:8080/multiBarLasso";
        xmlhttp.open("POST", theUrl);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "xValues": "" + xVals.join() + "",
            "yValues": "" + yVals.join() + "",
            "barValues": "" + barvals.join() + "",
            "xLabel": "" + xLabel + "",
            "yLabel": "" + yLabel + "",
            "chartNumber": "" + chartNumber + ""
        }));

        xmlhttp.onloadend = function () {
            console.log(xmlhttp.status)
            if (xmlhttp.status = 200) {
                // const res = xmlhttp.responseText;
                // console.log("res")
                // console.log(res)

                const myObj = JSON.parse(xmlhttp.response);
                var part_sum_arr = []
                part_sum_arr = myObj.summary.split("+");
                summary = partial_summary
                // console.log(part_sum_arr);

                partial_summary = part_sum_arr;
                console.log(partial_summary);
                set_partial_summary();
                speakText("Summary Generated");
            }
        };

        // const c = lasso.selectedItems().getNamedItem('fill').value;

        // Reset the style of the not selected dots
        lasso.notSelectedItems()
            .attr('stroke', 'none')
            .attr('stroke-width', '1');

        //lasso selected items calculation
        //mean of x axis values
        var mean_xVal = d3.mean(xVals);
        console.log(mean_xVal);

        //mean of y axis values
        var sum_yVal = d3.sum(yVals);
        console.log(sum_yVal);

        var string = "";
        string += "For the selected items, together they make up " + sum_yVal + " " + yLabel;
        console.log(string)
        textChange(string);


    };

    lasso = d3.lasso()
        .closePathDistance(75)
        .closePathSelect(true)
        .hoverSelect(false)
        .items(d3.selectAll("rect"))
        .targetArea(d3.select("#chart")) //new
        .on("start", lasso_start)
        .on("draw", lasso_draw)
        .on("end", lasso_end);


    d3.select("svg").call(lasso);

}


function lassoPie() {

    var lasso_end = function () {

        //reset all variables to empty set
        cluster_id = []; //reset clusters var to empty array every time user finishes drawing lasso
        xVals = [];
        yVals = [];

        // Reset the color of all dots
        lasso.items()
            .classed("not_possible", false)
            .classed("possible", false);

        // Style the selected dots
        lasso.selectedItems()
            .classed("selected", true)
            .attr('stroke', 'red')
            .attr('stroke-width', '3')
            .each(function (d) {
                var id = this.getAttribute("id");
                console.log("LassoSelected -> " + id);
                var nameValue = this.getAttribute("nameVal");
                var percentValue = this.getAttribute("percentVal");
                cluster_id.push(id);
                xVals.push(nameValue);
                yVals.push(percentValue);
                //tip.show(d);
                // d3.select(this)
                //     .attr('stroke', 'red')
                //     .attr('stroke-width', 3);
            });
        console.log(cluster_id);
        console.log(xVals);
        console.log(yVals);
        // const c = lasso.selectedItems().getNamedItem('fill').value;


        // Reset the style of the not selected dots
        lasso.notSelectedItems()
            .attr('stroke', "none")
            .attr('stroke-width', '1');

        //lasso selected items calculation
        //mean of x axis values
        // var sum_nameVal= d3.mean(xVals);
        // console.log(xVals);

        //mean of y axis values
        var sum_percentVal = d3.sum(yVals);
        console.log(xVals);

        var string = "";
        string += "The selected items, together  makes up " + sum_percentVal + " percent";
        console.log(string)
        textChange(string);

    };

    lasso = d3.lasso()
        .closePathDistance(75)
        .closePathSelect(true)
        .hoverSelect(false)
        .items(d3.selectAll("path"))
        .targetArea(d3.select("#chart")) //new
        .on("start", lasso_start)
        .on("draw", lasso_draw)
        .on("end", lasso_end);


    d3.select("svg").call(lasso);

}
