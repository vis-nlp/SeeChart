import json


for i in range(87, 1062):
    if i != 611 and i != 818 and i != 795 and i != 791:
        print(str(i))

        fileName = str(i)

        f = open('static/generated/' + fileName + '.json')
        found_data = json.load(f)

        if "gold" in found_data:

            found_data['gold'] = found_data['gold'].replace("\n", "")

            gold_list = found_data['gold'].replace(" . ", ".  + ")

            gold_list = gold_list.split(" + ")

            found_data['gold'] = gold_list

            # print(gold_list)
            print(found_data)

            with open('static/generated/' + fileName + '.json', 'w') as f:
                json.dump(found_data, f, indent=4)
