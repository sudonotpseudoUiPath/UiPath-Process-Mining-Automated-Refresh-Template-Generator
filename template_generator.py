#!/usr/bin/python3
#Written by Ben Weinfeld
import sys
import getopt
import csv
import json

def hex_encode(input_string):
	return ''.join([(hex(ord(x)).replace('0x', '%%%%').upper() if not(x.isalnum()) else x) for x in input_string])

def generate_template(input_file_name, output_file_name, is_parallel, template_type):
	if input_file_name == '':
		print("Please provide a valid input file.")
		sys.exit(1)
	elif output_file_name == '':
		output_file_name="output.txt"
	
	#Check for template type
	match template_type:
		case 'B':
			template_type="Batch"
		case 'P':
			template_type="Powershell"
			is_parallel=False
		case _:
			print("Please provide a valid template type")
			sys.exit(1)
	with open(input_file_name, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		login_id = ""
		workspace_name = ""
		dataset_name = ""
		environment_name = ""
		line_of_business = ""
		data_classification = ""
		url = ""
		schedule = ""
		module_name = []
		emails = []
		cc = []
		bcc = []
		for row in reader:
			if reader.line_num == 2:
				login_id=row["LOGIN_ID"].strip()
				workspace_name = row["WORKSPACE_NAME"].strip()
				dataset_name = row["DATASET_NAME"].strip()
				environment_name = row["ENVIRONMENT_NAME"].strip()
				line_of_business = row["LINE_OF_BUSINESS"].strip()
				data_classification = row["DATA_CLASSIFICATION"].strip()
				url = row["URL"].strip()
				schedule = row["SCHEDULE"].strip()
			if(row["MODULE_NAME"].strip()):
				module_name.append(row["MODULE_NAME"].strip())
			if(row["EMAIL"].strip()):
				emails.append(row["EMAIL"].strip())
			if(row["EMAIL_CC"].strip()):
				cc.append(row["EMAIL"].strip())
			if(row["EMAIL_BCC"].strip()):
				bcc.append(row["EMAIL"].strip())
		template = f"Templates/{template_type}/parallel_use_mod_codes_template.txt" if (is_parallel and len(module_name)>1) else f"Templates/{template_type}/use_mod_codes_template.txt" if len(module_name)>1 else f"Templates/{template_type}/no_mod_codes_template.txt"
		
		with open(template, "r") as file:
			file_text = file.read()
			file_text = file_text.replace("__LOGIN_ID_PLACEHOLDER__", hex_encode(login_id))
			file_text = file_text.replace("__WORKSPACE_NAME_PLACEHOLDER__", workspace_name)
			file_text = file_text.replace("__DATASET_NAME_PLACEHOLDER__", dataset_name)
			file_text = file_text.replace("__ENVIRONMENT_NAME_PLACEHOLDER__", environment_name)
			file_text = file_text.replace("__LOB__", line_of_business)
			file_text = file_text.replace("__DATA_CLASSIFICATION__", data_classification)
			file_text = file_text.replace("__URL__", url)
			file_text = file_text.replace("__SCHEDULE__", schedule)

			if(template_type=="Batch"):
				file_text = file_text.replace("__MODULE_NAME__", ",".join(module_name))
			elif(template_type=="Powershell"):
				file_text = file_text.replace("__MODULE_NAME__", ",".join([f'"{x}"' for x in module_name]))
				file_text = file_text.replace("__EMAILS__", ",".join(emails))
				file_text = file_text.replace("__EMAILS_CC__", ",".join(cc))
				file_text = file_text.replace("__EMAILS_BCC__", ",".join(bcc))
				
				smtp_settings = open("smtp_settings.json")
				smtp_data = json.load(smtp_settings)

				file_text = file_text.replace("__SMTP_SERVER__", smtp_data["smtp_server"])
				file_text = file_text.replace("__FROM__", smtp_data["from_address"])

			output_file = open("Output Files/"+output_file_name, "w")
			output_file.write(file_text)
			output_file.close()

		print(output_file_name + " has been successfully generated.")

def main(argv):
	inputfile, outputfile, parallel, template_type = '','', False, ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:t:p",["ifile=","ofile=", "type="])
	except getopt.GetoptError:
		print("Invalid or unrecognized parameters detected.  Please use -h for help.")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('template_generator.py -i <inputfile> -o <outputfile> -t <template_type> [-p]')
			print("<template_type> options are either '-t B' for the Batch Template or '-t P' for the Powershell Template.")
			print("[-p] parallel option is only available for Batch mode, if selected along with Powershell, will be ignored.")
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-p", "--parallel"):
			parallel = True
		elif opt in ("-t", "--type"):
			template_type = arg
	print('Input file is', inputfile)
	print('Output file is', outputfile)
	generate_template(inputfile, outputfile, parallel, template_type)

if __name__ == "__main__":
	main(sys.argv[1:])