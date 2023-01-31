var chart_list = [876, 899, 900, 611, 425, 818, 921, 304, 333, 445, 795, 806, 831, 839, 412, 34, 791, 817, 935, 389];

var selected_chart_list = [];
var current_chart_type = "";

var bar_list = [876, 898, 901, 611, 425];
var multi_bar_list = [818, 921, 304, 333, 445];
var line_list = [795, 806, 831, 839, 412];
var multi_line_list = [34, 791, 817, 935, 389];


var labelArr = [];
var xLabel = "";
var yLabel = "";
var title = "";
var graphType = "";
var summaryType = "";
var columnType = "";
var data = [];
var idArrays = [];
var summary = [];
var dis_summary = [];
var partial_summary = [];
var gold_summary_human = [];
var rootName = "876";
var summaryArray = [];
var maxSummaryArray = [];
var midSummaryArray = [];
var minSummaryArray = [];
var trendsArray = [];

var numberOfColumn = ""
var multi_number_of_group = ""
var multi_number_of_elements_in_each_group = ""

//for pie chart
var labelName= "";
var percentage="";

//for lasso
var lasso;

//for scatter plot (multiple classes/groups)
var classLabel= "";
//for heatMap
var valLabel = "";

var chart_number = "";

function admin_logged_in(){
    if (sessionStorage.getItem('chartNumber') != null) {
        rootName = sessionStorage.getItem('chartNumber');
    }

}

window.onload = function (){
    chart_number = document.getElementById('chartNumber').value;
    console.log("chart_id in JS")
    console.log(chart_number)
}


if (sessionStorage.getItem('barChartNumber') != null) {
    rootName = sessionStorage.getItem('barChartNumber');
    console.log("barChartNumber")
}
else if (sessionStorage.getItem('multiBarChartNumber') != null) {
    rootName = sessionStorage.getItem('multiBarChartNumber');
    console.log("multiBarChartNumber")
    console.log("rootName")
    console.log(rootName)
}
else if (sessionStorage.getItem('lineChartNumber') != null) {
    rootName = sessionStorage.getItem('lineChartNumber');
    console.log("lineChartNumber")
}
else if (sessionStorage.getItem('multiLineChartNumber') != null) {
    rootName = sessionStorage.getItem('multiLineChartNumber');
    console.log("multiLineChartNumber")
}
else if (sessionStorage.getItem('chartNumber') != null) {
    rootName = sessionStorage.getItem('chartNumber');
    console.log("chartNumber")
}


var summaryPath = "static/generated_new_summary_baseline/" + rootName + ".json";
var c2t_summaryPath = c2t_summaryPath = "static/generated/" + rootName + ".json";




function nextSelectedChart() {
    let cid = parseInt(document.getElementById('chartNumber').value);

    let index;
    let length;

    if (current_chart_type === "bar" || current_chart_type === "multi_bar" || current_chart_type === "line" || current_chart_type === "multi_line"){
        console.log("WE ARE HERE")

        index = selected_chart_list.indexOf(cid);
        length = selected_chart_list.length;

        if (index === (length - 1)){
            index = 0;
        }else {
            index = index + 1;
        }

        console.log(selected_chart_list[index])

        let next = parseInt(selected_chart_list[index])
        document.getElementById('chartNumber').setAttribute('value', next.toString());
        refresh();

    }
    else {
        console.log("THEY ARE THERE")


        index = chart_list.indexOf(cid);
        length = chart_list.length;

        if (index === (length - 1)){
            index = 0;
        }else {
            index = index + 1;
        }

        console.log(chart_list[index])

        let next = parseInt(chart_list[index])
        document.getElementById('chartNumber').setAttribute('value', next.toString());
        refresh();
    }

}

function previousSelectedChart() {
    let cid = parseInt(document.getElementById('chartNumber').value);
    let index;
    let length;

    if (current_chart_type === "bar" || current_chart_type === "multi_bar" || current_chart_type === "line" || current_chart_type === "multi_line"){
        index = selected_chart_list.indexOf(cid);
        length = selected_chart_list.length;

        if (index === 0) {
            index = length - 1;
        }
        else {
            index = index - 1;
        }

        console.log(selected_chart_list[index])

        let next = parseInt(selected_chart_list[index])
        document.getElementById('chartNumber').setAttribute('value', next.toString());
        refresh();

    }
    else {
        index = chart_list.indexOf(cid);
        length = chart_list.length;

        if (index === 0) {
            index = length - 1;
        }
        else {
            index = index - 1;
        }

        console.log(chart_list[index])

        let next = parseInt(chart_list[index])
        document.getElementById('chartNumber').setAttribute('value', next.toString());
        refresh();
    }

}


function set_chart_list(chart){
    if (chart === "bar"){
        selected_chart_list = bar_list;
        current_chart_type = "bar";
    }
    else if (chart === "multi_bar"){
        selected_chart_list = multi_bar_list;
        current_chart_type = "multi_bar";
    }
    else if (chart === "line"){
        selected_chart_list = line_list;
        current_chart_type = "line";
    }
    else if (chart === "multi_line"){
        selected_chart_list = multi_line_list;
        current_chart_type = "multi_line";
    }

}

function set_chart_id(cid){
    // if (sessionStorage.getItem('chartNumber') != null) {
    //     rootName = sessionStorage.getItem('chartNumber');
    // }
    if (cid == null){
        rootName = '33';
    }
    else {
        rootName = cid;
    }

    summaryPath = "static/generated_new_summary_baseline/" + rootName + ".json";
    c2t_summaryPath = "static/generated/" + rootName + ".json";
}




// Stores the currently loaded chart number before refreshing page
function refresh() {
    var x = document.getElementById('chartNumber').value;

    //var y = document.getElementById('chartType').value;

    if (current_chart_type === "bar"){
        sessionStorage.setItem('barChartNumber', x);

        sessionStorage.removeItem('multiBarChartNumber')
        sessionStorage.removeItem('lineChartNumber')
        sessionStorage.removeItem('multiLineChartNumber')
        sessionStorage.removeItem('chartNumber')
    }
    else if (current_chart_type === "multi_bar"){
        sessionStorage.setItem('multiBarChartNumber', x);

        sessionStorage.removeItem('barChartNumber')
        sessionStorage.removeItem('lineChartNumber')
        sessionStorage.removeItem('multiLineChartNumber')
        sessionStorage.removeItem('chartNumber')
    }
    else if (current_chart_type === "line"){
        sessionStorage.setItem('lineChartNumber', x);

        sessionStorage.removeItem('multiBarChartNumber')
        sessionStorage.removeItem('barChartNumber')
        sessionStorage.removeItem('multiLineChartNumber')
        sessionStorage.removeItem('chartNumber')
    }
    else if (current_chart_type === "multi_line"){
        sessionStorage.setItem('multiLineChartNumber', x);

        sessionStorage.removeItem('multiBarChartNumber')
        sessionStorage.removeItem('lineChartNumber')
        sessionStorage.removeItem('barChartNumber')
        sessionStorage.removeItem('chartNumber')
    }
    else {
        sessionStorage.setItem('chartNumber', x);

        sessionStorage.removeItem('multiBarChartNumber')
        sessionStorage.removeItem('lineChartNumber')
        sessionStorage.removeItem('multiLineChartNumber')
        sessionStorage.removeItem('barChartNumber')
    }

    //sessionStorage.setItem('chartType', y);
    location.reload(); //Reloads the current document
}

var elem;
let elem_orig = "";
var temp;

var elem_parent;


var slider;

window.onload = function (){

    elem_orig = document.getElementById("slider_table")

};



function template_summary(){
    // location.reload();
    unselectSelectedBrush();


    document.getElementById("cap_text").innerHTML = "Template-based Summary:"
    // document.getElementById("cap_text").innerHTML = "Description:"

    if (slider == null){
        slider = document.getElementById("summary_slider");
    }

    slider.value = "2";
    summary = midSummaryArray
    dis_summary = summary;
    if (document.getElementById("slider_table") == null){
        elem_parent.appendChild(elem_orig)
    }
    // document.getElementById("mid_summary_rb").checked = true;
    document.getElementById('summary').innerHTML = "";
    setSummary(summaryArray)

}


// function discrete_summary(){
//
//     console.log("PRINTING THE SUMMARY")
//
//     for ( var i = 0; i<summary.length; i++){
//         console.log(summary[i]);
//     }
//
//
// }

function c2t_summary(){
    unselectSelectedBrush();

    document.getElementById("cap_text").innerHTML = "ML-based Summary:"


    elem = document.getElementById("slider_table");

    if (elem !== null){
        temp = elem;
        elem_parent = elem.parentNode;
        console.log(elem_parent)
    }


    document.getElementById('summary').innerHTML = "";
    var c2t_summaryRequestURL = c2t_summaryPath;
    var c2t_summaryRequest = new XMLHttpRequest();
    c2t_summaryRequest.open('GET', c2t_summaryRequestURL);
    c2t_summaryRequest.responseType = 'json';
    c2t_summaryRequest.send();
    c2t_summaryRequest.onload = function () {
        var c2t_jsonObj = c2t_summaryRequest.response;
        c2t_summaryArray = c2t_jsonObj.summary;
        summary = c2t_summaryArray
        dis_summary = summary;
        setSummary(c2t_summaryArray);
        temp.remove();
    }
}

function gold_summary(){
    unselectSelectedBrush();

    document.getElementById("cap_text").innerHTML = "Human-written Summary:"


    elem = document.getElementById("slider_table");

    if (elem !== null){
        temp = elem;
        elem_parent = elem.parentNode;
        console.log(elem_parent)
    }


    document.getElementById('summary').innerHTML = "";
    var c2t_summaryRequestURL = c2t_summaryPath;
    var c2t_summaryRequest = new XMLHttpRequest();
    c2t_summaryRequest.open('GET', c2t_summaryRequestURL);
    c2t_summaryRequest.responseType = 'json';
    c2t_summaryRequest.send();
    c2t_summaryRequest.onload = function () {
        var c2t_jsonObj = c2t_summaryRequest.response;
        gold_summary_human = c2t_jsonObj.gold;
        summary = gold_summary_human
        dis_summary = summary;
        setSummary(gold_summary_human);
        temp.remove();
    }
}

function max_summary(){
    document.getElementById("cap_text").innerHTML = "Template-based Summary:"
    document.getElementById('summary').innerHTML = "";
    summary = maxSummaryArray
    dis_summary = summary;

    setSummary(maxSummaryArray)
}

function mid_summary(){
    document.getElementById("cap_text").innerHTML = "Template-based Summary:"
    document.getElementById('summary').innerHTML = "";
    summary = midSummaryArray
    dis_summary = summary;
    setSummary(midSummaryArray)
}

function min_summary(){
    document.getElementById("cap_text").innerHTML = "Template-based Summary:"
    document.getElementById('summary').innerHTML = "";
    summary = minSummaryArray
    dis_summary = summary;
    setSummary(minSummaryArray)
}

function set_partial_summary(){
    // var radio = document.getElementById("summary_type");
    // radio.checked = false;
    // var radio2 = document.getElementById("summary_type_c2t");
    // radio2.checked = false;

    if (document.getElementById("slider_table") != null){
        elem = document.getElementById("slider_table");
        temp = elem;
        elem_parent = elem.parentNode;
    }

    document.getElementById("cap_text").innerHTML = "Summary based on selected data points:"
    document.getElementById('summary').innerHTML = "";
    summary = partial_summary;

    dis_summary = partial_summary[0].split(". ")
    dis_summary.pop(); // Deleting last unnecessary item

    console.log("partial_summary")
    console.log(partial_summary)
    console.log("summary")
    console.log(summary)


    setSummary(partial_summary)
    // setPartialSummary(partial_summary)

    if (document.getElementById("slider_table") != null){
        temp.remove();

    }
}


// Get data from JSON
function getMetaData() {
  //console.log("getMetaData called");
    var summaryRequestURL = summaryPath;
    var summaryRequest = new XMLHttpRequest();
    summaryRequest.open('GET', summaryRequestURL);
    summaryRequest.responseType = 'json';
    summaryRequest.send();
    summaryRequest.onload = function () {
        var jsonObj = summaryRequest.response;
        graphType = jsonObj.graphType;
        console.log(graphType)
        columnType = jsonObj.columnType;
        summaryType = jsonObj.summaryType;
      //console.log(summaryType)
        title = jsonObj.title;
      //console.log(title)
        if (columnType === "two" && graphType === "line") {
            yLabel = jsonObj.yAxis;
            xLabel = jsonObj.xAxis;
            data = jsonObj.data;
            numberOfColumn = data.length;
        }
        else if (columnType === "two" && graphType === "bar") {
            yLabel = jsonObj.yAxis;
            console.log(yLabel);
            xLabel = jsonObj.xAxis;
            data = jsonObj.data;
            numberOfColumn = data.length;
        }
        else if (columnType === "two" && graphType === "scatter") {
            yLabel = jsonObj.yAxis;
            console.log(yLabel);
            xLabel = jsonObj.xAxis;
            classLabel = jsonObj.class;
            data = jsonObj.data;
            numberOfColumn = data.length;
        }
        else if (columnType === "two" && graphType === "heatmap") {
            yLabel = jsonObj.yAxis;
            console.log(yLabel);
            xLabel = jsonObj.xAxis;
            valLabel = jsonObj.val;
            data = jsonObj.data;
            numberOfColumn = data.length;
            var myGroups = d3.map(data, function(d){return d[xLabel];}).keys()
            var myVars = d3.map(data, function(d){return d[yLabel];}).keys()
            multi_number_of_group = myGroups.length - 1;
            multi_number_of_elements_in_each_group = myVars.length;

        }
        else if (columnType === "multi") {
            // e.g. 11.json
            labelArr = jsonObj.labels;
            const length = jsonObj.data.length;
            data = jsonObj.data;
            yLabel = jsonObj.yAxis;
            console.log(yLabel);
            xLabel = labelArr[0];
            multi_number_of_group = labelArr.length - 1;
            multi_number_of_elements_in_each_group = data.length;

        }
        else if (columnType === "two" && graphType === "pie") { 
            labelName = jsonObj.name;
            percentage = jsonObj.percent;           
            data = jsonObj.data;
            numberOfColumn = data.length;
        }
        setTitle(title);
        summaryArray = jsonObj.summary;

        trendsArray = jsonObj.trends;  // DID NOT UNDERSTAND THE PURPOSE OF TRENDS

        maxSummaryArray = jsonObj.max_summary;
        midSummaryArray = jsonObj.mid_summary;
        minSummaryArray = jsonObj.min_summary;


        run(summaryArray, trendsArray, data);
    };
}

function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        /* next line works with strings and numbers,
         * and you may want to customize it to your needs
         */
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

// var toSort = false;
function sortTheBarChart(){
    data.sort(dynamicSort(yLabel));
    svg.remove();

    barGraph();


}


function run(summaryArray, trendsArray, chartData) {
    getCurrentChart();
    sumArrayLength = summaryArray.length;
    summary = summaryArray;
    dis_summary = summary;
    let idArray = []
    if (columnType === "two") {
        if (graphType === "line") {
            idArray = getLineIds(trendsArray);
            idArrays = idArray;
            lineGraph(chartData);
            setSummary(summaryArray);
            addLineListeners(idArray);
            } else if (graphType === "bar") {
                idArray = getBarIds(trendsArray);
                idArrays = idArray;
                barGraph();
                setSummary(summaryArray);
                addBarListeners(idArray);
            } else if (graphType === "pie") {
                //idArray = getBarIds(trendsArray);
                //idArrays = idArray;
                drawPieChart(chartData);
                setSummary(summaryArray);
                //addBarListeners(idArray);
            } else if (graphType === "scatter") {
            //idArray = getBarIds(trendsArray);
            //idArrays = idArray;
            drawScatterPlot(chartData);
            setSummary(summaryArray);
            //addBarListeners(idArray);
        } else if (graphType === "heatmap") {
            //idArray = getBarIds(trendsArray);
            //idArrays = idArray;
            drawHeatMap(chartData);
            setSummary(summaryArray);
            //addBarListeners(idArray);
        }
    }
    else if (columnType === "multi") {
        if (graphType === "line") {
            idArray = getMultiLineIds(trendsArray);
            idArrays = idArray;
            multiLineGraph();
            setSummary(summaryArray);
            addLineListeners(idArray);
        } else if (graphType === "bar") {
            if (summaryType === "baseline") {
            idArray  = getMultiLineIds(trendsArray);
            idArrays = idArray;
            multiBarGraph();
            setSummary(summaryArray);
            addLineListeners(idArray);
            }
            else {
                idArray = getMultiBarIds(trendsArray);
                idArrays = idArray;
                multiBarGraph();
                setSummary(summaryArray);
                addBarListeners(idArray);
            }
        }
    }
    document.getElementById('summary').childNodes.forEach(function(d) {
        for (let n = 0; n < d.childNodes.length; n++) {
            if (d.childNodes[n].innerText.includes('_')) {
                while (d.childNodes[n].innerText.includes('_')) {
                    d.childNodes[n].innerText = d.childNodes[n].innerText.replace('_',  ' ')
                }
            }
        }
    });

}

var count = 0;
var lineCount = 0;

function setId() {
    var id = ("Column" + count);
    d3.select(this).attr("id", id);
    xValue = d3.select(this).attr("xVal");
    yValue = d3.select(this).attr("yVal");
    var string = yLabel + " is " + yValue + " at " + xLabel + " " + xValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count = count + 1;
}

function pieSetId() {
    var id = ("Column" + count); 
    d3.select(this).attr("id", id); //gives a new id attribute to each arc/path --> the first one "Column0"
    nameValue = d3.select(this).attr("nameVal");
    percentValue = d3.select(this).attr("percentVal");
    var string = labelName + " is " + nameValue + " at " + percentage + " " + percentValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count = count + 1;
}

function scatterSetId() {
    var id = ("Column" + count); 
    d3.select(this).attr("id", id); //gives a new id attribute to each arc/path --> the first one "Column0"
    xValue = d3.select(this).attr("xVal");
    yValue = d3.select(this).attr("yVal");
    classValue = d3.select(this).attr("classVal");
    var string = yLabel + " is " + yValue + " at " + xLabel + " " + xValue + " belonging to " + classLabel + " "+ classValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count++;
}

function heatMapSetID() {
    // var id = d3.select(this).attr("id");

    var id = ("Column" + count);
    d3.select(this).attr("id", id); //gives a new id attribute to each arc/path --> the first one "Column0"

    cellValue = d3.select(this).attr("cellVal");
    xValue = d3.select(this).attr("xVal");
    yValue = d3.select(this).attr("yVal");
    var string = "Value of cell is " + cellValue + " at " + xLabel + " "+ xValue + " and " + yLabel + " " + yValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count++;
}

function mulitLineSetID() {
    const lineIndex = d3.select(this).attr("lineIndex");
    const dotIndex = d3.select(this).attr("dotIndex");
    const id = ("Column[" + lineIndex +  "][" + dotIndex + ']')
    d3.select(this).attr("id", id);
    lineValue = d3.select(this).attr("lineVal");
    xValue = d3.select(this).attr("xVal");
    yValue = d3.select(this).attr("yVal");
    var string = lineValue + " is " + yValue + " at " + xLabel + " " + xValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count++;
}

function mulitBarSetID() {
    if (count === Object.keys(data[0]).length - 1) {
        count = 0;
        lineCount++;
    }
    const id = ("Column[" + lineCount +  "][" + count + ']')
    console.log("THIS IS -> "+ this)
    d3.select(this).attr("id", id);
    barValue = d3.select(this).attr("barVal");
    xValue = d3.select(this).attr("xVal");
    yValue = d3.select(this).attr("yVal");
    var string = barValue + " is " + yValue + " at " + xLabel + " " + xValue;
    document.getElementById(id).addEventListener("mouseover", function () {
        textChange(string);
    });
    count++;
}

function setTitle(title) {
    document.getElementById('title').innerText = title;
}

function setSummary(summaryArray) {
  console.log("setSummary method was called");
  //console.log(summaryArray);
    for (let i = 0; i < summaryArray.length; i++) {
        var anchor = document.createElement("A");
        let id = "A" + i
        anchor.setAttribute("id", id);
        tokens = summaryArray[i].split(" ")
        for (let n = 0; n < tokens.length; n++) {
            let tokenAnchor = document.createElement("A");
            let subId = 'Token' + n;
            tokenAnchor.setAttribute("id", subId);
            tokenAnchor.innerHTML = tokens[n] + ' ';
            anchor.appendChild(tokenAnchor);
        }
        document.getElementById('summary').appendChild(anchor);

    }
}

function setPartialSummary(summaryArray) {

    for (let i = 0; i < summaryArray.length; i++) {
        var anchor = document.createElement("A");
        let id = "A" + i
        anchor.setAttribute("id", id);
        tokens = summaryArray[i].split("")
        for (let n = 0; n < tokens.length; n++) {
            let tokenAnchor = document.createElement("A");
            let subId = 'Token' + n;
            tokenAnchor.setAttribute("id", subId);
            tokenAnchor.innerHTML = tokens[n] + ' ';
            anchor.appendChild(tokenAnchor);
        }
        document.getElementById('summary').appendChild(anchor);
    }
}

function setChartListeners(graphIds, trendAnchor) {
  //console.log("setChartListeners was called");
  //console.log(graphIds);
  //console.log(trendAnchor);
  //console.log("graphIds.toString().length" + graphIds.toString().length);
    if (graphIds.toString().length < 13) {
      //console.log("HAHA");
      //console.log(graphIds);
        let dot = document.getElementById(graphIds);
        let graphFill = dot.getAttribute('fill');
        dot.addEventListener("mouseover", function () {
            trendAnchor.style.backgroundColor = '#d9f6ff';
            dot.style.fill = shadeColor(graphFill, -10);
        });
        dot.addEventListener("mouseout", function () {
            trendAnchor.style.backgroundColor = 'transparent';
            dot.style.fill = graphFill;
        });
    }
    else {
      //console.log("HOHO");

        for (let i=0;i<graphIds.length;i++) {
            let dot = document.getElementById(graphIds[i]);
          //console.log("DOT -> "+dot);
          //console.log(graphIds[i]);
            dot.addEventListener("mouseover", function () {
                trendAnchor.style.backgroundColor = '#d9f6ff';
                for (graphId of graphIds) {
                    let graph = document.getElementById(graphId);
                    let graphFill = graph.getAttribute('fill')
                    graph.style.fill = shadeColor(graphFill, -50);// = '#cf6830';
                }
            });
            dot.addEventListener("mouseout", function () {
                trendAnchor.style.backgroundColor = 'transparent';
                for (graphId of graphIds) {
                    let graph = document.getElementById(graphId);
                    let graphFill = graph.getAttribute('fill')
                    graph.style.fill = graphFill;// = '#cf6830';
                }
            });
        }
    }
}

function addLineListeners(idArray) {
  //console.log("addLineListeners was called");
  //console.log("idArray -> " + idArray[0]);
  //console.log("idArray -> " + idArray[1]);

    let sentences = idArray[1];
  //console.log("sentences -> "+ sentences);
    for (let i=0; i < sentences.length; i++) {
        let trends = sentences[i];
      //console.log("trends -> "+trends)
        let sentenceId = 'A'+i;
        let sentence = document.getElementById(sentenceId);
        for (let n=0; n < trends.length; n++) {
            trendArr = [];
            let trend = trends[n]
          //console.log(trend)
          //console.log(trend.toString())
            //edge case where accessing a trend of length 1 will iterate through each character
            //one trend converted to string is 7/8 characters
            if (trend.toString().length < 9 && trend.toString().length > 0) {
              //console.log("Edge case occurred")
                let tokenId = trend
              //console.log(tokenId)
                let tokenEl = sentence.querySelector('#' + tokenId);
                let token = tokenEl.innerHTML;
                let trendAnchor = document.createElement("A");
                let id = "T" + n
                trendAnchor.setAttribute("id", id);
                trendAnchor.setAttribute("class", "outline");
                trendAnchor.innerHTML = token + ' ';
              //console.log(idArray[0][i][n].toString().length)
                //edge case where accessing a graphID of length 1 will iterate through each character
                //one graphID converted to string is 13 characters
                if (idArray[0][i][n].toString().length < 13) {
                    trendAnchor.addEventListener("mouseover", function () {
                        trendAnchor.style.backgroundColor = '#d9f6ff';
                        const id = idArray[0][i][n]
                      //console.log(id)
                        let graph = document.getElementById(id);
                        let graphFill = graph.getAttribute('fill')
                        graph.style.fill = shadeColor(graphFill, -50);
                    });
                    trendAnchor.addEventListener("mouseout", function () {
                        trendAnchor.style.backgroundColor = 'transparent';
                        const id = idArray[0][i][n]
                      //console.log(id)
                        let graph = document.getElementById(id);
                        let graphFill = graph.getAttribute('fill')
                        graph.style.fill = graphFill;
                    });
                }
                else {
                    trendAnchor.addEventListener("mouseover", function () {
                        trendAnchor.style.backgroundColor = '#d9f6ff';
                        for (graphId of idArray[0][i][n]) {
                            const id = graphId
                            let graph = document.getElementById(id);
                            let graphFill = graph.getAttribute('fill')
                            graph.style.fill = shadeColor(graphFill, -50);// = '#cf6830';
                        }
                    });
                    trendAnchor.addEventListener("mouseout", function () {
                        trendAnchor.style.backgroundColor = 'transparent';
                        for (graphId of idArray[0][i][n]) {
                            const id = graphId
                            let graph = document.getElementById(id);
                            let graphFill = graph.getAttribute('fill')
                            graph.style.fill = graphFill;// = '#cf6830';
                        }
                    });
                }
                sentence.replaceChild(trendAnchor, sentence.querySelector('#' + tokenId));
                //if (columnType === 'two') {
                setChartListeners(idArray[0][i][n], trendAnchor);
                //}
            }
            else {
                // Add listeners to line chart dots
                for (let m = 0; m < trend.length; m++) {
                    let tokenId = trend[m];
                  //console.log(tokenId)
                  //console.log(trend)
                    let tokenEl = sentence.querySelector('#' + tokenId);
                    let token = tokenEl.innerHTML;
                    trendArr.push(token)
                    if (m === trend.length - 1) {
                        let trendAnchor = document.createElement("A");
                        let id = "T" + n
                        trendAnchor.setAttribute("id", id);
                        trendAnchor.setAttribute("class", "outline");
                        trendAnchor.innerHTML = trendArr.join(' ') + ' ';
                        trendAnchor.addEventListener("mouseover", function () {
                            trendAnchor.style.backgroundColor = '#d9f6ff';
                            for (graphId of idArray[0][i][n]) {
                              //console.log("Graph ID -> " +graphId)
                                let graph = document.getElementById(graphId);
                                let graphFill = graph.getAttribute('fill')
                                graph.style.fill = shadeColor(graphFill, -50);// = '#cf6830';
                            }
                        });
                        trendAnchor.addEventListener("mouseout", function () {
                            trendAnchor.style.backgroundColor = 'transparent';
                            for (graphId of idArray[0][i][n]) {
                                let graph = document.getElementById(graphId);
                                let graphFill = graph.getAttribute('fill')
                                graph.style.fill = graphFill;// = '#cf6830';
                            }
                        });
                        sentence.replaceChild(trendAnchor, sentence.querySelector('#' + tokenId));
                    } else {
                        sentence.removeChild(sentence.querySelector('#' + tokenId));
                    }
                }
                trendAnchorId = "T" + n;
                let trendAnchor = sentence.querySelector('#' + trendAnchorId)
              //console.log("trendAnchor -> "+trendAnchor)
              //console.log("idArray[0][i][n] -> "+idArray[0][i][n])

                //if (columnType === 'two') {
                setChartListeners(idArray[0][i][n], trendAnchor);
                //}
            }
        }
    }
}

function addBarListeners(idArray) {
    let sentences = idArray[1];
    for (let i=0; i < sentences.length; i++) {
        let trends = sentences[i];
        let sentenceId = 'A'+i;
        let sentence = document.getElementById(sentenceId);
        if (trends.length === 1) {
            //edge case where accessing a trend of length 1 will iterate through each character
            //one trend converted to string is 7 characters
            if (trends.toString().length < 8) {
                let tokenId = trends[0]
                let tokenEl = sentence.querySelector('#' + tokenId);
                let token = tokenEl.innerHTML;
                let trendAnchor = document.createElement("A");
                let id = "T0"
                trendAnchor.setAttribute("id", id);
                trendAnchor.setAttribute("class", "outline");
                trendAnchor.innerHTML = token + ' ';
                const graphId = idArray[0][i][0]
              //console.log(graphId)
                trendAnchor.addEventListener("mouseover", function () {
                    trendAnchor.style.backgroundColor = '#d9f6ff';
                    let graph = document.getElementById(graphId);
                    let graphFill = graph.getAttribute('fill')
                    graph.style.fill = shadeColor(graphFill, -50);// = '#cf6830';
                });
                trendAnchor.addEventListener("mouseout", function () {
                    trendAnchor.style.backgroundColor = 'transparent';
                    let graph = document.getElementById(graphId);
                    let graphFill = graph.getAttribute('fill')
                    graph.style.fill = graphFill;// = '#cf6830';
                });
                sentence.replaceChild(trendAnchor, sentence.querySelector('#' + tokenId));
                setChartListeners(graphId, trendAnchor);
            }
        }
        else if (trends.length > 1) {
            for (let n = 0; n < trends.length; n++) {
                trendArr = [];
                let trend = trends[n]
                // Add listeners to bars
                let tokenId = trend;
                let tokenEl = sentence.querySelector('#' + tokenId);
                //check if token actually exists. some backend code may have bug which gives incorrect token index
                if (tokenEl !== null) {
                    let token = tokenEl.innerHTML;
                    trendArr.push(token)
                    let trendAnchor = document.createElement("A");
                    let id = "T" + n
                    trendAnchor.setAttribute("id", id);
                    trendAnchor.setAttribute("class", "outline");
                    trendAnchor.innerHTML = trendArr.join(' ') + ' ';
                    const graphId = idArray[0][i][n]
                  //console.log(graphId)
                    trendAnchor.addEventListener("mouseover", function () {
                        trendAnchor.style.backgroundColor = '#d9f6ff';
                        let graph = document.getElementById(graphId);
                        let graphFill = graph.getAttribute('fill')
                        graph.style.fill = shadeColor(graphFill, -50);// = '#cf6830';
                    });
                    trendAnchor.addEventListener("mouseout", function () {
                        trendAnchor.style.backgroundColor = 'transparent';
                        let graph = document.getElementById(graphId);
                        let graphFill = graph.getAttribute('fill')
                        graph.style.fill = graphFill;// = '#cf6830';
                    });
                    sentence.replaceChild(trendAnchor, sentence.querySelector('#' + tokenId));
                    setChartListeners(graphId, trendAnchor);
                }
            }
        }
    }
}

function speakCompleteSentence(text){
    document.getElementById("audioPlayback").addEventListener("ended", function (){
        speakText(text);
        this.removeEventListener("ended", arguments.callee)
    });
}

function textChange(text) {
    document.getElementById("summaryText").innerText = text;
    speakText(text);
}

var help_text = []

function help(){

    help_text.push("Press Enter, to hear the general description of the chart. ")
    help_text.push("Press X, to hear the X axis label of the chart. ")
    help_text.push("Press Y, to hear the Y axis label of the chart. ")
    help_text.push("Press Space, to hear the summary of the chart. ")
    help_text.push("Press J, or L, to hear the summary line by line. ")
    help_text.push("Press K, to hear the same line of the summary you just heard. ")
    help_text.push("Press Left, or right arrow, to navigate through the bars or points of the chart. ")
    help_text.push("Press Shift, + right arrow, to select multiple data points and hear a summary based on the selected points. ")
    help_text.push("Press S, to hear the selected points. ")
    help_text.push("Press Escape, to reset the selected points. ")
    help_text.push("Press 1, 2, or 3 to switch summary length. ")
    help_text.push("Press Control, to cancel ongoing narration. ")
    help_text.push("Press T, to toggle speech rate from slowest to fastest. ")
    help_text.push("Press R to reload the chart.  ")
    help_text.push("Press H to active help mode.  ")

    var text = "";

    for (var i = 0; i < help_text.length; i++){
        text += help_text[i];
    }


    // var text = "Press Enter, to hear the general description of the chart. " +
    //     "Press X, to hear the X axis label of the chart. " +
    //     "Press Y, to hear the Y axis label of the chart. " +
    //     "Press Space, to hear the summary of the chart. " +
    //     "Press Left or right arrow, to navigate through the bars or points of the chart. " +
    //     "Press Up or Down arrow, to switch between lines in multiline chart. " +
    //     "Press Control, + right arrow, to select multiple data points and hear a summary based on the selected points. " +
    //     // "Press Shift plus left, or right arrow, to move to next or previous chart. " +
    //     "Press 1, to get the Short length summary. " +
    //     "Press 2, to get the Default length summary. " +
    //     "Press 3, to get the Maximum length summary. " +
    //     "Press H, to hear the keyboard shortcuts. " +
    //     "And, you may press Escape to cancel or redo any operation. "
    var tab = "<h2>Keyboard Shortcuts: </h2><table border='1' bgcolor='#f5f5dc'> <tr><th>Key/s</th> <th>Action</th></tr>" +
        "<tr><td> ENTER </td><td> To hear the general description of the chart. </td></tr>" +
        "<tr><td> X </td><td> To hear the X axis label. </td></tr>" +
        "<tr><td> Y </td><td> To hear the Y axis label. </td></tr>" +
        "<tr><td> SPACE </td><td> To hear the chart summary.</td></tr>" +
        "<tr><td> J, K, L </td><td> To hear the chart summary line-by-line.</td></tr>" +
        "<tr><td> Left or Right Arrow </td><td> To navigate through the bars or points of the chart.</td></tr>" +
        "<tr><td> Up or Down Arrow </td><td> To switch between categories in multi-line or multi-bar chart.</td></tr>" +
        "<tr><td> Shift + Right Arrow </td><td> To select bars or points to hear partial summary based on the selected points.</td></tr>" +
        // "<tr><td> Press Shift+Right/Left arrow </td><td> To move to next or previous chart.</td></tr>" +
        "<tr><td> S </td><td> To hear the list of selected points. </td></tr>" +
        "<tr><td> Escape </td><td> To reset the selected points. </td></tr>" +
        "<tr><td> 1,2, or 3 </td><td> To change summary length. </td></tr>" +
        "<tr><td> T </td><td> To toggle voice rate. </td></tr>" +
        "<tr><td> H </td><td> To hear the keyboard shortcuts. </td></tr> </table>"
    tempAlert(tab, 180000)

    speakText("Help list is presented. Press J, K, L to hear line by line. Press ESCAPE to exit Help.")
    // speakText("To hear the available keyboard shortcuts one by one, keep pressing G button. And, Press F, to re-hear.")
}

function xAxisLabelNameByColumnId(col_id){

    // var string = "";
    // if (point === "first"){
    //     string += "You're at the beginning of the graph. "
    // }
    // else if (point === "last"){
    //     string += "This is the last point of the graph. "
    // }
    var attr = document.getElementById(col_id).attributes
    // string += yLabel + " is " + attr.getNamedItem('yVal').value + " at " + xLabel + " " + attr.getNamedItem('xVal').value;
    string = xLabel + " " + attr.getNamedItem('xVal').value + " is selected. ";
    console.log(string)
    textChange(string);
}


function d3PointDescriptionById(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    // string += yLabel + " is " + attr.getNamedItem('yVal').value + " at " + xLabel + " " + attr.getNamedItem('xVal').value;
    string += "In " + xLabel + " " + attr.getNamedItem('xVal').value + ", the " + yLabel + " was, " + attr.getNamedItem('yVal').value;
    console.log(string)
    textChange(string);
}

function tempAlert(msg,duration)
{
    var el = document.createElement("div");
    el.setAttribute("id", "temp_alert");
    el.setAttribute("style","position:absolute;top:70%;left:20%;background-color:white;");
    el.innerHTML = msg;

    document.addEventListener('keyup', function(event) {
        if (event.code === 'Escape' ) {
            el.parentNode.removeChild(el);
            duration = 0;
            speakText("Exiting help mode.")
        }
    });

    setTimeout(function(){
        el.parentNode.removeChild(el);
        speakText("Exiting help mode.")
    },duration);
    document.body.appendChild(el);
}

function d3PointDescriptionForMultiGraphById(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    // string += "Value of "+attr.getNamedItem('lineVal').value + " is " + yValue + ", at " + xLabel + " " + xValue;

    string += "In " + xLabel + " " + xValue + ", the " + yLabel + " for " +attr.getNamedItem('lineVal').value + " was, " + yValue + ". "

    console.log(string)
    textChange(string);
}

function d3PointDescriptionForMultiBarById(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    // var string = barValue + " is " + yValue + " at " + xLabel + " " + xValue;
    // string += attr.getNamedItem('barVal').value + " is " + attr.getNamedItem('yVal').value + ", at " + attr.getNamedItem('xLabel').value + " " + attr.getNamedItem('xVal').value;

    string += "At " + attr.getNamedItem('xLabel').value + " " + attr.getNamedItem('xVal').value + ", the " + yLabel +" for " + attr.getNamedItem('barVal').value +  " was, " + attr.getNamedItem('yVal').value + ". ";

    // string += "For " + attr.getNamedItem('barVal').value + ", the " + yLabel + " was, " + attr.getNamedItem('yVal').value + ", at " + attr.getNamedItem('xLabel').value + " " + attr.getNamedItem('xVal').value;

    console.log(string)
    textChange(string);

}


function d3PointDescriptionForPieChartById(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    // var string = barValue + " is " + yValue + " at " + xLabel + " " + xValue;
    string += attr.getNamedItem('nameVal').value + " is " + attr.getNamedItem('percentVal').value + " percent";

    console.log(string)
    textChange(string);

}

function d3PointDescriptionForHeatMapById(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    string += "Value of cell is " + attr.getNamedItem('cellVal').value + " at " + xLabel + " "+ attr.getNamedItem('xVal').value + " and " + yLabel + " " + attr.getNamedItem('yVal').value;

    console.log(string)
    textChange(string);

}



function d3PointDescriptionByIdForScatterPlot(col_id, point){
    var string = "";
    if (point === "first"){
        string += "You're at the beginning of the graph. "
    }
    else if (point === "last"){
        string += "This is the last point of the graph. "
    }
    var attr = document.getElementById(col_id).attributes
    string += "This cereal has "  + attr.getNamedItem('yVal').value + " "+ yLabel + ", and "  + attr.getNamedItem('xVal').value + " " + xLabel + ", belonging to " + classLabel + " "+ attr.getNamedItem('classVal').value;
    console.log(string)
    textChange(string);
}


function chartTypeDescriber(){

    if (columnType === "multi"){
        var text = "This is a "+columnType+ " " +graphType+" chart. That represents "+title+". ";
        speakText(text);
    }
    else {
        var text = "This is a " +graphType+" chart. That represents "+title+". ";
        speakText(text);
    }

    // speakCompleteSentence(text);

}


function narrateSummary() {
    //executes on press of narrate summary button
    let tokens = idArrays[1];
  //console.log(tokens)
    var audioPlayer = document.getElementById("audioPlayback");
    let i = 0
    // sentence 1
    speakText(summary[0]);
    let sentence = document.getElementById('A0');
    sentence.style.backgroundColor = '#d9f6ff';
    i++;
    // next sentences. use onended handler so entire audio finishes before moving to next sentence
    audioPlayer.onended = function() {
        let priorSentence = document.getElementById('A'+(i-1));
        priorSentence.style.backgroundColor = 'transparent';
        if (i < summary.length) {
            const text = summary[i];
            speakText(text);
            let sentence = document.getElementById('A'+i);
            sentence.style.backgroundColor = '#d9f6ff';
            i++;
        }
    };
    audioPlayer.removeEventListener("ended", this);
}

function isAlphaNumeric(str) {
    var code, i, len;

    for (i = 0, len = str.length; i < len; i++) {
        code = str.charCodeAt(i);
        if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123)) { // lower alpha (a-z)
            return false;
        }
    }
    return true;
};

function isNumeric(str) {
    var code, i, len;

    for (i = 0, len = str.length; i < len; i++) {
        code = str.charCodeAt(i);
        if (!(code > 47 && code < 58)) {  // 1-10
            return false;
        }
    }
    return true;
}

function getLineIds(trendsArray) {
  //console.log("getLineIds method called")
    let graphArray = [];
    let tokenArray = [];
    //iterate sentences
    for (n = 0; n < trendsArray.length; n++) {
        // console.log("trendsArray[n] ->" + trendsArray[n])
        let keys = Object.keys(trendsArray[n])
        //fix bug where first trend misses 1st token
      //console.log("KEYS -> " + keys)
        if (keys.length > 0) {
            keys[0] = (keys[0] - 1).toString()
          //console.log("keys[0] -> " +keys[0])
        }
        const values = Object.values(trendsArray[n])
      //console.log(keys)
        let sentenceGraphIds = []
        let sentenceTokenIds = []
        //iterate through trends and generate ranges
        if (keys.length > 1) {
            for (let i = 0; i < keys.length - 1; i++) {
                trendTokenRanges = []
                trendGraphRanges = []
              //console.log(keys[i], keys[i + 1])
                tokenRangeStart = Math.min(keys[i], keys[i + 1])
                tokenRangeEnd = Math.max(keys[i], keys[i + 1])
              //console.log("tokenRangeStart -> " + tokenRangeStart+i);
              //console.log("tokenRangeEnd -> " + tokenRangeEnd);
                // console.log(keys[i], keys[i + 1])
                // BUG HERE
                for (let n = tokenRangeStart+i; n <= tokenRangeEnd; n++) {
                    const id = "Token" + n;
                  //console.log(id);
                    trendTokenRanges.push(id);
                }
                graphRangeStart = Math.min(values[i], values[i + 1]);
                graphRangeEnd = Math.max(values[i], values[i + 1]);


              //console.log("graphRangeStart -> " + graphRangeStart);
              //console.log("graphRangeEnd -> " + graphRangeEnd);

                for (let i = graphRangeStart; i <= graphRangeEnd; i++) {
                    const id = "Column" + i;
                  //console.log(id);
                    trendGraphRanges.push(id);
                }
                sentenceGraphIds.push(trendGraphRanges);
                sentenceTokenIds.push(trendTokenRanges);
            }
        }
        else if (keys.length === 1){
            sentenceGraphIds.push("Column" + values);
            sentenceTokenIds.push("Token" + keys);
        }
        graphArray.push(sentenceGraphIds);
        tokenArray.push(sentenceTokenIds);
    }
  //console.log("graphArray -> " + graphArray);
  //console.log("tokenArray -> " + tokenArray);

    let idArray = [graphArray, tokenArray];
    return idArray;
}

function getBarIds(trendsArray) {
  //console.log("getBarIds was called")
    let graphArray = [];
    let tokenArray = [];
    //iterate sentences
    for (n = 0; n < trendsArray.length; n++) {
        const keys = Object.keys(trendsArray[n])
        const values = Object.values(trendsArray[n])
        let sentenceGraphIds = []
        let sentenceTokenIds = []
        //iterate through trends and generate ranges
        for (let i = 0; i < keys.length; i++) {
            const newCol = "Column" + values[i];
            const newTok = "Token" + keys[i];
            sentenceGraphIds.push(newCol);
            sentenceTokenIds.push(newTok);
        }
        graphArray.push(sentenceGraphIds);
        tokenArray.push(sentenceTokenIds);
    }
  //console.log("graphArray -> "+graphArray);
  //console.log("tokenArray -> "+tokenArray);
    let idArray = [graphArray, tokenArray];
    return idArray;
}

function getMultiLineIds(trendsArray) {
    let graphArray = [];
    let tokenArray = [];
    //iterate sentences
    for (n = 0; n < trendsArray.length; n++) {
        let keys = Object.keys(trendsArray[n])
        //fix bug where first trend misses 1st token
        if (keys.length > 0) {
            if (keys[0] > 1)
                keys[0] = (keys[0] - 1).toString()
        }
        const values = Object.values(trendsArray[n])
        let sentenceGraphIds = []
        let sentenceTokenIds = []
        //iterate through trends and generate ranges
        if (keys.length > 1) {
            for (let i = 0; i < keys.length - 1; i++) {
                trendTokenRanges = []
                trendGraphRanges = []
                tokenRangeStart = Math.min(keys[i], keys[i + 1])
                tokenRangeEnd = Math.max(keys[i], keys[i + 1])
                for (let n = tokenRangeStart+i; n <= tokenRangeEnd; n++) {
                    const id = "Token" + n;
                    trendTokenRanges.push(id);
                }
                const lineDelta = Math.abs(values[0][1] - values[values.length-1][1])
              //console.log(lineDelta)
                /*//if index is 0 it means it refers to the x axis rather than a specific line,
                //therefore we highlight each line in this range
              //console.log(values)
                if (values[i][1] === '0' && values.length < 3) {
                  //console.log(values)
                    for (let n = 0; n < labelArr.length - 1; n++) {
                        graphRangeStart = Math.min(values[i][0], values[i + 1][0]);
                        graphRangeEnd = Math.max(values[i][0], values[i + 1][0]);
                        for (let i = graphRangeStart; i <= graphRangeEnd; i++) {
                            const id = "Column[" + n + "][" + i + "]";
                            trendGraphRanges.push(id);
                        }
                    }
                }*/
                //if trend n and trend n+1 refer to different lines, run this code which highlights templates 1 at a time
                if (lineDelta !== 0) {
                  //console.log('here2')
                  //console.log(values)
                    const index = values[i][1]
                    const id = "Column[" + index + "][" + values[i][0] + "]";
                    trendGraphRanges.push(id);
                }
                else {
                  //console.log(values)
                    graphRangeStart = Math.min(values[i][0], values[i + 1][0]);
                    graphRangeEnd = Math.max(values[i][0], values[i + 1][0]);
                    const index = values[i][1];
                    for (let i = graphRangeStart; i <= graphRangeEnd; i++) {
                        const id = "Column[" + index + "][" + i + "]";
                        trendGraphRanges.push(id);
                    }
                }
                sentenceGraphIds.push(trendGraphRanges);
                sentenceTokenIds.push(trendTokenRanges);
            }
        }
        else if (keys.length === 1){
          //console.log(values)
          //console.log(keys)
            sentenceGraphIds.push("Column[" + values[0][1] + "][" + values[0][0] + "]");
            sentenceTokenIds.push("Token" + keys);
        }
        graphArray.push(sentenceGraphIds);
        tokenArray.push(sentenceTokenIds);
    }
  //console.log(graphArray);
  //console.log(tokenArray);
    let idArray = [graphArray, tokenArray];
    return idArray;
}

function getMultiBarIds(trendsArray) {
    let graphArray = [];
    let tokenArray = [];
    //iterate sentences
    for (n = 0; n < trendsArray.length; n++) {
        const keys = Object.keys(trendsArray[n])
        const values = Object.values(trendsArray[n])
      //console.log(keys)
      //console.log(values)
        let sentenceGraphIds = []
        let sentenceTokenIds = []
        //iterate through trends and generate ranges
        for (let i = 0; i < keys.length; i++) {
          //console.log(values[i])
            const colNumber = values[i][0]
            let indexNumber = 0
            if (values[i][1] > 1) {
                indexNumber = values[i][1] - 1
            }
            else {
                indexNumber = values[i][1]
            }
            const newCol = "Column[" + colNumber + "][" + indexNumber + "]";
            const newTok = "Token" + keys[i];
            sentenceGraphIds.push(newCol);
            sentenceTokenIds.push(newTok);
        }
        graphArray.push(sentenceGraphIds);
        tokenArray.push(sentenceTokenIds);
    }
  //console.log(graphArray);
  //console.log(tokenArray);
    let idArray = [graphArray, tokenArray];
    return idArray;
}
