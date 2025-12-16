## Requirements
Install the following packages:
Sphinx==7.4.7
sphinx-rtd-theme==3.0.2
breathe==4.36.0

Install Doxygen: https://www.doxygen.nl/download.html

## Manual Docs Update
Temporary update procedure until someone automates it through Github Actions.
Open terminal and go into docs/ folder, run:
```shell
doxygen
```
This will update the files in doxy_xml/.
Then run: 
```shell
 sphinx-build -b html .\sphinx_source\ .\sphinx_out\
```
And the docs should be updated.