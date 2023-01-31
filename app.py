from datetime import datetime
import json
import csv
import os
from os import listdir
from os.path import isfile, join
import ssl
from flask_jsglue import JSGlue  # pip install Flask-JSGlue  -> http://stewartpark.github.io/Flask-JSGlue/
import math
from qna import askMe

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_from_directory,
    flash
)
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from BaselineSummarizer import summarize
from users import users
from utility import make_directory, check_in_csv, save_image_from_url, write_on_csv, get_random_label, make_JSON, \
    write_image, single_line_input, multi_line_input, single_bar_input, multi_bar_input, \
    single_bar_input_from_mutli_bar_data, single_bar_input_brush, multi_bar_input_brush, single_line_input_brush, \
    multi_line_input_brush, multi_bar_input_for_single_brush
import tasks

# UNCOMMENT THE FOLLOWING TWO LINES TO RUN LOCALLY

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certificate/server.crt', 'certificate/server.key')

app = Flask(__name__, template_folder='templates')
app.secret_key = 'somesecretkeythatonlyshovanshouldknow'
api = Api(app)
CORS(app)
jsglue = JSGlue(app)

screenshot_post_args = reqparse.RequestParser()
screenshot_post_args.add_argument("vis_id", type=str, help="ID of the visual")
screenshot_post_args.add_argument("url", type=str, help="URL")
screenshot_post_args.add_argument("date", type=str, help="Date")
screenshot_post_args.add_argument("imgBase64", type=str, help="imgBase64")

url_post_args = reqparse.RequestParser()
url_post_args.add_argument("iframe_url", type=str, help="ID of the visual")
url_post_args.add_argument("original_url", type=str, help="URL")

decon_post_args = reqparse.RequestParser()
decon_post_args.add_argument("decon", type=str, help="Decon data string")

crawl_image_post_args = reqparse.RequestParser()
crawl_image_post_args.add_argument("img_url", type=str, help="Image URL string")

multi_line_lasso_post_args = reqparse.RequestParser()
multi_line_lasso_post_args.add_argument("xValues", type=str, help="xVals")
multi_line_lasso_post_args.add_argument("yValues", type=str, help="yValues")
multi_line_lasso_post_args.add_argument("lineValues", type=str, help="lineValues")
multi_line_lasso_post_args.add_argument("xLabel", type=str, help="xLabel")
multi_line_lasso_post_args.add_argument("yLabel", type=str, help="yLabel")
multi_line_lasso_post_args.add_argument("chartNumber", type=int, help="chartNumber")
multi_line_lasso_post_args.add_argument("summary", type=str, help="summary")

multi_bar_lasso_post_args = reqparse.RequestParser()
multi_bar_lasso_post_args.add_argument("xValues", type=str, help="xVals")
multi_bar_lasso_post_args.add_argument("yValues", type=str, help="yValues")
multi_bar_lasso_post_args.add_argument("barValues", type=str, help="barValues")
multi_bar_lasso_post_args.add_argument("xLabel", type=str, help="xLabel")
multi_bar_lasso_post_args.add_argument("yLabel", type=str, help="yLabel")
multi_bar_lasso_post_args.add_argument("chartNumber", type=int, help="chartNumber")
multi_bar_lasso_post_args.add_argument("summary", type=str, help="summary")

bar_brush_post_args = reqparse.RequestParser()
bar_brush_post_args.add_argument("chart", type=str, help="chart (line/bar)")
bar_brush_post_args.add_argument("chartType", type=str, help="chartType (single/multi)")
bar_brush_post_args.add_argument("barValues", type=str, help="barValues")
bar_brush_post_args.add_argument("groupNames", type=str, help="groupNames")
bar_brush_post_args.add_argument("xLabel", type=str, help="xLabel")
bar_brush_post_args.add_argument("yLabel", type=str, help="yLabel")
bar_brush_post_args.add_argument("chartNumber", type=int, help="chartNumber")
bar_brush_post_args.add_argument("summary", type=str, help="summary")

login_post_args = reqparse.RequestParser()
login_post_args.add_argument("pid", type=str, help="Participant ID")
login_post_args.add_argument("pwd", type=str, help="Password")
login_post_args.add_argument("status", type=str, help="Status")

task_reset_post_args = reqparse.RequestParser()
task_reset_post_args.add_argument("pid", type=str, help="pid")
task_reset_post_args.add_argument("task_name", type=str, help="task_name")
task_reset_post_args.add_argument("status", type=str, help="status")

question_response_post_args = reqparse.RequestParser()
question_response_post_args.add_argument("pid", type=str, help="pid")
question_response_post_args.add_argument("task", type=str, help="task_name")
question_response_post_args.add_argument("question", type=str, help="question")
question_response_post_args.add_argument("answer", type=str, help="answer")
question_response_post_args.add_argument("time", type=str, help="time taken")
question_response_post_args.add_argument("status", type=str, help="status")

timer_post_args = reqparse.RequestParser()
timer_post_args.add_argument("pid", type=str, help="pid")
timer_post_args.add_argument("question_no", type=str, help="question_no")
timer_post_args.add_argument("answer", type=str, help="answer")
timer_post_args.add_argument("result", type=str, help="result")
timer_post_args.add_argument("taken_time", type=str, help="taken_time")
timer_post_args.add_argument("status", type=str, help="status")

key_post_args = reqparse.RequestParser()
key_post_args.add_argument("pid", type=str, help="pid")
key_post_args.add_argument("chart_no", type=str, help="chart_no")
key_post_args.add_argument("key_presses", type=str, help="key_presses")
key_post_args.add_argument("status", type=str, help="status")

search_post_args = reqparse.RequestParser()
search_post_args.add_argument("chart", type=str, help="chart")
search_post_args.add_argument("x_axis", type=str, help="x_axis")
search_post_args.add_argument("y_axis", type=str, help="y_axis")
search_post_args.add_argument("graphType", type=str, help="graphType")
search_post_args.add_argument("columnType", type=str, help="columnType")
search_post_args.add_argument("search_val", type=str, help="search_val")
search_post_args.add_argument("summary", type=str, help="summary")

qna_post_args = reqparse.RequestParser()
qna_post_args.add_argument("chart", type=str, help="chart")
qna_post_args.add_argument("question", type=str, help="question")
qna_post_args.add_argument("summary", type=str, help="summary")

search_highchart_post_args = reqparse.RequestParser()
search_highchart_post_args.add_argument("url", type=str, help="URL")
search_highchart_post_args.add_argument("json_no", type=str, help="URL")

search_highchart_resource_fields = {
    'url': fields.String,
    'json_no': fields.String
}

qna_resource_fields = {
    'chart': fields.String,
    'question': fields.String,
    'summary': fields.String
}

search_resource_fields = {
    'chart': fields.String,
    'x_axis': fields.String,
    'y_axis': fields.String,
    'graphType': fields.String,
    'columnType': fields.String,
    'search_val': fields.String,
    'summary': fields.String
}

key_resource_fields = {
    'pid': fields.String,
    'chart_no': fields.String,
    'key_presses': fields.String,
    'status': fields.String
}

timer_resource_fields = {
    'pid': fields.String,
    'question_no': fields.String,
    'answer': fields.String,
    'result': fields.String,
    'taken_time': fields.String,
    'status': fields.String
}

question_response_resource_fields = {
    'pid': fields.String,
    'task': fields.String,
    'question': fields.String,
    'answer': fields.String,
    'time': fields.String,
    'status': fields.String
}

screenshot_resource_fields = {
    'vis_id': fields.String,
    'url': fields.String,
    'date': fields.String,
    'imgBase64': fields.String
}

url_resource_fields = {
    'iframe_url': fields.String,
    'original_url': fields.String
}

decon_resource_fields = {
    'decon': fields.String
}

crawl_image_resource_fields = {
    'img_url': fields.String
}

multi_line_lasso = {
    'xValues': fields.String,
    'yValues': fields.String,
    'lineValues': fields.String,
    'xLabel': fields.String,
    'yLabel': fields.String,
    'chartNumber': fields.Integer,
    'summary': fields.String
}

multi_bar_lasso = {
    'xValues': fields.String,
    'yValues': fields.String,
    'barValues': fields.String,
    'xLabel': fields.String,
    'yLabel': fields.String,
    'chartNumber': fields.Integer,
    'summary': fields.String
}

bar_brush = {
    'chart': fields.String,
    'chartType': fields.String,
    'barValues': fields.String,
    'groupNames': fields.String,
    'xLabel': fields.String,
    'yLabel': fields.String,
    'chartNumber': fields.Integer,
    'summary': fields.String
}

login = {
    'pid': fields.String,
    'pwd': fields.String,
    'status': fields.String
}

task_reset = {
    'pid': fields.String,
    'task_name': fields.String,
    'status': fields.String
}

global task_obj


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [i for i in users if i.id == session['user_id']][0]
        g.user = user


# @app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    g.task_file = None
    g.bar_chart = None
    g.bar_chart2 = None
    g.bar_chart3 = None
    g.multi_bar_chart = None
    g.line_chart = None
    g.multi_line_chart = None

    if request.method == 'POST':
        session.pop('user_id', None)  # Going to remove user ID if there is already a logged in one
        session.pop('task_file_name', None)
        username = request.form['username']
        password = request.form['password']

        if len([i for i in users if i.username == username]) > 0:
            user = [i for i in users if i.username == username][0]
        else:
            flash("Please provide a valid Participant ID.", 'error')
            # flash(u'Invalid password provided', 'error')
            return redirect(url_for('login'))

        if user and user.password == password:
            session['user_id'] = user.id
            global task_obj
            task_obj = tasks.Tasks(str(user.id))
            task_obj.set_logged_in_true()
            d = task_obj.get_all_task_status_info()
            print(json.dumps(d, indent=4))

            session['task_file_name'] = 'data_' + str(user.id)

            if username == "1000":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))

        flash("Please provide valid credentials.", 'error')
        # flash(u'Invalid password provided', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    global task_obj
    task_obj = tasks.Tasks(session['user_id'])
    task_obj.set_logged_in_false()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session.pop('user_id', None)  # Going to remove user ID if there is already a logged in one
    session.pop('task_file_name', None)

    return redirect(url_for('login'))


@app.route('/home')
def home():
    if not g.user:
        # abort(403)
        return redirect(url_for('login'))
    if g.user.id == "1000":
        return redirect(url_for('admin'))
    return render_template('home.html')


@app.route('/admin')
def admin():
    # if not g.user:
    #     # abort(403)
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    # if g.user.id != "1000":
    #     print("Unauthorized admin portal request blocked!")
    #     return redirect(url_for('home'))
    return render_template('admin_config.html')
    # return render_template('home_admin.html')


@app.route('/config')
def config():
    # if not g.user:
    #     # abort(403)
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    # if g.user.id != "1000":
    #     print("Unauthorized admin portal request blocked!")
    #     return redirect(url_for('home'))
    return render_template('admin_config.html')


@app.route('/timer')
def timer():
    # if not g.user:
    #     # abort(403)
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    # if g.user.id != "1000":
    #     print("Unauthorized admin portal request blocked!")
    #     return redirect(url_for('home'))
    return render_template('admin_time_config.html')


@app.route('/allcharts')
def all_charts():
    # if not g.user:
    #     # abort(403)
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    # if g.user.id != "1000":
    #     print("Unauthorized admin portal request blocked!")
    #     return redirect(url_for('home'))
    return render_template('original_all_charts.html')


@app.route('/consent')
def consent():
    return render_template('consent.html')


def clear():
    g.task_file = None
    g.bar_chart = None
    g.bar_chart2 = None
    g.bar_chart3 = None
    g.multi_bar_chart = None
    g.line_chart = None
    g.multi_line_chart = None


@app.route('/pid1001')
def consent_pid1001():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1001'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]

    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1002')
def consent_pid1002():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1002'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1003')
def consent_pid1003():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1003'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1004')
def consent_pid1004():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1004'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1005')
def consent_pid1005():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1005'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1006')
def consent_pid1006():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1006'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1007')
def consent_pid1007():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1007'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/pid1008')
def consent_pid1008():
    clear()
    session.pop('user_id', None)
    session.pop('task_file_name', None)
    username = '1008'
    if len([i for i in users if i.username == username]) > 0:
        user = [i for i in users if i.username == username][0]
    session['user_id'] = username
    g.user = username

    global task_obj
    task_obj = tasks.Tasks(username)
    task_obj.set_logged_in_true()
    d = task_obj.get_all_task_status_info()
    print(json.dumps(d, indent=4))

    session['task_file_name'] = 'data_' + str(username)
    return render_template('consent.html')


@app.route('/new_pre')
def new_pre():
    return render_template('new_pre.html')


@app.route('/new_post')
def new_post():
    return render_template('new_post.html')


# @app.route('/original')
@app.route("/")
def original():
    # return render_template('original.html')
    return render_template('selectedChart.html')


@app.route('/question')
def question():
    print("QUESTION WAS CALLED")
    if not g.user:
        # abort(403)
        global task_obj
        task_obj = tasks.Tasks(session['user_id'])
        task_obj.set_logged_in_false()
        return redirect(url_for('login'))

    if request.args:
        args = request.args

        if "number" in args:
            if args.get("number") == "a2":
                return render_template('taskA2_questions.html')
            elif args.get("number") == "a3":
                return render_template('taskA3_questions.html')
            elif args.get("number") == "a4":
                return render_template('taskA4_questions.html')
            elif args.get("number") == "bar2_a1":
                return render_template('bar2_taskA1_questions.html')
            elif args.get("number") == "bar2_a2":
                return render_template('bar2_taskA2_questions.html')
            elif args.get("number") == "bar2_a3":
                return render_template('bar2_taskA3_questions.html')
            elif args.get("number") == "bar2_a4":
                return render_template('bar2_taskA4_questions.html')
            elif args.get("number") == "bar3_a1":
                return render_template('bar3_taskA1_questions.html')
            elif args.get("number") == "bar3_a2":
                return render_template('bar3_taskA2_questions.html')
            elif args.get("number") == "bar3_a3":
                return render_template('bar3_taskA3_questions.html')
            elif args.get("number") == "bar3_a4":
                return render_template('bar3_taskA4_questions.html')
            elif args.get("number") == "b2":
                return render_template('taskB2_questions.html')
            elif args.get("number") == "b3":
                return render_template('taskB3_questions.html')
            elif args.get("number") == "b4":
                return render_template('taskB4_questions.html')
            elif args.get("number") == "c2":
                return render_template('taskC2_questions.html')
            elif args.get("number") == "c3":
                return render_template('taskC3_questions.html')
            elif args.get("number") == "c4":
                return render_template('taskC4_questions.html')
            elif args.get("number") == "d2":
                return render_template('taskD2_questions.html')
            elif args.get("number") == "d3":
                return render_template('taskD3_questions.html')
            elif args.get("number") == "d4":
                return render_template('taskD4_questions.html')
            elif args.get("number") == "multi_bar2_a1":
                return render_template('multi_bar2_taskA1_questions.html')
            elif args.get("number") == "multi_bar2_a2":
                return render_template('multi_bar2_taskA2_questions.html')
            elif args.get("number") == "multi_bar2_a3":
                return render_template('multi_bar2_taskA3_questions.html')
            elif args.get("number") == "multi_bar2_a4":
                return render_template('multi_bar2_taskA4_questions.html')
            elif args.get("number") == "multi_bar3_a1":
                return render_template('multi_bar3_taskA1_questions.html')
            elif args.get("number") == "multi_bar3_a2":
                return render_template('multi_bar3_taskA2_questions.html')
            elif args.get("number") == "multi_bar3_a3":
                return render_template('multi_bar3_taskA3_questions.html')
            elif args.get("number") == "multi_bar3_a4":
                return render_template('multi_bar3_taskA4_questions.html')
            elif args.get("number") == "line2_a1":
                return render_template('line2_taskA1_questions.html')
            elif args.get("number") == "line2_a2":
                return render_template('line2_taskA2_questions.html')
            elif args.get("number") == "line2_a3":
                return render_template('line2_taskA3_questions.html')
            elif args.get("number") == "line2_a4":
                return render_template('line2_taskA4_questions.html')
            elif args.get("number") == "line3_a1":
                return render_template('line3_taskA1_questions.html')
            elif args.get("number") == "line3_a2":
                return render_template('line3_taskA2_questions.html')
            elif args.get("number") == "line3_a3":
                return render_template('line3_taskA3_questions.html')
            elif args.get("number") == "line3_a4":
                return render_template('line3_taskA4_questions.html')
            elif args.get("number") == "multi_line2_a1":
                return render_template('multi_line2_taskA1_questions.html')
            elif args.get("number") == "multi_line2_a2":
                return render_template('multi_line2_taskA2_questions.html')
            elif args.get("number") == "multi_line2_a3":
                return render_template('multi_line2_taskA3_questions.html')
            elif args.get("number") == "multi_line2_a4":
                return render_template('multi_line2_taskA4_questions.html')
            elif args.get("number") == "multi_line3_a1":
                return render_template('multi_line3_taskA1_questions.html')
            elif args.get("number") == "multi_line3_a2":
                return render_template('multi_line3_taskA2_questions.html')
            elif args.get("number") == "multi_line3_a3":
                return render_template('multi_line3_taskA3_questions.html')
            elif args.get("number") == "multi_line3_a4":
                return render_template('multi_line3_taskA4_questions.html')
            else:
                return redirect(url_for('home'))


@app.route('/task')
def task():
    # if not g.user:
    #     # abort(403)
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    #
    # if g.user.id == "1000":
    #     return redirect(url_for('admin'))

    f = open('static/task/selected_chart_ids.json')
    selected_chart_ids = json.load(f)

    # print(selected_chart_ids["bar"])

    if request.args:
        args = request.args

        if "chart" in args:
            if args.get("chart") == "bar" or args.get("chart") == "bar1":
                g.bar_chart = selected_chart_ids["bar"]
            elif args.get("chart") == "bar2":
                g.bar_chart2 = selected_chart_ids["bar2"]
            elif args.get("chart") == "bar3":
                g.bar_chart3 = selected_chart_ids["bar3"]
            elif args.get("chart") == "multi_bar" or args.get("chart") == "multi_bar1":
                g.multi_bar_chart = selected_chart_ids["multi_bar"]
            elif args.get("chart") == "multi_bar2":
                g.multi_bar_chart2 = selected_chart_ids["multi_bar2"]
            elif args.get("chart") == "multi_bar3":
                g.multi_bar_chart3 = selected_chart_ids["multi_bar3"]
            elif args.get("chart") == "multi_line" or args.get("chart") == "multi_line1":
                g.multi_line_chart = selected_chart_ids["multi_line"]
            elif args.get("chart") == "multi_line2":
                g.multi_line_chart2 = selected_chart_ids["multi_line2"]
            elif args.get("chart") == "multi_line3":
                g.multi_line_chart3 = selected_chart_ids["multi_line3"]
            elif args.get("chart") == "line" or args.get("chart") == "line1":
                g.line_chart = selected_chart_ids["line"]
            elif args.get("chart") == "line2":
                g.line_chart2 = selected_chart_ids["line2"]
            elif args.get("chart") == "line3":
                g.line_chart3 = selected_chart_ids["line3"]
            elif args.get("chart") == "test1":
                g.test_chart1 = selected_chart_ids["test_chart1"]
            elif args.get("chart") == "test2":
                g.test_chart2 = selected_chart_ids["test_chart2"]
            elif args.get("chart") == "bar_158":
                g.bar_158 = selected_chart_ids["bar_158"]
            elif args.get("chart") == "bar_180":
                g.bar_180 = selected_chart_ids["bar_180"]
            elif args.get("chart") == "bar_186":
                g.bar_186 = selected_chart_ids["bar_186"]
            elif args.get("chart") == "bar_206":
                g.bar_206 = selected_chart_ids["bar_206"]
            elif args.get("chart") == "bar_775":
                g.bar_775 = selected_chart_ids["bar_775"]
            elif args.get("chart") == "bar_1092":
                g.bar_1092 = selected_chart_ids["bar_1092"]
            elif args.get("chart") == "bar_308":
                g.bar_308 = selected_chart_ids["bar_308"]
            elif args.get("chart") == "bar_309":
                g.bar_309 = selected_chart_ids["bar_309"]
            elif args.get("chart") == "bar_377":
                g.bar_377 = selected_chart_ids["bar_377"]
            elif args.get("chart") == "bar_45":
                g.bar_45 = selected_chart_ids["bar_45"]
            elif args.get("chart") == "bar_669":
                g.bar_669 = selected_chart_ids["bar_669"]
            elif args.get("chart") == "bar_694":
                g.bar_694 = selected_chart_ids["bar_694"]
            elif args.get("chart") == "multi_line_170":
                g.multi_line_170 = selected_chart_ids["multi_line_170"]
            elif args.get("chart") == "multi_line_176":
                g.multi_line_176 = selected_chart_ids["multi_line_176"]
            elif args.get("chart") == "multi_line_189":
                g.multi_line_189 = selected_chart_ids["multi_line_189"]
            elif args.get("chart") == "multi_line_197":
                g.multi_line_197 = selected_chart_ids["multi_line_197"]
            elif args.get("chart") == "multi_line_205":
                g.multi_line_205 = selected_chart_ids["multi_line_205"]
            elif args.get("chart") == "multi_line_220":
                g.multi_line_220 = selected_chart_ids["multi_line_220"]
            elif args.get("chart") == "multi_line_711":
                g.multi_line_711 = selected_chart_ids["multi_line_711"]
            elif args.get("chart") == "multi_line_752":
                g.multi_line_752 = selected_chart_ids["multi_line_752"]
            elif args.get("chart") == "multi_line_245":
                g.multi_line_245 = selected_chart_ids["multi_line_245"]
            elif args.get("chart") == "multi_line_457":
                g.multi_line_457 = selected_chart_ids["multi_line_457"]
            elif args.get("chart") == "multi_line_545":
                g.multi_line_545 = selected_chart_ids["multi_line_545"]
            elif args.get("chart") == "multi_line_524":
                g.multi_line_524 = selected_chart_ids["multi_line_524"]
            else:
                return redirect(url_for('home'))

            # return render_template('taskA_questions.html', query_string=query_string)
            return render_template('selectedChart.html')
    return redirect(url_for('home'))


@app.route('/questionnaire')
def questionnaire():
    if not g.user:
        global task_obj
        task_obj = tasks.Tasks(session['user_id'])
        task_obj.set_logged_in_false()
        return redirect(url_for('login'))

    if g.user.id == "1000":
        return redirect(url_for('admin'))
    return render_template('questionnaire.html')


@app.route('/post_questionnaire')
def post_questionnaire():
    if not g.user:
        global task_obj
        task_obj = tasks.Tasks(session['user_id'])
        task_obj.set_logged_in_false()
        return redirect(url_for('login'))

    if g.user.id == "1000":
        return redirect(url_for('admin'))
    return render_template('post_questionnaire.html')


@app.route('/taskA_questions')
def taskA_questions():
    return render_template('taskA_questions.html')


@app.route('/taskA2_questions')
def taskA2_questions():
    return render_template('taskA2_questions.html')


@app.route('/taskA3_questions')
def taskA3_questions():
    return render_template('bar2_taskA3_questions.html')


@app.route('/taskA4_questions')
def taskA4_questions():
    return render_template('task_questions_temp_sum_rating.html')


@app.route('/taskB_questions')
def taskB_questions():
    return render_template('taskB_questions.html')


@app.route('/taskC_questions')
def taskC_questions():
    return render_template('taskC_questions.html')


@app.route('/taskD_questions')
def taskD_questions():
    return render_template('taskD_questions.html')


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # if not g.user:
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))
    path = 'static/task/responses/'
    # uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # return send_from_directory(directory=path, filename=filename + '.json', as_attachment=True)
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/downloadAll', methods=['GET', 'POST'])
def downloadAll():
    if not g.user:
        global task_obj
        task_obj = tasks.Tasks(session['user_id'])
        task_obj.set_logged_in_false()
        return redirect(url_for('login'))

    path = os.getcwd() + '/static/task/responses/'

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    print(onlyfiles)

    filename = "post_study_pid_1001"
    return send_from_directory(path, onlyfiles, as_attachment=True)


@app.route('/summary_set/<s_type>/<stat>', methods=['GET', 'POST'])
def summary_set(s_type, stat):
    # if not g.user:
    #     global task_obj
    #     task_obj = tasks.Tasks(session['user_id'])
    #     task_obj.set_logged_in_false()
    #     return redirect(url_for('login'))

    f = open('static/task/active_summary_types.json')
    summary_types = json.load(f)

    if s_type == "grp_a":
        summary_types["grp_a"] = True
        summary_types["grp_b"] = False
        summary_types["grp_c"] = False
        summary_types["grp_d"] = False
    elif s_type == "grp_b":
        summary_types["grp_a"] = False
        summary_types["grp_b"] = True
        summary_types["grp_c"] = False
        summary_types["grp_d"] = False
    elif s_type == "grp_c":
        summary_types["grp_a"] = False
        summary_types["grp_b"] = False
        summary_types["grp_c"] = True
        summary_types["grp_d"] = False
    elif s_type == "grp_d":
        summary_types["grp_a"] = False
        summary_types["grp_b"] = False
        summary_types["grp_c"] = False
        summary_types["grp_d"] = True
    else:
        if stat == "true":
            summary_types[s_type] = True
        elif stat == "false":
            summary_types[s_type] = False

    with open('static/task/active_summary_types.json', 'w') as f:
        json.dump(summary_types, f, indent=4)

    return {'summary': 'Status changed.'}, 200


class CrawlImage(Resource):

    @marshal_with(crawl_image_resource_fields)
    def post(self):
        args = crawl_image_post_args.parse_args()
        print('POST: CrawlImage Called')
        url = args['img_url']

        label = get_random_label()
        make_directory(os.getcwd() + "\\Data\\Images")

        if os.path.exists(os.getcwd() + "\\Data\\Images\\CrawledImageList.csv"):
            if not check_in_csv(os.getcwd() + "\\Data\\Images\\CrawledImageList", url, 1):
                write_on_csv(os.getcwd() + "\\Data\\Images\\CrawledImageList", [label, args['img_url']])
                save_image_from_url(label, url, os.getcwd() + "\\Data\\Images\\")
            else:
                print("Already crawled")
                return {'img_url': args['img_url']}, 409
        else:
            write_on_csv(os.getcwd() + "\\Data\\Images\\CrawledImageList", [label, args['img_url']])
            save_image_from_url(label, url, os.getcwd() + "\\Data\\Images\\")

        # save_image_from_url(label, url, os.getcwd() + "\\Data\\Images\\")

        return {'img_url': args['img_url']}, 200


class Screenshot(Resource):

    @marshal_with(screenshot_resource_fields)
    def post(self):
        args = screenshot_post_args.parse_args()
        print('POST: Screenshot Called')
        make_directory(os.getcwd() + "\\Data\\Screenshots")

        image_name = get_random_label()

        image_data = args['imgBase64']
        image_data = image_data[22:]

        write_image(os.getcwd() + "\\Data\\Screenshots\\" + image_name, image_data)
        write_on_csv(os.getcwd() + "\\Data\\image_list", [image_name, args['vis_id'], args['url'], args['date']])

        return {'vis_id': args['vis_id'],
                'url': args['url'],
                'date': args['date'],
                'imgBase64': args['imgBase64']
                }


class AddURL(Resource):

    @marshal_with(url_resource_fields)
    def post(self):
        args = url_post_args.parse_args()
        print('POST: AddURL Called')
        # print(args['iframe_url'])
        # print(args['original_url'])
        make_directory(os.getcwd() + "\\Data")
        write_on_csv(os.getcwd() + "\\Data\\iframe_url", [args['iframe_url'], args['original_url']])

        return {'iframe_url': args['iframe_url'],
                'original_url': args['original_url']
                }


class Deconstruct(Resource):

    @marshal_with(decon_resource_fields)
    def post(self):
        print('POST: Deconstruct Called')
        args = decon_post_args.parse_args()

        deconString = args['decon']
        deconJson = json.loads(deconString)

        status = make_JSON(deconJson)
        if status == "Success":
            return {'decon': args['decon']}, 200
        elif status == "Error":
            return {'decon': args['decon']}, 403

        #
        # return Response("{'decon': args['decon']}", status=201, mimetype='application/json')


def find_json(url):
    csv_file = csv.reader(open('recorded_data.csv', 'r'), delimiter=',')

    for row in csv_file:
        if url == row[3]:
            print(row[4])
            return row[4]

    return False


class SearchHighchart(Resource):

    @marshal_with(search_highchart_resource_fields)
    def post(self):
        print('POST: SearchHighchart Called')
        args = search_highchart_post_args.parse_args()

        out = find_json(args['url'])

        if out is not False:
            return {'json_no': out}, 200
        else:
            return {'json_no': out}, 403


class MultiLineLasso(Resource):

    @marshal_with(multi_line_lasso)
    def post(self):
        print('POST: MultiLineLasso Called')
        args = multi_line_lasso_post_args.parse_args()

        xVals = args['xValues'].replace(' ', '_')
        yVals = args['yValues'].replace(' ', '_')
        lineVals = args['lineValues'].replace(' ', '_')
        xLabel = args['xLabel'].replace(' ', '_')
        yLabel = args['yLabel'].replace(' ', '_')
        chartNumber = args['chartNumber']

        print("chartNumber")
        print(str(chartNumber))

        xValsAr = xVals.split(",")
        yValsAr = yVals.split(",")
        lineValsAr = lineVals.split(",")

        number_of_group = len(set(lineValsAr))

        output_data = []

        # print("str(len(xValsAr))")
        # print(str(len(xValsAr)))
        if len(xValsAr) == 1:
            output_data = "You have selected only 1 point at " + xLabel + " " + str(
                xValsAr[0]) + " where the " + yLabel.replace("_", " ") + " is " + str(yValsAr[0]) + ". "
        else:
            if number_of_group == 1:
                print("SINGLE LINE CHART")
                input_data = single_line_input(xLabel, xValsAr, yLabel, yValsAr)

                output_data = summarize(data=input_data, all_y_label=yLabel, name="Partial", title="Partial",
                                        partial=True)
                if len(input_data) == 0:
                    return {'summary': "Input data could not be prepared"}, 400

                output_data = output_data.replace(". ", ". +")
                print("output_data")
                print(output_data)
            else:
                # IT IS A MULTI LINE CHART
                print("MULTI LINE CHART")
                input_data = multi_line_input(chartNumber, xLabel, xValsAr, lineValsAr)
                # print("input_data")
                # print(input_data)

                if len(input_data) == 0:
                    return {'summary': "Input data could not be prepared"}, 400

                output_data = summarize(data=input_data, all_y_label=yLabel, name="Partial", title="Partial",
                                        partial=True)
                print("output_data")
                print(output_data)

        return {'summary': output_data}, 200


class MultiBarLasso(Resource):

    @marshal_with(multi_bar_lasso)
    def post(self):
        global barVals
        print('POST: MultiBarLasso Called')
        args = multi_bar_lasso_post_args.parse_args()

        xVals = args['xValues']
        yVals = args['yValues']
        if args['barValues'] is not None:
            barVals = args['barValues']
        xLabel = args['xLabel']
        yLabel = args['yLabel']
        chartNumber = args['chartNumber']

        print("chartNumber")
        print(str(chartNumber))

        xValsAr = xVals.split(",")
        yValsAr = yVals.split(",")
        if args['barValues'] is not None:
            barValsAr = barVals.split(",")

            print("barValsAr")
            print(barValsAr)

            if barValsAr[0] == "":
                print("TRUE")

        number_of_group = len(set(barValsAr))
        # print("number_of_group")
        # print(number_of_group)

        print("str(len(xValsAr))")
        print(str(len(xValsAr)))

        output_data = ""

        if len(xValsAr) == 1:
            output_data = "You have selected only 1 point at " + xLabel + " " + str(
                xValsAr[0]) + " where the " + yLabel.replace("_", " ") + " is " + str(yValsAr[0]) + ". "

        else:
            if barValsAr[0] == "":
                print("SINGLE BAR CHART")
                input_data = single_bar_input(xLabel, xValsAr, yLabel, yValsAr)
                print("input_data")
                print(input_data)
                if len(input_data) == 0:
                    return {'summary': "Input data could not be prepared"}, 400
                output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                        title="Partial", partial=True)
                output_data = output_data.replace(". ", ". +")
                print("output_data")
                print(output_data)
            else:
                # IT IS A MULTI LINE CHART
                print("MULTI BAR CHART")
                if len(set(xValsAr)) == 1:
                    print("REPRESENTING A SINGLE BAR CHART")
                    input_data = single_bar_input_from_mutli_bar_data(xLabel, xValsAr, yLabel, yValsAr, barValsAr)
                    print("input_data")
                    print(input_data)
                    if len(input_data) == 0:
                        return {'summary': "Input data could not be prepared"}, 400

                    output_data = "You have selected data points for " + xLabel + " " + xValsAr[0] + ". "
                    output_data += summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                             title="Partial", partial=True)
                    output_data = output_data.replace(". ", ". +")

                    # output_data = "You have selected bars from 1 group at " + xLabel + " " + str(
                    #     xValsAr[0]) + ". Please select at least two groups' data points for the partial summary. "

                    print("output_data")
                    print(output_data)

                else:

                    input_data = multi_bar_input(chartNumber, xLabel, xValsAr, barValsAr)
                    print("input_data")
                    print(input_data)

                    if len(input_data) == 0:
                        return {'summary': "Input data could not be prepared"}, 400

                    output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                            title="Partial", partial=True)
                    print("output_data")
                    print(output_data)

        if output_data is not None:
            return {'summary': output_data}, 200
        else:
            return {'summary': "Partial Summary could not be generated"}, 400


class BarBrush(Resource):

    @marshal_with(bar_brush)
    def post(self):
        global output_data
        print('POST: BarBrush Called')
        args = bar_brush_post_args.parse_args()
        chart = args['chart']
        chartType = args['chartType']
        barValues = args['barValues']
        barValuesAr = barValues.split(",")

        xLabel = args['xLabel']
        yLabel = args['yLabel']
        chartNumber = args['chartNumber']

        if chartType == "single":
            if chart == "bar":
                if len(barValuesAr) == 1:
                    output_data = "You have selected only 1 point at " + xLabel + " " + str(
                        barValuesAr[0]) + ". Please select more points for a summary. "
                else:
                    input_data = single_bar_input_brush(chartNumber, xLabel, yLabel, barValuesAr)
                    print("input_data")
                    print(input_data)

                    if len(input_data) == 0:
                        return {'summary': "Input data could not be prepared"}, 400
                    output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                            title="Partial", partial=True)
                    print("output_data")
                    print(output_data)
            elif chart == "line":
                if len(barValuesAr) == 1:
                    output_data = "You have selected only 1 point at " + xLabel + " " + str(
                        barValuesAr[0]) + ". Please select more points for a summary. "
                else:
                    input_data = single_line_input_brush(chartNumber, xLabel, yLabel, barValuesAr)
                    print("input_data")
                    print(input_data)

                    if len(input_data) == 0:
                        return {'summary': "Input data could not be prepared"}, 400
                    output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                            title="Partial", partial=True)
                    print("output_data")
                    print(output_data)

        elif chartType == "multi":
            if chart == "bar":
                groupNames = args['groupNames']
                groupNamesAr = groupNames.split(",")

                added_text = ""

                if len(barValuesAr) == 1:
                    [input_data, added_text] = multi_bar_input_for_single_brush(chartNumber, xLabel, yLabel,
                                                                                groupNamesAr, barValuesAr[0])
                else:
                    input_data = multi_bar_input_brush(chartNumber, xLabel, groupNamesAr, barValuesAr)

                if len(input_data) == 0:
                    return {'summary': "Input data could not be prepared"}, 400

                output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                        title="Partial", partial=True)
                print("output_data")
                print(output_data)

                if added_text is not None:
                    output_data = added_text + output_data

            elif chart == "line":
                if len(barValuesAr) == 1:
                    output_data = "You have selected only 1 point at " + xLabel + " " + str(
                        barValuesAr[0]) + ". Please select more points for a summary. "
                else:
                    groupNames = args['groupNames']
                    groupNamesAr = groupNames.split(",")

                    print("groupNamesAr")
                    print(groupNamesAr)
                    print("barValuesAr")
                    print(barValuesAr)
                    input_data = multi_line_input_brush(chartNumber, xLabel, groupNamesAr, barValuesAr)
                    print("input_data multi line")
                    print(input_data)

                    if len(input_data) == 0:
                        return {'summary': "Input data could not be prepared"}, 400

                    output_data = summarize(data=input_data, all_y_label=yLabel.replace("_", " "), name="Partial",
                                            title="Partial", partial=True)
                    print("output_data")
                    print(output_data)

        if output_data is not None:
            return {'summary': output_data}, 200
        else:
            return {'summary': "Partial Summary could not be generated"}, 400


class question_response(Resource):

    @marshal_with(question_response_resource_fields)
    def post(self):
        args = question_response_post_args.parse_args()

        time = str(datetime.now())

        data = [args['pid'], args['task'], args['question'], args['answer'], args['time'], time]

        # print(data)

        with open('static/task/responses/question_response' + args['pid'] + '.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        global task_obj
        task_obj = tasks.Tasks(args['pid'])
        task_obj.set_logged_in_true()
        task_obj.set_task_status(args['task'], "DONE")
        task_obj.update_json()

        return {'summary': args['task'] + ' done.'}, 200


class TaskReset(Resource):

    @marshal_with(task_reset)
    def post(self):
        args = task_reset_post_args.parse_args()

        data = {
            'pid': args['pid'],
            'task_name': args['task_name']
        }

        global task_obj
        task_obj = tasks.Tasks(data['pid'])
        task_obj.set_logged_in_true()
        task_obj.set_task_status(data['task_name'], "NOT DONE")
        task_obj.update_json()

        res = data['task_name'] + " has been reset for user# " + data['pid']
        print(res)

        return {'summary': res}, 200


class task_timer(Resource):

    @marshal_with(timer_resource_fields)
    def post(self):
        args = timer_post_args.parse_args()

        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # data = {
        #     'pid': args['pid'],
        #     'taken_time': args['taken_time'],
        #     'time_stamp': dt_string
        # }

        pid = args['pid']
        question_no = args['question_no']
        answer = args['answer']
        taken_time = args['taken_time']

        # header = ['PID', 'Question#', 'Answer', 'Result', 'Time', 'Timestamp']
        data = [args['pid'], args['question_no'], args['answer'], args['result'], args['taken_time'], dt_string]
        #
        #
        # with open('static/task/responses/Timer_' + args['pid'] + '.json', 'w') as f:
        #     json.dump(data, f, indent=4)

        with open('static/task/responses/Timer_' + args['pid'] + '.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            # writer.writerow(header)

            # write the data
            writer.writerow(data)

        res = pid + "'s time has been updated with " + taken_time
        print(res)

        return {'summary': res}, 200


class key_counter(Resource):

    @marshal_with(key_resource_fields)
    def post(self):
        args = key_post_args.parse_args()

        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # header = ['PID', 'Question#', 'Answer', 'Result', 'Time', 'Timestamp']
        data = [args['pid'], args['chart_no'], args['key_presses'], dt_string]

        with open('static/task/responses/key.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        # res = pid+ "'s time has been updated with " + taken_time
        print(dt_string + " : Updated Key Press.")

        return {'summary': "Updated"}, 200


class qna(Resource):

    @marshal_with(qna_resource_fields)
    def post(self):
        args = qna_post_args.parse_args()

        chart_id = args['chart']
        question_text = args['question']

        # f = open('static/generated_new_summary_baseline/' + chart_id + '.json')
        # target_json = json.load(f)

        answer = askMe(chart_id, question_text)

        if answer is None or answer == "":
            answer = "Sorry! SeeChart could not answer!"

        return {'summary': answer}, 200


class search(Resource):

    @marshal_with(search_resource_fields)
    def post(self):
        args = search_post_args.parse_args()

        chart_id = args['chart']
        search_val = args['search_val']
        x_axis = args['x_axis']
        y_axis = args['y_axis']
        graphType = args['graphType']
        columnType = args['columnType']

        found = False

        f = open('static/generated_new_summary_baseline/' + chart_id + '.json')
        target_json = json.load(f)

        # print(x_axis)
        # print(y_axis)

        result_str = ""

        if columnType == "two":

            for a in target_json["data"]:
                if a[x_axis].lower() == search_val.lower():
                    found = True
                    print(a[x_axis])
                    # print(a[y_axis])
                    search_res = a[y_axis]

                    if graphType == "bar":
                        search_res = str(math.floor(int(search_res)))

                    # print(search_res)

                    result_str = "Value of " + x_axis + " " + search_val + " is, " + str(search_res) + ". "

                    break
        else:
            for a in target_json["data"]:
                if a[x_axis].lower() == search_val.lower():
                    found = True
                    print("a[x_axis] -> " + a[x_axis])

                    result_str = "We have multiple values for " + x_axis + " " + search_val + ". These are, "

                    for i in a:
                        if i != x_axis:
                            print(i)
                            result_str += i + " is "
                            print(a[i])
                            result_str += str(a[i]) + ", "

                    # search_res = a[y_axis]
                    #
                    # if graphType == "bar":
                    #     search_res = str(math.floor(int(search_res)))
                    #
                    # print(search_res)

                    break

        if found is True:
            return {'summary': result_str}, 200
        else:
            result_str = "Provided text " + search_val + " is not a valid x axis label. "
            return {'summary': result_str}, 200


api.add_resource(Screenshot, "/getScreenshot")
api.add_resource(AddURL, "/addURL")
api.add_resource(Deconstruct, "/decon")
api.add_resource(SearchHighchart, "/high")
api.add_resource(CrawlImage, "/crawlImage")
api.add_resource(MultiLineLasso, "/multiLineLasso")
api.add_resource(MultiBarLasso, "/multiBarLasso")
api.add_resource(BarBrush, "/multiBarBrush")
api.add_resource(TaskReset, "/reset")
api.add_resource(question_response, "/response")
api.add_resource(task_timer, "/report")
api.add_resource(key_counter, "/key")
api.add_resource(search, "/search")
api.add_resource(qna, "/qna")

# UNCOMMENT THESE TWO LINES TO RUN LOCALLY


if __name__ == "__main__":
    app.run(host='192.168.0.106', port='8080', debug=True, ssl_context=context, threaded=True)
    # app.run(host='127.0.0.1', port='8080', debug=True, ssl_context=context, threaded=True)

# if __name__ == '__main__':
#     # Threaded option to enable multiple instances for multiple user access support
#     app.run(threaded=True, port=5000)
