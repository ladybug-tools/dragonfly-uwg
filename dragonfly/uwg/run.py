# import core modules
import os

# import dragonfly dependencies
from ..bldgtypes import BuildingTypes
from .regionpar import RefEPWSitePar, BoundaryLayerPar

# import ladybug dependency
try:
    from ladybug.analysisperiod import AnalysisPeriod
    from ladybug.epw import EPW
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

# imort uwg dependency
uwg_installed = True
try:
    from uwg import uwg
except ImportError as e:
    uwg_installed = False


class RunManager(object):
    """Object to interface between dragonfly and the uwg.

    Properties:
        epw_file: An .epw file path on your system.
            This is the rural or airport file that will be morphed to
            reflect the climate conditions within an urban canyon.
        district: A dragonfly District object representing the urban area.
        epw_site_par: Optional dragonfly RefEPWSitePar object.
        boundary_layer_par: Optional dragonfly BoundaryLayerPar object.
        analysis_period: A ladybug AnalysisPeriod indicating the time period
            of the epw_file to be morphed.  The default is set to run the
            entire year
        sim_timestep: The timestep at which the simulation is run in seconds.
            The default is set to 300 seconds (5 minutes).

    Methods:
        run: Directly run the UWG to generate a morphed EPW.
            This method will only work if you have the uwg Python library installed.
        save: Save all of the properties of the RunManager to a .uwg file.
            These .uwg files can be parsed by the UWG engine.
    """
    def __init__(self, epw_file, district, epw_site_par=None, boundary_layer_par=None,
                 analysis_period=None, sim_timestep=None):
        """Initialize the dragonfly uwg RunManager"""
        self.epw_file = epw_file
        self.district = district
        self.epw_site_par = epw_site_par
        self.boundary_layer_par = boundary_layer_par
        self.analysis_period = analysis_period
        self.sim_timestep = sim_timestep

    @property
    def epw_file(self):
        """Get or set the EPW file path"""
        return self._epw_file

    @epw_file.setter
    def epw_file(self, file_path):
        self._epw_file = os.path.normpath(file_path)
        if not os.path.isfile(self._epw_file):
            raise ValueError(
                'Cannot find an epw file at {}'.format(self._epw_file))
        if not self._epw_file.lower().endswith('epw'):
            raise TypeError('{} is not an .epw file.'.format(self._epw_file))

    @property
    def district(self):
        """Get or set the District object."""
        return self._district

    @district.setter
    def district(self, dist):
        assert hasattr(dist, 'isDistrict'), \
            'district is not a dragonfly district object. Got {}'.format(
                type(dist))
        self._district = dist

    @property
    def epw_site_par(self):
        """Get or set the RefEPWSitePar object."""
        return self._epw_site_par

    @epw_site_par.setter
    def epw_site_par(self, par):
        if par is not None:
            assert hasattr(par, 'isRefEPWSitePar'), \
                'epw_site_par is not a RefEPWSitePar object. Got {}'.format(
                    type(par))
            self._epw_site_par = par
        else:
            self._epw_site_par = RefEPWSitePar()

    @property
    def boundary_layer_par(self):
        """Get or set the BoundaryLayerPar object."""
        return self._boundary_layer_par

    @boundary_layer_par.setter
    def boundary_layer_par(self, par):
        if par is not None:
            assert hasattr(par, 'isBoundaryLayerPar'), \
                'boundary_layer_par is not a BoundaryLayerPar object. Got {}'.format(
                    type(par))
            self._boundary_layer_par = par
        else:
            self._boundary_layer_par = BoundaryLayerPar()

    @property
    def analysis_period(self):
        """Get or set the AnalysisPeriod over which the simulation runs."""
        return self._analysis_period

    @analysis_period.setter
    def analysis_period(self, period):
        if period is not None:
            assert hasattr(period, 'isAnalysisPeriod'), \
                'analysis_period is not a AnalysisPeriod object. Got {}'.format(
                    type(period))
            self._analysis_period = period
        else:
            self._analysis_period = AnalysisPeriod()

    @property
    def sim_timestep(self):
        """Get or set the simulation timestep in seconds."""
        return self._sim_timestep

    @sim_timestep.setter
    def sim_timestep(self, timestep):
        if timestep is not None:
            assert isinstance(timestep, (float, int)), \
                'sim_timestep must be a number got {}'.format(type(timestep))
            assert timestep > 0, \
                'sim_timestep must be greater than 0. Got {}'.format(timestep)
            self._sim_timestep = timestep
        else:
            self._sim_timestep = 300

    def run(self, morphed_epw_path=None):
        """Run the UWG using the inputs to the RunManager.

        Args:
            morhed_epw_path: Full file path to the morphed epw.
                The default is set to go to an URBAN folder in the same
                directory as the existing rural EPW.
        """
        # check to see if UWG is installed
        assert uwg_installed is True, \
            'uwg must be installed to use the run() method.'

        # create a uwg_object from the dragonfly objects.
        uwg_object, new_epw_path = self._create_uwg(morphed_epw_path)
        uwg_object = self._set_uwg_input(uwg_object)
        uwg_object.init_BEM_obj()
        uwg_object = self._set_individual_typologies(uwg_object)
        uwg_object = self._set_global_facade_props(uwg_object)

        # get the object ready to simulate
        uwg_object.read_epw()
        uwg_object.init_input_obj()
        uwg_object.hvac_autosize()

        # run the UWG object.
        uwg_object.simulate()
        uwg_object.write_epw()

    def _create_uwg(self, end_file_path):
        """Create a UWG object using the urban weather generator."""
        start_folder, epw_name = os.path.split(self._epw_file)
        epw_name = epw_name.replace('.epw', '')
        if end_file_path is None:
            end_folder = '{}\\URBAN\\'.format(start_folder)
            name = '{}_URBAN.epw'.format(epw_name)
        else:
            end_folder, name = os.path.split(end_file_path)
        if not os.path.isdir(end_folder):
            os.mkdir(end_folder)
        uwg_obj = uwg(epw_name, None, start_folder, None, end_folder, name)
        return uwg_obj, os.path.join(end_folder, name)

    def _set_uwg_input(self, uwg_obj):
            """Assign all inputs to the uwg """
            # define simulation and weather parameters
            month, day, n_day = self._parse_ladybug_analysis_period()
            uwg_obj.Month = month
            uwg_obj.Day = day
            uwg_obj.nDay = n_day
            uwg_obj.dtSim = self._sim_timestep
            uwg_obj.dtWeather = 3600.0

            # HVAC system and internal laod (not currently exposed in API)
            uwg_obj.autosize = 0
            uwg_obj.sensOcc = 100.0
            uwg_obj.LatFOcc = 0.3
            uwg_obj.RadFOcc = 0.2
            uwg_obj.RadFEquip = 0.5
            uwg_obj.RadFLight = 0.7

            # define urban microclimate parameters
            uwg_obj.h_ubl1 = self._boundary_layer_par.day_boundary_layer_height
            uwg_obj.h_ubl2 = self._boundary_layer_par.night_boundary_layer_height
            uwg_obj.h_ref = self._boundary_layer_par.inversion_height
            uwg_obj.c_circ = self._boundary_layer_par.circulation_coefficient
            uwg_obj.c_exch = self._boundary_layer_par.exchange_coefficient
            uwg_obj.h_temp = self._epw_site_par.temp_measure_height
            uwg_obj.h_wind = self._epw_site_par.wind_measure_height
            uwg_obj.maxDay = 150.
            uwg_obj.maxNight = 20.
            uwg_obj.windMin = 1.
            uwg_obj.h_obs = self._epw_site_par.average_obstacle_height

            # Urban characteristics
            uwg_obj.bldHeight = self._district.average_bldg_height
            uwg_obj.h_mix = self._district.fract_heat_to_canyon
            uwg_obj.bldDensity = self._district.site_coverage_ratio
            uwg_obj.verToHor = self._district.facade_to_site_ratio
            uwg_obj.charLength = self._district.characteristic_length
            uwg_obj.sensAnth = self._district.traffic_parameters.sensible_heat
            uwg_obj.SchTraffic = self._district.traffic_parameters.get_uwg_matrix()

            # Define optional Building characteristics
            uwg_obj.bld = self._district.get_uwg_matrix()

            # climate Zone
            uwg_obj.zone = self._district._climate_zone

            # Vegetation parameters
            uwg_obj.vegCover = self._district.grass_coverage_ratio
            uwg_obj.treeCoverage = self._district.tree_coverage_ratio
            uwg_obj.albVeg = self._district.vegetation_parameters.vegetation_albedo
            uwg_obj.latTree = self._district.vegetation_parameters.tree_latent_fraction
            uwg_obj.latGrss = self._district.vegetation_parameters.grass_latent_fraction
            uwg_obj.rurVegCover = self._epw_site_par.vegetation_coverage

            if self._district.vegetation_parameters.vegetation_start_month == 0 \
                    or self._district.vegetation_parameters.vegetation_end_month == 0:
                        veg_start, veg_end = self._autocalc_start_end_vegetation(
                            self._epw_file)
            if self._district.vegetation_parameters.vegetation_start_month == 0:
                uwg_obj.veg_start = veg_start
            else:
                uwg_obj.veg_start = \
                    self._district.vegetation_parameters.vegetation_start_month
            if self._district.vegetation_parameters.vegetation_end_month == 0:
                uwg_obj.veg_end = veg_end
            else:
                uwg_obj.veg_end = \
                    self._district.vegetation_parameters.vegetation_end_month

            # Define road
            uwg_obj.alb_road = self._district.pavement_parameters.albedo
            uwg_obj.d_road = self._district.pavement_parameters.thickness
            uwg_obj.kRoad = self._district.pavement_parameters.conductivity
            uwg_obj.cRoad = self._district.pavement_parameters.volumetric_heat_capacity

            return uwg_obj

    def _set_individual_typologies(self, uwg_obj):
        # create a dictonary to convert between the dragonfly and uwg typologies
        district_typologies = self._district.building_typologies
        district_typ_names = [','.join([typ.bldg_program, typ.bldg_era])
                              for typ in district_typologies]
        typology_dict = dict(zip(district_typ_names, district_typologies))

        # update each typology
        for uwg_typology in uwg_obj.BEM:
            df_typology = typology_dict[','.join(
                [uwg_typology.building.Type,
                 BuildingTypes.get_uwg_era_index(uwg_typology.building.Era)])]
            uwg_typology.floorHeight = df_typology.floor_to_floor
            uwg_typology.building.glazingRatio = df_typology.glz_ratio
            uwg_typology.building.canyon_fraction = \
                df_typology.uwg_parameters.fract_heat_to_canyon
            uwg_typology.building.shgc = \
                df_typology.uwg_parameters.shgc
            uwg_typology.wall.albedo = \
                df_typology.uwg_parameters.wall_albedo
            uwg_typology.roof.albedo = \
                df_typology.uwg_parameters.roof_albedo
            uwg_typology.roof.vegCoverage = \
                df_typology.uwg_parameters.roof_veg_fraction

        return uwg_obj

    def _set_global_facade_props(self, uwg_obj):
        # parameters for the UCMdef that must be overwritten
        uwg_obj.r_glaze_total = self._district.glz_ratio
        uwg_obj.SHGC_total = self._district.shgc
        uwg_obj.alb_wall_total = self._district.wall_albedo

        # parameters that are correctly by _set_individual_typologies
        uwg_obj.albRoof = self._district.roof_albedo
        uwg_obj.vegRoof = self._district.roof_veg_fraction
        uwg_obj.flr_h = self._district.floor_height

        return uwg_obj

    def _parse_ladybug_analysis_period(self):
        st_month = self._analysis_period.st_month
        st_day = self._analysis_period.st_day
        start_doy = int(self._analysis_period.st_time.doy)
        end_doy = int(self._analysis_period.end_time.doy)
        simDuration = end_doy - start_doy + 1
        return st_month, st_day, simDuration

    def _autocalc_start_end_vegetation(self, epw_file, threshold_temp=10):
        epw_obj = EPW(epw_file)
        temperature_data = epw_obj.dry_bulb_temperature.group_by_month()
        month_temps = []
        for month in range(1, 13):
            month_temps.append(sum(temperature_data[month]) /
                               len(temperature_data[month]))

        veg_end = 12
        veg_start = 1
        veg_start_set = False
        for i, t in enumerate(month_temps):
            if t > threshold_temp and veg_start_set is False:
                veg_start = i+1
                veg_start_set = True
            elif t < threshold_temp and veg_start_set is True:
                veg_end = i+1
                veg_start_set = False

        return veg_start, veg_end

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt UWG RunManager."""
        return 'UWG RunManager: ' \
               '\n Rural EPW: {}' \
               '\n Analysis Period: {}' \
               '\n District: {}'.format(
                   self.epw_file, self.analysis_period, self.district
               )
