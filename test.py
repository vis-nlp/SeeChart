import csv

csv_file = csv.reader(open('recorded_data.csv', 'r'), delimiter=',')

url = "https://www.statista.com/statistics/755069/pubg-player-share/"

for row in csv_file:
    if url == row[3]:
        print(row[4])
