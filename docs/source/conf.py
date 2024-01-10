# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Ventalis.settings'
import django
django.setup()

project = 'Ventalis'
copyright = '2024, Aleks512'
author = 'Aleks512'
release = '1.0'

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib_django',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files.
exclude_patterns = []

# The theme to use for HTML and HTML Help pages. See the documentation for a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here, relative to this directory. They are copied after the builtin static files, so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/stable/', 'https://docs.djangoproject.com/en/stable/_objects/')
}

# Todo extension configuration
todo_include_todos = True

# Napoleon extension for Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# HTML theme options (specific to sphinx_rtd_theme)
html_theme_options = {
    'collapse_navigation': False,
    'display_version': True,
    # more options here...
}
