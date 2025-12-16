import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OptiGeo'
copyright = '2025, femDEV'
author = 'femDEV'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# BREATHE CONFIGURATION
sys.path.append("../.venv/Lib/breathe/")
extensions = ['sphinx.ext.todo', 'breathe', "sphinx.ext.mathjax"]
breathe_projects = {"OptiGeo": "../doxy_xml/"}
breathe_default_project = "OptiGeo"