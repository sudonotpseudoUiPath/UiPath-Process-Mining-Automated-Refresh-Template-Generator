#!/usr/bin/python3
#Written by Ben Weinfeld
import sys
import getopt
import json
from datetime import date

def hex_encode(input_string):
    return ''.join([(hex(ord(x)).replace('0x', '%%%%').upper() if not(x.isalnum()) else x) for x in input_string])

def generate_template(input_file_name, output_file_name, is_parallel, template_type, version):
    #Check for template type
    default_file_extension = ".bat.txt"
    match template_type:
        case 'B':
            template_type = "Batch"
        case 'P':
            template_type = "Powershell"
            is_parallel = False
            default_file_extension = ".ps1.txt"
        case _:
            print("Please provide a valid template type")
            sys.exit(1)
    
    if input_file_name == '':
        input_file_name = "config.json"
    if output_file_name == '':
        output_file_name = f"output{default_file_extension}"
    elif not("." in output_file_name):
        output_file_name += default_file_extension
    if version == '':
        version = date.today().strftime("%Y.%m.%d")

    config = open(input_file_name)
    data = json.load(config)
    template = f"Templates/{template_type}/parallel_use_mod_codes_template.txt" if (is_parallel and len(data["MODULE_NAME"])>1) else f"Templates/{template_type}/use_mod_codes_template.txt" if len(data["MODULE_NAME"])>1 else f"Templates/{template_type}/no_mod_codes_template.txt"
    
    with open(template, "r") as file:
        file_text = file.read()
        file_text = file_text.replace("__LOGIN_ID_PLACEHOLDER__", hex_encode(data["LOGIN_ID"]))
        file_text = file_text.replace("__WORKSPACE_NAME_PLACEHOLDER__", data["WORKSPACE_NAME"])
        file_text = file_text.replace("__DATASET_NAME_PLACEHOLDER__", data["DATASET_NAME"])
        file_text = file_text.replace("__ENVIRONMENT_NAME_PLACEHOLDER__", data["ENVIRONMENT_NAME"])
        file_text = file_text.replace("__LOB__", data["LINE_OF_BUSINESS"])
        file_text = file_text.replace("__DATA_CLASSIFICATION__", data["DATA_CLASSIFICATION"])
        file_text = file_text.replace("__URL__", data["URL"])
        file_text = file_text.replace("__SCHEDULE__", data["SCHEDULE"])
        file_text = file_text.replace("__VERSION__", version)

        if(template_type=="Batch"):
            file_text = file_text.replace("__MODULE_NAME__", ",".join(data["MODULE_NAME"]))
        elif(template_type=="Powershell"):
            file_text = file_text.replace("__MODULE_NAME__", ",".join([f'"{x}"' for x in data["MODULE_NAME"]]))
            file_text = file_text.replace("__EMAILS__", ", ".join(data["EMAIL"]))
            file_text = file_text.replace("__EMAILS_CC__", ", ".join(data["EMAIL_CC"]))
            file_text = file_text.replace("__EMAILS_BCC__", ", ".join(data["EMAIL_BCC"]))
            file_text = file_text.replace("__SMTP_SERVER__", data["SMTP_SERVER"])
            file_text = file_text.replace("__FROM__", data["FROM_ADDRESS"])

        output_file = open("Output Files/"+output_file_name, "w")
        output_file.write(file_text)
        output_file.close()

    print(output_file_name + " has been successfully generated.")

def main(argv):
    inputfile, outputfile, parallel, template_type, version = '','', False, 'B', ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:t:p:v:",["ifile=","ofile=", "parallel", "type=", "version="])
    except getopt.GetoptError:
        print("Invalid or unrecognized parameters detected.  Please use -h for help.")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('template_generator.py [-i <inputfile>] [-o <outputfile>] [-t <template_type>] [-p] [-v <version>]')
            print("[-i <inputfile>] defines the name of the input configuration JSON file.  If omitted, config.json will be used.")
            print("[-o <outputfile>] defines the name of the output file.  If omitted, output.bat.txt or output.ps1.txt will be used. If no file extension is included in <outfile>, .bat.txt or .ps1.txt will be appended, depending on <template_type>.")
            print("[-t <template_type>] options are either '-t B' for the Batch Template or '-t P' for the Powershell Template.  If omitted, Batch mode will be used.")
            print("[-p] parallel option is only available for Batch mode, if selected along with Powershell, will be ignored.")
            print("[-v <version>] defines version number of the script.  If omitted, version number will be set to YYYY.MM.DD")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--parallel"):
            parallel = True
        elif opt in ("-t", "--type"):
            template_type = arg
        elif opt in ("-v", "--version"):
            version = arg

    generate_template(inputfile, outputfile, parallel, template_type, version)

if __name__ == "__main__":
    main(sys.argv[1:])