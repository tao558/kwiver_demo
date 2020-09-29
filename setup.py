from setuptools import setup, find_packages
setup( name='demo_detected_object_set_output',
       version="0.1.0",
       packages=find_packages(),
       install_requires=[
                            'pickle-mixin',
                        ],
       entry_points={
                'kwiver.python_plugin_registration':
                    [
                        'demo_detected_object_set_output=demo_detected_object_set_output.detected_object_set_output_binary',
                    ],
                },
      python_requires=">=3.5",
    )