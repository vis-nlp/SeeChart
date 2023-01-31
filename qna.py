# !pip install transformers
# !pip install datasets
# !pip install nltk

import json
import math

import os
import sys
import nltk  # Here to have a nice missing dependency error message early on

import transformers
from filelock import FileLock
from transformers import (
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from transformers.file_utils import is_offline_mode
from transformers.utils import check_min_version
from transformers.utils.versions import require_version

# Will error if the minimal version of Transformers is not installed. Remove at your own risks.
check_min_version("4.11.0.dev0")
require_version("datasets>=1.8.0", "To fix: pip install -r examples/pytorch/summarization/requirements.txt")


def postprocess_text(preds):
    preds = [pred.strip() for pred in preds]
    # rougeLSum expects newline after each sentence
    preds = ["\n".join(nltk.sent_tokenize(pred)) for pred in preds]
    return preds


try:
    nltk.data.find("tokenizers/punkt")
except (LookupError, OSError):
    if is_offline_mode():
        raise LookupError(
            "Offline mode: run this script without TRANSFORMERS_OFFLINE first to download nltk data files"
        )
    with FileLock(".lock") as lock:
        nltk.download("punkt", quiet=True)

# Load pretrained model and tokenizer
#
# Distributed training:
# The .from_pretrained methods guarantee that only one local process can concurrently
# download model & vocab.

model_name = "t5-base"
# checkpoint_path = "/content/t5_best_checkpoint_plotqa"  # OLD
checkpoint_path = "t5_best_checkpoint_plotqa/checkpoint-560000/"

config = AutoConfig.from_pretrained(
    checkpoint_path,
    cache_dir="cache",
    revision="main",
    use_auth_token=None,
)
tokenizer = AutoTokenizer.from_pretrained(
    checkpoint_path,
    cache_dir="cache",
    use_fast=True,
    revision="main",
    use_auth_token=None,
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint_path,
    config=config,
    cache_dir="cache",
    revision="main",
    use_auth_token=None,
)

model.resize_token_embeddings(len(tokenizer))


# input_text = "Question: What does the 2nd bar from the top in Primary schools represents ? Table: Schools | Pre-primary schools | Primary schools | Secondary schools | Tertiary schools & Egypt Gross enrolment ratio (%) | 100.05 | 99.54 | 84.65 | 23.86 & Luxembourg Gross enrolment ratio (%) | 92.75 | 88.51 | 71.8 | 2.05"
# input_text = "Question: How many bars are there ? Table: Country | Lebanon | Mali | Nepal | Peru & Female  % of children under 5 | 1.3 | 11.8 | 3.7 | 0.7 & Male  % of children under 5 | 1.8 | 13.9 | 4.5 | 0.8 Chart Type: hbar_categorical Title: Prevalence of severe wasting in children of different countries with age under 5 years x_axis_title:  % of children under 5 y_axis_title: Country"


def predict_answer(tokenizer, model, input_text):
    model_inputs = tokenizer(input_text, return_tensors="pt")
    preds = model.generate(**model_inputs)

    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    # Some simple post-processing
    decoded_preds = postprocess_text(decoded_preds)

    return decoded_preds[0]


def askMe(chart_id, question):
    f = open('static/generated_new_summary_baseline/' + chart_id + '.json')
    target_json = json.load(f)

    title = target_json['title']

    xAxis = target_json['xAxis']
    yAxis = target_json['yAxis']
    column_type = target_json['columnType']
    graphType = target_json['graphType']

    if column_type == "two" and graphType in ['bar', 'line']:

        str1 = xAxis.strip()
        str2 = yAxis.strip()

        for i in target_json['data']:
            str1 += " | " + str(i[xAxis]).strip()
            str2 += " | " + str(i[yAxis]).strip()

        # print(str1)
        # print(str2)

        input_text = "Question: " + question + "? Table: " + str1 + " & " + str2 + " Title: " + title + " x_axis_title: " + xAxis + " y_axis_title: " + yAxis

        print(input_text)

        answer = predict_answer(tokenizer, model, input_text)

        print(answer)
        return answer

    elif column_type == "multi":
        str1 = xAxis.strip()
        str2 = yAxis.strip()

        group = []

        for i in target_json['data']:
            str1 += " | " + str(i[xAxis]).strip()

        for i in range(1, len(target_json['labels'])):
            group.append(target_json['labels'][i])

        group_str = ""

        for i in group:
            group_str += " & " + i
            for j in target_json['data']:
                group_str += " | " + j[i]

        input_text = "Question: " + question + "? Table: " + str1 + group_str + " Title: " + title + " x_axis_title: " + xAxis + " y_axis_title: " + yAxis

        print(input_text)

        print(question)
        answer = predict_answer(tokenizer, model, input_text)

        print(answer)

        # if answer.is_integer():
        #     answer = math.ceil(answer)

        return answer


# QUESTION EXAMPLE : https://arxiv.org/pdf/1909.00997.pdf

question = "Does the Time in minutes increase over the years for Desktop"
# question = "Across all Years, what is the maximum value"
# question = "Across all years, what is the minimum value"
# question = "What is the difference between 2006 and 2007"
# question = "Does the graph contain any zero values"
# question = "Does the graph contain grids"
# question = "How many legend labels are there"
# question = "How many years are there"   # WRONG
# question = "How many lines intersect with each other?"
# question = "How many lines are there"
# question = "What is the maximum value for desktop"


# chart_id = "1092"
# chart_id = "795"
# chart_id = "818"
chart_id = "545"

# askMe(chart_id=chart_id, question=question)
