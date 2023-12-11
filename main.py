import pandas as pd
import json
import requests

def prepare_data_for_api(assemblies):
	json_object = json.dumps(assemblies)
	return json_object

def send_data_to_api(json_object, api_endpoint):
	response = requests.post(api_endpoint, data = json_object)
	if response.status_code != 200:
		print(f"Failed to send data to API. Status code: {response.status_code}")
		return None
	return response

def read_d(file_path):
	if file_path.endswith('.csv'):
		data = pd.read_csv(file_path)
	elif file_path.endswith('.xlsx'):
		data = pd.read_excel(file_path, engine = 'openpyxl')
	else:
		print('File format not supported, you need to enter either CSV or Excl fle')
		return None
	return data

# def parse_d(data):
# 	assemblies = {}
# 	for index, row in data.iterrows():
# 		part_name = row['Assembly-Part']
# 		assembly_name = row['Assembly-Name']
# 		replaced_by = row['replaced by']
# 		start_date = row['Valid from']
# 		end_date = row['Valid to']

# 		if pd.notnull(replaced_by):
# 			part_name = replaced_by
# 		if pd.notnull(start_date) and pd.notnull(end_date):
# 			current_date = pd.Timestamp.now()
# 			start_date = pd.to_datetime(start_date)
# 			end_date = pd.to_datetime(end_date)
# 			if not (start_date <= current_date <= end_date):
# 				continue

# 		if part_name in assemblies:
# 			assemblies[part_name].append(assembly_name)
# 		else:
# 			assemblies[part_name] = [assembly_name]
# 	return assemblies

def parse_d(data):
	assemblies = {}
	for index, row in data.iterrows():
		part_name = row['Assembly-Part']
		assembly_name = row['Assembly-Name']
		replaced_by = row['replaced by']
		start_date = row['Valid from']
		end_date = row['Valid to']

		if pd.notnull(replaced_by):
			part_name = replaced_by
		if pd.notnull(start_date) and pd.notnull(end_date):
			try:
				current_date = pd.Timestamp.now()
				start_date = pd.to_datetime(start_date)
				end_date = pd.to_datetime(end_date)
			except pd.errors.OutOfBoundsDatetime:
				print(f"Skipping row {index} due to out of bounds date.")
				continue
			if not (start_date <= current_date <= end_date):
				continue

		if part_name in assemblies:
			assemblies[part_name].append(assembly_name)
		else:
			assemblies[part_name] = [assembly_name]
	return assemblies

file_path = '/Users/abhudulo/Downloads/task_11/data.csv'
api_endpoint = 'http://127.0.0.1:5000/endpoint'
data = read_d(file_path)
assemblies = parse_d(data)
json_object = prepare_data_for_api(assemblies)
response = send_data_to_api(json_object, api_endpoint)