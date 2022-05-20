#!/usr/bin/python3
#Written by Ben Weinfeld
#If any further customizations are required, or you have any questions, please reach out via email <benjamin.weinfeld@uipath.com>
from os import environ
import sys, getopt, csv

def generate_template(input_file_name, output_file_name, is_parallel):
   if input_file_name == '':
      print("Please provide a valid input file.")
      sys.exit(1)
   elif output_file_name == '':
      output_file_name="output.txt"
    
   with open(input_file_name, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      login_id = ""
      workspace_name = ""
      dataset_name = ""
      environment_name = ""
      module_name = []
      for row in reader:
         if reader.line_num == 2:
            login_id=row["LOGIN_ID"].strip()
            workspace_name = row["WORKSPACE_NAME"].strip()
            dataset_name = row["DATASET_NAME"].strip()
            environment_name = row["ENVIRONMENT_NAME"].strip()
         module_name.append(row["MODULE_NAME"].strip())
      template = "Templates/parallel_use_mod_codes_template.txt" if (is_parallel and len(module_name)>1) else "Templates/use_mod_codes_template.txt" if len(module_name)>1 else "Templates/no_mod_codes_template.txt"
        
      with open(template, "r") as file:
         file_text = file.read()
         file_text = file_text.replace("__LOGIN_ID_PLACEHOLDER__", login_id)
         file_text = file_text.replace("__WORKSPACE_NAME_PLACEHOLDER__", workspace_name)
         file_text = file_text.replace("__DATASET_NAME_PLACEHOLDER__", dataset_name)
         file_text = file_text.replace("__ENVIRONMENT_NAME_PLACEHOLDER__", environment_name)
         file_text = file_text.replace("__MODULE_NAME__", ",".join(module_name))
         output_file = open("Output Files/"+output_file_name, "w")
         output_file.write(file_text)
         output_file.close()

      print(output_file_name + " has been successfully generated.")

def main(argv):
   inputfile, outputfile, parallel = '','', False
   try:
      opts, args = getopt.getopt(argv,"hi:o:p",["ifile=","ofile="])
   except getopt.GetoptError:
      print('template_generator.py -i <inputfile> -o <outputfile> [-p]')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('template_generator.py -i <inputfile> -o <outputfile> [-p]')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-p", "--parllel"):
         parallel = True
   print('Input file is', inputfile)
   print('Output file is', outputfile)
   generate_template(inputfile, outputfile, parallel)

if __name__ == "__main__":
   main(sys.argv[1:])