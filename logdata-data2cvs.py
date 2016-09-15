import json
import csv
import collections

from pprint import pprint


def to_time(seconds):
	seconds = int(seconds) + 7200
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	time = '{:02d}:{:02d}'.format(h, m)
	#print(time)
	return time


with open('examples/logdata-data20160913235000.json') as data_file:    
    data = json.load(data_file)

#pprint(data)
#print(data['Body']['inverter/1']['Data']['Current_DC_String_1']['Values'])

c_dc_1_values = data['Body']['inverter/1']['Data']['Current_DC_String_1']['Values']

# Dictionaraies, returned by the json reader, have no order.
# So, convert it to a list of key/value tupels (.items()) and
# sort it with sorted(), using a lambda function to convert the key/first tupel item to an integer
# so that the sorting is based on numbers not text
c_dc_1_values_ordered = sorted(c_dc_1_values.items(), key=lambda x: int(x[0]) )

# no header text for the time column so that excel treats it as x axis values
fieldnames = ['', 'Current_DC_String_1']

with open('examples/c_dc_1.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, dialect='excel-tab')
    writer.writerow(fieldnames)

    for key, value in c_dc_1_values_ordered:
       writer.writerow([key, value])




wac_plus_abs = data['Body']['meter:16220118']['Data']['EnergyReal_WAC_Plus_Absolute']['Values']
wac_plus_abs_ordered = sorted(wac_plus_abs.items(), key=lambda x: int(x[0]) )

wac_plus_diff = []

previous_value = int(wac_plus_abs_ordered[0][1])
for key, value in wac_plus_abs_ordered:
	diff = int(value) - previous_value
	wac_plus_diff.append( (to_time(key), float(diff)/1000) )
	previous_value = int(value)

fieldnames = ['', 'EnergyReal_WAC_Plus_Absolute']

with open('examples/wac_plus_diff.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, dialect='excel-tab')
    writer.writerow(fieldnames)

    for key, value in wac_plus_diff:
       writer.writerow([key, value])





wac_minus_abs = data['Body']['meter:16220118']['Data']['EnergyReal_WAC_Minus_Absolute']['Values']
wac_minus_abs_ordered = sorted(wac_minus_abs.items(), key=lambda x: int(x[0]) )

wac_minus_diff = []

previous_value = int(wac_minus_abs_ordered[0][1])
for key, value in wac_minus_abs_ordered:
	diff = int(value) - previous_value
	wac_minus_diff.append( (to_time(key), float(diff)/1000) )
	previous_value = int(value)


fieldnames = ['', 'EnergyReal_WAC_Minus_Absolute']

with open('examples/wac_minus_diff.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, dialect='excel-tab')
    writer.writerow(fieldnames)

    for key, value in wac_minus_diff:
       writer.writerow([key, value])


