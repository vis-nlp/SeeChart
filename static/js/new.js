var svgFound = "";

// doesSVGexist();


function doesSVGexist() {
    console.log("doesSVGexist called")
    var elementExists = document.getElementsByName('svg');
    if (elementExists !== null) {
        svgFound = true;
    }
}

function test(svg_node) {
    console.log('I AM HERE');
    // var svgNodes = $('svg');
    var svgNodes = svg_node;
    // console.log('svgnodes'+svgNodes.length);
    console.log(svgNodes);


    svgNodes.each(function (i, svgNode) {
        console.log("Haha")

    });

}


var col1Id;
var col2Id;


// This method splits number/s from text and returns the numeric portion only
function splitNumberFromText(inputText) {
    var number = inputText.match(/\d+/g).map(Number);
    console.log(number);
    col1Id = number[0];
    col2Id = number[1];
    console.log(col1Id + " , " + col2Id)

}

// This method splits number/s from text and returns the text potion only
function deleteNumberFromText(inputText) {
    var letr = inputText.match(/[a-zA-Z]+/g);
    return letr[0];

}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

// delay(1000).then(() => console.log('ran after 1 second1 passed'));

function runSpeechRecognition() {
    document.getElementById("mic_on").play();

    // get output div reference
    var output = document.getElementById("output");
    output.innerHTML = "";
    // get action element reference
    var action = document.getElementById("action");
    var sf = document.getElementById("search_input");
    // new speech recognition object
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
    var recognition = new SpeechRecognition();

    // This runs when the speech recognition service starts
    recognition.onstart = function () {
        sf.setAttribute('value', "");
        action.innerHTML = "<small>Listening, please speak...</small>";
    };

    recognition.onspeechend = function () {
        // action.innerHTML = "<small>Stopped listening.</small>";
        action.innerHTML = "";
        document.getElementById("mic_off").play();

        recognition.stop();
    }

    // This runs when the speech recognition service returns result
    recognition.onresult = function (event) {
        console.log(event)
        var transcript = event.results[0][0].transcript;
        var confidence = event.results[0][0].confidence;
        // output.innerHTML = "<small><i>Detected Question:</i> <strong>" + transcript + "</strong> </small>";
        sf.setAttribute('value', transcript);
        // output.classList.remove("hide");

        if (countWords(transcript) < 3) {
            document.getElementById("search_result").innerHTML = "Please provide more information.";

            speakText("Please provide more information.")
        } else if (countWords(transcript) > 2) {
            var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
            var theUrl = "https://127.0.0.1:8080/qna";
            xmlhttp.open("POST", theUrl);

            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send(JSON.stringify({
                "chart": "" + document.getElementById('chartNumber').value + "",
                "question": "" + transcript + "",
            }));

            xmlhttp.onloadend = function () {

                if (xmlhttp.status === 200) {
                    // document.getElementById("search_input").value = "";
                    const myObj = JSON.parse(xmlhttp.response);
                    console.log(myObj.summary)

                    // document.getElementById("search_result").innerHTML = myObj.summary;
                    //
                    // speakText(myObj.summary)

                    delay(500).then(() => sayResult(myObj.summary));
                }
            };
        } else {
            speakText("Sorry! Could not hear properly! ");
        }
    };

    // start recognition
    recognition.start();
}

function sayResult(output) {
    document.getElementById("search_result").innerHTML = output;

    speakText(output)
}


function moveRight() {
    if (graphType === "bar") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();
                d3PointDescriptionById('Column0', 'first')

            } else {
                col1Id++;
                if (col1Id === numberOfColumn) {
                    col1Id = 0;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'first')

                } else if (col1Id === (numberOfColumn - 1)) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'last')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus)
                }

            }
        } else if (columnType === "multi") {
            if (col1Id == null) {
                col1Id = 0;
                col2Id = 0;
                var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                console.log(eid)
                document.getElementById(eid).focus();
                d3PointDescriptionForMultiBarById(eid, 'first')


            } else {
                if (col2Id < multi_number_of_elements_in_each_group && col1Id < (multi_number_of_group - 1)) {
                    col1Id++;
                    var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiBarById(eid)
                } else if (col1Id === (multi_number_of_group - 1) && col2Id < multi_number_of_elements_in_each_group) {
                    col2Id++;
                    col1Id = 0;
                    if (col2Id === multi_number_of_elements_in_each_group) {
                        col2Id = 0;
                        col1Id = 0;
                        var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                        console.log(eid)
                        document.getElementById(eid).focus();
                        d3PointDescriptionForMultiBarById(eid, 'first')
                    } else {
                        var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                        console.log(eid)
                        document.getElementById(eid).focus();
                        d3PointDescriptionForMultiBarById(eid)
                    }
                }
            }

        }
    } else if (graphType === "line") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = numberOfColumn - 1;
                document.getElementById('Column' + col1Id).focus();
                d3PointDescriptionById('Column' + col1Id, 'first')

            } else {
                col1Id--;
                if (col1Id < 0) {
                    col1Id = numberOfColumn - 1;

                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'first')
                } else if (col1Id === 0) {
                    col1Id = 0;

                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'last')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus)
                }

            }
        } else if (columnType === "multi") {
            // work needs to be done here
            if (col1Id == null) {
                col1Id = multi_number_of_group - 1;
                col2Id = multi_number_of_elements_in_each_group - 1;
                var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                console.log(eid)
                document.getElementById(eid).focus();
                d3PointDescriptionForMultiGraphById(eid, 'first')


            } else {
                if (col1Id <= (multi_number_of_group - 1) && col2Id > 0) {
                    col2Id--;
                    var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiGraphById(eid)
                } else if (col2Id === 0 && col1Id >= 0) {
                    col1Id--;
                    col2Id = multi_number_of_elements_in_each_group - 1;
                    if (col1Id < 0) {
                        col1Id = multi_number_of_group - 1;
                        col2Id = multi_number_of_elements_in_each_group - 1;
                        var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                        console.log(eid)
                        document.getElementById(eid).focus();
                        d3PointDescriptionForMultiGraphById(eid)
                    }
                    var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiGraphById(eid)
                }
            }
        }
    } else if (graphType === "pie") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();

                //arc_elem= document.getElementById('Column0');
                //arc_elem.style.stroke = "red";
                d3PointDescriptionForPieChartById('Column0', 'first') //in script.js

            } else {
                col1Id++;
                if (col1Id === numberOfColumn) {
                    col1Id = 0;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus()
                    d3PointDescriptionForPieChartById(newFocus, 'first')

                } else if (col1Id === (numberOfColumn - 1)) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForPieChartById(newFocus, 'last')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForPieChartById(newFocus)
                }

            }
        }

    } else if (graphType === "scatter") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();

                //arc_elem= document.getElementById('Column0');
                //arc_elem.style.stroke = "red";
                d3PointDescriptionByIdForScatterPlot('Column0', 'first') //in script.js

            } else {
                col1Id++;
                if (col1Id === numberOfColumn) {
                    col1Id = 0;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus()
                    d3PointDescriptionByIdForScatterPlot(newFocus, 'first')

                } else if (col1Id === (numberOfColumn - 1)) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionByIdForScatterPlot(newFocus, 'last')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionByIdForScatterPlot(newFocus)
                }

            }
        }

    }
        // else if (graphType === "heatmap"){
        //     if (col1Id == null){
        //         col1Id = 0;
        //         col2Id = 0;
        //         var eid = 'Column['+col1Id+']['+col2Id+']'
        //         console.log(eid)
        //         document.getElementById(eid).focus();
        //         d3PointDescriptionForHeatMapById(eid, 'last')
        //
        //
        //     }
        //     else {
        //         if (col1Id < multi_number_of_group && col2Id < (multi_number_of_elements_in_each_group - 1) ){
        //             col2Id++;
        //             var eid = 'Column['+col1Id+']['+col2Id+']'
        //             console.log(eid)
        //             document.getElementById(eid).focus();
        //             d3PointDescriptionForHeatMapById(eid)
        //         }
        //         else if (col2Id === (multi_number_of_elements_in_each_group - 1) && col1Id < multi_number_of_group){
        //             col1Id++;
        //             col2Id=0;
        //             if (col1Id === multi_number_of_group) {
        //                 col1Id = 0;
        //                 col2Id = 0;
        //                 var eid = 'Column['+col1Id+']['+col2Id+']'
        //                 console.log(eid)
        //                 document.getElementById(eid).focus();
        //                 d3PointDescriptionForHeatMapById(eid)
        //             }
        //             var eid = 'Column['+col1Id+']['+col2Id+']'
        //             console.log(eid)
        //             document.getElementById(eid).focus();
        //             d3PointDescriptionForHeatMapById(eid)
        //         }
        //     }
    // }
    else if (graphType === "heatmap") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();

                //arc_elem= document.getElementById('Column0');
                //arc_elem.style.stroke = "red";
                d3PointDescriptionForHeatMapById('Column0', 'first') //in script.js

            } else {
                col1Id++;
                if (col1Id === numberOfColumn) {
                    col1Id = 0;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus()
                    d3PointDescriptionForHeatMapById(newFocus, 'first')

                } else if (col1Id === (numberOfColumn - 1)) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForHeatMapById(newFocus, 'last')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForHeatMapById(newFocus)
                }

            }
        }

    }
}

function moveLeft() {
    if (graphType === "bar") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();
                d3PointDescriptionById('Column0', 'first')

            } else {
                col1Id--;
                if (col1Id < 0) {
                    col1Id = numberOfColumn - 1;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'last')
                } else if (col1Id === 0) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'first')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus)
                }
            }
        } else if (columnType === "multi") {
            // work needs to be done here
            if (col2Id == null) {
                col2Id = multi_number_of_elements_in_each_group - 1;
                col1Id = multi_number_of_group - 1;
                var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                console.log(eid)
                document.getElementById(eid).focus();
                d3PointDescriptionForMultiBarById(eid)


            } else {
                if (col2Id <= (multi_number_of_elements_in_each_group - 1) && col1Id > 0) {
                    col1Id--;


                    var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiBarById(eid)
                } else if (col1Id === 0 && col2Id >= 0) {
                    col2Id--;
                    col1Id = multi_number_of_group - 1;
                    if (col2Id < 0) {
                        col2Id = multi_number_of_elements_in_each_group - 1;
                        col1Id = multi_number_of_group - 1;
                        var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                        console.log(eid)
                        document.getElementById(eid).focus();
                        d3PointDescriptionForMultiBarById(eid)
                    }
                    var eid = 'Column[' + col2Id + '][' + col1Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiBarById(eid)
                }
            }

        }
    } else if (graphType === "line") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column' + col1Id).focus();
                d3PointDescriptionById('Column' + col1Id, 'last')

            } else {
                col1Id++;
                if (col1Id === numberOfColumn - 1) {
                    col1Id = numberOfColumn - 1;

                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionById(newFocus, 'first')
                } else {
                    if (col1Id === numberOfColumn) {
                        col1Id = 0;

                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionById(newFocus, 'last')
                    } else {
                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionById(newFocus)
                    }
                }


            }
        } else if (columnType === "multi") {
            if (col1Id == null) {
                col1Id = 0;
                col2Id = 0;
                var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                console.log(eid)
                document.getElementById(eid).focus();
                d3PointDescriptionForMultiGraphById(eid, 'last')


            } else {
                if (col1Id < multi_number_of_group && col2Id < (multi_number_of_elements_in_each_group - 1)) {
                    col2Id++;
                    var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiGraphById(eid)
                } else if (col2Id === (multi_number_of_elements_in_each_group - 1) && col1Id < multi_number_of_group) {
                    col1Id++;
                    col2Id = 0;
                    if (col1Id === multi_number_of_group) {
                        col1Id = 0;
                        col2Id = 0;
                        var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                        console.log(eid)
                        document.getElementById(eid).focus();
                        d3PointDescriptionForMultiGraphById(eid)
                    }
                    var eid = 'Column[' + col1Id + '][' + col2Id + ']'
                    console.log(eid)
                    document.getElementById(eid).focus();
                    d3PointDescriptionForMultiGraphById(eid)
                }
            }
        }
    } else if (graphType === "pie") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column' + col1Id).focus();
                d3PointDescriptionForPieChartById('Column' + col1Id, 'last')

            } else {
                col1Id++;
                if (col1Id === numberOfColumn - 1) {
                    col1Id = numberOfColumn - 1;

                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForPieChartById(newFocus, 'first')
                } else {
                    if (col1Id === numberOfColumn) {
                        col1Id = 0;

                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionForPieChartById(newFocus, 'last')
                    } else {
                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionForPieChartById(newFocus)
                    }
                }


            }
        }
    } else if (graphType === "scatter") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column' + col1Id).focus();
                d3PointDescriptionByIdForScatterPlot('Column' + col1Id, 'last')

            } else {
                col1Id++;
                if (col1Id === numberOfColumn - 1) {
                    col1Id = numberOfColumn - 1;

                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionByIdForScatterPlot(newFocus, 'first')
                } else {
                    if (col1Id === numberOfColumn) {
                        col1Id = 0;

                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionByIdForScatterPlot(newFocus, 'last')
                    } else {
                        var newFocus = 'Column' + col1Id
                        document.getElementById(newFocus).focus();
                        d3PointDescriptionByIdForScatterPlot(newFocus)
                    }
                }


            }
        }
    } else if (graphType === "heatmap") {
        if (columnType === "two") {
            if (col1Id == null) {
                col1Id = 0;
                document.getElementById('Column0').focus();
                d3PointDescriptionForHeatMapById('Column0', 'first')

            } else {
                col1Id--;
                if (col1Id < 0) {
                    col1Id = numberOfColumn - 1;
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForHeatMapById(newFocus, 'last')
                } else if (col1Id === 0) {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForHeatMapById(newFocus, 'first')
                } else {
                    var newFocus = 'Column' + col1Id
                    document.getElementById(newFocus).focus();
                    d3PointDescriptionForHeatMapById(newFocus)
                }
            }
        }
    }
}

function moveUpLine() {
    if (col1Id == null) {
        col1Id = 0;
        col2Id = 0;
        var eid = 'Column[' + col1Id + '][' + col2Id + ']'
        console.log(eid)
        document.getElementById(eid).focus();
        d3PointDescriptionForMultiGraphById(eid)
    } else {
        if (col1Id < multi_number_of_group - 1) {
            col1Id++;
            var eid = 'Column[' + col1Id + '][' + col2Id + ']'
            console.log(eid)
            document.getElementById(eid).focus();
            d3PointDescriptionForMultiGraphById(eid)
        } else {
            playBeep();
            // col1Id = 0;
            // var eid = 'Column[' + col1Id + '][' + col2Id + ']'
            // console.log(eid)
            // document.getElementById(eid).focus();
            // d3PointDescriptionForMultiGraphById(eid)
        }
    }
}

function moveDownLine() {
    if (col1Id == null) {
        col1Id = 0;
        col2Id = 0;
        var eid = 'Column[' + col1Id + '][' + col2Id + ']'
        console.log(eid)
        document.getElementById(eid).focus();
        d3PointDescriptionForMultiGraphById(eid)
    } else {
        if (col1Id > 0) {
            col1Id--;
            var eid = 'Column[' + col1Id + '][' + col2Id + ']'
            console.log(eid)
            document.getElementById(eid).focus();
            d3PointDescriptionForMultiGraphById(eid)
        } else {
            playBeep();

            // col1Id = multi_number_of_group - 1;
            // var eid = 'Column[' + col1Id + '][' + col2Id + ']'
            // console.log(eid)
            // document.getElementById(eid).focus();
            // d3PointDescriptionForMultiGraphById(eid)
        }
    }
}

function moveUpBar() {
    if (col1Id == null) {
        col1Id = 0;
        col2Id = 0;
        var eid = 'Column[' + col2Id + '][' + col1Id + ']'
        console.log(eid)
        document.getElementById(eid).focus();
        d3PointDescriptionForMultiBarById(eid)
    } else {
        if (col2Id < multi_number_of_elements_in_each_group - 1) {
            col2Id++;
            var eid = 'Column[' + col2Id + '][' + col1Id + ']'
            console.log(eid)
            document.getElementById(eid).focus();
            d3PointDescriptionForMultiBarById(eid)
        } else {
            playBeep();
            // col2Id = 0;
            // var eid = 'Column[' + col2Id + '][' + col1Id + ']'
            // console.log(eid)
            // document.getElementById(eid).focus();
            // d3PointDescriptionForMultiBarById(eid)
        }
    }
}

function moveDownBar() {
    if (col1Id == null) {
        col1Id = 0;
        col2Id = 0;
        var eid = 'Column[' + col2Id + '][' + col1Id + ']'
        console.log(eid)
        document.getElementById(eid).focus();
        d3PointDescriptionForMultiBarById(eid)
    } else {
        if (col2Id > 0) {
            col2Id--;
            var eid = 'Column[' + col2Id + '][' + col1Id + ']'
            console.log(eid)
            document.getElementById(eid).focus();
            d3PointDescriptionForMultiBarById(eid)
        } else {
            playBeep();
            // col2Id = multi_number_of_elements_in_each_group - 1;
            // var eid = 'Column[' + col2Id + '][' + col1Id + ']'
            // console.log(eid)
            // document.getElementById(eid).focus();
            // d3PointDescriptionForMultiBarById(eid)
        }
    }
}

function playBeep() {
    document.getElementById("mic").play();
}

function countWords(text) {
    return text.trim().split(/\s+/).length;
}

function findMaxCountOfWordsInList(list) {

    let max = 0;

    for (let i = 0; i < list.length; i++) {
        if (countWords(list[i].toString()) > max) {
            max = countWords(list[i].toString());
        }
    }

    return max;
}

function search_field() {

    var search_string = document.getElementById("search_input").value;

    if (search_string === "") {
        document.getElementById("search_result").innerHTML = "Search field is empty";
    } else if (countWords(search_string.toString()) < findMaxCountOfWordsInList(columnArrInString)) {
        document.getElementById("search_result").innerHTML = "Provided input did not match any valid result.";
        speakText("Provided input did not match any valid result.")
    } else if (countWords(search_string.toString()) === findMaxCountOfWordsInList(columnArrInString)) {
        // console.log(columnArr);
        // console.log(columnArrInString);
        if (!columnArrInString.includes(search_string)) {
            document.getElementById("search_result").innerHTML = "Input data " + search_string + " did not match any X-Axis value.";
            speakText("Input data " + search_string + " did not match any X-Axis value.")
            return;
        }

        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        var theUrl = "https://127.0.0.1:8080/search";
        xmlhttp.open("POST", theUrl);

        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "chart": "" + document.getElementById('chartNumber').value + "",
            "x_axis": "" + xLabel + "",
            "y_axis": "" + yLabel + "",
            "graphType": "" + graphType + "",
            "columnType": "" + columnType + "",
            "search_val": "" + search_string + ""
        }));

        xmlhttp.onloadend = function () {

            if (xmlhttp.status === 200) {
                // document.getElementById("search_input").value = "";
                const myObj = JSON.parse(xmlhttp.response);
                console.log(myObj.summary)
                document.getElementById("search_result").innerHTML = myObj.summary;
                speakText(myObj.summary)
            }
        };
    } else {
        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        var theUrl = "https://127.0.0.1:8080/qna";
        xmlhttp.open("POST", theUrl);

        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "chart": "" + document.getElementById('chartNumber').value + "",
            "question": "" + search_string + "",
        }));

        xmlhttp.onloadend = function () {

            if (xmlhttp.status === 200) {
                // document.getElementById("search_input").value = "";
                const myObj = JSON.parse(xmlhttp.response);
                console.log(myObj.summary)
                document.getElementById("search_result").innerHTML = myObj.summary;
                speakText(myObj.summary)

            }
        };
    }


}