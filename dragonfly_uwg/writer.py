"""Methods to write files for UWG simulation from a Model."""
from .simulation.parameter import UWGSimulationParameter


def model_to_uwg(model, epw_file, simulation_parameter=None):
    """Create a fully simulate-able uwg dictionary from a Model.

    Args:
        model: A dragonfly Model for which an URBANopt feature geoJSON and corresponding
            honeybee Model JSONs will be returned.
        epw_file: File path to the EPW that will be morphed by the UWG. This will be
            used to fill all autocalculated fields like the ASHRAE climate zone
            and vegetation start/end.
        simulation_parameter: A UWGSimulationParameter object that dictates various
            settings about the UWG simulation. If None, default parameters will
            be generated. (Default: None).

    Returns:
        A dictionary following the UWG schema. This dictionary can be serialized
        into a JSON in order to be run through the UWG.
    """
    # get the base dictionary from the model; independent of simulation parameters
    if model.units != 'Meters':
        model = model.duplicate()  # duplicate the model to avoid mutating the input
        model.convert_to_units('Meters')
    uwg_dict = model.properties.uwg.to_uwg_dict()

    # get a dictionary for the simulation parameters and update the base
    sim_par = simulation_parameter if simulation_parameter is not None \
        else UWGSimulationParameter()
    sim_par_dict = sim_par.to_uwg_dict(epw_file)
    uwg_dict.update(sim_par_dict)

    # get the average SHGC across the buildings using the climate zone
    uwg_dict['shgc'] = model.properties.uwg.average_shgc(uwg_dict['zone'])

    # add other properties that have not been exposed elsewhere in the SDK
    uwg_dict['dtweather'] = 3600
    uwg_dict['autosize'] = False
    uwg_dict['sensocc'] = 100
    uwg_dict['latfocc'] = 0.3
    uwg_dict['radfocc'] = 0.2
    uwg_dict['radfequip'] = 0.5
    uwg_dict['radflight'] = 0.7
    uwg_dict['maxday'] = 150
    uwg_dict['maxnight'] = 20
    uwg_dict['windmin'] = 1
    return uwg_dict
