import pandas as pd
import json

def read_d(file_path):
	if file_path.endswith('.csv'):
		data = pd.read_csv(file_path)
	elif file_path.endswith('.xlsx'):
		data = pd.read_excel(file_path, engine = 'openpyxl')
	else:
		print('File format not supported, you need to enter either CSV or Excl fle')
		return None
	return data

def parse_d(data):
	assemblies = {}
	for index, ron in data.iterrows():
		part_name = row ['Part-name']
		assembly_name = row['Assembly-name']
		replaced_by = row['Replaced-By']
		start_date = row['Start-Date']
		end_date = row['End-Date']

		if pd.notnull(replaced_by):
			part_name = replaced_by
		if pd.notnull(start_date) and pd.notnull(end_date):
			current_date = pd.Timestamp.now()
			start_date = pd.to_datetime(start_date)
			end_date = pd.to_datetime(end_date)
			if not (start_date <= current_date <= end_date):
				continue

		if part_name in assemblies:
			part_assemblies[part_name].append(assembly_name)
		else:
			assemblies[part_name] = [assembly_name]
	return assemblies

def prepare_data_for_api(assemblies):
	json_object = json.dumps(assemblies)
	return json_object