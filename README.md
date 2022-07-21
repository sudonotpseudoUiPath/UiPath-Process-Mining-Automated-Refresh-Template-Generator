
# UiPath Process Mining Automated Refresh Template Generator

A script designed to aid in the automated refresh file generation process for use with the UiPath Process Mining tool.

![Logo](https://files.readme.io/e04f75c-small-ui_path_Logo_PREF_rgb_Orange_digital_309x110.png)
## Authors

- [Ben Weinfeld](https://www.github.com/sudonotpseudoUiPath) - <benjamin.weinfeld@uipath.com>
## Dependencies
- Python 3.10+
## Changelog
- **07/21/22** - v1.4.0
  - `config.csv` and `smtp_settings.json` have been merged into a single `config.json` file to condense all fields into a single location.
    - `stmp_server` renamed to `SMTP_SERVER`.
    - `from_address` renamed to `FROM_ADDRESS`.
  - Made the `-i <inputfile>` command line flag optional.  If omitted, the script will default to using `config.json`.  Other `*.json` files can be used in the traditional manner.
  - Made the `-t <template_type>` command line flag optional.  If omitted, the script will default to using Batch mode.
  - Added `-o <outputfile>` name correction.  If the provided value of `outputfile` does not contain a file extension, `.bat.txt` or `.ps1.txt` will be appended, depending on `template_type`.
  - `README.md` updated with corrected instructions.
- **07/20/2022** - v1.3.1
  - Corrected email formatting in Powershell template generator use case.
  - Corrected `Send-Mail` function in Powershell template.
  - Added `Startup-Email` function to Powershell template to allow for an email notification to be sent out on script startup.
- **07/18/2022** - v1.3.0
  - Dependencies updated to **Python 3.10+** from **Python 3.x**
  - Corrected error causing the longform command line flag for `-p` parallel to be `--parllel` instead of `--parallel`.
  - Naming convention, formatting, and whitespace cleanup.
  - Name changed to reflect both Powershell and Batch file creation capacity.
  - Updated example Output Files to reflect updated formatting and syntax.
  - Changes made to the `Templates` directory to add subdirectories for Powershell and Batch templates, respectively.
  - Updated `-h` Help command line flag to explain the new command line syntax. 
  - Added new command line flag `-t <template_type>` to allow for either `-t B` Batch or `-t P` Powershell script creation.
  - New Powershell script allows for email notifications, with detailed Logfile attachments, to be sent out to specified email addresses using SMTP to notify when failures occur during the Connector Level Cache Generation, Connector Level Dataset Loading, and Application Level Cache Generation individually for aided visibility.
  - New Logfile generated in the `/logs/<date>/` folder named `auto_log_<scriptname>_<date>.txt` containing direct reference to the corresponding log files for each of the steps performed, as well as exit codes.
  - `config.csv` has been updated with the following additional fields: `LINE_OF_BUSINESS`,`DATA_CLASSIFICATION`,`URL`,`SCHEDULE`, `EMAIL`,`EMAIL_CC`,`EMAIL_BCC`.  The additional fields: `EMAIL`,`EMAIL_CC`,`EMAIL_BCC` are only used for the Powershell version of the script's email sending functionality.
  - `smtp_settings.json` has been added to provide the necessary SMTP settings for the Powershell version of the script's email sending functionality.  It contains the following values: 
    - `stmp_server` denotes the desired SMTP server.
    - `from_address` denotes the email address that your email notifications will come from.
- **05/31/2022** - v1.2.0
  - Added `hexEncode()` function to handle HTML encoding for Login ID's containing special characters.
  - Adjusted `parallel_use_mod_codes_template.txt` to account for an edge case occurring from scheduling a chronjob at root directory level for the batch execution leading to a failure to execute the subroutine callback.
  - Added exit codes to all batch templates to account for chronjob scheduling checks.
  - Corrected grammar and spelling in `README.md`
- **05/20/2022** - v1.1.0
  - Updated formatting and syntax for template referencing files
  - Created additional template reference file for multi module parallel loading
  - Added additional command line flag `-p [--parallel]` to allow for parallel data loading
- **05/11/2022** - v1.0.0
  - Initial version of the Batch Template Generator
  - Created separate template reference files for single module and multi module formatting.
  - Created sample `config.csv` file for ease of use.
  - Compatibility tested for for all versions of UiPath Process Mining up to Release **21.10.1**
## Usage/Examples

```
usage: template_generator.py [-i <inputfile>] [-o <outputfile>] [-t <template_type>] [-p]
```
- **-h**
  - Default help function, returns the expected format to invoke the script, returns the following 
    ```
    template_generator.py [-i <inputfile>] [-o <outputfile>] [-t <template_type>] [-p]
    [-i <inputfile>] defines the name of the input configuration JSON file.  If omitted, config.json will be used.
    [-o <outputfile>] defines the name of the output file.  If omitted, output.bat.txt or output.ps1.txt will be used. If no file extension is included in <outfile>, .bat.txt or .ps1.txt will be appended, depending on <template_type>.
    [-t <template_type>] options are either '-t B' for the Batch Template or '-t P' for the Powershell Template.  If omitted, Batch mode will be used.
    [-p] parallel option is only available for Batch mode, if selected along with Powershell, will be ignored.    
    ```
- **-i [--ifile] <_inputfile_>** 
  - By default, the expected `inputfile` is the provided **config.json**, which contains all of the necessary fields to properly generate the batch script.
  - _E.G._ `-i config.json` or `--ifile config.json`
- **-o [--ofile] <_outputfile_>**
  - For the value provided for `outputfile`, it is suggested a file extension be provided.  If no file extension is provided, `.bat.txt` or `.ps1.txt` will be appended, depending on `template_type`.  You can output to any file extension, recommended extensions are __*.txt__, __*.bat__, or __*.ps1__.
  - _E.G._ `-o data_refresh_script.bat` or `--ofile data_refresh_script.ps1`
- **-t [--type] <_template_type_>**
  - The value provided for `template_type` can be either `B` for Batch or `P` for Powershell.  This command line flag determines which template is used to generate your script file.
  - _E.G._ `-t B` or `--type P`
- **-p [--parallel]**
  - A flag to select the parallel data loading template for multi module applicaitons.  Has no effect on single module loading.  Can only be used alongside the Batch template type.  If used with the Powershell template type, will be ignored.

```python3 template_generator.py -i config.json -o data_refresh_script.bat -t B -p```
## FAQ

#### I have run the script, where is my output file?

All generated output files will be located within the **Output Files** directory.

#### Why is my output file named `output.bat.txt` or `output.ps1.txt`?

If you do not provide a value for the `-o <outputfile>` command line argument, the default `outputfile` name will be `output.bat.txt` or `output.ps1.txt`, depending on the selected value for `template_type`.

#### I need to change my script from Single Module to Sharded Multi Module, what do I do?

The script checks the number of provided module names in the `config.json` template file, and automatically selects the correct template and formatting to achieve either Single or Multi Module implementations.  No need to worry about anything too complex!

#### What is the difference between Parallel and Sequential Multi Module loading?

When running the sequential multi module refresh script, each sharded module will be loaded one at at time, and then each module in the released application will have its cache refreshed one at a time.  This can take a very long time for large datasets with a high number of shards.  By implementing the parallel multi module refresh script, we can have each separate data shard be loaded and cached independent of one another, allowing us to save time.

**NOTE:** Using parallel mutli module refreshing consumes a large amount of system resource, and may not be suitable for all systems.  It is recommended to test on Development/UAT before deploying to Production.

#### I have a question that is not answered above...

Not a worry at all!  Feel free to email the author about any further questions you might happen to have, he will be more than happy to help.