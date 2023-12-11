import pandas as pd

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
		if part_name in assemblies:
			part_assemblies[part_name].append(assembly_name)
		else:
			assemblies[part_name] = [assembly_name]
	return assemblies