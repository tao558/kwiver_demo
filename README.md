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

1. First, create a python package for your new algorithm implementation. In this example, we have the package `demo_detected_object_set_output`
which contains two files:

  An empty `__init__.py` making the directory a Python package
  A source file for our new algorithm implementation, `detected_object_set_output_binary.py`
