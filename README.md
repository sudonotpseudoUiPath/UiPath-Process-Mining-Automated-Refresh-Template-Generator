
# UiPath Process Mining Batch Template Generator

A script designed to aid in the batch file generation process 
for use with the UiPath Process Mining tool.

![Logo](https://files.readme.io/e04f75c-small-ui_path_Logo_PREF_rgb_Orange_digital_309x110.png)
## Authors

- [Ben Weinfeld](https://www.github.com/sudonotpseudoUiPath) - <benjamin.weinfeld@uipath.com>
## Dependencies
- Python 3.x
## Changelog
- **05/11/2022** - v1.0.0
  - Initial version of the Batch Template Generator
  - Created separate template reference files for single module and multi module formatting.
  - Created sample `config.csv` file for ease of use.
  - Compatibility tested for for all versions of UiPath Process Mining up to Release **21.10.1**
## Usage/Examples

```
usage: python3 template_generator.py [-h] [-i <inputfile>] [-o <outputfile>]
```
- **-h**
  - Default help function, returns the expected format to invoke the script, returns the following `'template_generator.py -i <inputfile> -o <outputfile>'`
- **-i <inputfile>** 
  - By default, the expected `inputfile` is the provided **config.csv**, which contains all of the necessary fields to properly generate the batch script.
  - _E.G._ `-i config.csv`
- **-o <outputfile>**
  - The value provided for `outputfile` requires a file extension to be provided.  You can output to any file extension, recommended extensions would be __*.txt__ or __*.bat__.
  - _E.G._ `-o data_refresh_script.bat`

```python3 template_generator.py -i config.csv -o data_refresh_script.bat```
## FAQ

#### I have run the script, where is my output file?

All generated output files will be located within the **Output Files** directory.

#### Why is my output file named `output.txt`?

If you do not provide a value for the `-o <outputfile>` command line argument, the default `outputfile` name will be `output.txt`.

#### I need to change my script from Single Module to Sharded Multi Module, what do I do?

The script checks the number of provided module names in the `config.csv` template file, and automatically selects the correct template and formatting to achieve either Single or Multi Module implementations.  No need to worry about anything too complex!

#### I have a question that is not answered above...

Not a worry at all!  Feel free to email the author about any further questions you might happen to have, he will be more than happy to help.

