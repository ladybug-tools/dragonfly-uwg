# coding=utf-8
"""Module for running models through the Urban Weather Generator (UWG)."""
from __future__ import division

import os
import json
import subprocess

from honeybee.config import folders as hb_folders
from ladybug.config import folders as lb_folders
from ladybug.futil import write_to_file, preparedir


def run_uwg(model, epw_file_path, simulation_parameter=None, directory=None,
            silent=False):
    """Run a UWG dictionary file through the UWG on any operating system.

    Args:
        model: A Dragonfly Model to be used to morph the EPW for the urban area.
        epw_file_path: The full path to an EPW file.
        simulation_parameter: A UWGSimulationParameter object that dictates various
            settings about the UWG simulation. If None, default parameters will
            be generated. (Default: None).
        directory: Text for the directory into which the the uwg JSON and morphed
            urban EPW will be written. If None, it will be written into the
            ladybug default_epw_folder within a subfolder bearing the name
            of the dragonfly Model. (Default: None).
        silent: Boolean to note whether the simulation should be run silently.
            This only has an effect on Windows simulations since Unix-based
            simulations always use shell and are always silent (Default: False).

    Returns:
        The following files output from the UWG CLI run

        -   uwg_json -- Path to a .json file derived from the input uwg_dict.

        -   epw -- File path to the morphed EPW. Will be None if the UWG
            failed to run.
    """
    # get the name of the EPW and the directory into which the urban epw will be written
    epw_file_path = os.path.abspath(epw_file_path)
    epw_name = '{}.epw'.format(model.identifier)
    if directory is None:
        directory = os.path.join(lb_folders.default_epw_folder, model.identifier)
    preparedir(directory, remove_content=True)

    # write the model to a UWG dictionary
    uwg_dict = model.to.uwg(model, epw_file_path, simulation_parameter)
    uwg_json = os.path.join(directory, '{}_uwg.json'.format(model.identifier))
    with open(uwg_json, 'w') as fp:
        json.dump(uwg_dict, fp, indent=4)

    # run the simulation
    if os.name == 'nt':  # we are on Windows
        epw = _run_uwg_windows(uwg_json, epw_file_path, epw_name, silent)
    else:  # we are on Mac, Linux, or some other unix-based system
        epw = _run_uwg_unix(uwg_json, epw_file_path, epw_name)
    return uwg_json, epw


def _run_uwg_windows(uwg_json_path, epw_file_path, epw_name, silent=False):
    """Run a JSON file through the UWG on a Windows-based operating system.

    A batch file will be used to run the simulation unless silent is True.

    Args:
        uwg_json_path: The full path to a UWG JSON file.
        epw_file_path: The full path to an EPW file.
        epw_name: Text for the name of the EPW file.
        silent: Boolean to note whether the simulation should be run silently
            (without the batch window). If so, the simulation will be run using
            subprocess with shell set to True. (Default: False).

    Returns:
        File path to the morphed EPW. Will be None if the UWG failed to run.
    """
    directory = os.path.dirname(uwg_json_path)
    if not silent:  # run the simulations using a batch file
        working_drive = directory[:2]
        # write the batch file
        batch = '{}\ncd "{}"\n"{}" -m uwg simulate model "{}" "{}" --new-epw-dir "{}" ' \
            '--new-epw-name "{}"'.format(
                working_drive, directory, hb_folders.python_exe_path, uwg_json_path,
                epw_file_path, directory, epw_name)
        batch_file = os.path.join(directory, 'in.bat')
        write_to_file(batch_file, batch, True)
        os.system('"{}"'.format(batch_file))  # run the batch file
    else:  # run the simulation using subprocess
        cmds = [hb_folders.python_exe_path, '-m', 'uwg', 'simulate', 'model',
                uwg_json_path, epw_file_path, '--new-epw-dir', directory,
                '--new-epw-name', epw_name]
        process = subprocess.Popen(cmds, stdout=subprocess.PIPE, shell=True)
        process.communicate()  # prevents the script from running before command is done

    epw_file = os.path.join(directory, epw_name)
    return epw_file if os.path.isfile(epw_file) else None


def _run_uwg_unix(uwg_json_path, epw_file_path, epw_name):
    """Run a JSON file through the UWG on a Unix-based operating system.

    This includes both Mac OS and Linux since a shell will be used to run
    the simulation.

    Args:
        uwg_json_path: The full path to a UWG JSON file.
        epw_file_path: The full path to an EPW file.
        epw_name: Text for the name of the EPW file.

    Returns:
        File path to the morphed EPW. Will be None if the UWG failed to run.
    """
    directory = os.path.dirname(uwg_json_path)
    # write a shell file
    shell = '#!/usr/bin/env bash\n\ncd "{}"\n {} -m uwg simulate model "{}" "{}" ' \
        '--new-epw-dir "{}" --new-epw-name "{}"'.format(
            directory, hb_folders.python_exe_path, uwg_json_path,
            epw_file_path, directory, epw_name)
    shell_file = os.path.join(directory, 'in.sh')
    write_to_file(shell_file, shell, True)

    # make the shell script executable using subprocess.check_call
    # this is more reliable than native Python chmod on Mac
    subprocess.check_call(['chmod', 'u+x', shell_file])

    # run the shell script
    subprocess.call(shell_file)

    epw_file = os.path.join(directory, epw_name)
    return epw_file if os.path.isfile(epw_file) else None
