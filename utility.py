import csv
import os
import shutil
from datetime import datetime
import random
import string
import base64
# from PIL import Image
from io import BytesIO
import json
import requests
import io
from BaselineSummarizer import summarize

url_name = ""


def make_directory(name):
    if os.path.exists(name):
        print("Directory exists already")
    else:
        try:
            os.mkdir(name)
        except OSError:
            print("Creation of the directory %s failed" % name)
        else:
            print("Successfully created the directory %s " % name)


def write_on_csv(name, data):
    with open(name + ".csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def save_image_from_url(label, url, path):
    response = requests.get(url)

    file = open(path + label + ".png", "wb")
    file.write(response.content)
    file.close()


def check_in_csv(path, value, column):
    # print("check_in_csv")
    with open(path + ".csv", "r") as f:
        reader = csv.reader(f)
        for line_num, content in enumerate(reader):
            # print("C O N T E N T :" + content[1])
            if content[column] == value:
                # print(content, line_num + 1)
                return True

    return False


def write_as_JSON(name, data):
    with open(name + '.json', 'w') as outfile:
        # json.dump(data, outfile)
        p_data = json.dumps(data, indent=4, sort_keys=True)
        outfile.write(p_data)


def get_random_label():
    p1 = ''.join(random.choice(string.ascii_letters) for i in range(5))
    p2 = ''.join(random.choice(string.digits) for i in range(5))
    label = p1 + p2
    return label


def write_image(name, imgBase64):
    im = Image.open(BytesIO(base64.b64decode(imgBase64)))
    im.save(name + '.png', 'PNG')


def make_JSON(data):
    # print(len(data['d3data']))
    # print(data['url'])

    name = get_random_label()
    global url_name
    url_name = data['url']
    make_directory(os.getcwd() + "\\Data\\D3JSONData")
    write_on_csv(os.getcwd() + "\\Data\\D3JSONData\\deconstructedPageList", [name, data['url'], data['scrap_date']])
    write_as_JSON(os.getcwd() + "\\Data\\D3JSONData\\" + name + "_RAW", data)

    reshaped_data = reshape_JSON(data)
    if reshaped_data == "Error":
        return "Error"
    else:
        return "Success"


def reshape_JSON(data):
    lenCheck = (data['d3data'])

    chart_type = ""
    x_axis_label = ""
    y_axis_label = ""
    node_id = 0

    # print("C H E C K  L E N G T H --> " + str(len(lenCheck)))

    if len(lenCheck) == 0:
        if os.path.exists(os.getcwd() + "\\Data\\test\\" + "testData.txt"):
            os.remove(os.getcwd() + "\\Data\\test\\" + "testData.txt")
            print("testData.txt deleted")
        if os.path.exists(os.getcwd() + "\\static\\generated\\" + "0_SHAPED.json"):
            # os.remove(os.getcwd() + "\\static\\generated\\" + "0_SHAPED.json")
            folder = os.getcwd() + "\\static\\generated\\"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        print("Error occurred during deletion.")
        return "Error"
    else:
        print("C H E C K  L E N G T H --> " + str(len(lenCheck)))

        for key in range(len(lenCheck)):
            print("K E Y -> " + str(key))
            temp = (data['d3data'][key]['schematized'])
            # temp = (data['d3data'][0]['schematized'])

            axes = []

            chart_found = False

            for i in range(len(temp)):
                if str(temp[i]["markType"]) == "rect":
                    chart_type = "bar"
                    chart_found = True
                    node_id = i
                    temp2 = data['d3data'][key]['schematized'][node_id]['data']
                    for j in temp2:
                        if not j.startswith('_deriv_'):
                            axes.append(j)

                elif str(temp[i]["markType"]) == "circle":
                    chart_type = "line"
                    chart_found = True
                    node_id = i
                    temp2 = data['d3data'][key]['schematized'][node_id]['data']
                    for j in temp2:
                        if not j.startswith('_deriv_'):
                            axes.append(j)

                elif str(temp[i]["markType"]) == "path" and "name" not in temp[i]:
                    # elif str(temp[i]["markType"]) == "path" and len(temp[i]["name"]) == 0:
                    chart_type = "pie"
                    chart_found = True
                    print("Chart type : " + chart_type)

                    node_id = i
                    temp2 = data['d3data'][key]['schematized'][node_id]['data']
                    for j in temp2:
                        if not j.startswith('_deriv_'):
                            axes.append(j)

            if chart_found is False:
                print("Could not identify the chart type")
                return "Error"

            if len(axes) != 0:
                if chart_type == "line" or chart_type == "bar":
                    if axes[0] == "Value":
                        x_axis_label = axes[1]
                        y_axis_label = axes[0]
                    else:
                        x_axis_label = axes[0]
                        y_axis_label = axes[1]

                    temp1 = (data['d3data'][key]['schematized'][node_id]['data'][y_axis_label])
                    temp2 = (data['d3data'][key]['schematized'][node_id]['data'][x_axis_label])

                    dataStr = ""
                    for i in range(len(temp1)):
                        dataStr += x_axis_label.replace(" ", "_") + "|" + str(temp2[i]).replace(" ",
                                                                                                "_") + "|x|" + chart_type + "_chart "
                        dataStr += y_axis_label.replace(" ", "_") + "|" + str(temp1[i]).replace(" ",
                                                                                                "_") + "|y|" + chart_type + "_chart "

                    print(dataStr)

                    name = key + 1

                    summarize(data=dataStr, title="This is a " + chart_type + " chart", name=str(name))

                    # with io.open(os.getcwd() + "/Data/test/testData.txt", "a", encoding="utf-8") as f:
                    #     f.write(dataStr)

                    # return dataStr

                    # tempStr = "{\"data\" : ["
                    #
                    # for i in range(len(temp1)):
                    #     tempStr += "{\""+str(x_axis_label)+"\":\"" + str(temp2[i]) + "\", \""+str(y_axis_label)+"\": \"" + str(temp1[i]) + "\"}"
                    #     if i != len(temp1) - 1:
                    #         tempStr += ","
                    #
                    # tempStr += "]}"
                    #
                    # z = json.loads(tempStr)
                    # y = {"title": "Chart generated from "+url_name}
                    # z.update(y)
                    # y = {"xAxis": x_axis_label}
                    # z.update(y)
                    # y = {"yAxis": y_axis_label}
                    # z.update(y)
                    # y = {"columnType": "two"}
                    # z.update(y)
                    # if chart_type == "bar":
                    #     y = {"graphType": "bar"}
                    #     z.update(y)
                    # elif chart_type == "line":
                    #     y = {"graphType": "line"}
                    #     z.update(y)
                    # y = {"trends": [{"0": "0"}]}
                    # z.update(y)
                    # y = {
                    #     "summary": ["There's no way to really mock up or simulate what I'm doing until I'm there. ",
                    #                 "An exhibition for me is not a statement but an experiment. "]}
                    # z.update(y)
                    # # write_as_JSON(os.getcwd() + "\\static\\generated\\" + str(key) + "_SHAPED", z)
                    #
                    # name = key+1
                    # write_as_JSON(os.getcwd() + "\\static\\generated\\" + str(name), z)
                    # print(json.dumps(z, indent=4, sort_keys=True))
                    #
                    # return z

                elif chart_type == "pie":
                    # PIE PART
                    pie_temp = (data['d3data'][key]['schematized'][node_id]['data']['data'])
                    # print("pie_temp")
                    # print(pie_temp)

                    x = pie_temp[0].values()

                    keys = list(pie_temp[0].keys())

                    category = keys[0]
                    amount = keys[1]

                    pie_str = ""
                    for a in range(len(pie_temp)):
                        pie_str += category + "|" + str(pie_temp[a][category]) + "|x|" + chart_type + "_chart "
                        pie_str += amount + "|" + str(pie_temp[a][amount]) + "|y|" + chart_type + "_chart "

                    # print(pie_str)

                    name = key + 1

                    # with io.open(os.getcwd() + "/Data/test/testData.txt", "a", encoding="utf-8") as f:
                    #     f.write(pie_str)

                    summarize(data=pie_str, title="This is a " + chart_type + " chart", name=str(name))
                    # return pie_str
            else:
                print("This happened")
                return "Error"


def single_line_input(xLabel, xValsAr, yLabel, yValsAr):
    input_data = ""

    for i in range(len(xValsAr)):
        input_data += xLabel + "|" + xValsAr[i] + "|x|line_chart " + yLabel + "|" + yValsAr[i] + "|y|line_chart "

    return input_data


def single_bar_input(xLabel, xValsAr, yLabel, yValsAr):
    input_data = ""

    for i in range(len(xValsAr)):
        input_data += xLabel + "|" + xValsAr[i].replace(' ', '_') + "|x|bar_chart " + yLabel.replace(' ', '_') + "|" + \
                      yValsAr[i].replace(' ', '_') + "|y|bar_chart "

    return input_data


def single_bar_input_from_mutli_bar_data(xLabel, xValsAr, yLabel, yValsAr, barValsAr):
    input_data = ""
    # State_And_Union_Territory | Kerala | x | bar_chart
    # Old - age_dependency_ratio | 19.6 | y | bar_chart
    # State_And_Union_Territory | Punjab | x | bar_chart
    # Old - age_dependency_ratio | 16.1 | y | bar_chart

    barUniqueValsAr = list(dict.fromkeys(barValsAr))  # removes duplicates

    for i in range(len(xValsAr)):
        input_data += "Group" + "|" + barUniqueValsAr[i].replace(' ', '_') + "|x|bar_chart " + yLabel.replace(' ',
                                                                                                              '_') + "|" + \
                      yValsAr[i].replace(' ', '_') + "|y|bar_chart "

    return input_data


def multi_line_input(chartNumber, xLabel, xValsAr, lineValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)
        print(str(len(data["data"])))

        # print(xValsAr)
        # print(lineValsAr)
        xUniqueValsAr = list(dict.fromkeys(xValsAr))  # removes duplicates
        lineUniqueValsAr = list(dict.fromkeys(lineValsAr))  # removes duplicates
        print(xUniqueValsAr)
        print(lineUniqueValsAr)

        numberOfGroup = len(lineUniqueValsAr)

        # keyAr = []
        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in xUniqueValsAr:
                # keyAr.append(i)
                # print(str(data["data"][i][xLabel]))
                input_data += xLabel + "|" + str(data["data"][i][xLabel].replace(' ', '_')) + "|0|line_chart "
                k = 1
                for j in range(len(lineUniqueValsAr)):
                    input_data += str(lineUniqueValsAr[j].replace(' ', '_')) + "|" + str(
                        data["data"][i][lineUniqueValsAr[j]].replace(' ', '_')) + "|" + str(k) + "|line_chart "
                    k = k + 1

        print(input_data)
        return input_data


def multi_bar_input(chartNumber, xLabel, xValsAr, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)

        xUniqueValsAr = list(dict.fromkeys(xValsAr))  # removes duplicates

        xUniqueValsArWithOutUnderscore = []
        for a in range(len(xUniqueValsAr)):
            xUniqueValsArWithOutUnderscore.append(xUniqueValsAr[a].replace("_", " "))

        barUniqueValsAr = list(dict.fromkeys(barValsAr))  # removes duplicates

        numberOfGroup = len(barUniqueValsAr)

        # keyAr = []
        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in xUniqueValsAr or data["data"][i][xLabel] in xUniqueValsArWithOutUnderscore:
                # keyAr.append(i)
                # print(str(data["data"][i][xLabel]))
                input_data += xLabel + "|" + str(data["data"][i][xLabel].replace(' ', '_')) + "|0|bar_chart "
                k = 1
                for j in range(len(barUniqueValsAr)):
                    input_data += str(barUniqueValsAr[j].replace(' ', '_')) + "|" + str(
                        data["data"][i][barUniqueValsAr[j]].replace(' ', '_')) + "|" + str(k) + "|bar_chart "
                    k = k + 1

        print(input_data)
        return input_data


def single_bar_input_brush(chartNumber, xLabel, yLabel, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)

        barValsArWithUnderscore = []
        for a in range(len(barValsAr)):
            barValsArWithUnderscore.append(barValsAr[a].replace(" ", "_"))

        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in barValsAr or data["data"][i][xLabel] in barValsArWithUnderscore:
                input_data += xLabel.replace(" ", "_") + "|" + str(
                    data["data"][i][xLabel].replace(' ', '_')) + "|x|bar_chart " + yLabel.replace(' ', '_') + "|" + str(
                    data["data"][i][yLabel]) + "|y|bar_chart "

        print(input_data)
        return input_data


def single_line_input_brush(chartNumber, xLabel, yLabel, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)

        barValsArWithUnderscore = []
        for a in range(len(barValsAr)):
            barValsArWithUnderscore.append(barValsAr[a].replace(" ", "_"))

        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in barValsAr or data["data"][i][xLabel] in barValsArWithUnderscore:
                input_data += xLabel.replace(" ", "_") + "|" + str(
                    data["data"][i][xLabel].replace(' ', '_')) + "|x|line_chart " + yLabel.replace(' ',
                                                                                                   '_') + "|" + str(
                    data["data"][i][yLabel]) + "|y|line_chart "

        print(input_data)
        return input_data


def multi_bar_input_brush(chartNumber, xLabel, groupNamesAr, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)

        barValsArWithUnderscore = []
        for a in range(len(barValsAr)):
            barValsArWithUnderscore.append(barValsAr[a].replace(" ", "_"))

        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in barValsAr or data["data"][i][xLabel] in barValsArWithUnderscore:
                # keyAr.append(i)
                # print(str(data["data"][i][xLabel]))
                input_data += xLabel + "|" + str(data["data"][i][xLabel].replace(' ', '_')) + "|0|bar_chart "

                # print(str(len(data["data"][i])))

                for k in range(len(data["data"][i]) - 1):
                    print(groupNamesAr[k])
                    print(data["data"][i][groupNamesAr[k]])

                    input_data += groupNamesAr[k].replace(" ", "_") + "|" + str(k + 1) + data["data"][i][
                        groupNamesAr[k]].replace(" ", "_") + "|" + str(k + 1) + "|bar_chart "

    print(input_data)
    return input_data


def multi_bar_input_for_single_brush(chartNumber, xLabel, yLabel, groupNamesAr, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)

        barValsArWithUnderscore = []
        for a in range(len(barValsAr)):
            barValsArWithUnderscore.append(barValsAr[a].replace(" ", "_"))

        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in barValsAr or data["data"][i][xLabel] in barValsArWithUnderscore:
                added_text = "In case of " + xLabel + " " + str(data["data"][i][xLabel]) + ", "
                for k in range(len(data["data"][i]) - 1):
                    input_data += "Group|" + groupNamesAr[k].replace(" ", "_") + "|x|bar_chart "
                    input_data += yLabel + "|" + str(data["data"][i][groupNamesAr[k]]).replace(" ",
                                                                                               "_") + "|y|bar_chart "

    print(input_data)
    return [input_data, added_text]


def multi_line_input_brush(chartNumber, xLabel, groupNamesAr, barValsAr):
    json_path = "/static/generated_new_summary_baseline/" + str(chartNumber) + ".json"

    print("json_path")
    print(json_path)

    with open(os.getcwd() + json_path) as json_file:
        data = json.load(json_file)
        barValsArWithUnderscore = []
        for a in range(len(barValsAr)):
            barValsArWithUnderscore.append(barValsAr[a].replace(" ", "_"))

        input_data = ""

        for i in range(len(data["data"])):
            if data["data"][i][xLabel] in barValsAr or data["data"][i][xLabel] in barValsArWithUnderscore:
                # keyAr.append(i)
                input_data += xLabel + "|" + str(data["data"][i][xLabel].replace(' ', '_')) + "|0|line_chart "
                for k in range(len(data["data"][i]) - 1):
                    input_data += groupNamesAr[k].replace(" ", "_") + "|" + data["data"][i][
                        groupNamesAr[k]].replace(" ", "_") + "|" + str(k + 1) + "|line_chart "

    print(input_data)
    return input_data


# multi_bar_input_for_single_brush(chartNumber=140, xLabel="Community", yLabel="Population", groupNamesAr=[
#     "Male",
#     "Female"
# ], barValsAr="Galicia")

# "Community": "Galicia",
# "Male": "1302611",
# "Female": "1396153"
# Group|Male|x|bar_chart Population|1302611|y|bar_chart Group|Female|x|bar_chart Population|1396153|y|bar_chart


# strtext = multi_bar_input(13, "Actor", [
#     "Roger Moore",
#     "Roger Moore",
#     "Roger Moore",
#     "Daniel Craig",
#     "Daniel Craig"
# ], [
#     "Very favorable",
#     "Somewhat favorable",
#     "Don't know/no opinion",
#     "Very favorable",
#     "Somewhat favorable"
# ])
# #
# output_data = summarize(data=strtext, all_y_label="yLabel", name="Partial", title="Partial", partial=True)
# print("output_data")
# print(output_data)


def try_me():
    # with open(os.getcwd() + "\\Data\\D3JSONData\\"+'IlKrg16739_RAW.json') as json_file:

    pie = "KBsvb60656_RAW"
    bar = "iBkjI44058_RAW"
    line = "UCccq81803_RAW"
    multi = "zNbXO23077"
    test = "mixed"

    with open(os.getcwd() + "\\Data\\D3JSONData\\" + test + '.json') as json_file:
        data = json.load(json_file)

        reshaped_data = reshape_JSON(data)
        if reshaped_data == "Error":
            return "Error"
        else:
            return "Success"

    # mod = reshape_JSON(data)

    # print(json.dumps(data, indent=4, sort_keys=True))

# try_me()
