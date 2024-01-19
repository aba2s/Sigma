# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Sigma"
copyright = "2023, A. NDIAYE"
author = "A. NDIAYE"

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# sys.path.insert(0, os.path.abspath('.'))
# os.path.abspath('')) : return path to access source (.../Sigma/docs)
# we need to take two steps back to go back to the Sigma foler (../..)
sys.path.append(os.path.abspath("../../.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigma_project.settings")
django.setup()


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# pip install sphinxcontrib-apidoc
# pip install sphinxcontrib-napoleon

extensions = [
    "sphinx.ext.autodoc",  # To auto generate django_app files,
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
