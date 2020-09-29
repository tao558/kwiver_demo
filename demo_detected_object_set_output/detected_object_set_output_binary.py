from kwiver.vital.algo import DetectedObjectSetOutput

class DetectedObjectSetOutputBinary(DetectedObjectSetOutput):
    def __init__(self):
        DetectedObjectSetOutput.__init__(self)

    def get_configuration(self):
        # Inherit from the base class
        cfg = super(DetectedObjectSetOutput, self).get_configuration()
        return cfg

    def set_configuration(self, cfg_in):
        cfg = self.get_configuration()
        cfg.merge_config(cfg_in)

    def check_configuration(self, cfg):
        return True

    # Pybind will know that we are overriding this virtual method
    def write_set(self, set_, image_name):
        import pickle
        out = {"set_length": len(set_), "image_name": image_name}
        pickle.dump(out, open(self.filename(), "wb"))

def __vital_algorithm_register__():
    from kwiver.vital.algo import algorithm_factory

    # Register Algorithm
    implementation_name  = "DetectedObjectSetOutputBinary"
    if algorithm_factory.has_algorithm_impl_name(
                            DetectedObjectSetOutputBinary.static_type_name(),
                            implementation_name):
        return
    algorithm_factory.add_algorithm(implementation_name,
                                "Output detected object sets using Python's pickle package",
                                 DetectedObjectSetOutputBinary)
    algorithm_factory.mark_algorithm_as_loaded(implementation_name)
