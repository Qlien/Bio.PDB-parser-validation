import csv
data = []
with open('namesToSizeToErrorsCount.csv', 'rb') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        line['Price'] = float(line['Price'])
        data.append(line)