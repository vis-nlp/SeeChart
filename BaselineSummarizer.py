import \
    json  # Serialization: process of encoding data into JSON format (like converting a Python list to JSON). Deserialization: process of decoding JSON data back into native objects you can work with (like reading JSON data into a Python list)

import math  # To use mathematical functions
import \
    re  # Regular Expression, The functions in this module let you check if a particular string matches a given regular expression
import random  # random number generation. random() function, generates random numbers between 0 and 1.
from random import randint  # randint() is an inbuilt function of the random module in Python3
from statistics import mean, median, \
    stdev  # mean() function can be used to calculate mean/average of a given list of numbers.
from operator import \
    itemgetter  # operator is a built-in module providing a set of convenient operators #operator. itemgetter(n) assumes an iterable object (e.g. list, tuple, set) as input, and fetches the n-th element out of it. If multiple items are specified, returns a tuple of lookup values.
from scipy.stats import \
    linregress  # Calculate a linear least-squares regression for two sets of measurements. Parameters x, yarray_like.
from sklearn import \
    preprocessing  # The sklearn. preprocessing package provides several functions that transform your data before feeding it to the algorithm.
import \
    pandas as pd  # presents a diverse range of utilities, ranging from parsing multiple file formats to converting an entire data table into a NumPy matrix array.
import \
    numpy as np  # NumPy is a general-purpose array-processing package. It provides a high-performance multidimensional array object, and tools for working with these arrays.

dataPath = 'Data/test/testData.txt'
titlePath = 'Data/test/testTitle.txt'
yLabelPath = 'Data/test/all_Y_labels.txt'

# websitePath = 'results/generated_baseline'
websitePath = 'static/generated'  # Folder where the json file is created as the final output
# websitePath = '../TourDeChart/generated'

summaryList = []


def globalTrendBarChart(yValueArr):
    reversed_yValueArr = yValueArr[::-1]  # reversing

    globalDifference = float(reversed_yValueArr[0]) - float(reversed_yValueArr[len(reversed_yValueArr) - 1])
    if reversed_yValueArr[len(reversed_yValueArr) - 1] == 0:
        reversed_yValueArr[len(reversed_yValueArr) - 1] = 1
    globalPercentChange = (globalDifference / float(reversed_yValueArr[len(reversed_yValueArr) - 1])) * 100

    bar_trend = ""

    up_trend = ["increased", "grew", "climbed", "risen"]
    down_trend = ["decreased", "declined", "reduced", "lowered"]
    constant_trend = ["stable", "constant", "unchanged", "unvaried"]

    if globalPercentChange > 0:
        bar_trend = up_trend[random.randint(0, len(up_trend) - 1)]
    elif globalPercentChange < 0:
        bar_trend = down_trend[random.randint(0, len(down_trend) - 1)]
    else:
        bar_trend = "remained " + constant_trend[random.randint(0, len(constant_trend) - 1)]

    return bar_trend


def match_trend(trend1, trend2):
    if trend1 in ["increased", "grew", "climbed", "risen"] and trend2 in ["increased", "grew", "climbed", "risen"]:
        return 1
    elif trend1 in ["decreased", "declined", "reduced", "lowered"] and trend2 in ["decreased", "declined", "reduced",
                                                                                  "lowered"]:
        return 1
    elif trend1 in ["stable", "constant", "unchanged", "unvaried"] and trend2 in ["stable", "constant", "unchanged",
                                                                                  "unvaried"]:
        return 1
    else:
        return 0


def checkIfDuplicates(listOfElems):
    # Check if given list contains any duplicates
    setOfElems = set()
    for elem in listOfElems:
        if elem in setOfElems:
            return True
        else:
            setOfElems.add(elem)
    return False


def most_frequent(List):
    # to find most frequent
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


def getChartType(x):
    if x.lower() == 'year':
        return 'line_chart'
    else:
        return 'bar_chart'


def openCaption(captionPath):
    with open(captionPath, 'r', encoding='utf-8') as captionFile:
        caption = captionFile.read()
    return caption


def openData(dataPath):
    df = pd.read_csv(dataPath)
    cols = df.columns
    size = df.shape[0]
    xAxis = cols[0]
    yAxis = cols[1]
    chartType = getChartType(xAxis)
    return df, cols, size, xAxis, yAxis, chartType


def cleanAxisLabel(label):
    cleanLabel = re.sub('\s', '_', label)
    cleanLabel = cleanLabel.replace('%', '').replace('*', '')
    return cleanLabel


def cleanAxisValue(value):
    # print(value)
    if value == '-' or value == 'nan':
        return '0'
    cleanValue = re.sub('\s', '_', value)
    cleanValue = cleanValue.replace('|', '').replace(',', '').replace('%', '').replace('*', '')
    return cleanValue


def getMagnitude(normalizedSlope):
    magnitude = "slightly"
    # print(normalizedSlope)
    if (abs(normalizedSlope) > 0.75):
        magnitude = "extremely"
    elif (abs(normalizedSlope) > 0.25 and abs(normalizedSlope) <= 0.75):
        magnitude = "moderately"
    else:
        mangitude = "slightly"
    return magnitude


## shehnaz-- The functions created by me

# Initilizing constant values for the fucntions below
# mean_percentArray= 0
# sd_percentArray= 0


# constant_rate = 3.45# avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
# significant_rate = 6.906 # avg(% chnage)*0.1 # Meaning any chnage >constant rate and less than this rate is considered not significant and so it's trend direction is chnaged to the trend of the succesive interval # Determines the start and end of the trend
# rapidly_rate= 57.55
# gradually_rate= 28.77

# constant_rate = mean_percentArray- 1*(sd_percentArray) # avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
# significant_rate = mean_percentArray# avg(% chnage)*0.1 # Meaning any chnage >constant rate and less than this rate is considered not significant and so it's trend direction is chnaged to the trend of the succesive interval # Determines the start and end of the trend
# gradually_rate= mean_percentArray+ 1*(sd_percentArray)
# rapidly_rate= mean_percentArray+ 2*(sd_percentArray)

# meanRefinedSlope= 0
# sdRefinedSlope= 0

# constant_rate = 20# avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
# significant_rate= 40 # avg(% chnage)*0.1 # Meaning any chnage >constant rate and less than this rate is considered not significant and so it's trend direction is chnaged to the trend of the succesive interval # Determines the start and end of the trend
# gradually_rate= 50
# rapidly_rate= 70

# These rate stay constant
constant = 5
sig = 10
gradual = 20
rapid = 70

## These rate chnages dynamically with c_rate and mean(percentChnageArr)
constant_rate = constant
significant_rate = 0
gradually_rate = gradual
rapidly_rate = rapid

c_rate = 0.6  # 0.6 avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
s_rate = 1.2  # 1.2
g_rate = 2  # 2
r_rate = 3  # 3

zigZagNum = 30  # The number of y values there needs for chart to be considered zig zag


def directionTrend(new, old, constant_rate):
    difference = new - old
    if (old != 0):
        percentageChange = ((new - old) / old) * 100
    else:
        old = 0.00000000001
        percentageChange = ((new - old) / old) * 100

    absChnage = abs(percentageChange)
    if (difference > 0 and absChnage > constant_rate):  # if change is significant >5%
        return "increasing"
    elif (difference < 0 and absChnage > constant_rate):
        return "decreasing"
    else:
        return "constant"


def rateOfChnage(refinedPercentChnageArr, direction, c, g, r):
    # new_x= float(new_x)
    # old_x= float(old_x)

    # percentageChange = ((new_y - old_y) / new_x-old_x)

    # # min_val= 0
    # # max_val= 100

    # if (max_val-min_val != 0):
    #     normalized_percentChange= (100*(percentageChange- min_val))/(max_val-min_val)
    # else:
    #     normalized_percentChange= (100*(percentageChange- min_val))/0.00000000001

    constant_rate = c
    gradually_rate = g
    rapidly_rate = r

    absChnage = abs(refinedPercentChnageArr)
    if (direction == "constant"):
        return "roughly"
    elif (absChnage > rapidly_rate):
        return "rapidly"
    elif (absChnage > gradually_rate):
        return "gradually"
    elif (absChnage > constant_rate):
        return "slightly"
    else:
        return "roughly"


def globalDirectionTrend(percent, constant_rate):
    absChnage = abs(percent)
    if (percent > 0 and absChnage > constant_rate):  # if change is significant >5%
        return "increasing"
    elif (percent < 0 and absChnage > constant_rate):
        return "decreasing"
    else:
        return "constant"


def globalRateOfChange(percentChange, c, g, r):
    # new_x= float(new_x)
    # old_x= float(old_x)

    # percentageChange = ((new_y - old_y) / new_x-old_x)

    # # min_val= 0
    # # max_val= 100

    # if (max_val-min_val != 0):
    #     normalized_percentChange= (100*(percentageChange- min_val))/(max_val-min_val)
    # else:
    #     normalized_percentChange= (100*(percentageChange- min_val))/0.00000000001

    constant_rate = c
    gradually_rate = g
    rapidly_rate = r

    absChnage = abs(percentChange)
    if (absChnage > rapidly_rate):
        return "rapidly"
    elif (absChnage > gradually_rate):
        return "gradually"
    elif (absChnage > constant_rate):
        return "slightly"


def percentChnageFunc(new, old):
    difference = new - old
    if (old != 0):
        percentageChange = ((new - old) / old) * 100
    else:
        old = 0.00000000001
        percentageChange = ((new - old) / old) * 100
    return percentageChange


def percentChnageRangeFunc(new, old, maximum):
    difference = new - old
    if (old != 0):
        percentageChange = ((new - old) / (maximum - 0)) * 100
    else:
        old = 0.00000000001
        percentageChange = ((new - old) / (maximum - 0)) * 100
    return percentageChange


def increaseDecrease(x):
    if (x == "increasing"):
        return "increase"
    elif (x == "decreasing"):
        return "decrease"
    else:
        return "stays the same"


def increasedDecreased(x):
    if (x == "increasing"):
        return "increased"
    elif (x == "decreasing"):
        return "decreased"
    else:
        return "remained stable"


def get_indexes(l, val):
    return l.tolist().index(val)


def get_indexes_max_value(l):
    max_value = max(l)  # key=lambda x:float(x))
    return [i for i, x in enumerate(l) if x == max(l)]


def get_indexes_min_value(l):
    min_value = min(l)  # key=lambda x:float(x))
    return [i for i, x in enumerate(l) if x == min(l)]


def stringToFloat(str):
    list = []
    for i in str:
        extractNums = re.findall(r"[-+]?\d*\.\d+|\d+", i)
        num = extractNums[0]
        list.append(num)
    return list


def floatToStr(x):
    for i in range(0, len(x)):
        x[i] = str(x[i])
    return x


def commaAnd(arr):
    if (len(arr) < 2):
        arr = arr[0]
    else:
        slice1 = arr[:len(arr) - 1]
        # print(slice1)
        slice2 = ", ".join(slice1)
        slice2 += ", and " + arr[-1]
        # print(slice2)
        arr = slice2
    return arr


# scaler = preprocessing.MinMaxScaler()
count = 0


# with open(dataPath, 'r', encoding='utf-8') as dataFile, \
#         open(titlePath, 'r', encoding='utf-8') as titleFile:
#
#     fileIterators = zip(dataFile.readlines(), titleFile.readlines())
#     for data, title in fileIterators:

def summarize(data, all_y_label, name, title, partial=None):
    # scaler = preprocessing.MinMaxScaler()
    # count += 1
    datum = data.split()  # Splits data where space is found. So datum[0] is groups of data with no space. e.g. Country|Singapore|x|bar_chart                 `
    # check if data is multi column
    columnType = datum[0].split('|')[
        2].isnumeric()  # e.g. Country|Singapore|x|bar_chart, ...  x means single, numeric means multiline

    # print("Column Type -> " + str(columnType) + " this is -> " + str(datum[0].split('|')[2]))

    # fp = open("all_Y_labels.txt", "a")

    if columnType:  # If MULTI

        # fp.write(str(name) + "\t\n")
        # fp.close()

        y_label = all_y_label

        labelArr = []
        chartType = datum[0].split('|')[3].split('_')[0]

        values = [value.split('|')[1] for value in datum]  # for every datum take the 2nd element

        # find number of columns:
        columnCount = max([int(data.split('|')[2]) for data in
                           datum]) + 1  # The number of categories #for every datum take the 3rd element
        # Get labels
        for i in range(columnCount):
            label = datum[i].split('|')[0].split('_')
            labelArr.append(
                label)  # e.g. "Year|2018|0|line_chart Export|55968.7|1|line_chart Import|108775.3|2|line_chart Year|2017|0|line_chart ==> [['Year'], ['Export'], ['Import']]

        # print(labelArr)

        stringLabels = [' '.join(label) for label in labelArr]  # e.g. stringLabels = ['Year', 'Export', 'Import']

        # Get values
        valueArr = [[] for i in range(columnCount)]
        cleanValArr = [[] for i in range(columnCount)]

        # print("columnCount -> " + str(columnCount))

        # columnCount : how many grouped bars
        # stringLabels : label of X-axis and the individual groups

        groupedLabels = []

        for i in range(len(stringLabels)):
            groupedLabels.append(str(stringLabels[i]).replace('_', ' '))

        # print("groupedLabels")
        # for a in groupedLabels:
        #     print(a)

        a = 0
        b = 0

        groupedCol = int(len(values) / len(stringLabels))

        row = groupedCol
        col = columnCount
        arr = np.empty((row, col),
                       dtype=object)  # creates a martic with rows representing each distinct x value and cols representing y values for different categories/lines (2 in this case)
        # arr[0, 0] = stringLabels[0]

        m = 0
        n = 0

        for b in range(len(values)):
            if n == col:
                m += 1
                n = 0
            if a == len(stringLabels):
                a = 0
            if (b % columnCount) == 0:
                arr[m][b % columnCount] = str(values[b]).replace('_', ' ')
            else:
                num = ""
                for c in values[b]:  # Done for error: could not convert string to float: '290$'
                    if c.isdigit():
                        num = num + c
                arr[m][b % columnCount] = float(num)

            n += 1
            a += 1

        max_row = []
        max_row_val = []
        min_row = []
        min_row_val = []

        number_of_group = len(groupedLabels) - 1

        for i in range(len(groupedLabels) - 1):
            arr1 = arr[arr[:, (i + 1)].argsort()]
            min_row.append(arr1[0][0])
            min_row_val.append(arr1[0][i + 1])
            arr2 = arr[arr[:, (i + 1)].argsort()[::-1]]
            max_row.append(arr2[0][0])
            max_row_val.append(arr2[0][i + 1])

        # print(max_row) # x values at which max occured for each category (e.g. ['2013', '2018'] ==> Export max occured at 2013 and Import at 2018)
        # print(max_row_val) # y values at which max occured for each category (e.g. [91886.1, 108775.3] ==> Export max occured at 91886.1 and Import at 108775.3)
        # print(min_row)
        # print(min_row_val)

        global_max = max(max_row_val)
        global_max_index = get_indexes_max_value(max_row_val)
        global_max_category_label = groupedLabels[global_max_index[0] + 1]
        global_max_category_xlabel = str(max_row[global_max_index[0]])

        if len(groupedLabels) > 3:
            global_2nd_max = sorted(max_row_val)[1]
            global_2nd_max_index = get_indexes_max_value(max_row_val)
            global_2nd_max_category_label = groupedLabels[global_2nd_max_index[0] + 1]
            global_2nd_max_category_xlabel = str(max_row[global_2nd_max_index[0]])

        global_min = min(min_row_val)
        global_min_index = get_indexes_min_value(min_row_val)
        global_min_category_label = groupedLabels[global_min_index[0] + 1]
        global_min_category_xlabel = str(min_row[global_min_index[0]])

        rowCount = round(
            len(datum) / columnCount)  # same as groupedCols or row, with rows representing each distinct x value

        categoricalValueArr = [[] for i in range(rowCount)]

        i = 0
        for n in range(rowCount):
            for m in range(columnCount):
                value = values[i]
                cleanVal = datum[i].split('|')[1].replace('_', ' ')
                valueArr[m].append(value)
                cleanValArr[m].append(cleanVal)
                if m == 0:
                    categoricalValueArr[n].append(cleanVal)
                else:
                    categoricalValueArr[n].append(float(re.sub("[^\d\.]", "", cleanVal)))
                i += 1
        titleArr = title.split()
        # calculate top two largest categories
        summaryArray = []
        dataJson = []
        # iterate over index of a value
        for i in range(len(cleanValArr[0])):
            # iterate over each value
            dico = {}
            for value, label in zip(cleanValArr, labelArr):
                cleanLabel = ' '.join(label)
                dico[cleanLabel] = value[i]
            dataJson.append(dico)

        # HERE

        # print(json.dumps(dataJson, indent=4, sort_keys=True))

        if (chartType == "bar"):

            meanCategoricalDict = {}
            stringLabels.insert(len(stringLabels) - 1, 'and')
            categories = ', '.join(stringLabels[1:-1]) + f' {stringLabels[-1]}'
            # if rowCount > 2:
            for category in categoricalValueArr:
                meanCategoricalDict[category[0]] = mean(category[1:])
            sortedCategories = sorted(meanCategoricalDict.items(), key=lambda x: x[1])

            # print("sortedCategories")
            # print(sortedCategories)

            numerator = abs(sortedCategories[-1][1] - sortedCategories[-2][1])
            denominator = (sortedCategories[-1][1] + sortedCategories[-2][1]) / 2
            topTwoDelta = round((numerator / denominator) * 100, 1)

            numerator1 = abs(sortedCategories[-1][1] - sortedCategories[0][1])
            denominator1 = (sortedCategories[-1][1] + sortedCategories[0][1]) / 2
            minMaxDelta = round((numerator1 / denominator1) * 100, 1)

            group_names = groupedLabels[1:]
            group_names_text = ""

            for a in range(len(group_names)):
                if a == len(group_names) - 1:
                    group_names_text += "and " + group_names[a]
                else:
                    group_names_text += group_names[a] + ", "

            rand_category_index = random.randint(0, number_of_group - 1)
            global_max_min_categorical = []
            global_max_min_categorical.append(
                " For " + str(groupedLabels[0]) + " " + str(max_row[rand_category_index]) + ", " + str(
                    groupedLabels[rand_category_index + 1]) + " had the highest " + y_label + " among all " + str(
                    rowCount) + " " + str(groupedLabels[0]) + "s and it has the lowest " + y_label + " in " + str(
                    groupedLabels[0]) + " " + str(min_row[rand_category_index]) + ". ")
            global_max_min_categorical.append(
                " For " + str(groupedLabels[0]) + " " + str(max_row[rand_category_index]) + ", " + str(groupedLabels[
                                                                                                           rand_category_index + 1]) + " had the maximum " + y_label + " and it saw the lowest in " + str(
                    groupedLabels[0]) + " " + str(min_row[rand_category_index]) + " out of all " + str(
                    rowCount) + " " + str(groupedLabels[0]) + "s. ")
            global_max_min_categorical.append(" Among all the " + str(groupedLabels[0]) + "s, " + str(
                groupedLabels[rand_category_index + 1]) + " had the highest " + y_label + " in " + str(
                groupedLabels[0]) + " " + str(max_row[rand_category_index]) + " and lowest " + y_label + " in " + str(
                groupedLabels[0]) + " " + str(min_row[rand_category_index]) + ". ")
            global_max_min_categorical.append(" Among all the " + str(groupedLabels[0]) + "s, " + str(
                groupedLabels[rand_category_index + 1]) + " had the highest " + y_label + " " + str(
                max_row_val[rand_category_index]) + " in " + str(groupedLabels[0]) + " " + str(
                max_row[rand_category_index]) + " and lowest value " + str(
                min_row_val[rand_category_index]) + " in " + str(groupedLabels[0]) + " " + str(
                min_row[rand_category_index]) + ". ")

            extrema_categorical = global_max_min_categorical[random.randint(0, len(global_max_min_categorical) - 1)]
            print("Extrema [min/max][categorical] : " + global_max_min_categorical[
                random.randint(0, len(global_max_min_categorical) - 1)])

            trend_global = None

            if groupedLabels[0].lower() == "year" or groupedLabels[0].lower() == "years" or groupedLabels[
                0].lower() == "month" or groupedLabels[0].lower() == "months" or groupedLabels[
                0].lower() == "quarter" or groupedLabels[0].lower() == "quarters":
                category_trend = []

                for a in range(1, len(arr[0])):
                    # print(arr[:, a])
                    category_trend.append(globalTrendBarChart(arr[:, a]))

                # print(category_trend)
                categorical_global_trend = []

                if match_trend(category_trend[rand_category_index], category_trend[rand_category_index - 1]):
                    categorical_global_trend.append(" Over the " + str(rowCount) + " " + groupedLabels[
                        0] + "s, the " + y_label + " for both " + str(
                        groupedLabels[rand_category_index + 1]) + " and " + str(
                        groupedLabels[rand_category_index]) + " have " + category_trend[rand_category_index] + ". ")
                    categorical_global_trend.append(
                        " All through the " + groupedLabels[0] + "s, similar trend was observed for " + str(
                            groupedLabels[rand_category_index + 1]) + " and " + str(
                            groupedLabels[rand_category_index]) + ". In both cases, the " + y_label + " have " +
                        category_trend[rand_category_index] + ". ")
                else:
                    categorical_global_trend.append(
                        " Over the " + str(rowCount) + " " + groupedLabels[0] + "s, the " + y_label + " for " + str(
                            groupedLabels[rand_category_index + 1]) + " have been " + category_trend[
                            rand_category_index] + " whereas " + category_trend[
                            rand_category_index - 1] + " for " + str(groupedLabels[rand_category_index]) + ". ")
                    categorical_global_trend.append(
                        " All through the " + groupedLabels[0] + "s, the " + y_label + " for " + str(
                            groupedLabels[rand_category_index + 1]) + " have " + category_trend[
                            rand_category_index] + ". On the other hand, for " + str(
                            groupedLabels[rand_category_index]) + " the " + y_label + " have " + category_trend[
                            rand_category_index - 1] + ". ")

                trend_global = categorical_global_trend[random.randint(0, len(categorical_global_trend) - 1)]
                print("Trend [global] : " + categorical_global_trend[
                    random.randint(0, len(categorical_global_trend) - 1)])

            # sorted_max_row = sorted(max_row_val)
            # print("sorted_max_row")
            # print(sorted_max_row)

            max_gap_abs = 0
            max_gap_rel = 0
            max_gap_index = 0
            for i in range(number_of_group - 1):
                if max_row_val[i] - min_row_val[i] > max_gap_abs:
                    max_gap_abs = max_row_val[i] - min_row_val[i]
                    if min_row_val[i] == 0:
                        min_row_val[i] = 1
                    max_gap_rel = round((max_row_val[i] / min_row_val[i]), 2)
                    max_gap_index = i

            max_diff_all_cat = []
            max_diff_all_cat.append(" Out of all " + str(
                number_of_group) + " groups, the highest gap between the maximum and minimum " + y_label + " was found in case of " + str(
                groupedLabels[max_gap_index + 1]) + ". ")
            max_diff_all_cat.append(" Among the groups, " + str(groupedLabels[
                                                                    max_gap_index + 1]) + " had the biggest difference in " + y_label + ". Where the maximum " + y_label + " was " + str(
                max_gap_rel) + " times larger than the minimum " + y_label + ". ")
            max_diff_all_cat.append(" Among all " + str(number_of_group) + " groups, " + str(
                groupedLabels[max_gap_index + 1]) + " had the gap of " + str(
                max_gap_abs) + " between the maximum and minimum " + y_label + " observed in " + str(
                groupedLabels[0]) + " " + max_row[max_gap_index] + " and " + min_row[max_gap_index] + " respectively. ")

            extrema_max_diff_in_cat = max_diff_all_cat[random.randint(0, len(max_diff_all_cat) - 1)]
            print("Extrema [difference in a category] : " + max_diff_all_cat[
                random.randint(0, len(max_diff_all_cat) - 1)])

            max_min_difference_abs = max_row_val[rand_category_index] - min_row_val[rand_category_index]
            if min_row_val[rand_category_index] != 0:
                max_min_difference_rel = round((max_row_val[rand_category_index] / min_row_val[rand_category_index]), 2)
            else:
                max_min_difference_rel = 0

            diff_in_category = []
            diff_in_category.append(" The maximum " + y_label + " for " + str(
                groupedLabels[rand_category_index + 1]) + " that was found in " + str(groupedLabels[0]) + " " + str(
                max_row[rand_category_index]) + " was " + str(
                max_min_difference_rel) + " times larger than the minimum " + y_label + " observed in " + str(
                groupedLabels[0]) + " " + str(min_row[rand_category_index]) + ". ")
            diff_in_category.append(" There is a gap of " + str(
                max_min_difference_abs) + " between the highest and lowest " + y_label + " found for " + str(
                groupedLabels[rand_category_index + 1]) + " in " + str(groupedLabels[0]) + " " + str(
                max_row[rand_category_index]) + " and " + str(min_row[rand_category_index]) + ". ")
            diff_in_category.append(str(groupedLabels[0]) + " " + str(max_row[rand_category_index]) + " and " + str(
                min_row[rand_category_index]) + " had the biggest gap of " + str(
                max_min_difference_abs) + " between the highest and lowest " + y_label + " found for " + str(
                groupedLabels[rand_category_index + 1]) + ". ")

            comparison_categorical = diff_in_category[random.randint(0, len(diff_in_category) - 1)]
            print("Comparison [categorical] : " + diff_in_category[random.randint(0, len(diff_in_category) - 1)])

            average_stat = []
            average_stat.append("On average, the " + str(groupedLabels[0]) + " " + sortedCategories[-1][
                0] + " had the highest " + y_label + " for all " + str(
                number_of_group) + " groups " + group_names_text + ". Whereas " + sortedCategories[0][
                                    0] + " had the lowest average " + y_label + ". ")
            average_stat.append(
                "Averaging all " + str(number_of_group) + " groups " + group_names_text + ", the " + str(
                    groupedLabels[0]) + " " + sortedCategories[-1][0] + " is the maximum " + y_label + " and " +
                sortedCategories[0][0] + " is the minimum " + y_label + ". ")

            compute_der_val_avg = average_stat[random.randint(0, len(average_stat) - 1)]
            print("Compute derived val [avg] : " + average_stat[random.randint(0, len(average_stat) - 1)])

            global_extrema = []
            global_extrema.append(
                " For " + str(groupedLabels[0]) + " " + str(global_max_category_xlabel) + ", " + str(
                    global_max_category_label) + " had the highest " + y_label + " " + str(
                    global_max) + " among the " + str(
                    number_of_group) + " groups and in " + str(global_min_category_xlabel) + ", " + str(
                    global_min_category_label) + " had the lowest " + y_label + " " + str(global_min) + ". ")
            global_extrema.append(" Out of all " + str(number_of_group) + " groups, " + str(
                global_max_category_label) + " had the highest " + y_label + " for " + str(
                groupedLabels[0]) + " " + str(
                global_max_category_xlabel) + " and " + str(
                global_min_category_label) + " had the lowest " + y_label + " for " + str(groupedLabels[0]) + " " + str(
                global_min_category_xlabel) + ". ")
            global_extrema.append(" " + str(groupedLabels[0]) + " " + str(
                global_max_category_xlabel) + " had the maximum " + y_label + " among all " + str(
                number_of_group) + " groups, and it was for " + str(
                global_max_category_label) + ". The minimum " + y_label + " was observed in " + str(
                groupedLabels[0]) + " " + str(global_min_category_xlabel) + " for " + str(
                global_min_category_label) + ". ")

            extrema_global = global_extrema[random.randint(0, len(global_extrema) - 1)]
            print("Extrema [global] : " + global_extrema[random.randint(0, len(global_extrema) - 1)])
            order_global = []
            if len(groupedLabels) > 3:
                order_global.append(
                    " In case of " + str(groupedLabels[0]) + " " + str(global_max_category_xlabel) + ", " + str(
                        global_max_category_label) + " had the highest " + y_label + " " + str(
                        global_max) + " among the " + str(number_of_group) + " groups and in " + str(
                        global_min_category_xlabel) + ", " + str(
                        global_min_category_label) + " had the lowest " + y_label + " " + str(
                        global_min) + ". The second highest " + y_label + " " + str(
                        global_2nd_max) + " was observed for " + str(global_2nd_max_category_label) + " in " + str(
                        groupedLabels[0]) + " " + str(global_2nd_max_category_xlabel) + ". ")
                order_global.append(
                    " " + str(global_max_category_label) + " had the maximum " + y_label + " out of all " + str(
                        number_of_group) + " groups in " + str(groupedLabels[0]) + " " + str(
                        global_max_category_xlabel) + " followed by " + str(
                        global_2nd_max_category_label) + " in " + str(
                        global_2nd_max_category_xlabel) + ", and the minimum " + y_label + " is found for " + str(
                        global_min_category_label) + " in " + str(global_min_category_xlabel) + ". ")

                order_extrema = order_global[random.randint(0, len(order_global) - 1)]
                print("Order [Extrema(max/min)] : " + order_global[random.randint(0, len(order_global) - 1)])

            x_label = str(stringLabels[0])

            intro = []

            if x_label.lower() == "month" or x_label.lower() == "year" or x_label.lower() == "months" or x_label.lower() == "years":
                intro.append("This is a grouped bar chart showing " + y_label + " on the Y-axis throughout " + str(
                    rowCount) + " " + x_label + "s for " + categories + " on the X-axis. ")
                intro.append(
                    "This grouped bar chart represents " + y_label + " on the Y-axis. And, its value throughout " + str(
                        rowCount) + " " + x_label + "s for " + categories + ". ")
                intro.append(
                    "This grouped bar chart represents " + y_label + " on the Y-axis. And, how the value changed throughout " + str(
                        rowCount) + " " + x_label + "s for " + categories + ". ")
            else:
                intro.append("This grouped bar chart represents " + str(
                    rowCount) + " different " + x_label + "s on X-axis for " + str(
                    number_of_group) + " groups " + categories + ". On the Y-axis it shows their corresponding " + y_label + ". ")
                intro.append("This grouped bar chart shows " + y_label + " on the Y-axis for " + str(
                    rowCount) + " different " + x_label + "s for " + str(
                    number_of_group) + " groups " + categories + " that are presented on the X-axis. ")

            intro_summary = intro[random.randint(0, len(intro) - 1)]

            summary1 = f"This grouped bar chart has {rowCount} categories of {stringLabels[0]} on the x axis representing {str(number_of_group)} groups: {categories}."

            min_summary = []
            mid_summary = []
            max_summary = []

            min_summary.append(random.choice(intro))

            if trend_global is not None:
                min_summary.append(random.choice(categorical_global_trend))
            else:
                min_summary.append(random.choice(global_extrema))

            mid_summary.append(random.choice(intro))
            if trend_global is not None:
                mid_summary.append(random.choice(categorical_global_trend))
                mid_summary.append(random.choice(global_extrema))
                mid_summary.append(random.choice(diff_in_category))

            else:
                mid_summary.append(random.choice(global_extrema))
                mid_summary.append(random.choice(diff_in_category))
                mid_summary.append(random.choice(average_stat))

            max_summary.append(random.choice(intro))
            if trend_global is not None:
                max_summary.append(random.choice(categorical_global_trend))
                max_summary.append(random.choice(global_extrema))
                max_summary.append(random.choice(global_max_min_categorical))
                max_summary.append(random.choice(diff_in_category))
                max_summary.append(random.choice(max_diff_all_cat))
                if len(order_global) != 0:
                    max_summary.append(random.choice(order_global))
                max_summary.append(random.choice(average_stat))

            else:
                max_summary.append(random.choice(global_extrema))
                max_summary.append(random.choice(global_max_min_categorical))
                max_summary.append(random.choice(diff_in_category))
                max_summary.append(random.choice(max_diff_all_cat))
                if len(order_global) != 0:
                    max_summary.append(random.choice(order_global))
                max_summary.append(random.choice(average_stat))

            summary2 = f" Averaging these {str(number_of_group)} groups, the highest category is found for {str(groupedLabels[0])} {sortedCategories[-1][0]} with a mean value of {round(sortedCategories[-1][1], 2)}."

            summaryArray = mid_summary

            maxValueIndex = cleanValArr[0].index(sortedCategories[-1][0])
            secondValueIndex = cleanValArr[0].index(sortedCategories[-2][0])

            trendsArray = [
                {}, {"2": ["0", str(maxValueIndex)], "13": [str(columnCount - 1), str(maxValueIndex)]},
                {"2": ["0", str(secondValueIndex)], "14": [str(columnCount - 1), str(secondValueIndex)]}, {}
            ]
            # elif rowCount == 2:
            #     for category in categoricalValueArr:
            #         meanCategoricalDict[category[0]] = mean(category[1:])
            #     sortedCategories = sorted(meanCategoricalDict.items(), key=lambda x: x[1])
            #     numerator = abs(sortedCategories[-1][1] - sortedCategories[-2][1])
            #     denominator = (sortedCategories[-1][1] + sortedCategories[-2][1]) / 2
            #     topTwoDelta = round((numerator / denominator) * 100, 1)
            #
            #     summary1 = f"This grouped bar chart has {rowCount} categories of {stringLabels[0]} on the x axis representing {str(number_of_group)} groups: {categories}."
            #     summary2 = f" Averaging the {str(number_of_group)} groups, the highest category is found for {str(groupedLabels[0])} {sortedCategories[-1][0]} with a mean value of {round(sortedCategories[-1][1], 2)}."
            #     summaryArray.append(summary1)
            #     summaryArray.append(summary2)
            #     maxValueIndex = cleanValArr[0].index(sortedCategories[-1][0])
            #     secondValueIndex = cleanValArr[0].index(sortedCategories[-2][0])
            #     summary3 = f" The minimum category is found at {sortedCategories[-2][0]} with a mean value of {round(sortedCategories[-2][1], 2)}."
            #     summaryArray.append(summary3)
            #
            #     if topTwoDelta >= 5:
            #         summary4 = f" This represents a difference of {topTwoDelta}%."
            #         summaryArray.append(summary4)
            #
            #     summaryArray.append(chosen_summary)
            #     trendsArray = [
            #         {}, {"2": ["0", str(maxValueIndex)], "13": [str(columnCount - 1), str(maxValueIndex)]},
            #         {"2": ["0", str(secondValueIndex)], "14": [str(columnCount - 1), str(secondValueIndex)]}, {}
            #     ]
            # else:
            #     summary1 = f"This grouped bar chart has 1 category for the x axis of {stringLabels[0]}."
            #     summary2 = f" This category is {stringLabels[1]}, with a mean value of {round(mean(categoricalValueArr[1]), 2)}."
            #     summaryArray.append(summary1)
            #     summaryArray.append(summary2)
            #     summaryArray.append(chosen_summary)
            #     trendsArray = [{}, {"3": ["0", "0"], "9": ["0", "0"]}]
            websiteInput = {"title": title.strip(),
                            "labels": [' '.join(label) for label in labelArr],
                            "columnType": "multi",
                            "graphType": chartType, "summaryType": "baseline", "summary": summaryArray,
                            "xAxis": x_label,
                            "yAxis": y_label,
                            "min_summary": min_summary,
                            "mid_summary": mid_summary,
                            "max_summary": max_summary,
                            "trends": trendsArray,
                            "data": dataJson}
            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)
            # oneFile.writelines(''.join(summaryArray)+'\n')

        # run scatter
        if (chartType == "scatter"):
            stringLabels = [' '.join(label) for label in labelArr]
            print("stringLabels")
            print(stringLabels)

            summaryArray.append("TEST TEST")

            # dataJson = [{xLabel: xVal, yLabel: yVal} for xVal, yVal in zip(cleanXArr, cleanYArr)]

            className = str(stringLabels[0])
            x_label = str(stringLabels[1])
            y_label = str(stringLabels[2])

            dataJson = []
            # iterate over index of a value
            for i in range(len(cleanValArr[0])):
                # iterate over each value
                dico = {}
                for value, label in zip(cleanValArr, labelArr):
                    cleanLabel = ' '.join(label)
                    dico[cleanLabel] = value[i]
                dataJson.append(dico)

            trendsArray = [{}]
            websiteInput = {"title": title,
                            "xAxis": x_label,
                            "yAxis": y_label,
                            "columnType": "two",
                            "graphType": chartType,
                            "class": className,
                            "summaryType": "baseline",
                            "summary": summaryArray,
                            "trends": trendsArray,
                            "data": dataJson}
            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)

        ## for Multi Line charts
        elif (chartType == "line"):
            # clean data
            intData = []
            # print(valueArr)
            # print(valueArr[1:])
            for line in valueArr[1:]:  # take 2nd to end elements in valueArr array
                cleanLine = []
                for data in line:

                    if data.isnumeric():
                        cleanLine.append(float(data))
                    else:
                        cleanData = re.sub("[^\d\.]", "",
                                           data)  # Delete pattern [^\d\.] from data  where [^\d\.] probably denotes digits
                        if len(cleanData) > 0:
                            cleanLine.append(
                                float(cleanData[:4]))  # character from the beginning to position 4 (excluded)
                        else:
                            cleanLine.append(float(cleanData))
                intData.append(cleanLine)
                # print(len(intData))
            # calculate mean for each line
            meanLineVals = []

            # print("stringLabels")
            # print(stringLabels[1:])
            # print("intData")
            # print(intData)
            x_label = str(stringLabels[0])

            assert len(stringLabels[1:]) == len(
                intData)  # tests if a condition is true. If a condition is false, the program will stop with an optional message
            for label, data in zip(stringLabels[1:],
                                   intData):  # zip output: \(('Export', [5596.0, 4562.0, 4875.0, 7140.0, 4325.0, 9188.0, 5565.0, 6574.0, 4827.0, 2945.0, 4252.0, 3876.0, 2867.0, 2404.0]), ('Import', [1087.0, 9410.0, 7853.0, 8865.0, 6917.0, 1034.0, 7262.0, 7509.0, 5715.0, 4458.0, 6268.0, 5996.0, 4299.0, 3742.0]))
                x = (label, round(mean(data), 1))  # round to 1 d.p
                # print(x)
                meanLineVals.append(x)
            sortedLines = sorted(meanLineVals, key=itemgetter(1))
            # print(sortedLines)  # Ranks all the lines from bottomost to topmost using mean values
            # if more than 2 lines
            lineCount = len(labelArr) - 1  # no of categories

            # The line with higest overall mean
            maxLine = sortedLines[-1]  # the category with highest overall mean
            index1 = stringLabels.index(maxLine[0]) - 1  # index for line with max mean
            maxLineData = round(max(intData[index1]), 2)  # the max data point (y axis value) of the line with max mean
            maxXValue = valueArr[0][
                intData[index1].index(maxLineData)]  # the corrsponding x value for the above y value

            # The line with second higest overall mean
            secondLine = sortedLines[-2]  # line with second highest overall mean value
            rowIndex1 = intData[index1].index(
                maxLineData)  # the index for the max y value data point of the line with max mean
            index2 = stringLabels.index(secondLine[0]) - 1  # index for line with second max mean
            secondLineData = round(max(intData[index2]),
                                   2)  # the max data point (y axis value) of the line with max mean
            secondXValue = valueArr[0][
                intData[index2].index(secondLineData)]  ## the corrsponding x value for the above y value
            rowIndex2 = intData[index2].index(
                secondLineData)  # the index for the max y value data point of the line with second max mean

            # The line with the smallest overall mean
            minLine = sortedLines[0]
            index_min = stringLabels.index(minLine[0]) - 1
            minLineData = round(max(intData[index_min]), 2)
            minXValue = valueArr[0][intData[index_min].index(minLineData)]

            line_names = ""
            for i in range(len(stringLabels) - 1):
                if i < len(stringLabels) - 2:
                    line_names += stringLabels[i + 1] + ", "
                else:
                    line_names += "and " + stringLabels[i + 1]
            print(line_names)

            ## New Summary Template-shehnaz
            valueArrMatrix = np.array(valueArr)
            # print(valueArrMatrix)
            # valueArr_CorrectOrder= np.flip(valueArrMatrix, axis=1)

            xVal = valueArrMatrix[0, :]
            # print(xVal)

            yVals = valueArrMatrix[1:, :]
            # print(yVals)

            yVals_float = yVals
            # print(len(yVals))
            for i in range(0, len(yVals)):
                yVals_float[i] = stringToFloat(yVals[i])
            # print(yVals_float)

            yVals = np.array(yVals_float).astype(np.float)  # yVal is now in float type
            # print(yVals)

            coordinates = dict(zip(xVal, zip(*yVals)))
            # print(coordinates)

            sorted_coordinates = dict(sorted(coordinates.items()))
            # for key, value in sorted(coordinates.items()): # Note the () after items!
            #     print(key, value)
            # print("sorted_coordinates")
            # print(sorted_coordinates)

            keys, values = zip(*sorted_coordinates.items())

            # print(keys)
            # print(values)

            arr = []
            for j in range(0, len(values[0])):
                array = []
                for i in range(0, len(values)):
                    array.append(values[i][j])
                arr.append(array)

            # print("keys== xVal")
            # print(keys)
            # print("arr== yVals")
            # print(arr)

            # xVal_sorted = xVal[len(xVal)::-1]

            # yVals_sorted= yVals
            # for i in range(0, len(yVals)):
            #     yVals_sorted[i] = yVals[i][len(yVals[i])::-1]  ## Ordered correctly this time

            xVal_sorted = np.array(keys)
            yVals_sorted = np.array(arr)

            print("Sorted X vals")
            print(xVal_sorted)
            print("Sorted Y vals")
            print(yVals_sorted)

            ###### Order/Rank of all lines

            # print(sortedLines)

            sortedLines_descending = sortedLines[len(sortedLines)::-1]
            # print(sortedLines_descending)

            ###### Topmost Line
            # print(maxLine[0])
            # print(stringLabels.index(maxLine[0]))
            topmostLineIndex = stringLabels.index(maxLine[0]) - 1
            max_yVal_ofTopmost = max(yVals_sorted[topmostLineIndex])
            max_yValIndx_ofTopmost = get_indexes_max_value(yVals_sorted[topmostLineIndex])
            max_xVal_ofTopmost = xVal_sorted[max_yValIndx_ofTopmost]  # Is an array of xVals

            ## To concatenate commas and "and" in max_xVal_ofTopmost
            if (len(max_xVal_ofTopmost) < 2):
                max_xVal_ofTopmost = max_xVal_ofTopmost[0]
            else:
                slice1 = max_xVal_ofTopmost[:len(max_xVal_ofTopmost) - 1]
                # print(slice1)
                slice2 = ", ".join(slice1)
                slice2 += ", and " + max_xVal_ofTopmost[-1]
                # print(slice2)
                max_xVal_ofTopmost = slice2

            meanOfTopmost = mean(yVals_sorted[topmostLineIndex]).round(2)
            # print(meanOfTopmost)

            ###### Bottommost Line
            # print(minLine[0])
            # print(stringLabels.index(minLine[0]))
            bottomostLineIndex = stringLabels.index(minLine[0]) - 1
            max_yVal_ofBotommost = max(yVals_sorted[bottomostLineIndex])
            max_yValIndx_ofBotommost = get_indexes_max_value(yVals_sorted[bottomostLineIndex])
            max_xVal_ofBotommost = xVal_sorted[max_yValIndx_ofBotommost]  # Is an array of xVals

            ## To concatenate commas and "and" in max_xVal_ofTopmost
            if (len(max_xVal_ofBotommost) < 2):
                max_xVal_ofBotommost = max_xVal_ofBotommost[0]
            else:
                slice1 = max_xVal_ofBotommost[:len(max_xVal_ofBotommost) - 1]
                # print(slice1)
                slice2 = ", ".join(slice1)
                slice2 += ", and " + max_xVal_ofBotommost[-1]
                # print(slice2)
                max_xVal_ofBotommost = slice2

            meanOfBotommost = mean(yVals[bottomostLineIndex]).round(2)
            # print(meanOfBotommost)

            # Extrema [max, absolute, allLines]
            ## To find max of all the categories
            maxLocal_array = []
            maxLineNames = []
            maxLine_xVals = []
            num_of_xVals_max = []  # number of x values listed for each line (e.g. Suppose same max val occurred at two lines and one of those lines reached the max val twice. Then maxLine_xVals = [2010, 2013, 2016]) where 2010 and 2013 are for line 1 and 2016 for line 2. So n for line 1 is: 2 and for line 2 is: 1. So num_of_xVals will be [2,1]
            for i in range(0, len(yVals_sorted)):
                max_local = max(yVals_sorted[i])  # key=lambda x:float(x)
                maxLocal_array.append(max_local)

            # max_global= max(maxLocal_array, key=lambda x:float(x))
            # print(max_global)
            # print(maxLocal_array)
            maxLineIndex = get_indexes_max_value(maxLocal_array)  # Line which has the max value

            # print("maxLineIndex")
            # print(maxLineIndex)
            for i in range(0, len(maxLineIndex)):
                maxLineName = stringLabels[maxLineIndex[i] + 1]
                maxLineNames.append(maxLineName)
                # print(valueArr[maxLineIndex[i]+1])

                maxValIndex = get_indexes_max_value(
                    yVals_sorted[maxLineIndex[i]])  # Index at which the max value occurred for that line
                n = 0
                for j in range(0, len(maxValIndex)):
                    maxLine_xVal = xVal_sorted[maxValIndex[j]]
                    maxLine_xVals.append(maxLine_xVal)
                    n = n + 1
                num_of_xVals_max.append(n)
            # print(valueArr)

            maxLineNames = commaAnd(maxLineNames)
            maxLine_xVals = commaAnd(maxLine_xVals)

            minLocal_array = []
            minLineNames = []
            minLine_xVals = []
            num_of_xVals_min = []  # number of x values listed for each line (e.g. Suppose same max val occurred at two lines and one of those lines reached the max val twice. Then maxLine_xVals = [2010, 2013, 2016]) where 2010 and 2013 are for line 1 and 2016 for line 2. So n for line 1 is: 2 and for line 2 is: 1. So num_of_xVals will be [2,1]
            for i in range(0, len(yVals_sorted)):
                min_local = min(yVals_sorted[i])  # key=lambda x:float(x)
                minLocal_array.append(min_local)

            # max_global= max(maxLocal_array, key=lambda x:float(x))
            # print(max_global)
            # print(maxLocal_array)
            minLineIndex = get_indexes_min_value(minLocal_array)  # Line which has the max value

            # print("maxLineIndex")
            # print(maxLineIndex)
            for i in range(0, len(minLineIndex)):
                minLineName = stringLabels[minLineIndex[i] + 1]
                minLineNames.append(minLineName)
                # print(valueArr[maxLineIndex[i]+1])

                minValIndex = get_indexes_min_value(
                    yVals_sorted[minLineIndex[i]])  # Index at which the max value occurred for that line
                n = 0
                for j in range(0, len(minValIndex)):
                    minLine_xVal = xVal_sorted[minValIndex[j]]
                    minLine_xVals.append(minLine_xVal)
                    n = n + 1
                num_of_xVals_min.append(n)
            # print(valueArr)

            minLineNames = commaAnd(minLineNames)
            minLine_xVals = commaAnd(minLine_xVals)

            ############# GlobalTrend ##############
            direction = []
            rate = []

            for i in range(0, len(yVals_sorted)):
                n = float(yVals_sorted[i][len(yVals_sorted[i]) - 1])
                o = float(yVals_sorted[i][0])
                m = max(maxLocal_array)
                globalPercentChange = percentChnageRangeFunc(n, o, m)
                rate.append(globalPercentChange)

                d = globalDirectionTrend(globalPercentChange, constant)

                direction.append(d)

            lineNames = stringLabels[1:]
            # print(lineNames)
            # print(direction)
            # print(rate)

            lineNames_increasing = []
            lineNames_decreasing = []
            lineNames_constant = []
            for i in range(0, len(direction)):
                if (direction[i] == "increased"):
                    lineNames_increasing.append(lineNames[i])
                elif (direction[i] == "decreased"):
                    lineNames_decreasing.append(lineNames[i])
                else:
                    lineNames_constant.append(lineNames[i])

            # print(lineNames_increasing)
            # print(lineNames_decreasing)
            # print(lineNames_constant)

            if (len(lineNames) == 2):

                difference_arr = []
                if (len(yVals_sorted) == 2):
                    for i in range(0, len(xVal_sorted)):
                        diff = yVals_sorted[0][i] - yVals_sorted[1][i]
                        difference_arr.append(diff)
                # print(difference_arr)

                abs_difference_arr = []
                for i in range(0, len(difference_arr)):
                    abs_difference_arr.append(abs(difference_arr[i]))
                # print(abs_difference_arr)

                constant_rate = 5
                diffPercentChange = percentChnageFunc(abs_difference_arr[-1], abs_difference_arr[0])
                diff_direction = directionTrend(abs_difference_arr[-1], abs_difference_arr[0], constant_rate)
                # print(diffPercentChange)
                # print(diff_direction)

                if (diff_direction == "increasing"):
                    diff_direction = "greater"
                elif (diff_direction == "decreasing"):
                    diff_direction = "smaller"
                else:
                    diff_direction = "roughly same"

                # Find and report the max and the min gap between two Lines
                max_diff = max(abs_difference_arr)
                max_diff_indx = get_indexes_max_value(abs_difference_arr)

                min_diff = min(abs_difference_arr)
                min_diff_indx = get_indexes_min_value(abs_difference_arr)

            # Global Trends with rate of change

            globalTrends = []
            # print(constant)
            # print(gradual)
            # print(rapid)
            for i in rate:
                rate = globalRateOfChange(i, constant, gradual, rapid)
                globalTrends.append(rate)
            # print(globalTrends)

            lineNames = stringLabels[1:]
            # print(lineNames)
            # print(direction)
            # print(rate)
            # print(globalTrends)

            lineNames_increasing_r = []
            lineNames_increasing_g = []

            lineNames_decreasing_r = []
            lineNames_decreasing_g = []

            lineNames_constant_c = []

            for i in range(0, len(direction)):
                if (direction[i] == "increasing"):
                    if (globalTrends[i] == "rapidly"):
                        lineNames_increasing_r.append(lineNames[i])
                    else:
                        lineNames_increasing_g.append(lineNames[i])
                elif (direction[i] == "decreasing"):
                    if (globalTrends[i] == "rapidly"):
                        lineNames_decreasing_r.append(lineNames[i])
                    else:
                        lineNames_decreasing_g.append(lineNames[i])
                else:
                    lineNames_constant_c.append(lineNames[i])

            # Zig zag
            zig_zagLines = []
            if (len(lineNames_increasing_r) != 0):
                zig_zagLines.append(lineNames_increasing_r)
            if (len(lineNames_increasing_g) != 0):
                zig_zagLines.append(lineNames_increasing_g)
            if (len(lineNames_decreasing_r) != 0):
                zig_zagLines.append(lineNames_decreasing_r)
            if (len(lineNames_decreasing_g) != 0):
                zig_zagLines.append(lineNames_decreasing_g)

            zig_zagLineNames = []
            for i in range(0, len(zig_zagLines)):
                for j in range(0, len(zig_zagLines[i])):
                    zig_zagLineNames.append(zig_zagLines[i][j])
            # print("zig_zagLineNames" + str(zig_zagLineNames))

            # For rapidly incresing lines report percentage increase or factor of increase
            percentChng_in = []
            factorChng_in = []

            if (len(lineNames_increasing_r) != 0):
                for i in range(0, len(lineNames_increasing_r)):
                    indx = lineNames.index(lineNames_increasing_r[i])
                    n = float(yVals_sorted[indx][len(yVals_sorted[indx]) - 1])
                    o = float(yVals_sorted[indx][0])
                    if (o == 0):
                        o = 0.00000000001

                    if (n == 0):
                        n = 0.00000000001

                    p = abs(percentChnageFunc(n, o))

                    # Factor
                    if (n != 0.00000000001 and o != 0.00000000001):
                        if (n > o):
                            f = round(n / o, 1)
                        else:
                            f = round(o / n, 1)
                        factorChng_in.append(f)

                    percentChng_in.append(p)

            # print("percentChng_in:   " + str(percentChng_in))
            # print("factorChng_in:   " + str(factorChng_in))

            # For rapidly decreasing lines report percentage decrease or factor of decrease
            percentChng_de = []
            factorChng_de = []

            if (len(lineNames_decreasing_r) != 0):
                for i in range(0, len(lineNames_decreasing_r)):
                    indx = lineNames.index(lineNames_decreasing_r[i])
                    n = float(yVals_sorted[indx][len(yVals_sorted[indx]) - 1])
                    o = float(yVals_sorted[indx][0])

                    if (o == 0):
                        o = 0.00000000001
                    if (n == 0):
                        n = 0.00000000001

                    p = abs(percentChnageFunc(n, o))

                    # Factor
                    if (n != 0.00000000001 and o != 0.00000000001):
                        if (n > o):
                            f = round(n / o, 1)
                        else:
                            f = round(o / n, 1)
                        factorChng_in.append(f)

                    percentChng_de.append(p)

            # print(percentChng_de)
            # print(factorChng_de)

            percentChngSumm = ""
            factorChngSumm = ""

            # print("percentChng_in:     " + str(percentChng_in))
            print(percentChng_in)
            print(factorChng_in)

            # for i in range(0, len(percentChng_in)):
            #     percentChng_in[i]= str(percentChng_in[i])
            # print(percentChng_in)

            percentChng_in = floatToStr(percentChng_in)
            if (bool(factorChng_in)):
                factorChng_in = floatToStr(factorChng_in)
            percentChng_de = floatToStr(percentChng_de)
            if (bool(factorChng_de)):
                factorChng_de = floatToStr(factorChng_de)

            print(percentChng_in)
            print(factorChng_in)

            # Line that are rapidly increasing
            if (len(lineNames_increasing_r) > 1):
                percentChngSumm += commaAnd(lineNames_increasing_r) + " has increased by " + commaAnd(
                    percentChng_in) + " percent respectively. "
                if (len(factorChng_in) != 0):
                    factorChngSumm += commaAnd(lineNames_increasing_r) + " has increased by " + commaAnd(
                        factorChng_in) + " times respectively. "  # globalTrendRate_summary.append(summary_increasing_r)
            elif (len(lineNames_increasing_r) == 1):
                percentChngSumm += commaAnd(lineNames_increasing_r) + " has increased by " + commaAnd(
                    percentChng_in) + " percent. "
                if (len(factorChng_in) != 0):
                    factorChngSumm += commaAnd(lineNames_increasing_r) + " has increased by " + commaAnd(
                        factorChng_in) + " times. "
                # globalTrendRate_summary.append(summary_increasing_r)

            # Line that are rapidly decreasing
            if (len(lineNames_decreasing_r) > 1):
                percentChngSumm += commaAnd(lineNames_decreasing_r) + " has decreased by " + commaAnd(
                    percentChng_de) + " percent respectively. "
                if (len(factorChng_de) != 0):
                    factorChngSumm += commaAnd(lineNames_decreasing_r) + " has decreased by " + commaAnd(
                        factorChng_de) + " times respectively. "
                # globalTrendRate_summary.append(summary_increasing_r)
            elif (len(lineNames_decreasing_r) == 1):
                percentChngSumm += commaAnd(lineNames_decreasing_r) + " has decreased by " + commaAnd(
                    percentChng_de) + " percent. "
                if (len(factorChng_de) != 0):
                    factorChngSumm += commaAnd(lineNames_decreasing_r) + " has decreased by " + commaAnd(
                        factorChng_de) + " times. "
                # globalTrendRate_summary.append(summary_increasing_r)

            # print("percentChngSumm: " + str(percentChngSumm))
            # print("factorChngSumm: ", str(factorChngSumm))

            if (len(factorChngSumm) == 0):
                selectedChange = percentChngSumm
            else:
                chnageFactor = [percentChngSumm, factorChngSumm]
                selectedChange = random.choice(chnageFactor)
            # print("selectedChange:   " + str(selectedChange))

            # PRINT SUMMARY

            # Done by Shehnaz
            summaryArr = []
            summary1 = []
            summary1.append("This is a multi-line chart with " + str(
                lineCount) + " lines representing " + line_names + ". " + "The y axis denotes " + y_label + " and the x axis denotes " + x_label + ". ")
            summary1.append("The given chart is of multi-line type with " + str(
                lineCount) + " lines namely " + line_names + ". " + "The y axis represents " + y_label + " and the x axis represents " + x_label + ". ")
            summary1.append("You are viewing a chart of multi-line type with " + str(
                lineCount) + " lines denoting " + line_names + ". " + "The y axis indicates the " + y_label + " and the x axis indicates " + x_label + ". ")
            # summary2 = "The line for " + str(maxLine[0]) + " has the highest values across " + str(
            #     stringLabels[0]) + " with a mean value of " + str(maxLine[1]) + ", "
            summaryArr.append(random.choice(summary1))

            ###### Global Trends with Rate of chnage
            globalTrendRate_summary = "Overall "

            # Lines that rapidly increase
            # summary_increasing_r= ""
            if (len(lineNames_increasing_r) > 1):
                globalTrendRate_summary += commaAnd(lineNames_increasing_r) + " are rapidly increasing, "
                # globalTrendRate_summary.append(summary_increasing_r)
            elif (len(lineNames_increasing_r) == 1):
                globalTrendRate_summary += commaAnd(lineNames_increasing_r) + " is rapidly increasing, "
                # globalTrendRate_summary.append(summary_increasing_r)

            # Lines that gradually increase
            # summary_increasing_g= ""
            if (len(lineNames_increasing_g) > 1):
                globalTrendRate_summary += commaAnd(lineNames_increasing_g) + " are gradually increasing, "
                # globalTrendRate_summary.append(summary_increasing_g)
            elif (len(lineNames_increasing_g) == 1):
                globalTrendRate_summary += commaAnd(lineNames_increasing_g) + " is gradually increasing, "
                # globalTrendRate_summary.append(summary_increasing_g)

            # Lines that rapidly decrease
            # summary_decreasing_r= ""
            if (len(lineNames_decreasing_r) > 1):
                globalTrendRate_summary += commaAnd(lineNames_decreasing_r) + " are rapidly decreasing, "
                # globalTrendRate_summary.append(lineNames_decreasing_r)
            elif (len(lineNames_decreasing_r) == 1):
                globalTrendRate_summary += commaAnd(lineNames_decreasing_r) + " is rapidly decreasing, "
                # globalTrendRate_summary.append(lineNames_decreasing_r)

            # Lines that gradually decrease
            # summary_decreasing_g= ""
            if (len(lineNames_decreasing_g) > 1):
                globalTrendRate_summary += commaAnd(lineNames_decreasing_g) + " are gradually decreasing, "
                # globalTrendRate_summary.append(lineNames_decreasing_g)
            elif (len(lineNames_decreasing_g) == 1):
                globalTrendRate_summary += commaAnd(lineNames_decreasing_g) + " is gradually decreasing, "
                # globalTrendRate_summary.append(lineNames_decreasing_g)

            # Lines that stay constant
            # summary_constant_c= ""
            if (len(lineNames_constant_c) > 1):
                globalTrendRate_summary += commaAnd(lineNames_constant_c) + " are roughly constant, "
                # globalTrendRate_summary.append(summary_constant_c)
            elif (len(lineNames_constant_c) == 1):
                globalTrendRate_summary += commaAnd(lineNames_constant_c) + " is roughly constant, "
                # globalTrendRate_summary.append(summary_constant_c)

            globalTrendRate_summary += " throughout the " + stringLabels[0] + ". "
            summaryArr.append(globalTrendRate_summary)

            ##Zig Zag
            ## If >zigZagNum points and lines not constant then they are considered zig zag
            sum_zigzag_arr = []
            if (len(yVals_sorted[0]) > zigZagNum and len(zig_zagLineNames) != 0):
                sum_zigzag = str(commaAnd(zig_zagLineNames)) + " has in general many fluctuations."
                sum_zigzag_arr.append(sum_zigzag)
                sum_zigzag = "The lines" + str(commaAnd(zig_zagLineNames)) + " in general has a zig zag shape."
                sum_zigzag_arr.append(sum_zigzag)
                summaryArr.append(random.choice(sum_zigzag_arr))

            #### Order/Ranking of all lines given total no of lines is < 5
            sum_rank_arr = []
            if (len(sortedLines_descending) < 5):  # Given there are no more than 5 lines
                summary_rank1 = "The ranking of the lines from topmost to botommmost is as follows: "
                for i in range(0, len(sortedLines_descending) - 1):
                    summary_rank1 += str(i + 1) + ", " + sortedLines_descending[i][0] + ", "
                summary_rank1 += "and lastly, " + str(len(sortedLines_descending)) + ", " + \
                                 sortedLines_descending[len(sortedLines_descending) - 1][0] + ". "
                sum_rank_arr.append(summary_rank1)

                # 2nd Version of wording the sentence
                summary_rank2 = "The lines ordered according to average values of " + y_label + " in descending order is: "
                for i in range(0, len(sortedLines_descending) - 1):
                    summary_rank2 += str(i + 1) + ", " + sortedLines_descending[i][0] + ", "
                summary_rank2 += "and lastly, " + str(len(sortedLines_descending)) + ", " + \
                                 sortedLines_descending[len(sortedLines_descending) - 1][0] + ". "

                sum_rank_arr.append(summary_rank2)
                # Choose randomly between 2 versions
                summaryArr.append(random.choice(sum_rank_arr))

                ## Talks about the topmost line
            summary2 = []
            summary2.append("During this period, " + str(maxLine[
                                                             0]) + " generally had the highest " + y_label + " relative to others" + " with an average of " + str(
                meanOfTopmost) + ", and it reached its maximum at " + str(
                max_xVal_ofTopmost) + " with a value of " + str(
                max_yVal_ofTopmost) + ". ")  # revised

            # Version 2
            summary2.append("Overall across the " + stringLabels[0] + ", " + str(maxLine[
                                                                                     0]) + " mostly maintained the highest " + y_label + " when compared to others" + " with a mean value of " + str(
                meanOfTopmost) + ", and it peaked at " + str(max_xVal_ofTopmost) + ". ")

            summaryArr.append(random.choice(summary2))

            ## Talks about the second topmost line
            summ_2top_arr = []
            if lineCount > 2:
                summary4 = "After " + str(maxLine[0]) + ", " + str(
                    secondLine[0]) + " overall has the second highest values " + ", with a mean value of " + str(
                    secondLine[1]) + ", peaking at " + str(secondXValue) + ". "
                summ_2top_arr.append(summary4)

                # Version 2
                summary4 = "Followed by " + str(
                    secondLine[0]) + " which ranks as the second topmost line " + ", with an average of " + str(
                    secondLine[1]) + " " + y_label + ",reaching its highest point  at " + str(
                    secondXValue) + " with a value of " + str(secondLineData) + ". "
                summ_2top_arr.append(summary4)

                summaryArr.append(random.choice(summ_2top_arr))

            ## Talks about the bottomost line
            sum_bottom_arr = []
            summary6 = str(minLine[0]) + " mostly had the least " + y_label + " with a mean value of " + str(
                meanOfBotommost) + ", which peaked at " + str(max_xVal_ofBotommost) + " with a value of " + str(
                max_yVal_ofBotommost) + ". "
            sum_bottom_arr.append(summary6)

            # 2nd version
            summary6 = "The bottommost line, " + str(minLine[0]) + ", " + " has a mean of " + str(
                meanOfBotommost) + ", and peaked at " + str(max_xVal_ofBotommost) + ". "
            sum_bottom_arr.append(summary6)

            summaryArr.append(random.choice(sum_bottom_arr))

            # Additional summaries -shehnaz

            # Global Max
            sum_max_arr = []
            if (max_yVal_ofTopmost != max(maxLocal_array) and len(maxLine_xVals) < 5):
                summary8 = maxLineNames + " reported the highest " + y_label + " about " + str(
                    max(maxLocal_array)) + " in " + stringLabels[0] + " " + maxLine_xVals
                sum_max_arr.append(summary8)

                # 2nd Version
                summary8 = "The maximum " + y_label + " about " + str(
                    max(maxLocal_array)) + "," + " occured at " + maxLine_xVals + " by " + maxLineNames + ". "
                sum_max_arr.append(summary8)

                summaryArr.append(random.choice(sum_max_arr))

            # Global Min
            sum_min_arr = []
            if (len(minLine_xVals) < 5):  # given no more than 5 x values are reported
                summary9 = minLineNames + " reported the lowest " + y_label + " about " + str(
                    min(minLocal_array)) + " in " + stringLabels[0] + " " + minLine_xVals
                sum_min_arr.append(summary9)

                # Version 2
                summary9 = "The minimum " + y_label + " about " + str(
                    min(minLocal_array)) + "," + " occured at " + minLine_xVals + " by " + minLineNames + ". "
                sum_min_arr.append(summary9)

                summaryArr.append(random.choice(sum_min_arr))

            #### Global Trend without rate

            # #Lines that increase
            # summary_increasing= "Overall "
            # if (len(lineNames_increasing)>1):
            #     summary_increasing+= commaAnd(lineNames_increasing) + " are increasing throughout the " + stringLabels[0]
            #     summaryArr.append(summary_increasing)
            # elif(len(lineNames_increasing)==1):
            #     summary_increasing+= commaAnd(lineNames_increasing) + "is increasing throughout the " + stringLabels[0]
            #     summaryArr.append(summary_increasing)

            # #Lines that decrease
            # summary_decreasing= "Overall "
            # if (len(lineNames_decreasing)>1):
            #     summary_decreasing+= commaAnd(lineNames_decreasing) + " are decreasing throughout the " + stringLabels[0]
            #     summaryArr.append(summary_decreasing)
            # elif(len(lineNames_decreasing)==1):
            #     summary_decreasing+= commaAnd(lineNames_decreasing) + "is decreasing throughout the " + stringLabels[0]
            #     summaryArr.append(summary_decreasing)

            # # Lines that stay constant
            # summary_constant= "Overall "
            # if (len(lineNames_constant)>1):
            #     summary_constant+= commaAnd(lineNames_constant) + " are roughly constant throughout the " + stringLabels[0]
            #     summaryArr.append(summary_constant)
            # elif(len(lineNames_constant)==1):
            #     summary_constant+= commaAnd(lineNames_constant) + "is roughly constant throughout the " + stringLabels[0]
            #     summaryArr.append(summary_constant)

            # Comparison

            # Randomly picking abosolute vs relative comparison
            # Append randomly the factor of chnage given the chnage was rapid
            if (len(lineNames_increasing_r) != 0 or len(lineNames_decreasing_r) != 0):
                summaryArr.append(selectedChange)

            # Gap

            ###### The gap between two lines
            summary_Gap = []
            if (len(lineNames) == 2):
                summary10 = "The difference of " + y_label + " between " + lineNames[0] + " and " + lineNames[
                    1] + " is " + diff_direction + " at " + stringLabels[0] + " " + xVal_sorted[
                                -1] + " compared to the " + stringLabels[0] + " " + xVal_sorted[0] + ". "
                summary_Gap.append(summary10)

                summary11 = "The greatest difference of " + y_label + " between " + lineNames[0] + " and " + \
                            lineNames[1] + " occurs at " + stringLabels[0] + " " + str(
                    xVal_sorted[max_diff_indx[0]]) + " and the smallest difference occurs at " + str(
                    xVal_sorted[min_diff_indx[0]]) + ". "  # Assumes there is only one max and min gap or difference
                summary_Gap.append(summary11)

                summaryArr.append(random.choice(summary_Gap))

            # print("summary_Gap" + str(summary_Gap))

            ####### Min, Mid, Max Summaries

            # Minimum Summary
            min_summary = []  # Minimum length summary
            mid_summary = []  # Medium length summary
            max_summary = []  # Maximum length summary

            min_summary.append(random.choice(summary1))  # intro
            min_summary.append(globalTrendRate_summary)  # Global Trend
            min_summary.append(random.choice(summary2))  # Topmost
            if (len(summ_2top_arr) != 0):
                min_summary.append(random.choice(summ_2top_arr))  # Second Topmost
            min_summary.append(random.choice(sum_bottom_arr))  # Botommost
            if (len(sum_zigzag_arr) != 0):
                min_summary.append(random.choice(sum_zigzag_arr))  # Zig Zag

            # print( "min_summary" + str(min_summary) + "/n")

            # Medium Summary
            mid_summary.append(random.choice(summary1))  # intro
            mid_summary.append(globalTrendRate_summary)  # Global Trend
            if (len(lineNames_increasing_r) != 0 or len(lineNames_decreasing_r) != 0):
                mid_summary.append(selectedChange)  # Comparison
            if (len(sum_rank_arr) != 0):
                mid_summary.append(random.choice(sum_rank_arr))  # Order/Rank
            mid_summary.append(random.choice(summary2))  # Topmost
            if (len(summ_2top_arr) != 0):
                mid_summary.append(random.choice(summ_2top_arr))  # Second Topmost
            mid_summary.append(random.choice(sum_bottom_arr))  # Botommost
            if (len(sum_zigzag_arr) != 0):
                mid_summary.append(random.choice(sum_zigzag_arr))  # Zig Zag

            # print( "mid_summary" + str(mid_summary) + "/n")

            # Maximum Summary
            max_summary.append(random.choice(summary1))  # intro
            max_summary.append(globalTrendRate_summary)  # Global Trend
            if (len(lineNames_increasing_r) != 0 or len(lineNames_decreasing_r) != 0):
                max_summary.append(selectedChange)  # Comparison
            if (len(sum_rank_arr) != 0):
                max_summary.append(random.choice(sum_rank_arr))  # Order/Rank
            max_summary.append(random.choice(summary2))  # Topmost
            if (len(summ_2top_arr) != 0):
                max_summary.append(random.choice(summ_2top_arr))  # Second Topmost
            max_summary.append(random.choice(sum_bottom_arr))  # Botommost
            if (len(sum_max_arr) != 0):
                max_summary.append(random.choice(sum_max_arr))  # Global Max
            if (len(sum_min_arr) != 0):
                max_summary.append(random.choice(sum_min_arr))  # Global Min
            if (len(sum_zigzag_arr) != 0):
                max_summary.append(random.choice(sum_zigzag_arr))  # Zig Zag
            if (len(summary_Gap) != 0):
                max_summary.append(random.choice(summary_Gap))  # Gap (if 2 lines only )

            print("max_summary" + str(max_summary) + "/n")

            summaryArray = mid_summary

            trendsArray = [{},
                           {"2": ["0", str(index1)], "16": [str(rowCount - 1), str(index1)]},
                           {"1": [str(rowIndex1), str(index1)], "9": [str(rowIndex1), str(index1)]},
                           {"2": ["0", str(index2)], "15": [str(rowCount - 1), str(index2)]},
                           {"1": [str(rowIndex2), str(index2)], "10": [str(rowIndex2), str(index2)]}
                           ]
            websiteInput = {"title": title.strip(),
                            "labels": [' '.join(label) for label in labelArr],
                            "columnType": "multi",
                            "graphType": chartType, "summaryType": "baseline", "summary": summaryArray,
                            "xAxis": x_label,
                            "yAxis": y_label,
                            "min_summary": min_summary,
                            "mid_summary": mid_summary,
                            "max_summary": max_summary,
                            "trends": trendsArray,
                            "data": dataJson}

            # print(summaryArr)

            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)

            # oneFile.writelines(''.join(summaryArr)+'\n')

    else:
        xValueArr = []
        yValueArr = []
        cleanXArr = []
        cleanYArr = []
        xLabel = ' '.join(datum[0].split('|')[0].split('_'))
        yLabel = ' '.join(datum[1].split('|')[0].split('_'))
        chartType = datum[0].split('|')[3].split('_')[0]

        # fp.write(str(name) + "\t" + str(yLabel) + "\n")
        # fp.close()

        print(xLabel)
        print(yLabel)
        print(chartType)

        for i in range(0, len(datum)):
            if i % 2 == 0:
                xValueArr.append((datum[i].split('|')[1]))
                cleanXArr.append((datum[i].split('|')[1].replace('_', ' ')))
            else:
                yValueArr.append(float(re.sub("[^\d\.]", "", datum[i].split('|')[1])))
                cleanYArr.append(float(re.sub("[^\d\.]", "", datum[i].split('|')[1])))

        titleArr = title.split()
        maxValue = str(max(yValueArr))
        minValue = str(min(yValueArr))
        maxValueIndex = pd.Series(yValueArr).idxmax()
        minValueIndex = pd.Series(yValueArr).idxmin()
        summaryArray = []

        totalValue = sum(yValueArr)
        avgValueOfAllBars = totalValue / len(yValueArr)

        # print("totalValue -> " + str(totalValue))
        # print("avgValueOfAllBars -> " + str(avgValueOfAllBars))

        maxPercentage = int(math.ceil((max(yValueArr) / totalValue) * 100.00))
        minPercentage = int(math.ceil((min(yValueArr) / totalValue) * 100.00))

        position_in_X_axis_for_second_max_value = ""  # Added to deal with following error: UnboundLocalError: local variable 'secondMaxIndex' referenced before assignment

        if len(xValueArr) > 2:

            sortedDataY = sorted(yValueArr, reverse=True)
            secondMaxPercentage = int(math.ceil((int(sortedDataY[1]) / totalValue) * 100))

            secondMaxIndex = 0
            thirdMaxIndex = 0

            for a in range(len(yValueArr)):
                if yValueArr[a] == sortedDataY[1]:
                    secondMaxIndex = a
                if yValueArr[a] == sortedDataY[2]:
                    thirdMaxIndex = a

            position_in_X_axis_for_second_max_value = str(xValueArr[secondMaxIndex])
            position_in_X_axis_for_second_max_value = position_in_X_axis_for_second_max_value.replace("_", " ")
            y_axis_for_second_max_value = str(yValueArr[secondMaxIndex])

            # print("str(xValueArr[secondMaxIndex]")
            # print(position_in_X_axis_for_second_max_value)

            position_in_X_axis_for_third_max_value = str(xValueArr[thirdMaxIndex]).replace("_", " ")
            y_axis_for_third_max_value = str(yValueArr[thirdMaxIndex])

        num_of_category = str(len(xValueArr))
        position_in_X_axis_for_max_value = str(xValueArr[maxValueIndex])
        position_in_X_axis_for_max_value = position_in_X_axis_for_max_value.replace("_", " ")
        y_axis_for_max_value = str(yValueArr[maxValueIndex])

        position_in_X_axis_for_min_value = str(xValueArr[minValueIndex])
        position_in_X_axis_for_min_value = position_in_X_axis_for_min_value.replace("_", " ")
        y_axis_for_min_value = str(yValueArr[minValueIndex])

        if (chartType == "pie" or chartType == "bar"):
            if type(yValueArr[maxValueIndex]) == int or type(yValueArr[maxValueIndex]) == float:

                # proportion = int(math.ceil(yValueArr[maxValueIndex] / yValueArr[minValueIndex]))
                # proportion = round((yValueArr[maxValueIndex] / yValueArr[minValueIndex]), 2)
                try:
                    proportion = round((yValueArr[maxValueIndex] / yValueArr[minValueIndex]), 2)
                except ZeroDivisionError:
                    proportion = round((yValueArr[maxValueIndex] / 0.00000000001), 2)  # To avoid x/0 math error

                max_avg_diff_rel = round((yValueArr[maxValueIndex] / avgValueOfAllBars), 2)
                max_min_diff = (yValueArr[maxValueIndex] - yValueArr[minValueIndex])
                max_avg_diff_abs = (yValueArr[maxValueIndex] - avgValueOfAllBars)
                median_val = median(yValueArr)

                # print("proportion -> " + str(proportion))
                # print("max_min_diff -> " + str(max_min_diff))
                # print("max_avg_diff_rel -> " + str(max_avg_diff_rel))
                # print("max_avg_diff -> " + str(max_avg_diff_abs))
            else:
                print('The variable is not a number')

        # run pie
        if (chartType == "pie"):

            summary1 = "This is a pie chart showing the distribution of " + str(
                len(xValueArr)) + " different " + xLabel + ". "
            summary2 = xValueArr[maxValueIndex] + " " + xLabel + " has the highest proportion with " + str(
                maxPercentage) + "% of the pie chart area"
            summary3 = "followed by " + xLabel + " " + xValueArr[secondMaxIndex] + ", with a proportion of " + str(
                secondMaxPercentage) + "%. "
            summary4 = "Finally, " + xLabel + " " + xValueArr[
                minValueIndex] + " has the minimum contribution of " + str(minPercentage) + "%."

            summaryArray.append(summary1)
            summaryArray.append(summary2)
            summaryArray.append(summary3)
            summaryArray.append(summary4)

            dataJson = [{xLabel: xVal, yLabel: yVal} for xVal, yVal in zip(cleanXArr, cleanYArr)]
            trendsArray = [{}]
            websiteInput = {"title": title, "name": xLabel, "percent": yLabel,
                            "columnType": "two",
                            "graphType": chartType, "summaryType": "baseline", "summary": summaryArray,
                            "trends": trendsArray,
                            "data": dataJson}
            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)

        # run bar
        elif (chartType == "bar"):
            secondMaxIndex = 0  # to deal with error: local variable 'secondMaxIndex' referenced before assignment

            intro = []
            intro.append(
                "This is a bar chart representing " + xLabel + " in the x axis and " + yLabel + " in the y axis. ")
            intro.append("This bar chart has " + str(
                len(xValueArr)) + " columns on the x axis representing " + xLabel + ", and " + yLabel + " in each " + xLabel + " on the y axis. ")
            intro.append("This is a bar chart. It shows " + yLabel + " for " + str(
                len(xValueArr)) + " number of " + xLabel + "s. ")
            print("INTRO : " + intro[random.randint(0, len(intro) - 1)])
            print(intro)

            summaryArray.append(intro[random.randint(0, len(intro) - 1)])

            # Extrema [max/min]

            summary2_extrema_max_min = []
            summary2_extrema_max_min.append(
                "The maximum " + yLabel + " " + str(yValueArr[
                                                        maxValueIndex]) + " is found at " + xLabel + " " + position_in_X_axis_for_max_value + " and the minimum is found at " + position_in_X_axis_for_min_value + " where " + yLabel + " is " + str(
                    yValueArr[minValueIndex]) + ". ")
            summary2_extrema_max_min.append(
                "The " + yLabel + " is highest at " + xLabel + " " + position_in_X_axis_for_max_value + " and lowest at " + xLabel + " " + position_in_X_axis_for_min_value + ". ")
            summary2_extrema_max_min.append(
                xLabel + " " + position_in_X_axis_for_max_value + " has the highest " + yLabel + " and " + position_in_X_axis_for_min_value + " has the lowest " + yLabel + ". ")
            summary2_extrema_max_min.append(
                "The " + yLabel + " is appeared to be the highest at " + xLabel + " " + position_in_X_axis_for_max_value + " and lowest at " + xLabel + " " + position_in_X_axis_for_min_value + ". ")

            print("summary2_extrema_max_min")
            print(summary2_extrema_max_min)

            print(
                "Extrema [max/min] : " + summary2_extrema_max_min[random.randint(0, len(summary2_extrema_max_min) - 1)])

            summaryArray.append(summary2_extrema_max_min[random.randint(0, len(summary2_extrema_max_min) - 1)])

            global_trend_text = []
            # Trend [Pos/Neg]
            if xLabel.lower() == "year" or xLabel.lower() == "years" or xLabel.lower() == "month" or xLabel.lower() == "months" or xLabel.lower() == "quarter" or xLabel.lower() == "quarters":
                single_bar_trend = globalTrendBarChart(yValueArr)

                global_trend_text.append(
                    "Overall " + yLabel + " has " + single_bar_trend + " over the " + xLabel + "s. ")
                global_trend_text.append("The " + yLabel + " has " + single_bar_trend + " over the past " + str(
                    len(yValueArr)) + " " + xLabel + "s. ")
                global_trend_text.append("Over the past " + str(
                    len(yValueArr)) + " " + xLabel + "s, the " + yLabel + " has " + single_bar_trend + ". ")

                print("Trend [Pos/Neg] : " + global_trend_text[random.randint(0, len(global_trend_text) - 1)])
                summaryArray.append(global_trend_text[random.randint(0, len(global_trend_text) - 1)])

                print("global_trend_text")
                print(global_trend_text)

            # Order [position]
            summary3_order_2nd_max = []
            if len(xValueArr) > 2:
                summary3_order_2nd_max.append(
                    "The second highest " + yLabel + " is appeared to be the " + xLabel + " " + position_in_X_axis_for_second_max_value + ". ")
                summary3_order_2nd_max.append(
                    "Second maximum " + yLabel + " is found at " + xLabel + " " + position_in_X_axis_for_second_max_value + ". ")
                summary3_order_2nd_max.append(
                    xLabel + " " + position_in_X_axis_for_second_max_value + " has the second highest value for " + yLabel + ". ")
                print(
                    "Order [position] : " + summary3_order_2nd_max[random.randint(0, len(summary3_order_2nd_max) - 1)])

            print("summary3_order_2nd_max")
            print(summary3_order_2nd_max)

            # Order [rank]
            summary_order_rank = []
            if len(xValueArr) > 3:
                summary_order_rank.append(
                    "The " + xLabel + " " + position_in_X_axis_for_max_value + " has the highest " + yLabel + ", followed by " + position_in_X_axis_for_second_max_value + ", and " + position_in_X_axis_for_third_max_value + ". Down to the " + xLabel + " " + position_in_X_axis_for_min_value + " which is the lowest. ")
                summary_order_rank.append(
                    xLabel + " " + position_in_X_axis_for_max_value + " is higher than any other " + xLabel + "s with value " + str(
                        yValueArr[
                            maxValueIndex]) + ", followed by " + position_in_X_axis_for_second_max_value + ", and " + position_in_X_axis_for_third_max_value + ". Down to " + xLabel + " " + position_in_X_axis_for_min_value + " with the lowest value " + str(
                        yValueArr[minValueIndex]) + ". ")
                summary_order_rank.append(
                    yLabel + " at " + xLabel + " " + position_in_X_axis_for_max_value + " is " + str(yValueArr[
                                                                                                         maxValueIndex]) + " , second place is " + position_in_X_axis_for_second_max_value + " at " + str(
                        yValueArr[
                            secondMaxIndex]) + ", and thirdly is " + position_in_X_axis_for_third_max_value + " at " + str(
                        yValueArr[thirdMaxIndex]) + ". ")

                print("Order [rank] : " + summary_order_rank[random.randint(0, len(summary_order_rank) - 1)])
                summaryArray.append(summary_order_rank[random.randint(0, len(summary_order_rank) - 1)])

            # Comparison [Absolute]
            comparison_abs = []
            comparison_abs.append("There is a difference of " + str(round(max_min_diff,
                                                                          2)) + " between the maximum " + xLabel + " " + position_in_X_axis_for_max_value + " and minimum " + xLabel + " " + position_in_X_axis_for_min_value + ". ")
            comparison_abs.append(
                "The difference of " + yLabel + " between the highest and lowest " + xLabel + " is " + str(
                    round(max_min_diff, 2)) + ". ")
            comparison_abs.append("The highest " + xLabel + " " + position_in_X_axis_for_max_value + " has " + str(
                round(max_min_diff,
                      2)) + " more " + yLabel + " than the lowest " + xLabel + " " + position_in_X_axis_for_min_value + ". ")

            print("Comparison [Absolute] : " + comparison_abs[random.randint(0, len(comparison_abs) - 1)])

            # Comparison [Relative]
            comparison_rel = []
            comparison_rel.append(xLabel + " " + position_in_X_axis_for_max_value + " has " + str(
                proportion) + " times more " + yLabel + " than " + xLabel + " " + position_in_X_axis_for_min_value + " which is has the lowest. ")
            comparison_rel.append(xLabel + " " + position_in_X_axis_for_min_value + " has " + str(
                proportion) + " times less " + yLabel + " than " + xLabel + " " + position_in_X_axis_for_max_value + " which is the highest. ")
            comparison_rel.append(
                "The highest value at " + xLabel + " " + position_in_X_axis_for_max_value + " is " + str(
                    proportion) + "x times more than the lowest value at " + position_in_X_axis_for_min_value + ". ")
            comparison_rel.append(
                "The lowest value at " + xLabel + " " + position_in_X_axis_for_min_value + " is " + str(
                    proportion) + "x times less than the highest value at " + position_in_X_axis_for_max_value + ". ")
            comparison_rel.append(
                "The " + yLabel + " of " + xLabel + " " + position_in_X_axis_for_max_value + " is " + str(
                    proportion) + "% larger than the minimum value at " + position_in_X_axis_for_min_value + ". ")
            comparison_rel.append(
                "The " + yLabel + " of " + xLabel + " " + position_in_X_axis_for_min_value + " is " + str(
                    proportion) + "% smaller than the maximum value at " + position_in_X_axis_for_max_value + ". ")
            comparison_rel.append("The maximum " + xLabel + " " + position_in_X_axis_for_max_value + " has got " + str(
                proportion) + " times higher " + yLabel + " than the minimum " + xLabel + " " + position_in_X_axis_for_min_value + ". ")
            comparison_rel.append("The minimum " + xLabel + " " + position_in_X_axis_for_min_value + " has got " + str(
                proportion) + " times less " + yLabel + " than the maximum " + xLabel + " " + position_in_X_axis_for_max_value + ". ")

            print("Comparison [Relative] : " + comparison_rel[random.randint(0, len(comparison_rel) - 1)])

            if float(random.uniform(0, 1)) > 0.75:
                summaryArray.append(comparison_rel[random.randint(0, len(comparison_rel) - 1)])
            else:
                summaryArray.append(comparison_abs[random.randint(0, len(comparison_abs) - 1)])

            # Compute derived val [avg]
            derived_val_avg = []
            derived_val_avg.append(
                "The average " + yLabel + " in all " + str(len(yValueArr)) + " " + xLabel + "s is " + str(
                    round(avgValueOfAllBars, 2)) + ". ")
            derived_val_avg.append("The average " + yLabel + " in all " + str(
                len(yValueArr)) + " " + xLabel + "s is roughly " + str(round(avgValueOfAllBars, 2)) + ". ")

            print("Compute derived val [avg] : " + derived_val_avg[random.randint(0, len(derived_val_avg) - 1)])

            # Comparison [Relative, vs Avg]
            comparison_rel_with_avg = []
            comparison_rel_with_avg.append("The highest value " + str(
                yValueArr[maxValueIndex]) + " at " + position_in_X_axis_for_max_value + " is almost " + str(
                max_avg_diff_rel) + " times larger than the average value " + str(round(avgValueOfAllBars, 2)) + ". ")
            comparison_rel_with_avg.append("The lowest value " + str(
                yValueArr[minValueIndex]) + " at " + position_in_X_axis_for_min_value + " is almost " + str(
                max_avg_diff_rel) + " times smaller than the average value " + str(round(avgValueOfAllBars, 2)) + ". ")
            comparison_rel_with_avg.append("The " + xLabel + " " + position_in_X_axis_for_max_value + " has " + str(
                max_avg_diff_rel) + " times more " + yLabel + " than average. ")
            comparison_rel_with_avg.append("The " + xLabel + " " + position_in_X_axis_for_min_value + " has " + str(
                max_avg_diff_rel) + " times less " + yLabel + " than average. ")
            comparison_rel_with_avg.append(
                "The " + xLabel + " " + position_in_X_axis_for_max_value + " tends to be " + str(
                    max_avg_diff_rel) + " percent higher than average. ")
            comparison_rel_with_avg.append(
                "The " + xLabel + " " + position_in_X_axis_for_min_value + " tends to be " + str(
                    max_avg_diff_rel) + " percent lower than average. ")

            print("Comparison [Relative, vs Avg] : " + comparison_rel_with_avg[
                random.randint(0, len(comparison_rel_with_avg) - 1)])

            if float(random.uniform(0, 1)) > 0.75:
                summaryArray.append(comparison_rel_with_avg[random.randint(0, len(comparison_rel_with_avg) - 1)])
            else:
                summaryArray.append(derived_val_avg[random.randint(0, len(derived_val_avg) - 1)])

            # Compute derived val [sum]
            sum_text = []
            sum_text.append(
                "The " + yLabel + " is " + str(round(totalValue, 2)) + " if we add up values of all " + xLabel + "s. ")
            sum_text.append(
                "Summing up the values of all " + xLabel + "s, we get total " + str(round(totalValue, 2)) + ". ")

            print("Compute derived val [sum] : " + sum_text[random.randint(0, len(sum_text) - 1)])
            summaryArray.append(sum_text[random.randint(0, len(sum_text) - 1)])

            # Compute derived val [shared value]
            shared_value = []

            res = checkIfDuplicates(yValueArr)
            if res:
                # print('Yes, list contains duplicates')

                most_freq_value = most_frequent(yValueArr)
                most_freq_pos = []
                most_freq_x_label = []
                for i in range(len(yValueArr)):
                    if yValueArr[i] == most_freq_value:
                        most_freq_pos.append(i)
                        most_freq_x_label.append(xValueArr[i])

                shared_value_labels = ""
                for a in range(len(most_freq_x_label)):
                    if a == len(most_freq_x_label) - 1:
                        shared_value_labels += "and " + str(most_freq_x_label[a]).replace('_', ' ')
                    else:
                        shared_value_labels += str(most_freq_x_label[a]).replace('_', ' ') + ", "

                shared_value.append(
                    xLabel + " " + shared_value_labels + " have a similar " + yLabel + " that is " + str(
                        most_freq_value) + ". ")
                shared_value.append(
                    xLabel + " " + shared_value_labels + " share the same value " + str(most_freq_value) + ". ")
                shared_value.append(xLabel + " " + shared_value_labels + " have the same " + yLabel + ". ")
                shared_value.append("Similar " + yLabel + " is found in " + xLabel + " " + shared_value_labels + ". ")

                print("Compute derived val [shared value] : " + shared_value[random.randint(0, len(shared_value) - 1)])
                summaryArray.append(shared_value[random.randint(0, len(shared_value) - 1)])

            min_summary = []
            mid_summary = []
            max_summary = []

            min_summary.append(random.choice(intro))
            min_summary.append(random.choice(summary2_extrema_max_min))
            if len(global_trend_text) > 0:
                min_summary.append(random.choice(global_trend_text))

            mid_summary.append(random.choice(intro))
            mid_summary.append(random.choice(summary2_extrema_max_min))
            if len(global_trend_text) > 0:
                mid_summary.append(random.choice(global_trend_text))
            if float(random.uniform(0, 1)) > 0.75:
                mid_summary.append(random.choice(comparison_rel))
            else:
                mid_summary.append(random.choice(comparison_abs))

            max_summary.append(random.choice(intro))
            max_summary.append(random.choice(summary2_extrema_max_min))

            if len(global_trend_text) > 0:
                min_summary.append(random.choice(global_trend_text))

            if float(random.uniform(0, 1)) > 0.35 and len(summary3_order_2nd_max) > 0:
                max_summary.append(random.choice(summary3_order_2nd_max))

            if float(random.uniform(0, 1)) > 0.75:
                max_summary.append(random.choice(comparison_rel))
            else:
                max_summary.append(random.choice(comparison_abs))
            if len(summary_order_rank) > 0:
                max_summary.append(random.choice(summary_order_rank))
            if len(shared_value) > 0:
                max_summary.append(random.choice(shared_value))
            if float(random.uniform(0, 1)) > 0.75:
                max_summary.append(random.choice(derived_val_avg))
            else:
                max_summary.append(random.choice(comparison_rel_with_avg))
            if float(random.uniform(0, 1)) > 0.35:
                max_summary.append(random.choice(sum_text))

            print("max_summary")
            print(max_summary)

            summaryArray = mid_summary

            trendsArray = [{}, {"7": maxValueIndex, "12": maxValueIndex},
                           {"7": minValueIndex, "12": minValueIndex}, {}]
            dataJson = [{xLabel: xVal, yLabel: yVal} for xVal, yVal in zip(cleanXArr, cleanYArr)]
            websiteInput = {"title": title, "xAxis": xLabel, "yAxis": yLabel,
                            "columnType": "two",
                            "graphType": chartType, "summaryType": "baseline", "summary": summaryArray,
                            "min_summary": min_summary,
                            "mid_summary": mid_summary,
                            "max_summary": max_summary,
                            "trends": trendsArray,
                            "data": dataJson}
            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)
            # oneFile.writelines(''.join(summaryArray)+'\n')

        ## for single line charts
        # run line  
        elif (chartType == "line"):
            trendArray = []
            numericXValueArr = []
            for xVal, index in zip(xValueArr, range(
                    len(xValueArr))):  # Every x value is assigned an index from 0 to 11 (e.g. xval1: 0, xval2: 1)
                if xVal.isnumeric():
                    numericXValueArr.append(float(xVal))
                else:
                    # see if regex works better
                    cleanxVal = re.sub("[^\d\.]", "", xVal)
                    if len(cleanxVal) > 0:
                        numericXValueArr.append(float(cleanxVal[:4]))
                    else:
                        numericXValueArr.append(float(index))
            # determine local trends
            graphTrendArray = []
            i = 1
            # calculate variance between each adjacent y values
            # print(xValueArr)
            # print(yValueArr)

            ##For jason's smoothing
            while i < (len(yValueArr)):
                variance1 = float(yValueArr[i]) - float(yValueArr[
                                                            i - 1])  # 2nd yVal- Prev yVal # Note that xValueArr and yValueArr are ordered such that the start values are written at the end of the array
                if (variance1 > 0):
                    type1 = "decreasing"  # Drop/ falls/ goes down
                elif (variance1 < 0):
                    type1 = "increasing"  # Rise/ goes up
                else:
                    type1 = "constant"  # Stays the same
                trendArray.append(type1)
                i = i + 1
            ##### end of jason code

            ##Finding the direction of trend -shehnaz

            yVals_float = yValueArr  # yVals_float= stringToFloat(yValueArr)
            yVal = np.array(yVals_float).astype(np.float)  # yVal is now in float type

            # print(xValueArr)
            # print(yVal)

            coordinates = dict(zip(xValueArr, yVal))

            # print(coordinates)

            sorted_coordinates = dict(sorted(coordinates.items()))

            # print(sorted_coordinates)

            keys, values = zip(*sorted_coordinates.items())  # keys, values = zip(sorted_coordinates.items())
            print(keys)
            print(values)

            yValueArrCorrectOrder = np.array(values)  # yValueArr[len(yValueArr)::-1]  ## Ordered correctly this time
            xValueArrCorrectOrder = np.array(keys)  # xValueArr[len(xValueArr)::-1]  ## Ordered correctly this time

            ############# GlobalTrend ##############
            globalDifference = float(yValueArrCorrectOrder[len(yValueArrCorrectOrder) - 1]) - float(
                yValueArrCorrectOrder[0])
            globalPercentChange = (globalDifference / float(yValueArr[len(yValueArr) - 1])) * 100

            ############# LocalTrend ##############
            varianceArray = []

            ### Percentage change appraoch
            percentArray = []
            # directionArray = []
            i = 1
            while i < (len(yValueArrCorrectOrder)):
                old = yValueArrCorrectOrder[i - 1]
                if (old == 0 or old == 0.0):
                    old = 0.00000000001
                variance1 = float(yValueArrCorrectOrder[i]) - float(
                    old)  # 2nd yVal- Prev yVal # Note that xValueArr and yValueArr are ordered such that the start values are written at the end of the array
                localPercentChange = (variance1 / float(old)) * 100

                varianceArray.append(variance1)
                percentArray.append(localPercentChange)
                # directionArray.append(d)
                i = i + 1

            varianceArrayCorrectOrder = varianceArray  # varianceArray[len(varianceArray)::-1]  ## Ordered correctly this time
            percentArrayCorrectOrder = percentArray  # percentArray[len(percentArray)::-1]  ## Ordered correctly this time

            # print(varianceArrayCorrectOrder)
            # print(percentArrayCorrectOrder) #neww

            ## percentArray Appraoch
            ## Mean of abs_percentArrayCorrectOrder
            abs_percentArrayCorrectOrder = [abs(number) for number in percentArrayCorrectOrder]  # neww
            # print(abs_percentArrayCorrectOrder)
            mean_percentArray = mean(abs_percentArrayCorrectOrder)  # mean of abosulte values of percentArray

            constant_rate = c_rate * mean_percentArray  # avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
            significant_rate = s_rate * mean_percentArray
            gradually_rate = g_rate * mean_percentArray
            rapidly_rate = r_rate * mean_percentArray

            directionArray = []
            i = 1
            while i < (len(yValueArrCorrectOrder)):
                d = directionTrend(yValueArrCorrectOrder[i],
                                   yValueArrCorrectOrder[i - 1],
                                   constant_rate)  # direction e.g. increase, decrease or constant
                directionArray.append(d)
                i = i + 1
            # print("Orginal Direction Trend:")
            # print(directionArray)

            ### Previously indexs reported for only increasing and decresing trends
            # trendChangeIdx = []
            # for idx in range(0, len(varianceArrayCorrectOrder) - 1):

            #     # checking for successive opposite index
            #     if varianceArrayCorrectOrder[idx] > 0 and varianceArrayCorrectOrder[idx + 1] < 0 or varianceArrayCorrectOrder[idx] < 0 and varianceArrayCorrectOrder[idx + 1] > 0:
            #         trendChangeIdx.append(idx)

            # print("Sign shift indices : " + str(trendChangeIdx))

            # percentArray approach to smoothing
            ## Smoothing directionArray. If percentChange >10% then direction of trend is that of the next interval (regardless if it was increasing or decreasing)
            directionArraySmoothed = []
            for idx in range(0, len(percentArrayCorrectOrder) - 1):  # neww
                # checking for percent chnage >5% (not constant) and <10% (not significant) and chnaging their direction to be the direction of the succesive interval
                if (abs(percentArrayCorrectOrder[idx]) > constant_rate and abs(
                        percentArrayCorrectOrder[idx]) < significant_rate):  # neww
                    d = directionArray[idx + 1]
                    directionArraySmoothed.append(d)
                else:
                    directionArraySmoothed.append(directionArray[idx])
            directionArraySmoothed.append(directionArray[len(
                percentArrayCorrectOrder) - 1])  # neww # The last value doesn't have a succesive interval so it will be appended as is
            # print("Smoothed Direction Trend:")
            # print(directionArraySmoothed)

            # constant_rate = meanSlope- 1*(sdSlope)
            # significant_rate = meanSlope
            # gradually_rate= meanSlope+ 1*(sdSlope)
            # rapidly_rate= meanSlope + 2*(sdSlope)

            # slopeArray approach to smoothing
            ## Smoothing directionArray. If percentChange >10% then direction of trend is that of the next interval (regardless if it was increasing or decreasing)
            # directionArraySmoothed = []
            # for idx in range(0, len(normalized_slopeArray) - 1): #neww
            #     # checking for percent chnage >5% (not constant) and <10% (not significant) and chnaging their direction to be the direction of the succesive interval
            #     if (abs(normalized_slopeArray[idx]) > constant_rate and abs(normalized_slopeArray[idx]) < significant_rate): #neww
            #         d = directionArray[idx + 1]
            #         directionArraySmoothed.append(d)
            #     else:
            #         directionArraySmoothed.append(directionArray[idx])
            # directionArraySmoothed.append(directionArray[len(
            #     normalized_slopeArray) - 1])  #neww # The last value doesn't have a succesive interval so it will be appended as is
            # print("Smoothed Direction Trend:")
            # print(directionArraySmoothed)

            trendChangeIdx = []
            for idx in range(0, len(directionArraySmoothed) - 1):

                # checking for successive opposite index
                if directionArraySmoothed[idx] != directionArraySmoothed[idx + 1]:
                    trendChangeIdx.append(idx)

            print("Sign shift indices : " + str(trendChangeIdx))

            # yValueArrCorrectOrder = yValueArr[len(yValueArr)::-1]  ## Ordered correctly this time
            # print(yValueArrCorrectOrder)

            # xValueArrCorrectOrder = xValueArr[len(xValueArr)::-1]  ## Ordered correctly this time
            # print(xValueArrCorrectOrder)

            # trendArrayCorrectOrder = trendArray[len(trendArray)::-1] # no need since have my own directionArray now ordered correctly
            # print(trendArrayCorrectOrder)

            # print(trendChangeIdx)

            # Slope Approach
            ## Find the new slopes for the trendChangeIdx points
            # refinedSlope_array= []
            refinedPercentChnage_array = []
            x = 0
            # max_y= max(yValueArrCorrectOrder)

            if trendChangeIdx:  # if trendChangeIdx is not empty
                for i in trendChangeIdx:
                    if (x == 0):
                        # neumerator= yValueArrCorrectOrder[i+1]- yValueArrCorrectOrder[0]
                        # denominator= (i+1)- (0)
                        # slope= neumerator/denominator
                        # refinedSlope_array.append(slope)
                        new = yValueArrCorrectOrder[i + 1]
                        old = yValueArrCorrectOrder[0]

                        # percentChange= ((new-old)/old)*100
                        percentChange = percentChnageFunc(new, old)  # to account for error: float division by zero
                        refinedPercentChnage_array.append(percentChange)

                        # localPercentChange= percentChnageRangeFunc(new, old, max_y)
                        # refinedPercentChnage_array.append(localPercentChange)


                    elif (x > 0 or x < len(trendChangeIdx) - 1):
                        # neumerator= yValueArrCorrectOrder[i+1]-  yValueArrCorrectOrder[trendChangeIdx[x - 1] + 1]
                        # denominator= (i+1)- (trendChangeIdx[x - 1] + 1)
                        # slope= neumerator/denominator
                        # refinedSlope_array.append(slope)

                        new = yValueArrCorrectOrder[i + 1]
                        old = yValueArrCorrectOrder[trendChangeIdx[x - 1] + 1]
                        # percentChange= ((new-old)/old)*100
                        percentChange = percentChnageFunc(new, old)  # to account for error: float division by zero
                        refinedPercentChnage_array.append(percentChange)

                        # localPercentChange= percentChnageRangeFunc(new, old, max_y)
                        # refinedPercentChnage_array.append(localPercentChange)

                    x = x + 1

                # neumerator= yValueArrCorrectOrder[-1]-  yValueArrCorrectOrder[trendChangeIdx[-1] + 1]
                # denominator= (x)- (trendChangeIdx[-1] + 1)
                # slope= neumerator/denominator
                # refinedSlope_array.append(slope)

                new = yValueArrCorrectOrder[-1]
                old = yValueArrCorrectOrder[trendChangeIdx[-1] + 1]
                # percentChange= ((new-old)/old)*100
                percentChange = percentChnageFunc(new, old)  # to account for error: float division by zero
                refinedPercentChnage_array.append(percentChange)

                # localPercentChange= percentChnageRangeFunc(new, old, max_y)
                # refinedPercentChnage_array.append(localPercentChange)


            else:
                # neumerator= yValueArrCorrectOrder[-1]- yValueArrCorrectOrder[0]
                # denominator= (len(yValueArrCorrectOrder)-1)- 0
                # slope= neumerator/denominator
                # refinedSlope_array.append(slope)

                new = yValueArrCorrectOrder[-1]
                old = yValueArrCorrectOrder[0]
                # percentChange= ((new-old)/old)*100
                percentChange = percentChnageFunc(new, old)  # to account for error: float division by zero
                refinedPercentChnage_array.append(percentChange)

                # localPercentChange= percentChnageRangeFunc(new, old, max_y)
                # refinedPercentChnage_array.append(localPercentChange)

            # print("Refined Slope")
            # print(refinedSlope_array)

            print("Refined Percent Change")
            print(refinedPercentChnage_array)

            # Mean of abs_refinedPercentChnage_array
            abs_refinedPercentChnage_array = [abs(number) for number in refinedPercentChnage_array]  # neww
            # print(abs_percentArrayCorrectOrder)
            mean_abs_refinedPercentChnage = mean(
                abs_refinedPercentChnage_array)  # mean of abosulte values of percentArray
            print(mean_abs_refinedPercentChnage)
            # sd_abs_refinedPercentChnage= stdev(abs_refinedPercentChnage_array)
            # print(sd_abs_refinedPercentChnage)

            constant_rate = c_rate * mean_abs_refinedPercentChnage  # avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
            significant_rate = s_rate * mean_abs_refinedPercentChnage
            gradually_rate = g_rate * mean_abs_refinedPercentChnage
            rapidly_rate = r_rate * mean_abs_refinedPercentChnage

            # constant_rate = mean_abs_refinedPercentChnage- 1*(sd_abs_refinedPercentChnage) # avg(% chnage)*0.1 # Meaning any chnage less than 5% is considered roughly constant slope  # Determines if a trend is increasing, decreasing or constant
            # significant_rate = mean_abs_refinedPercentChnage# avg(% chnage)*0.1 # Meaning any chnage >constant rate and less than this rate is considered not significant and so it's trend direction is chnaged to the trend of the succesive interval # Determines the start and end of the trend
            # gradually_rate= mean_abs_refinedPercentChnage+ 1*(sd_abs_refinedPercentChnage)
            # rapidly_rate= mean_abs_refinedPercentChnage+ 2*(sd_abs_refinedPercentChnage)

            # Trying out the percentage using max-0 range of charts instead of dividing by old
            # constant_rate = constant
            # gradually_rate= gradual
            # rapidly_rate= rapid

            print(constant_rate)
            print(significant_rate)
            print(gradually_rate)
            print(rapidly_rate)

            ## Normalize refined Slope
            # abs_refinedSlope_array= [abs(number) for number in refinedSlope_array] #neww
            # print(abs_refinedSlope_array)

            # normalized_refinedSlope_array= []

            # minValRefinedSlope= min(abs_refinedSlope_array)
            # maxValRefinedSlope= max(abs_refinedSlope_array)

            # for i in range(0, len(abs_refinedSlope_array)):
            #     normalized_slope= (100*(abs_refinedSlope_array[i]- minValRefinedSlope))/(maxValRefinedSlope-minValRefinedSlope)
            #     normalized_refinedSlope_array.append(normalized_slope)
            # print("normalized_refinedSlopeArray")

            # meanRefinedSlope= mean(abs_refinedSlope_array)
            # sdRefinedSlope= stdev(abs_refinedSlope_array)

            # for i in range(0, len(abs_refinedSlope_array)):
            #     normalized_slope= (abs_refinedSlope_array[i]- meanRefinedSlope)/sdRefinedSlope
            #     normalized_refinedSlope_array.append(normalized_slope)
            # print("normalized_refinedSlopeArray")

            # print(normalized_refinedSlope_array)

            # constant_rate = meanRefinedSlope- 1*(sdRefinedSlope)
            # significant_rate = meanRefinedSlope
            # gradually_rate= meanRefinedSlope+ 1*(sdRefinedSlope)
            # rapidly_rate= meanRefinedSlope + 2*(sdRefinedSlope)
            # print(constant_rate)
            # print(significant_rate)
            # print(gradually_rate)
            # print(rapidly_rate)

            ############# Steepest Slope ##############

            # Absolute value of varianceArrayCorrectOrder elements
            absoluteVariance = [abs(ele) for ele in varianceArrayCorrectOrder]

            max_value = max(absoluteVariance)
            max_index = absoluteVariance.index(max_value)

            # print(absoluteVariance)
            # print(max_value)
            # print(max_index)
            # print(directionArraySmoothed)

            ##### Print the summary
            ###### Print all summaries for single line chart: #########

            #####  INTRO
            summary1 = []
            localTrendSentence1 = "This is a line chart with an x axis representing " + xLabel + " and a y axis representing " + yLabel + ", containing a total of " + str(
                len(yValueArrCorrectOrder)) \
                                  + " data points."
            summary1.append(localTrendSentence1)

            # Version 2
            localTrendSentence1 = "The chart at hand is a line chart where the x axis denotes " + xLabel + " and a y axis denotes " + yLabel + ". In total the number of data points it has is " + str(
                len(yValueArrCorrectOrder)) \
                                  + ". "
            summary1.append(localTrendSentence1)

            summaryArray.append(random.choice(summary1))

            #### GLOBAL TREND
            summary2_arr = []
            summary2 = " Overall " + yLabel + " has "

            if globalPercentChange > 0:
                summary2 += "increased"
            elif globalPercentChange < 0:
                summary2 += "decreased"
            else:
                summary2 += "constant"

            # summary2 +=direction

            summary2 += " over the " + xLabel + ". "
            summary2_arr.append(summary2)

            # Version 2
            summary2 = " In general, " + yLabel + " has "

            if globalPercentChange > 0 and abs(globalPercentChange) > constant:
                summary2 += "rose"
            elif globalPercentChange < 0 and abs(globalPercentChange) > constant:
                summary2 += "fallen"
            else:
                summary2 += "stayed the same"

            # summary2 +=direction

            summary2 += " over the " + xLabel + ". "
            summary2_arr.append(summary2)

            summaryArray.append(random.choice(summary2_arr))

            # LOCAL TREND
            summary3 = yLabel
            rateOfchange_array = []
            # rateOfchange_num_array= []
            x = 0
            if trendChangeIdx:  # if trendChangeIdx is not empty
                for i in trendChangeIdx:
                    if (x == 0):
                        # rateOfChange_num= rateOfChnageVal(yValueArrCorrectOrder[i + 1],yValueArrCorrectOrder[0], directionArraySmoothed[i], (i + 1), 0, max_val, min_val)
                        # rateOfchange_num_array.append(rateOfChange_num)

                        rateOfChange = rateOfChnage(refinedPercentChnage_array[x], directionArraySmoothed[i],
                                                    constant_rate, gradually_rate, rapidly_rate)
                        rateOfchange_array.append(rateOfChange)

                        summary3 += " is " + rateOfChange + " " + directionArraySmoothed[
                            i] + " from " + str(xValueArrCorrectOrder[0]) + " to " + str(xValueArrCorrectOrder[
                                                                                             i + 1]) + ", "
                    elif (x > 0 or x < len(trendChangeIdx) - 1):
                        # rateOfChange_num= rateOfChange(yValueArrCorrectOrder[i + 1], yValueArrCorrectOrder[trendChangeIdx[x - 1] + 1], directionArraySmoothed[i], (i + 1), (trendChangeIdx[x - 1] + 1), max_val, min_val)
                        # rateOfchange_num_array.append(rateOfChange_num)

                        rateOfChange = rateOfChnage(refinedPercentChnage_array[x], directionArraySmoothed[i],
                                                    constant_rate, gradually_rate, rapidly_rate)
                        rateOfchange_array.append(rateOfChange)

                        summary3 += rateOfChange + " " + \
                                    directionArraySmoothed[i] + " from " + str(xValueArrCorrectOrder[
                                                                                   trendChangeIdx[
                                                                                       x - 1] + 1]) + " to " + str(
                            xValueArrCorrectOrder[i + 1]) + ", "

                    x = x + 1

                # rateOfChange_num= rateOfChnageVal(yValueArrCorrectOrder[-1], yValueArrCorrectOrder[trendChangeIdx[-1] + 1], directionArraySmoothed[-1], (-1), (trendChangeIdx[-1] + 1), max_val, min_val)
                # rateOfchange_num_array.append(rateOfChange_num)

                rateOfChange = rateOfChnage(refinedPercentChnage_array[x], directionArraySmoothed[-1], constant_rate,
                                            gradually_rate, rapidly_rate)
                rateOfchange_array.append(rateOfChange)

                synonym = ["lastly", "finally"]
                word = random.choice(synonym)

                summary3 += "and " + str(word) + " " + rateOfChange + " " + \
                            directionArraySmoothed[-1] + " from " + str(xValueArrCorrectOrder[
                                                                            trendChangeIdx[-1] + 1]) + " to " + str(
                    xValueArrCorrectOrder[-1]) + ". "
            else:
                # rateOfChange_num= rateOfChnageVal(yValueArrCorrectOrder[-1], yValueArrCorrectOrder[0], directionArraySmoothed[-1], (-1), (0), max_val, min_val)
                # rateOfchange_num_array.append(rateOfChange_num)

                rateOfChange = rateOfChnage(refinedPercentChnage_array[x], directionArraySmoothed[-1], constant_rate,
                                            gradually_rate, rapidly_rate)
                rateOfchange_array.append(rateOfChange)

                summary3 += " is " + rateOfChange + " " + \
                            directionArraySmoothed[-1] + " from " + str(xValueArrCorrectOrder[0]) + " to " + \
                            str(xValueArrCorrectOrder[-1]) + ". "

            sum_zigzag_arr = []  # for ZIG Zag

            if (len(trendChangeIdx) < 5):
                summaryArray.append(summary3)

            # ZIG ZAG
            elif (len(yValueArrCorrectOrder) > zigZagNum):
                sum_zigzag = "The chart in general has a zig-zag shape."
                sum_zigzag_arr.append(sum_zigzag)
                sum_zigzag = "The chart generally has many fluctuations."
                sum_zigzag_arr.append(sum_zigzag)
                summaryArray.append(random.choice(sum_zigzag_arr))

            # print(rateOfchange_num_array)

            # print("percentArrayCorrectOrder:     " + str(percentArrayCorrectOrder))
            # print("directionArray:     " + str(directionArray))

            # COMPARISON

            print("")
            print("")
            print("######################################")
            print("C O M P A R I S O N")
            print("######################################")
            print("")
            print("")

            summ_Comp = []
            summ_Comp1 = "The line rapidly "
            summ_Comp2 = "The line "
            summ_Comp3 = "The line significantly "
            i = 0
            # print(rapid)

            # To find the number of rapid trends
            x = 0
            for i in range(0, len(percentArrayCorrectOrder)):
                if (abs(percentArrayCorrectOrder[i]) > rapid):
                    x = x + 1

            m = 0
            for i in range(0, len(percentArrayCorrectOrder)):
                if (abs(percentArrayCorrectOrder[i]) > rapid):
                    m = m + 1

                    n = float(yValueArrCorrectOrder[i + 1])
                    o = float(yValueArrCorrectOrder[i])
                    print(n)
                    print(o)
                    if (o == 0):
                        o = 0.00000000001
                    if (n == 0):
                        n = 0.00000000001
                    # percentage chnage
                    p = abs(percentChnageFunc(n, o))

                    # Factor
                    f = ""
                    if (n != 0.00000000001 and o != 0.00000000001):
                        if (n > o):
                            f = round(n / o, 1)
                        else:
                            f = round(o / n, 1)

                    # Absolue difference
                    absolute_diff = abs(n - o)

                    end = ","
                    conjucntion = ""
                    if (m == x):  # It is the last line to be printed and it is not only 1 line
                        end = ". "
                        if (x != 1):
                            conjucntion = " and lastly, "

                    # Version1
                    summ_Comp1 += conjucntion + str(increasedDecreased(directionArray[i])) + " by " + str(
                        round(p, 2)) + "% from " + str(xLabel) + " " + str(xValueArrCorrectOrder[i]) + " to " + str(
                        xValueArrCorrectOrder[i + 1]) + end

                    # Version 2
                    if (bool(f)):
                        summ_Comp2 += conjucntion + str(increasedDecreased(directionArray[i])) + " by " + str(
                            f) + " times from " + str(xLabel) + " " + str(xValueArrCorrectOrder[i]) + " to " + str(
                            xValueArrCorrectOrder[i + 1]) + end

                    # Version 3
                    summ_Comp3 += conjucntion + str(increasedDecreased(directionArray[i])) + " by " + str(
                        round(absolute_diff, 2)) + " from " + str(xLabel) + " " + str(
                        xValueArrCorrectOrder[i]) + " to " + str(xValueArrCorrectOrder[i + 1]) + end

            summ_Comp.append(summ_Comp1)
            if (len(summ_Comp2) != 0):
                summ_Comp.append(summ_Comp2)
            summ_Comp.append(summ_Comp3)

            summaryArray.append(random.choice(summ_Comp))

            # STEEPEST SLOPE
            summary4_arr = []
            if increaseDecrease(directionArraySmoothed[max_index]) != "stays the same":
                summary4 = "The steepest " + increaseDecrease(
                    directionArraySmoothed[max_index]) + " occurs in between the " + xLabel + " " + str(
                    xValueArrCorrectOrder[
                        max_index]) + " and " + str(xValueArrCorrectOrder[max_index + 1]) + ". "
                summary4_arr.append(summary4)

                # Version 2
                summary4 = "The most drastic " + increaseDecrease(
                    directionArraySmoothed[max_index]) + " took place within the " + xLabel + " " + str(
                    xValueArrCorrectOrder[
                        max_index]) + " and " + str(xValueArrCorrectOrder[max_index + 1]) + ". "
                summary4_arr.append(summary4)
                summaryArray.append(random.choice(summary4_arr))

            # EXTREMA MAX
            # print(yValueArrCorrectOrder)

            max_index = get_indexes_max_value(yValueArrCorrectOrder)
            # print(max_index)
            # print(len(max_index))

            summ_max_arr = []
            # version 1
            summary_v1 = "Maximum " + yLabel + ", about " + str(
                yValueArrCorrectOrder[max_index[0]]) + " was reported at " + xLabel
            summ_max_arr.append(summary_v1)

            # version2
            summary_v2 = "The highest " + yLabel + ", of value " + str(
                yValueArrCorrectOrder[max_index[0]]) + " was reached at " + xLabel
            summ_max_arr.append(summary_v2)

            chosen_max = random.choice(summ_max_arr)

            if len(max_index) > 1:
                i = 0
                while i < (len(max_index) - 1):
                    chosen_max += " " + str(xValueArrCorrectOrder[max_index[i]]) + ", "
                    i = i + 1
                chosen_max += "and " + str(xValueArrCorrectOrder[max_index[-1]])
            else:
                chosen_max += " " + str(xValueArrCorrectOrder[max_index[0]]) + ". "

            summaryArray.append(chosen_max)

            ## EXTREMA MIN
            # print(yValueArrCorrectOrder)

            min_index = get_indexes_min_value(yValueArrCorrectOrder)
            # print(min_index)
            # print(len(min_index))

            summ_min_arr = []

            # version 1
            summ_v1 = "Minimum " + yLabel + " about " + str(
                yValueArrCorrectOrder[min_index[0]]) + " was reached at " + xLabel
            summ_min_arr.append(summ_v1)

            # version 2
            summ_v2 = "The lowest " + yLabel + ", of value " + str(
                yValueArrCorrectOrder[min_index[0]]) + " was reported at " + xLabel
            summ_min_arr.append(summ_v2)

            chosen_min = random.choice(summ_min_arr)

            if len(min_index) > 1:
                i = 0
                while i < (len(min_index) - 1):
                    chosen_min += " " + str(xValueArrCorrectOrder[min_index[i]]) + ", "
                    i = i + 1
                chosen_min += "and " + str(xValueArrCorrectOrder[min_index[-1]])
            else:
                chosen_min += " " + str(xValueArrCorrectOrder[min_index[0]]) + ". "

            summaryArray.append(chosen_min)

            ####### Min, Mid, Max Summaries

            # Minimum Summary
            min_summary = []  # Minimum length summary
            mid_summary = []  # Medium length summary
            max_summary = []  # Maximum length summary

            min_summary.append(random.choice(summary1))  # intro
            min_summary.append(random.choice(summary2_arr))  # Global Trend
            if (len(yValueArrCorrectOrder) > zigZagNum and len(sum_zigzag_arr) != 0):
                max_summary.append(random.choice(sum_zigzag_arr))  # Zig zag
            if (len(trendChangeIdx) < 5):
                min_summary.append(summary3)  # Local Trends

            print("min_summary:   " + str(min_summary) + "/n")

            # Medium Summary
            mid_summary.append(random.choice(summary1))  # intro
            mid_summary.append(random.choice(summary2_arr))  # Global Trend
            if (len(yValueArrCorrectOrder) > zigZagNum and len(sum_zigzag_arr) != 0):
                max_summary.append(random.choice(sum_zigzag_arr))  # Zig zag
            if (len(trendChangeIdx) < 5):
                mid_summary.append(summary3)  # Local Trends
            if (len(summary4_arr) != 0):
                mid_summary.append(random.choice(summary4_arr))  # Steepest Slope
            mid_summary.append(chosen_max)  # Extrema max
            mid_summary.append(chosen_min)  # Extrema Min

            print("mid_summary:   " + str(mid_summary) + "/n")

            # Maximum Summary
            max_summary.append(random.choice(summary1))  # intro
            max_summary.append(random.choice(summary2_arr))  # Global Trend
            if (len(yValueArrCorrectOrder) > zigZagNum and len(sum_zigzag_arr) != 0):
                max_summary.append(random.choice(sum_zigzag_arr))  # Zig zag
            if (len(trendChangeIdx) < 5):
                max_summary.append(summary3)  # Local Trends
            if (len(summary4_arr) != 0):
                max_summary.append(random.choice(summary4_arr))  # Steepest Slope
            max_summary.append(chosen_max)  # Extrema max
            max_summary.append(chosen_min)  # Extrema Min
            if (len(summ_Comp) != 0):
                max_summary.append(random.choice(summ_Comp))  # Comparison

            print("max_summary:   " + str(max_summary) + "/n")

            summaryArray = mid_summary

            dataJson = [{xLabel: xVal, yLabel: yVal} for xVal, yVal in zip(cleanXArr, cleanYArr)]
            websiteInput = {"title": title, "xAxis": xLabel, "yAxis": yLabel,
                            "columnType": "two",
                            "graphType": chartType, "summaryType": "baseline", "summary": summaryArray,
                            "min_summary": min_summary,
                            "mid_summary": mid_summary,
                            "max_summary": max_summary,
                            "trends": graphTrendArray,
                            "data": dataJson}
            with open(f'{websitePath}/{name}.json', 'w', encoding='utf-8') as websiteFile:
                json.dump(websiteInput, websiteFile, indent=3)
            # oneFile.writelines(''.join(summaryArray) + '\n')

    if partial is True:
        summaryArray.pop(0)

    print(summaryArray)
    summaryStr = ""
    for a in range(len(summaryArray)):
        summaryStr += summaryArray[a]

    return summaryStr


# input_data = "Year|2010|x|line_chart Trade_in_thousands_metric_tons|57152.3|y|line_chart Year|2009|x|line_chart Trade_in_thousands_metric_tons|44580.8|y|line_chart Year|2008|x|line_chart Trade_in_thousands_metric_tons|62685.1|y|line_chart Year|2007|x|line_chart Trade_in_thousands_metric_tons|59961.2|y|line_chart Year|2006|x|line_chart Trade_in_thousands_metric_tons|42992.7|y|line_chart "
#
# output_data = summarize(data=input_data, all_y_label="yLabel", name="Partial", title="Partial")
# print("output_data")
# print(output_data["summary"])

pie_chart = "Strategy|advertising|x|pie_chart Amount|20|y|pie_chart Strategy|email|x|pie_chart Amount|40|y|pie_chart Strategy|sale_offers|x|pie_chart Amount|25|y|pie_chart Strategy|leaflet|x|pie_chart Amount|10|y|pie_chart "
scatter = "Manufacturer|Nabisco|0|scatter_chart Calories|50|1|scatter_chart Protein_(g)|1|2|scatter_chart Manufacturer|Quaker_Oats|0|scatter_chart Calories|115|1|scatter_chart Protein_(g)|2.5|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|75|1|scatter_chart Protein_(g)|3|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|63|1|scatter_chart Protein_(g)|4|2|scatter_chart Manufacturer|Ralston_Purina|0|scatter_chart Calories|160|1|scatter_chart Protein_(g)|5|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|130|1|scatter_chart Protein_(g)|6|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|89|1|scatter_chart Protein_(g)|7|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|70|1|scatter_chart Protein_(g)|1|2|scatter_chart Manufacturer|Ralston_Purina|0|scatter_chart Calories|140|1|scatter_chart Protein_(g)|2|2|scatter_chart Manufacturer|Post|0|scatter_chart Calories|135|1|scatter_chart Protein_(g)|3|2|scatter_chart Manufacturer|Quaker_Oats|0|scatter_chart Calories|85|1|scatter_chart Protein_(g)|4|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|80|1|scatter_chart Protein_(g)|6|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|127|1|scatter_chart Protein_(g)|5|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|140|1|scatter_chart Protein_(g)|7|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|145|1|scatter_chart Protein_(g)|1|2|scatter_chart Manufacturer|Ralston_Purina|0|scatter_chart Calories|90|1|scatter_chart Protein_(g)|2|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|111|1|scatter_chart Protein_(g)|1|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|63|1|scatter_chart Protein_(g)|3|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|57|1|scatter_chart Protein_(g)|4|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|82|1|scatter_chart Protein_(g)|5|2|scatter_chart Manufacturer|Nabisco|0|scatter_chart Calories|72|1|scatter_chart Protein_(g)|6|2|scatter_chart Manufacturer|Kelloggs|0|scatter_chart Calories|132|1|scatter_chart Protein_(g)|7|2|scatter_chart Manufacturer|General_Mills|0|scatter_chart Calories|142|1|scatter_chart Protein_(g)|5|2|scatter_chart "

# line1 = "Year|2018|x|line_chart Sales_volume_in_millions|12.88|y|line_chart Year|2017|x|line_chart Sales_volume_in_millions|13.51|y|line_chart Year|2016|x|line_chart Sales_volume_in_millions|16.17|y|line_chart Year|2015|x|line_chart Sales_volume_in_millions|15.94|y|line_chart Year|2014|x|line_chart Sales_volume_in_millions|15.46|y|line_chart Year|2013|x|line_chart Sales_volume_in_millions|13.5|y|line_chart Year|2012|x|line_chart Sales_volume_in_millions|15.85|y|line_chart Year|2011|x|line_chart Sales_volume_in_millions|13.82|y|line_chart Year|2010|x|line_chart Sales_volume_in_millions|11.78|y|line_chart Year|2009|x|line_chart Sales_volume_in_millions|12.99|y|line_chart Year|2008|x|line_chart Sales_volume_in_millions|13.0|y|line_chart Year|2007|x|line_chart Sales_volume_in_millions|8.18|y|line_chart Year|2006|x|line_chart Sales_volume_in_millions|5.0|y|line_chart Year|2005|x|line_chart Sales_volume_in_millions|3.2|y|line_chart Year|2004|x|line_chart Sales_volume_in_millions|2.03|y|line_chart "
line1 = "Year|2018|x|line_chart Sales_volume_in_millions|1288|y|line_chart Year|2017|x|line_chart Sales_volume_in_millions|1351|y|line_chart Year|2016|x|line_chart Sales_volume_in_millions|1617|y|line_chart Year|2015|x|line_chart Sales_volume_in_millions|1594|y|line_chart Year|2014|x|line_chart Sales_volume_in_millions|1546|y|line_chart Year|2013|x|line_chart Sales_volume_in_millions|135|y|line_chart Year|2012|x|line_chart Sales_volume_in_millions|1585|y|line_chart Year|2011|x|line_chart Sales_volume_in_millions|1382|y|line_chart Year|2010|x|line_chart Sales_volume_in_millions|1178|y|line_chart Year|2009|x|line_chart Sales_volume_in_millions|1299|y|line_chart Year|2008|x|line_chart Sales_volume_in_millions|130|y|line_chart Year|2007|x|line_chart Sales_volume_in_millions|818|y|line_chart Year|2006|x|line_chart Sales_volume_in_millions|50|y|line_chart Year|2005|x|line_chart Sales_volume_in_millions|32|y|line_chart Year|2004|x|line_chart Sales_volume_in_millions|203|y|line_chart "

line2 = "Year|2019|x|line_chart Net_income_in_million_U.S._dollars|15119|y|line_chart Year|2018|x|line_chart Net_income_in_million_U.S._dollars|15297|y|line_chart Year|2017|x|line_chart Net_income_in_million_U.S._dollars|1300|y|line_chart Year|2016|x|line_chart Net_income_in_million_U.S._dollars|16540|y|line_chart Year|2015|x|line_chart Net_income_in_million_U.S._dollars|15409|y|line_chart Year|2014|x|line_chart Net_income_in_million_U.S._dollars|16323|y|line_chart Year|2013|x|line_chart Net_income_in_million_U.S._dollars|13831|y|line_chart Year|2012|x|line_chart Net_income_in_million_U.S._dollars|10853|y|line_chart Year|2011|x|line_chart Net_income_in_million_U.S._dollars|9672|y|line_chart Year|2010|x|line_chart Net_income_in_million_U.S._dollars|13334|y|line_chart Year|2009|x|line_chart Net_income_in_million_U.S._dollars|12266|y|line_chart Year|2008|x|line_chart Net_income_in_million_U.S._dollars|12949|y|line_chart Year|2007|x|line_chart Net_income_in_million_U.S._dollars|10576|y|line_chart Year|2006|x|line_chart Net_income_in_million_U.S._dollars|11053|y|line_chart Year|2005|x|line_chart Net_income_in_million_U.S._dollars|10060|y|line_chart "

bar1 = "Month|Dec_19|x|bar_chart Units_sold|708|y|bar_chart Month|Nov_19|x|bar_chart Units_sold|157|y|bar_chart Month|Oct_19|x|bar_chart Units_sold|88|y|bar_chart Month|Sep_19|x|bar_chart Units_sold|526|y|bar_chart Month|Aug_19|x|bar_chart Units_sold|52|y|bar_chart Month|Jul_19|x|bar_chart Units_sold|103|y|bar_chart Month|Jun_19|x|bar_chart Units_sold|244|y|bar_chart Month|May_19|x|bar_chart Units_sold|138|y|bar_chart Month|Apr_19|x|bar_chart Units_sold|101|y|bar_chart Month|Mar_19|x|bar_chart Units_sold|632|y|bar_chart Month|Feb_19|x|bar_chart Units_sold|74|y|bar_chart Month|Jan_19|x|bar_chart Units_sold|174|y|bar_chart Month|Dec_18|x|bar_chart Units_sold|193|y|bar_chart Month|Nov_18|x|bar_chart Units_sold|145|y|bar_chart Month|Oct_18|x|bar_chart Units_sold|135|y|bar_chart Month|Sep_18|x|bar_chart Units_sold|829|y|bar_chart Month|Aug_18|x|bar_chart Units_sold|100|y|bar_chart Month|Jul_18|x|bar_chart Units_sold|112|y|bar_chart Month|Jun_18|x|bar_chart Units_sold|265|y|bar_chart Month|May_18|x|bar_chart Units_sold|231|y|bar_chart Month|Apr_18|x|bar_chart Units_sold|153|y|bar_chart Month|Mar_18|x|bar_chart Units_sold|761|y|bar_chart Month|Feb_18|x|bar_chart Units_sold|62|y|bar_chart Month|Jan_18|x|bar_chart Units_sold|155|y|bar_chart Month|Dec_17|x|bar_chart Units_sold|246|y|bar_chart Month|Nov_17|x|bar_chart Units_sold|216|y|bar_chart Month|Oct_17|x|bar_chart Units_sold|99|y|bar_chart Month|Sep_17|x|bar_chart Units_sold|510|y|bar_chart Month|Aug_17|x|bar_chart Units_sold|44|y|bar_chart Month|Jul_17|x|bar_chart Units_sold|152|y|bar_chart Month|Jun_17|x|bar_chart Units_sold|202|y|bar_chart Month|May_17|x|bar_chart Units_sold|155|y|bar_chart Month|Apr_17|x|bar_chart Units_sold|123|y|bar_chart Month|Mar_17|x|bar_chart Units_sold|706|y|bar_chart Month|Feb_17|x|bar_chart Units_sold|48|y|bar_chart Month|Jan_17|x|bar_chart Units_sold|178|y|bar_chart Month|Dec_16|x|bar_chart Units_sold|330|y|bar_chart Month|Nov_16|x|bar_chart Units_sold|219|y|bar_chart Month|Oct_16|x|bar_chart Units_sold|256|y|bar_chart Month|Sep_16|x|bar_chart Units_sold|762|y|bar_chart Month|Aug_16|x|bar_chart Units_sold|69|y|bar_chart Month|Jul_16|x|bar_chart Units_sold|148|y|bar_chart "

hchart1 = "Characteristic|Q3_'08|x|line_chart Number_of_users_in_millions|100|y|line_chart Characteristic|Q2_'09|x|line_chart Number_of_users_in_millions|242|y|line_chart Characteristic|Q4_'09|x|line_chart Number_of_users_in_millions|360|y|line_chart Characteristic|Q2_'10|x|line_chart Number_of_users_in_millions|482|y|line_chart Characteristic|Q4_'10|x|line_chart Number_of_users_in_millions|608|y|line_chart Characteristic|Q2_'11|x|line_chart Number_of_users_in_millions|739|y|line_chart Characteristic|Q4_'11|x|line_chart Number_of_users_in_millions|845|y|line_chart Characteristic|Q2_'12|x|line_chart Number_of_users_in_millions|955|y|line_chart Characteristic|Q4_'12|x|line_chart Number_of_users_in_millions|1056|y|line_chart Characteristic|Q2_'13|x|line_chart Number_of_users_in_millions|1155|y|line_chart Characteristic|Q4_'13|x|line_chart Number_of_users_in_millions|1228|y|line_chart Characteristic|Q2_'14|x|line_chart Number_of_users_in_millions|1317|y|line_chart Characteristic|Q4_'14|x|line_chart Number_of_users_in_millions|1393|y|line_chart Characteristic|Q2_'15|x|line_chart Number_of_users_in_millions|1490|y|line_chart Characteristic|Q4_'15|x|line_chart Number_of_users_in_millions|1591|y|line_chart Characteristic|Q2_'16|x|line_chart Number_of_users_in_millions|1712|y|line_chart Characteristic|Q4_'16|x|line_chart Number_of_users_in_millions|1860|y|line_chart Characteristic|Q2_'17|x|line_chart Number_of_users_in_millions|2006|y|line_chart Characteristic|Q4_'17|x|line_chart Number_of_users_in_millions|2129|y|line_chart Characteristic|Q2_'18|x|line_chart Number_of_users_in_millions|2234|y|line_chart Characteristic|Q4_'18|x|line_chart Number_of_users_in_millions|2320|y|line_chart Characteristic|Q2_'19|x|line_chart Number_of_users_in_millions|2414|y|line_chart Characteristic|Q4_'19|x|line_chart Number_of_users_in_millions|2498|y|line_chart Characteristic|Q2_'20|x|line_chart Number_of_users_in_millions|2701|y|line_chart Characteristic|Q4_'20|x|line_chart Number_of_users_in_millions|2797|y|line_chart"

hchart6 = "Label|White|0|bar_chart Active_duty_enlisted_women|53.76|1|bar_chart Active_duty_enlisted_men|69.98|2|bar_chart Label|Black|0|bar_chart Active_duty_enlisted_women|29.22|1|bar_chart Active_duty_enlisted_men|16.82|2|bar_chart Label|American|0|bar_chart Active_duty_enlisted_women|1.42|1|bar_chart Active_duty_enlisted_men|1.2|2|bar_chart Label|Asian|0|bar_chart Active_duty_enlisted_women|4.8|1|bar_chart Active_duty_enlisted_men|4.28|2|bar_chart Label|Native|0|bar_chart Active_duty_enlisted_women|1.62|1|bar_chart Active_duty_enlisted_men|1.18|2|bar_chart Label|Two or more|0|bar_chart Active_duty_enlisted_women|4.5|1|bar_chart Active_duty_enlisted_men|3.01|2|bar_chart Label|Unknown|0|bar_chart Active_duty_enlisted_women|4.68|1|bar_chart Active_duty_enlisted_men|3.51|2|bar_chart Label|Hispanic|0|bar_chart Active_duty_enlisted_women|20.55|1|bar_chart Active_duty_enlisted_men|17.32|2|bar_chart "

# output = summarize(data=hchart6, all_y_label="yLabel", name="Partial", title="Partial", partial=False)
# print("output")
# print(output)

### USE THIS PORTION TO RUN ALL CHARTS AT ONCE WITH Y LABELS

# with open(dataPath, 'r', encoding='utf-8') as dataFile, \
#         open(titlePath, 'r', encoding='utf-8') as titleFile, open(yLabelPath, 'r', encoding='utf-8') as all_y_label:
#     count = 1
#     fileIterators = zip(dataFile.readlines(), titleFile.readlines(), all_y_label.readlines())
#     for data, title, y_label in fileIterators:
#         summarize(data=data, all_y_label=y_label.rstrip('\n'), name=count, title=title.rstrip('\n'))
#         count += 1
