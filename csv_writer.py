import csv
#To write all outputs recieved in a csv file named output.csv
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)