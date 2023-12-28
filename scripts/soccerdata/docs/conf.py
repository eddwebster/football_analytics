"""Sphinx configuration."""

# -- Project information -----------------------------------------------------

project = "soccerdata"
author = "Pieter Robberechts"
copyright = f"2021, {author}"

# The full version, including alpha/beta/rc tags
release = '1.5.2'

# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "nbsphinx",
    # 'sphinx_gallery.load_style',
]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
autodoc_typehints = "description"
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_logo = "_static/logo2.png"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#2F3C7E",
        "color-brand-content": "#2F3C7E",
        "color-sidebar-background": "#fdf3f4",
        # "color-api-name": "#7bb5b2",
        # "color-api-pre-name": "#7bb5b2",
    },
    "dark_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
    },
}

html_static_path = ["_static"]
html_css_files = ["default.css"]

# -- Options for nbsphinx ---------------------------------------------------

nbsphinx_thumbnails = {
    'examples/datasources/ClubElo': '_static/ClubElo-logo.png',
    'examples/datasources/ESPN': '_static/ESPN-logo.png',
    'examples/datasources/WhoScored': '_static/WhoScored-logo.png',
    'examples/datasources/FBref': '_static/FBref-logo.png',
    'examples/datasources/FiveThirtyEight': '_static/FiveThirtyEight-logo.png',
    'examples/datasources/MatchHistory': '_static/FootballData-logo.jpg',
    'examples/datasources/SoFIFA': '_static/SoFIFA-logo.png',
}

# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = 'doc/' + env.doc2path(env.docname, base=None) %}

.. raw:: html

    <div class="admonition note">
      This page was generated from
      <a class="reference external" href="https://github.com/probberechts/soccerdata/blob/{{ env.config.release|e }}/{{ docname|e }}">{{ docname|e }}</a>.<br />
      You can <a href="{{ env.docname.split('/')|last|e + '.ipynb' }}" class="reference download internal" download>download the notebook</a>,
      <script>
        if (document.location.host) {
          let nbviewer_link = document.createElement('a');
          nbviewer_link.setAttribute('href',
            'https://nbviewer.org/url' +
            (window.location.protocol == 'https:' ? 's/' : '/') +
            window.location.host +
            window.location.pathname.slice(0, -4) +
            'ipynb');
          nbviewer_link.innerHTML = 'or view it on <em>nbviewer</em>';
          nbviewer_link.classList.add('reference');
          nbviewer_link.classList.add('external');
          document.currentScript.replaceWith(nbviewer_link, '.');
        }
      </script>
    </div>

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""  # noqa

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
{% set docname = 'doc/' + env.doc2path(env.docname, base=None) %}
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ docname | escape_latex }}}} ends here.}}
"""
