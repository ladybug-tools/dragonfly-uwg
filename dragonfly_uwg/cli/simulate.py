"""Commands for simulating Dragonfly JSON models in the UWG."""
import click
import sys
import logging
import json

from dragonfly_uwg.run import run_uwg
from dragonfly_uwg.simulation.parameter import UWGSimulationParameter
from dragonfly.model import Model

_logger = logging.getLogger(__name__)


@click.group(help='Commands for simulating Dragonfly JSON models in the UWG.')
def simulate():
    pass


@simulate.command('model')
@click.argument('model-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.argument('epw-file', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--sim-par-json', '-sp', help='Path to a dragonfly UWG Simulation '
              'Parameter JSON that describes all of the settings for the simulation.',
              default=None, show_default=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--folder', '-f', help='Folder into which the the uwg JSON and morphed '
              'urban EPW will be written. If not specified, it will be written into the '
              'ladybug default_epw_folder within a subfolder bearing the name of the '
              'dragonfly Model.', default=None, show_default=True,
              type=click.Path(file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--log-file', '-log', help='Optional log file to output a dictionary '
              'with the paths of the generated files under the following keys: '
              'uwg_json, epw. By default the list will be printed out to stdout',
              type=click.File('w'), default='-', show_default=True)
def simulate_model(model_json, epw_file, sim_par_json, folder, log_file):
    """Simulate a Dragonfly Model JSON file in the Urban Weather Generator (UWG).

    \b
    Args:
        model_json: Full path to a Dragonfly Model JSON file.
        epw_file: Full path to an .epw file to be morphed to account for urban
            heat island effect.
    """
    try:
        # process the simulation parameters and write new ones if necessary
        if sim_par_json is None:  # generate some default simulation parameters
            sim_par = UWGSimulationParameter()
        else:
            with open(sim_par_json) as json_file:
                data = json.load(json_file)
            sim_par = UWGSimulationParameter.from_dict(data)

        # re-serialize the Dragonfly Model
        with open(model_json) as json_file:
            data = json.load(json_file)
        model = Model.from_dict(data)
        model.convert_to_units('Meters')

        # run the model through the UWG
        uwg_json, urban_epw = run_uwg(model, epw_file, sim_par, folder)
        if urban_epw is None:
            raise Exception('Running the Urban Weather Generator failed.')
        log_file.write(json.dumps({'uwg_json': uwg_json, 'epw': urban_epw}))
    except Exception as e:
        _logger.exception('Model translation failed.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)
