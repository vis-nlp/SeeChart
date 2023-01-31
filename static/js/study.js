var participant_id = "147596";
var order = "NTH";

var loggedInPID = null;

var group = "a";

var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.

function validate(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/login";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": "" + username + "",
        "pwd": "" + password + ""
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            const myObj = JSON.parse(xmlhttp.response);
            console.log("myObj")
            console.log(myObj)
            loggedInPID = myObj.pid;
            console.log("loggedInPID")
            console.log(loggedInPID)
            window.location.href = "landingPage.html" + "#" + loggedInPID; // Redirecting to other page.

            return false;
        }
        else {
            attempt --;// Decrementing by one.
            alert("You have left "+attempt+" attempt;");
            // Disabling fields after 3 attempts.
            if( attempt == 0){
                document.getElementById("username").disabled = true;
                document.getElementById("password").disabled = true;
                document.getElementById("submit").disabled = true;
                return false;
            }
        }
    };


}


function preStudySubmit(that){

    var age_range = that.age_range.value;
    var gender = that.gender.value;
    var occupation = that.occupation.value;
    var study_field = that.study_field.value;
    var encounter = that.encounter.value;
    var tool = that.tool.value;
    var pid = that.study_pid.value;

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/preStudy";
    xmlhttp.open("POST", theUrl);

    console.log(theUrl)

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "age_range": age_range,
        "gender": gender,
        "occupation": occupation,
        "study_field": study_field,
        "encounter": encounter,
        "tool": tool
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("pre_study_head").innerHTML = "Thank you for submitting the Pre-Study questionnaires."
            document.getElementById("pre_study_head").style.background = "#74C900"
            // document.getElementById('pre_study_head').scrollIntoView();
            window.scrollTo(0, 0);
            disableEveryChildNode("pre_std_form")
        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

}


function postStudySubmit(that){

    var useful = that.useful.value
    var easiness = that.easiness.value
    var navigation = that.navigation.value
    var summaries = that.summaries.value
    var appropriate = that.appropriate.value
    var recommend = that.recommend.value
    var pid = that.study_pid.value;


    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/postStudy";
    xmlhttp.open("POST", theUrl);

    console.log(theUrl)

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "useful": useful,
        "easiness": easiness,
        "navigation": navigation,
        "summaries": summaries,
        "appropriate": appropriate,
        "recommend": recommend
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("post_study_head").innerHTML = "Thank you for submitting the Post-Study questionnaires."
            document.getElementById("post_study_head").style.background = "#74C900"
            // document.getElementById('pre_study_head').scrollIntoView();
            window.scrollTo(0, 0);
            disableEveryChildNode("post_std_form")

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }



}


function removeElementById(ElementID){
    var element = document.getElementById(ElementID);
    element.parentNode.removeChild(element);
}

function disableEveryChildNode(elementId){
    var fields = document.getElementById(elementId).getElementsByTagName('*');
    for(var i = 0; i < fields.length; i++)
    {
        fields[i].disabled = true;
    }

}
function enableEveryChildNode(elementId){
    var fields = document.getElementById(elementId).getElementsByTagName('*');
    for(var i = 0; i < fields.length; i++)
    {
        fields[i].disabled = false;
    }

}

function scrollToTargetAdjusted(elementId, offset){
    var element = document.getElementById(elementId);
    var headerOffset = offset;
    var elementPosition = element.getBoundingClientRect().top;
    var offsetPosition = elementPosition - headerOffset;

    window.scrollTo({
         top: offsetPosition,
         behavior: "smooth"
    });
}


function if_all_done(pid){
    var JSONRequestURL = "static/task/data_" + pid + ".json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {
        var jsonObj = JSONRequest.response;

        if (jsonObj["TASK A"] === "DONE" && jsonObj["TASK B"] === "DONE" && jsonObj["TASK C"] === "DONE" && jsonObj["TASK D"] === "DONE" && jsonObj["Pre-Study Questionnaire"] === "DONE" && jsonObj["Post-Study Questionnaire"] === "DONE"){
            console.log("HURRAH")
            document.getElementById("final_status").innerHTML = "<span style='color: #21600e'> CONGRATULATIONS! </span> <br>" + "You have completed the study. Thank you.";

        }
        else {
            document.getElementById("final_status").remove();
        }


    };
}

// function enable_questions(){
//         var el = document.activeElement
//         enable_question(el);
//     }

var focused_element;

function set_focused_element(){
    focused_element = document.activeElement;
}

function enable_questions(){
    // console.log("ELEMENT")
    // console.log(parent.focused_element)
    // // focused_element.focus();
    // parent.focused_element.focus();
    // console.log("document.activeElement")
    // console.log(document.activeElement)

    // var el = parent.document.getElementById("chart")
    // console.log("EL")
    // console.log(el)
    // el.focus();

    parent.focus();

    document.getElementById("task").style.opacity = "1";
    // document.getElementById("task_head").innerText = "Please answer the following question:";
    enableEveryChildNode("task_form");
    startTimer();

    removeElementById("timer");

}


function set_post_questionnaire_state(pid) {
    var JSONRequestURL = "static/task/data_" + pid + ".json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {
        var jsonObj = JSONRequest.response;

        if (jsonObj["TASK A"] !== "DONE" || jsonObj["TASK B"] !== "DONE" || jsonObj["TASK C"] !== "DONE" || jsonObj["TASK D"] !== "DONE" ){
            document.getElementById("post_study_head").innerHTML = "Please complete all other tasks and questionnaires to answer the Post-Study Questionnaires!"
            document.getElementById("post_study_head").style.background = "#c99000"
            disableEveryChildNode("post_std_form")
        }
        else if (jsonObj["TASK A"] === "DONE" && jsonObj["TASK B"] === "DONE" && jsonObj["TASK C"] === "DONE" && jsonObj["TASK D"] === "DONE" && jsonObj["Pre-Study Questionnaire"] === "DONE"){
            scrollToTargetAdjusted('post_study_head', 44)
            // blink_an_element('post_study_head', 200);
        }


    };
}

function blink_an_element(element_id, blink_speed) {
    // every 1000 == 1 second, adjust to suit

    var t = setInterval(function () {
        var ele = document.getElementById(element_id);
        // ele.style.visibility = (ele.style.visibility === 'hidden' ? '' : 'hidden');
        ele.style.opacity = (ele.style.opacity === '0.5' ? '1' : '0.5');
    }, blink_speed);
}

function reset_task_state(pid, task){
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/reset";
    xmlhttp.open("POST", theUrl);

    console.log(theUrl)

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "task_name": task
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            console.log(task + " has been reset for user# " + pid)
            location.reload()
        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

    return 0;

}


function read_task_state(pid, task){
    var JSONRequestURL = "static/task/data_" + pid + ".json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {
        var jsonObj = JSONRequest.response;
        var task_state = jsonObj[task]
        if (task_state === "DONE" && task==="Pre-Study Questionnaire"){
            document.getElementById("pre_study_head").innerHTML = "You have submitted the Pre-Study questionnaires already."
            document.getElementById("pre_study_head").style.background = "#74C900"
            disableEveryChildNode("pre_std_form")
            document.getElementById("pre_study_submit").style.color = "GRAY";


            var preJSONRequestURL = "static/task/responses/pre_study_pid_" + pid + ".json";
            var preJSONRequest = new XMLHttpRequest();
            preJSONRequest.open('GET', preJSONRequestURL);
            preJSONRequest.responseType = 'json';
            preJSONRequest.send();
            preJSONRequest.onload = function () {
                var jsonObjPre = preJSONRequest.response;

                document.getElementById("age_range " + jsonObjPre.age_range).checked = true;
                document.getElementById("gender " + jsonObjPre.gender).checked = true;
                document.getElementById("occupation").value = jsonObjPre.occupation;
                document.getElementById("study_field").value = jsonObjPre.study_field;
                document.getElementById("encounter " + jsonObjPre.encounter).checked = true;
                document.getElementById("tool " + jsonObjPre.tool).checked = true;

            }

            return "done";

        }
        else if (task_state === "DONE" && task==="Post-Study Questionnaire"){
            document.getElementById("post_study_head").innerHTML = "You have submitted the Post-Study questionnaires already."
            document.getElementById("post_study_head").style.background = "#74C900"
            disableEveryChildNode("post_std_form")
            document.getElementById("post_study_submit").style.color = "GRAY";

            var postJSONRequestURL = "static/task/responses/post_study_pid_" + pid + ".json";
            var postJSONRequest = new XMLHttpRequest();
            postJSONRequest.open('GET', postJSONRequestURL);
            postJSONRequest.responseType = 'json';
            postJSONRequest.send();
            postJSONRequest.onload = function () {
                var jsonObjPost = postJSONRequest.response;

                document.getElementById("useful " + jsonObjPost.useful).checked = true;
                document.getElementById("easiness " + jsonObjPost.easiness).checked = true;
                document.getElementById("navigation " + jsonObjPost.navigation).checked = true;
                document.getElementById("summaries " + jsonObjPost.summaries).checked = true;
                document.getElementById("appropriate " + jsonObjPost.appropriate).checked = true;
                document.getElementById("recommend " + jsonObjPost.recommend).checked = true;

            }
        }
        else if (task_state === "DONE" && task==="TASK A"){
            document.getElementById("task_head").innerHTML = "You have completed Task A already."
            document.getElementById("task_head").style.background = "#74C900"
            disableEveryChildNode("task_form")
            document.getElementById("task_a_submit").style.color = "GRAY";
            removeElementById("timer");
            removeElementById('stopwatch');
            document.getElementById("task").style.opacity = "1";


            var postJSONRequestURL = "static/task/responses/task_A_response_pid_" + pid + ".json";
            var postJSONRequest = new XMLHttpRequest();
            postJSONRequest.open('GET', postJSONRequestURL);
            postJSONRequest.responseType = 'json';
            postJSONRequest.send();
            postJSONRequest.onload = function () {
                var jsonObjPost = postJSONRequest.response;

                document.getElementById("T1_Q1").value = jsonObjPost.T1_Q1;
                document.getElementById("T1_Q2").value = jsonObjPost.T1_Q2;
                document.getElementById("T1_Q3").value = jsonObjPost.T1_Q3;
                document.getElementById("T1_Q4").value = jsonObjPost.T1_Q4;

            }
        }
        else if (task_state === "DONE" && task==="TASK B"){
            document.getElementById("task_head").innerHTML = "You have completed Task B already."
            document.getElementById("task_head").style.background = "#74C900"
            disableEveryChildNode("task_form")
            document.getElementById("task_b_submit").style.color = "GRAY";
            removeElementById("timer");
            removeElementById('stopwatch');
            document.getElementById("task").style.opacity = "1";

            var postJSONRequestURL = "static/task/responses/task_B_response_pid_" + pid + ".json";
            var postJSONRequest = new XMLHttpRequest();
            postJSONRequest.open('GET', postJSONRequestURL);
            postJSONRequest.responseType = 'json';
            postJSONRequest.send();
            postJSONRequest.onload = function () {
                var jsonObjPost = postJSONRequest.response;

                document.getElementById("T2_Q1").value = jsonObjPost.T2_Q1;
                document.getElementById("T2_Q2").value = jsonObjPost.T2_Q2;
                document.getElementById("T2_Q3").value = jsonObjPost.T2_Q3;
                document.getElementById("T2_Q4").value = jsonObjPost.T2_Q4;

            }
        }
        else if (task_state === "DONE" && task==="TASK C"){
            document.getElementById("task_head").innerHTML = "You have completed Task C already."
            document.getElementById("task_head").style.background = "#74C900"
            disableEveryChildNode("task_form")
            document.getElementById("task_c_submit").style.color = "GRAY";
            removeElementById("timer");
            removeElementById('stopwatch');
            document.getElementById("task").style.opacity = "1";

            var postJSONRequestURL = "static/task/responses/task_C_response_pid_" + pid + ".json";
            var postJSONRequest = new XMLHttpRequest();
            postJSONRequest.open('GET', postJSONRequestURL);
            postJSONRequest.responseType = 'json';
            postJSONRequest.send();
            postJSONRequest.onload = function () {
                var jsonObjPost = postJSONRequest.response;

                document.getElementById("T3_Q1").value = jsonObjPost.T3_Q1;
                document.getElementById("T3_Q2").value = jsonObjPost.T3_Q2;
                document.getElementById("T3_Q3").value = jsonObjPost.T3_Q3;
                document.getElementById("T3_Q4").value = jsonObjPost.T3_Q4;

            }
        }
        else if (task_state === "DONE" && task==="TASK D"){
            document.getElementById("task_head").innerHTML = "You have completed Task D already."
            document.getElementById("task_head").style.background = "#74C900"
            disableEveryChildNode("task_form")
            document.getElementById("task_d_submit").style.color = "GRAY";
            removeElementById("timer");
            removeElementById('stopwatch');
            document.getElementById("task").style.opacity = "1";

            var postJSONRequestURL = "static/task/responses/task_D_response_pid_" + pid + ".json";
            var postJSONRequest = new XMLHttpRequest();
            postJSONRequest.open('GET', postJSONRequestURL);
            postJSONRequest.responseType = 'json';
            postJSONRequest.send();
            postJSONRequest.onload = function () {
                var jsonObjPost = postJSONRequest.response;

                document.getElementById("T4_Q1").value = jsonObjPost.T4_Q1;
                document.getElementById("T4_Q2").value = jsonObjPost.T4_Q2;
                document.getElementById("T4_Q3").value = jsonObjPost.T4_Q3;
                document.getElementById("T4_Q4").value = jsonObjPost.T4_Q4;

            }
        }
    };
}

function check_summary_status() {
    var JSONRequestURL = "static/task/active_summary_types.json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {

        if (JSONRequest.status === 200) {
            var jsonObj = JSONRequest.response;
            console.log(jsonObj)
            if (jsonObj['template'] === true) {
                document.getElementById("summary_type_temp").checked = true;
            } else {
                document.getElementById("summary_type_temp").checked = false;
            }
            if (jsonObj['ml'] === true) {
                document.getElementById("summary_type_ml").checked = true;
            } else {
                document.getElementById("summary_type_ml").checked = false;
            }
            if (jsonObj['human'] === true) {
                document.getElementById("summary_type_human").checked = true;
            } else {
                document.getElementById("summary_type_human").checked = false;
            }
            if (jsonObj['brush'] === true) {
                document.getElementById("brush_selection").checked = true;
                document.getElementById("lasso_selection").checked = false;
            } else {
                document.getElementById("brush_selection").checked = false;
                document.getElementById("lasso_selection").checked = true;
            }
        }
    }
}

function remove_slider(){
    elem = document.getElementById("slider_table");

    if (elem !== null){
        temp = elem;
        elem_parent = elem.parentNode;
        console.log(elem_parent)
    }
    temp.remove();
}


function check_study_group(){
    var JSONRequestURL = "static/task/active_summary_types.json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {

        if (JSONRequest.status === 200) {
            var jsonObj = JSONRequest.response;
            console.log(jsonObj)


            if (jsonObj['grp_a'] === true){
                group = "a";
            }
            else if (jsonObj['grp_b'] === true){
                group = "b";
            }
            else if (jsonObj['grp_c'] === true){
                group = "c";
                return group;
            }
            else if (jsonObj['grp_d'] === true){
                group = "d";
            }

        }
        else {
            console.log("check_study_group: Something went wrong")
        }
    }
}



function set_summary_selection() {
    var JSONRequestURL = "static/task/active_summary_types.json";
    var JSONRequest = new XMLHttpRequest();
    JSONRequest.open('GET', JSONRequestURL);
    JSONRequest.responseType = 'json';
    JSONRequest.send();

    JSONRequest.onload = function () {

        if (JSONRequest.status === 200) {
            var jsonObj = JSONRequest.response;
            console.log(jsonObj)

            var tem = jsonObj['template']
            var ml = jsonObj['ml']
            var hum = jsonObj['human']
            var brush = jsonObj['brush']


            // lasso_selection = brush !== true;


            if (tem === false && ml === false && hum === false){
                document.getElementById("summary_type").disabled = true;
                document.getElementById("summary_type_c2t").disabled = true;
                document.getElementById("summary_type_gold").disabled = true;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = ml;
                document.getElementById("summary_type_gold").checked = hum;

                document.getElementById("narrate_button").disabled = true;
                document.getElementById("narrate_button").style.color = "GRAY";
                document.getElementById("cap_text").innerHTML = ""
                document.getElementById("summary").innerHTML = ""

                remove_slider();
            }
            else if (tem === false && ml === false && hum === true){
                document.getElementById("summary_type").disabled = true;
                document.getElementById("summary_type_c2t").disabled = true;
                document.getElementById("summary_type_gold").disabled = false;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = ml;
                document.getElementById("summary_type_gold").checked = hum;

                remove_slider();
                gold_summary();

            }
            else if (tem === false && ml === true && hum === false){
                document.getElementById("summary_type").disabled = true;
                document.getElementById("summary_type_c2t").disabled = false;
                document.getElementById("summary_type_gold").disabled = true;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = ml;
                document.getElementById("summary_type_gold").checked = hum;

                remove_slider();
                c2t_summary();
            }
            else if (tem === false && ml === true && hum === true){
                document.getElementById("summary_type").disabled = true;
                document.getElementById("summary_type_c2t").disabled = false;
                document.getElementById("summary_type_gold").disabled = false;
                document.getElementById("summary_type").checked = false;
                document.getElementById("summary_type_c2t").checked = ml;
                document.getElementById("summary_type_gold").checked = false;

                remove_slider();
                c2t_summary();
            }
            else if (tem === true && ml === false && hum === false){
                document.getElementById("summary_type").disabled = false;
                document.getElementById("summary_type_c2t").disabled = true;
                document.getElementById("summary_type_gold").disabled = true;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = ml;
                document.getElementById("summary_type_gold").checked = hum;

                template_summary();
            }
            else if (tem === true && ml === false && hum === true){
                document.getElementById("summary_type").disabled = false;
                document.getElementById("summary_type_c2t").disabled = true;
                document.getElementById("summary_type_gold").disabled = false;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = false;
                document.getElementById("summary_type_gold").checked = false;

                template_summary();
            }
            else if (tem === true && ml === true && hum === false){
                document.getElementById("summary_type").disabled = false;
                document.getElementById("summary_type_c2t").disabled = false;
                document.getElementById("summary_type_gold").disabled = true;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = false;
                document.getElementById("summary_type_gold").checked = false;

                template_summary();
            }
            else if (tem === true && ml === true && hum === true){
                document.getElementById("summary_type").disabled = false;
                document.getElementById("summary_type_c2t").disabled = false;
                document.getElementById("summary_type_gold").disabled = false;
                document.getElementById("summary_type").checked = tem;
                document.getElementById("summary_type_c2t").checked = false;
                document.getElementById("summary_type_gold").checked = false;

                template_summary();
            }
        }
    }
}


function GetURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam)
        {
            return sParameterName[1];
        }
    }
}


function question_response(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var question = document.getElementById("question").textContent;
    var answer = that.answer.value
    var pid = that.study_pid.value
    var task = that.task.value

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/response";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "task": task,
        "question": question,
        "answer": answer,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            // document.getElementById("task_head").innerHTML = "Congratulations. You have completed Task A!"
            // document.getElementById("task_head").style.background = "#74C900"
            window.scrollTo(0, 0);
            // disableEveryChildNode("task_form")
            // removeElementById('stopwatch');

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

    removeElementById('stopwatch');

}

function question_response_summary(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var question1 = document.getElementById("TempSum").textContent;
    var answer1 = that.temp_sum.value
    var question2 = document.getElementById("MlSum").textContent;
    var answer2 = that.ml_sum.value
    var question3 = document.getElementById("key").textContent;
    var answer3 = that.key_takeaway_answer.value
    var pid = that.study_pid.value
    var task = that.task.value

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/response";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "task": task,
        "question": question1,
        "answer": answer1,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            window.scrollTo(0, 0);

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.open("POST", theUrl);

    xmlhttp2.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp2.send(JSON.stringify({
        "pid": pid,
        "task": task,
        "question": question2,
        "answer": answer2,
        "time": time
    }));

    xmlhttp2.onloadend = function () {
        console.log(xmlhttp2.status)
        if (xmlhttp2.xmlhttp2 === 200) {
            window.scrollTo(0, 0);

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

    if (answer3 !== 'undefined' || answer3 !== null){
        var xmlhttp3 = new XMLHttpRequest();
        xmlhttp3.open("POST", theUrl);

        xmlhttp3.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp3.send(JSON.stringify({
            "pid": pid,
            "task": task,
            "question": question3,
            "answer": answer3,
            "time": time
        }));

        xmlhttp3.onloadend = function () {
            console.log(xmlhttp3.status)
            if (xmlhttp3.status === 200) {
                window.scrollTo(0, 0);

            }
            else {
                console.log("Something went wrong.")
                location.reload()
            }
        }
    }


    removeElementById('stopwatch');

}


function taskA_response(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var T1_Q1 = that.T1_Q1.value
    var T1_Q2 = that.T1_Q2.value
    var T1_Q3 = that.T1_Q3.value
    var T1_Q4 = that.temp_sum.value
    var T1_Q5 = that.ml_sum.value
    var pid = that.study_pid.value

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/taskA";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "T1_Q1": T1_Q1,
        "T1_Q2": T1_Q2,
        "T1_Q3": T1_Q3,
        "T1_Q4": T1_Q4,
        "T1_Q5": T1_Q5,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("task_head").innerHTML = "Congratulations. You have completed Task A!"
            document.getElementById("task_head").style.background = "#74C900"
            window.scrollTo(0, 0);
            disableEveryChildNode("task_form")
            removeElementById('stopwatch');

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

    removeElementById('stopwatch');

}


function taskB_response(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var T2_Q1 = that.T2_Q1.value
    var T2_Q2 = that.T2_Q2.value
    var T2_Q3 = that.T2_Q3.value
    var T2_Q4 = that.temp_sum.value
    var T2_Q5 = that.ml_sum.value
    var pid = that.study_pid.value


    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/taskB";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "T2_Q1": T2_Q1,
        "T2_Q2": T2_Q2,
        "T2_Q3": T2_Q3,
        "T2_Q4": T2_Q4,
        "T2_Q5": T2_Q5,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("task_head").innerHTML = "Congratulations. You have completed Task B!"
            document.getElementById("task_head").style.background = "#74C900"
            window.scrollTo(0, 0);
            disableEveryChildNode("task_form")
            removeElementById('stopwatch');

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

}


function taskC_response(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var T3_Q1 = that.T3_Q1.value
    var T3_Q2 = that.T3_Q2.value
    var T3_Q3 = that.T3_Q3.value
    var T3_Q4 = that.temp_sum.value
    var T3_Q5 = that.ml_sum.value
    var pid = that.study_pid.value


    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/taskC";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "T3_Q1": T3_Q1,
        "T3_Q2": T3_Q2,
        "T3_Q3": T3_Q3,
        "T3_Q4": T3_Q4,
        "T3_Q5": T3_Q5,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("task_head").innerHTML = "Congratulations. You have completed Task C!"
            document.getElementById("task_head").style.background = "#74C900"
            window.scrollTo(0, 0);
            disableEveryChildNode("task_form")
            removeElementById('stopwatch');

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

}


function taskD_response(that){
    stopTimer();
    var time = timer.innerText;
    console.log("TIME -> " + time)
    resetTimer();

    var T4_Q1 = that.T4_Q1.value
    var T4_Q2 = that.T4_Q2.value
    var T4_Q3 = that.T4_Q3.value
    var T4_Q4 = that.temp_sum.value
    var T4_Q5 = that.ml_sum.value
    var pid = that.study_pid.value


    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var theUrl = "https://infovis-userstudy.herokuapp.com/taskD";
    xmlhttp.open("POST", theUrl);

    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({
        "pid": pid,
        "T4_Q1": T4_Q1,
        "T4_Q2": T4_Q2,
        "T4_Q3": T4_Q3,
        "T4_Q4": T4_Q4,
        "T4_Q5": T4_Q5,
        "time": time
    }));

    xmlhttp.onloadend = function () {
        console.log(xmlhttp.status)
        if (xmlhttp.status === 200) {
            document.getElementById("task_head").innerHTML = "Congratulations. You have completed Task D!"
            document.getElementById("task_head").style.background = "#74C900"
            window.scrollTo(0, 0);
            disableEveryChildNode("task_form")
            removeElementById('stopwatch');

        }
        else {
            console.log("Something went wrong.")
            location.reload()
        }
    }

}


// STOPWATCH

var timer;

var hr;
var min;
var sec;
var stoptime;


function record_time(){
    var pid = document.getElementById('pid').value;
    var ans = document.getElementById('ans').value;

    if (pid === ""){
        alert("Please insert Participant ID!")
    } else if ( ans === ""){
        alert("Please insert ANSWER!")
    }
    else {
        stopTimer();


        var time = document.getElementById('stopwatch').innerText;
        var qstn = document.getElementById('q_no').value;
        var isCorrect = document.getElementById('result').checked


        console.log(pid)
        console.log(time)
        console.log(qstn)
        console.log(ans)
        console.log(isCorrect)

        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        // var theUrl = "https://127.0.0.1:8080/report";
        var theUrl = "https://infovis-userstudy.herokuapp.com/report";
        xmlhttp.open("POST", theUrl);

        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "pid": pid,
            "question_no": qstn,
            "answer": ans,
            "result": isCorrect,
            "taken_time": time
        }));

        xmlhttp.onloadend = function () {
            console.log(xmlhttp.status)
            if (xmlhttp.status === 200) {
                console.log("Reported!")
                document.getElementById('last_record').innerHTML = "Last recorded time was " + time;
                resetTimer();
                alert("Recorded " + qstn + ". ")

            } else {
                alert("SOMETHING WENT WRONG.")
            }
        }



    }

}


function record_key_presses(){

    var pid = document.getElementById("pid").textContent;
    var pressed = document.getElementById("key_counter").textContent;
    var chart_no = document.getElementById("numberLabel").textContent;

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        // var theUrl = "https://127.0.0.1:8080/key";
        var theUrl = "https://infovis-userstudy.herokuapp.com/key";
        xmlhttp.open("POST", theUrl);

        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({
            "pid": pid,
            "chart_no": chart_no,
            "key_presses": pressed
        }));

        xmlhttp.onloadend = function () {
            console.log(xmlhttp.status)
            if (xmlhttp.status === 200) {
                console.log("Key press recorded!")

            } else {
                alert("SOMETHING WENT WRONG.")
            }
        }
}

function no_cap(){
    summary = ["No description present for this chart."]
    dis_summary = ["No description present for this chart."]

    document.getElementById("summary").innerHTML = "No description present for this chart.";

    removeElementById("cap_text")
    removeElementById("summary_config")

}

function human_cap(){
    console.log("Human created summary is selected.")
    gold_summary()
    // curr = 0;
    document.getElementById("summary_type_gold").checked = "true"
}

function temp_cap(){
    console.log("Template based summary is selected.")
    document.getElementById("summary_type").checked = "true"


}

function select_summary_type(){
    if (order === "NTH"){
        all_temp();
        // NTH();
    }
    // else if (order === "HNT"){
    //     HNT();
    // }
    // else if (order === "TNH"){
    //     TNH();
    // }
    // else if (order === "HTN"){
    //     HTN();
    // }
    // else if (order === "NHT"){
    //     NHT();
    // }
    // else if (order === "THN"){
    //     THN();
    // }
    // else{
    //     all_temp();
    // }

}

function all_temp(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        temp_cap();
    }
}


function NTH(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        human_cap();
    }
}


function HNT(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        temp_cap();
    }
}

function TNH(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        human_cap();
    }
}

function HTN(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        no_cap();
    }
}

function NHT(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        temp_cap();
    }
}

function THN(){
    if (GetURLParameter('chart') === "bar_158" || GetURLParameter('chart') === "bar_180" || GetURLParameter('chart') === "bar_186" || GetURLParameter('chart') === "bar_206") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "bar_775" || GetURLParameter('chart') === "bar_1092" || GetURLParameter('chart') === "bar_308" || GetURLParameter('chart') === "bar_309") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "bar_377" || GetURLParameter('chart') === "bar_45" || GetURLParameter('chart') === "bar_669" || GetURLParameter('chart') === "bar_694") {
        no_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_170" || GetURLParameter('chart') === "multi_line_176" || GetURLParameter('chart') === "multi_line_189" || GetURLParameter('chart') === "multi_line_197") {
        temp_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_205" || GetURLParameter('chart') === "multi_line_220" || GetURLParameter('chart') === "multi_line_711" || GetURLParameter('chart') === "multi_line_752") {
        human_cap();
    }
    else if (GetURLParameter('chart') === "multi_line_245" || GetURLParameter('chart') === "multi_line_457" || GetURLParameter('chart') === "multi_line_545" || GetURLParameter('chart') === "multi_line_524") {
        no_cap();
    }
}



function download_report(){
    var pid = document.getElementById('pid').value;
    if (pid === ""){
        alert("Please insert Participant ID!")
    } else {
        var name = 'Timer_' + document.getElementById('pid').value + '.csv'

        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        // var theUrl = "https://infovis-userstudy.herokuapp.com/taskD";
        var theUrl = "https://127.0.0.1:8080/download/" + name;
        xmlhttp.open("GET", theUrl);

        // xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.responseType = 'blob'
        xmlhttp.send();

        xmlhttp.onloadend = function () {
            console.log(xmlhttp.status)
            if (xmlhttp.status === 200) {
                console.log("Downloaded")
            }
            else {
                alert("Could not download. Check PID.")
            }
        }
    }


}


function initStopWatch(){
    timer = document.getElementById('stopwatch');

    hr = 0;
    min = 0;
    sec = 0;
    stoptime = true;
}

function startTimer() {
    var pid = document.getElementById('pid').value;

    if (pid === ""){
        alert("Please insert Participant ID!")
    } else {
        if (stoptime == true) {
            stoptime = false;
            timerCycle();
            document.getElementById("stopwatch").classList.remove("blink");
            document.getElementById("stopwatch").style.color = "green";

        }
    }
}

function stopTimer() {
  if (stoptime == false) {
    stoptime = true;
        document.getElementById("stopwatch").style.color = "orange";
  }
}

function timerCycle() {
    if (stoptime == false) {
    sec = parseInt(sec);
    min = parseInt(min);
    hr = parseInt(hr);

    sec = sec + 1;

    if (sec == 60) {
      min = min + 1;
      sec = 0;
    }
    if (min == 60) {
      hr = hr + 1;
      min = 0;
      sec = 0;
    }

    if (sec < 10 || sec == 0) {
      sec = '0' + sec;
    }
    if (min < 10 || min == 0) {
      min = '0' + min;
    }
    if (hr < 10 || hr == 0) {
      hr = '0' + hr;
    }

    timer.innerHTML = hr + ':' + min + ':' + sec;

    if (min === "03"){
        document.getElementById("stopwatch").style.color = "red";
        document.getElementById("stopwatch").classList.add("blink");

    } else {
        document.getElementById("stopwatch").classList.remove("blink");
    }

    setTimeout("timerCycle()", 1000);
  }
}

function resetTimer() {
    timer.innerHTML = "00:00:00";
    stoptime = true;
    hr = 0;
    sec = 0;
    min = 0;
    document.getElementById("stopwatch").classList.remove("blink");
    document.getElementById("stopwatch").style.color = "black";
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


var keyList = []
var key_counter = 0;


function key_press_counter(e){
    // keyList.push(e)
    key_counter++;
    // console.log(keyList)
    document.getElementById("key_counter").innerHTML = "NUMBER OF KEY PRESSES: " + key_counter;
}

function reset_key_counter(){
    keyList = []
    key_counter = 0;
}

