# Integer Programming from Quantum Annealing and Open Quantum Systems

This repository contains software and data associated with the publication [Integer Programming from Quantum Annealing and Open Quantum Systems [2009.11970]](https://arxiv.org/abs/2009.11970).

It contains Python code for mapping [Integer Linear Programming problems](https://en.wikipedia.org/wiki/Integer_programming), notably the [Minimum Dominating Set](https://mathworld.wolfram.com/MinimumDominatingSet.html) Problem, to [QUBOs or Ising Hamiltonians utilized as input for Quantum Annealers](https://docs.dwavesys.com/docs/latest/c_gs_3.html#qubo).
It furthermore contains code that simulates the quantum hardware.


## How to install it?

This repository contains two modules:

1. `qlp` used for computations and
2. `qlpdb` for accessing and storing computation data


### Install the computation module
The `qlp` module can be installed via pip:
```bash
cd qlp
pip install [--user] .
```

### Install the data module

To interface with the publication data, you also have to install the data module `qlpdb`
```bash
cd qlpdb
pip install [--user] .
```

## Usage

### `qlp`

The module `qlp` contains the submodule `mds` which was used to map the Minimum Dominating Set Problem to annealing Hardware:
    ```python
    from qlp.mds.graph_tools as generate_nn_graph
    from qlp.mds.qubo import get_mds_qubo

    # generate line graph of length 4: o-o-o-o
    graph, tag = gt.generate_nn_graph(4)
    # Generate mds qubo
    qubo = get_mds_qubo(
        graph,          # The graph as a set of edges
        directed=False, # no directed edges
        penalty=2       # strength of penalty term
    )
    ```
    The solution to the MDS problem is given by the bit vector `psi`, which minimizes
    ```python
    E = psi.T@qubo@psi
    ```
    The QUBO serves as input for the annealing hardware.


### `qlpdb`

`qlpdb` is an [(ORM)](https://en.wikipedia.org/wiki/Object–relational_mapping) framework for mapping database structures to Python objects using [EspressoDB](https://espressodb.readthedocs.io/en/latest/) / [Django](https://www.djangoproject.com).

Once the database [is appropriately set up](qlpdb/README.md), you can launch a local web server for inspecting data and browsing the documentation (viewable in any browser)
```bash
cd qlpdb
python manage.py runserver
```
and query data in Python code
```python
from qlpdb.tdse.models import Tdse
...
solutions = Tdse.objects.filter(
    graph__tag=graph_params["tag"],
    offset__contains=convert_params(offset_params),
    ising__contains=convert_params(ising_params),
    solver__contains=solver_params,
    wave__contains=wave_params,
)
```

## Who is responsible for it?
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://www.ckoerber.com)
* [@lastyoru](https://github.com/lastyoru)

Feel free to reach out for questions.

## License

BSD 3-Clause License. See also the [LICENSE](LICENSE.md) file.
