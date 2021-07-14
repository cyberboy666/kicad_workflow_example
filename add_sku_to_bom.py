## export bom from kicad using the default exporter script: bom2grouped_csv
## then run python add_sku_to_bom.py ~/path/to/exported/file

import sys
import yaml
import csv
import pprint
import os

# print('path to input csv', sys.argv[1])

def read_parts_map():
    with open("parts_map.yml", "r") as stream:
        return list(yaml.load_all(stream))[0]

def read_raw_bom(path):
    with open(path) as csv_file:
        return list(csv.DictReader(csv_file, delimiter=','))

def write_to_csv_file(file_name, data):
    if not os.path.exists(f'{path_to_project}/bom/'):
        os.makedirs(f'{path_to_project}/bom/')

    with open(f'{path_to_project}/bom/{file_name}', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)

def set_part_type_group(refs):
    part_type = ''.join([i for i in refs.split(' ')[0] if not i.isdigit()])
    part_type_group = None
    if part_type == 'R':
        part_type_group = 'resistor'
    elif part_type == 'C':
        part_type_group = 'capacitor'
    elif part_type == 'D':
        part_type_group = 'diode'
    elif part_type in ['U', 'Q', 'Y']:
        part_type_group = 'ic'
    elif part_type in ['J', 'RV', 'SW']:
        part_type_group = 'interface'
    return part_type, part_type_group

def any_item_in_string(items, string):
    return any(item in string for item in items)

def find_key_with_this_substring(value, input_dict):
    for key in input_dict:
        if str(key).lower() in value.lower():
            return key

path_to_raw_csv = sys.argv[1]
path_to_project = '/'.join(sys.argv[1].split('/')[:-1])
print('path_to_project: ', path_to_project)

part_map = read_parts_map()
raw_bom = read_raw_bom(sys.argv[1])
full_bom = [['sku', 'qty', 'ref', 'val']]
tayda_bom = [['sku', 'qty', 'ref', 'val']]
mouser_bom = [['sku', 'qty', 'ref', 'val']]


for item in raw_bom:
    # print(item)
    new_item = ['-', item[' Quantity'], item['Reference'], item[' Value']]
    part_type, part_type_group = set_part_type_group(item['Reference'])
    value = item[' Value']
    value = f'_{value}_' if part_type_group == 'resistor' else value
    # value = f'{value}_pot' if part_type == 'RV' else value

    print('type is: ', part_type)
    
    footprint = item[' Footprint']
    vendor = None
    print('footprint is: ', item[' Footprint'])
    print('value is: ', value)
    value_match = find_key_with_this_substring(value, part_map.get(part_type_group, {}))
    print('value_match: ', value_match)
    footprint_match = find_key_with_this_substring(footprint, part_map.get(part_type_group, {}).get(value_match, {}))
    print('footprint_match: ', footprint_match)
    vendor_options = part_map.get(part_type_group, {}).get(value_match, {}).get(footprint_match)
    if vendor_options:
        vendor = 'tayda' if 'tayda' in vendor_options else 'mouser'
        # vendor = 'mouser' if 'mouser' in vendor_options else 'tayda'
        new_item[0] = vendor_options[vendor]
        if vendor == 'tayda':
            tayda_bom.append(new_item)
        elif vendor == 'mouser':
            mouser_bom.append(new_item)
    full_bom.append(new_item)
    # item['Datasheet']

# print(full_bom)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(full_bom)

write_to_csv_file('full_bom.csv', full_bom)
write_to_csv_file('tayda_bom.csv', tayda_bom)
write_to_csv_file('mouser_bom.csv', mouser_bom)
