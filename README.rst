Advent of Code 2019 Solutions in Python
=======================================
Advent of Code 2019 Solutions

If not python3 on linux:

.. code-block::

    module avail python
    module add python/3.8.0

For VDI:

.. code-block::

    unset PYTHONPATH


Regardless of OS:

.. code-block::

    python3 -m venv --prompt="aoc" venv
    source venv/bin/activate
    pip install --upgrade pip setuptools
    pip install -r requirements.txt


.. code-block::

    aoc 2 data/day2.txt


.. code-block::

    pytest

