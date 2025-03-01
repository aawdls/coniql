Contributing
============

Contributions and issues are most welcome! All issues and pull requests are
handled through GitHub_. Also, please check for any existing issues before
filing a new one. If you have a great idea but it involves big changes, please
file a ticket before making a pull request! We want to make sure you don't spend
your time coding something that might not fit the scope of the project.

.. _GitHub: https://github.com/dls-controls/coniql/issues

Running the tests
-----------------

To get the source source code and run the unit tests, run::

    $ git clone git://github.com/dls-controls/coniql.git
    $ cd coniql
    $ pipenv install --dev
    $ pipenv run tests

While 100% code coverage does not make a library bug-free, it significantly
reduces the number of easily caught bugs! Please make sure coverage remains the
same or is improved by a pull request!

Code Styling
------------

The code in this repository conforms to standards set by the following tools:

- black_ for code formatting
- flake8_ for style checks
- isort_ for import ordering
- mypy_ for static type checking

These checks will be run by pre-commit_. You can either choose to run these
tests on all files tracked by git::

    $ pipenv run lint

Or you can install a pre-commit hook that will run each time you do a ``git
commit`` on just the files that have changed::

    $ pipenv run pre-commit install

.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _mypy: https://github.com/python/mypy
.. _pre-commit: https://pre-commit.com/

Docstrings are pre-processed using the Sphinx Napoleon extension. As such,
google-style_ is considered as standard for this repository. Please use type
hints in the function signature for types. For example::

    def func(arg1: str, arg2: int) -> bool:
        """Summary line.

        Extended description of function.

        Args:
            arg1: Description of arg1
            arg2: Description of arg2

        Returns:
            Description of return value
        """
        return True

.. _google-style: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#google-vs-numpy

Documentation
-------------

Documentation is contained in the ``docs`` directory and extracted from
docstrings of the API.

Docs follow the underlining convention::

    Headling 1 (page title)
    =======================

    Heading 2
    ---------

    Heading 3
    ~~~~~~~~~

You can build the docs from the project directory by running::

    $ pipenv run docs
    $ firefox build/html/index.html

Release Process
---------------

To make a new release, please follow this checklist:

- Choose a new PEP440 compliant release number
- Git tag the version
- Push to GitHub and the actions will make a release on pypi
- Push to internal gitlab and do a dls-release.py of the tag
- Check and edit for clarity the autogenerated GitHub release_

.. _release: https://github.com/dls-controls/coniql/releases

Updating the tools
------------------

This module is merged with the dls-python3-skeleton_. This is a generic
Python project structure which provides a means to keep tools and
techniques in sync between multiple Python projects. To update to the
latest version of the skeleton, run::

    $ git pull https://github.com/dls-controls/dls-python3-skeleton skeleton

Any merge conflicts will indicate an area where something has changed that
conflicts with the setup of the current module. Check the `closed pull requests
<https://github.com/dls-controls/dls-python3-skeleton/pulls?q=is%3Apr+is%3Aclosed>`_
of the skeleton module for more details.

.. _dls-python3-skeleton: https://dls-controls.github.io/dls-python3-skeleton
