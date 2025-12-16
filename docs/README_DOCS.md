## Requirements
Install the following packages: <br>
Sphinx==7.4.7 <br>
sphinx-rtd-theme==3.0.2 <br>
breathe==4.36.0 <br>

Install Doxygen: https://www.doxygen.nl/download.html <br>

## Manual Docs Update
Temporary update procedure until someone automates it through Github Actions. <br>
Open terminal and go into docs/ folder, run:
```shell
doxygen
```
this will update the files in doxy_xml/. <br>
Then run: 
```shell
 sphinx-build -b html .\sphinx_source\ .\sphinx_out\
```
and the docs should be updated.