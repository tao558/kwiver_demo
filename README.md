# kwiver_demo
A small repository with a demonstration of the Python functionality added / being added to `KWIVER`. This demo includes:

1. Example usage of a few `vital types`, namely `Image` and `Image Container`.
2. An example of running an `embedded_pipeline` from `Python` using an `adapter_data_set`.
3. Providing an implementation for an abstract algorithm and registering with plugin loader. See instructions for this process below.

To run the demo, first build KWIVER and source the corresponding `setup_kwiver` file.

## Registering an Algorithm Implementation with `plugin_loader`
In this example, we define a custom implementation for the C++ algorithm `detected_object_set_output`, namely `DetectedObjectSetOutputBinary`.
Registering an implementation is straightforward. Essentially, we'll create a Python package for the algorithm implementation and implement the
`__vital_algorithm_register__` magic method to register it. Then we'll specify the entrypoint in a `setup.py` for our package, then pip install the package.


### Creating a Python Package for the Algorithm Implementation.
In this example, we have the package `demo_detected_object_set_output` which contains two files:

  * An empty `__init__.py` making the directory a Python package
  * A source file for our new algorithm implementation, `detected_object_set_output_binary.py`
  
Create a Python package with a similar structure.

### Filling Out the Source File
Algorithm implementations are subclasses in Python, just like in C++. Fill out the class definition and inherit from the algorithm you are implementing. Be sure to include the following line in the constructor, otherwise inheritance won't work properly with `Pybind11`:

```
def __init__(self):
        [ParentClass].__init__(self)
```

Also be sure to implement `get_configuration`, `set_configuration`, `check_configuration`, and any other virtual methods in your class definition.

Lastly, implement the `__vital_algorithm_register__()` magic method. Generally, this function can be implemented as follows:

```
def __vital_algorithm_register__():
    from kwiver.vital.algo import algorithm_factory

    # Register Algorithm
    implementation_name  = "MyImplementationName"
    if algorithm_factory.has_algorithm_impl_name(
                            MyImplementation.static_type_name(),
                            implementation_name):
        return
    algorithm_factory.add_algorithm(implementation_name,
                                "My description",
                                 MyImplementation)
    algorithm_factory.mark_algorithm_as_loaded(implementation_name)
```

Where `MyImplementation` is the Python implementation class. See `demo_detected_object_set_output/detected_object_set_output_binary.py` for an example.

### Defining a `setup.py`

In the same directory as the root of our package, create a setup.py with the following general structure

```
from setuptools import setup, find_packages
setup( name='mypackagename',
       version="0.1.0",
       packages=find_packages(),
       entry_points={
                'kwiver.python_plugin_registration':
                    [
                        'mypackage=mypackage.<implementation_file>',
                    ],
                },
    )
```

Now `pip install -e .` from the same directory as the setup.py, and the algorithm implementation should be registered.

