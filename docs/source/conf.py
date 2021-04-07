# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os
import sys
project_path = os.path.join(os.path.dirname(__file__), '../../../nextorch')
sys.path.insert(0, os.path.abspath(project_path))

# -- Project information -----------------------------------------------------

project = 'nextorch'
copyright = '2021, Vlachos Research Group'
author = 'Vlachos Research Group'

# The full version, including alpha/beta/rc tags
release = '0.0.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx_gallery.load_style',
]

#Automatically generate summaries
autosummary_generate = True
autodoc_default_flags = ['members',
                         'undoc-members',
                         'show-inheritance',
                         'inherited-members']
napoleon_google_docstring = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', '**.ipynb_checkpoints',   '404.rst' ]#'**.ipynb',]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'#'sphinx_boogergreen_theme' #'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# # -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Logo
html_logo = './logos/nextorch_logo_1.png'
html_favicon = './logos/x_icon.ico'

# auto mock imports 
# This will allow your docs to import the example code 
# without requiring those modules be installed.
autodoc_mock_imports = ['torch', 'pyDOE2', 'scipy', 'gpytorch', 'botorch']


def setup(app):
    app.add_stylesheet('css/modify.css')


# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]
nbsphinx_thumbnails = {
    'examples/01_simple_1d': 'examples/_images/01.png',
    'examples/02_sin_1d': 'examples/_images/02.png',
    'examples/03_LH_mechanism': 'examples/_images/03.png',
    'examples/04_NDC_catalyst': 'examples/_images/04.png',
    'examples/05_PFR_yield': 'examples/_images/05.png',
    'examples/06_ellipse_MOO': 'examples/_images/06.png',
    'examples/07_PFR_MOO': 'examples/_images/07.png',
    'examples/08_Stub_tuner': 'examples/_images/08.png',
    'examples/09_Stub_tuner_MOO': 'examples/_images/09.png',
    'examples/10_PFR_mixed_type_inputs': 'examples/_images/10.png',
    'examples/11_PFR_EHVI_MOO': 'examples/_images/11.png'
}
