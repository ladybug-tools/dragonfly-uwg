# coding=utf-8
from __future__ import division
import os

# import dragonfly dependencies
from ..bldgtypes import BuildingTypes
from .regionpar import RefEPWSitePar, BoundaryLayerPar
from ..district import District

# import ladybug dependency
try:
    from ladybug.analysisperiod import AnalysisPeriod
    from ladybug.epw import EPW
    from ladybug.futil import write_to_file_by_name
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
        save_uwg_file: Save all of the properties of the RunManager to a .uwg file.
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

    @classmethod
    def from_json(cls, data):
        """Create a RunManager object from a dictionary
        Args:
            data: {
                epw_file: list of Typology objects
                district: dragonfly district disct
                epw_site_par: epw site parameter dict
                boundary_layer_par: boundary layer parameter dict
                analysis_period: ladybug analysis period dict
                sim_timestep: simulation timestep in seconds
            }
        """

        required_keys = ('epw_file', 'district')
        nullable_keys = ('epw_site_par', 'boundary_layer_par',
                         'analysis_period', 'sim_timestep')

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(epw_file=data['epw_file'],
                   district=District.from_json(
                       data['district']),
                   epw_site_par=RefEPWSitePar.from_json(
                       data['epw_site_par']),
                   boundary_layer_par=BoundaryLayerPar.from_json(
                       data['boundary_layer_par']),
                   analysis_period=AnalysisPeriod.from_json(
                       data['analysis_period']),
                   sim_timestep=data['sim_timestep']
                   )

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

    @property
    def uwg_file_string(self):
        """Return a string that can be written to a .uwg file."""
        # extract certain values from the obects
        veg_start, veg_end = self._get_start_end_vegetation()
        traffic_matrix = self._district.traffic_parameters.get_uwg_matrix()
        month, day, n_day = self._parse_ladybug_analysis_period()

        # get a commented matrix showing the ratios of building types
        programs = BuildingTypes.get_program_list()
        bldg_type_str_list = [str(typ).replace('[', '').replace(']', '')
                              + '  #' + programs[i]
                              for i, typ in enumerate(self._district.get_uwg_matrix())]
        bldg_type_mtx = '\n'.join(bldg_type_str_list)

        # build the text string
        return '# ================================================='\
            '\n# UWG INPUT PARAMETERS'\
            '\n# =================================================\n'\
            '\n# Urban characteristics'\
            '\nbldHeight,{},     # average building height (m)'\
            '\nbldDensity,{},   # urban area building plan density (0-1)'\
            '\nverToHor,{},     # urban area vertical to horizontal ratio'\
            '\nh_mix,{},       # fraction of building HVAC heat output to street canyon'\
            '\ncharLength,{}, # dimension of a square that encompasses the district (m)'\
            '\nalbRoad,{},      # road albedo (0 - 1)'\
            '\ndRoad,{},        # road pavement thickness (m)'\
            '\nkRoad,{},          # road pavement conductivity (W/m K)'\
            '\ncRoad,{},    # road volumetric heat capacity (J/m^3 K)'\
            '\nsensAnth,{},  # non-building sensible heat at street level (W/m^2)'\
            '\nlatAnth,0,   # non-building latent heat (W/m^2) (not used)\n'\
            '\nzone,{},    # Climate zone index (ie. 4=3A, 11=5A, 16=8)\n'\
            '\n# Vegetation parameters'\
            '\nvegCover,{},     # Fraction of the district covered in grass/shrub (0-1)'\
            '\ntreeCoverage,{}, # Fraction of the district covered in trees (0-1)'\
            '\nvegStart,{},    # The month in which vegetation starts to evapotranspire'\
            '\nvegEnd,{},        # The month in which vegetation stops evapotranspiring'\
            '\nalbVeg,{},      # Vegetation albedo'\
            '\nrurVegCover,{},  # Fraction of the rural ground covered by vegetation'\
            '\nlatGrss,{},    # Fraction of the heat absorbed by grass as latent'\
            '\nlatTree,{},    # Fraction of the heat absorbed by trees as latent\n'\
            '\n# Traffic schedule [1 to 24 hour]'\
            '\nSchTraffic,'\
            '\n{}, # weekday'\
            '\n{}, # saturday'\
            '\n{}, # sunday\n'\
            '\n# Fraction of building stock for each era (Pre80, Pst80, new)'\
            '\n# Note that sum(bld) must be equal to 1'\
            '\n{}\n'\
            '\n# Simulation parameters,'\
            '\nMonth,{},        # starting month (1-12)'\
            '\nDay,{},          # starting day (1-31)'\
            '\nnDay,{},        # number of days to run simultion'\
            '\ndtSim,{},      # simulation time step (s)'\
            '\ndtWeather,3600.0, # weather time step (s)\n'\
            '\n# HVAC system and internal loads'\
            '\nautosize,0,     # autosize HVAC (1 for yes; 0 for no)'\
            '\nsensOcc,100.0,    # Sensible heat per occupant (W)'\
            '\nLatFOcc,0.3,    # Latent heat fraction from occupant (normally 0.3)'\
            '\nRadFOcc,0.2,    # Radiant heat fraction from occupant (normally 0.2)'\
            '\nRadFEquip,0.5,  # Radiant heat fraction from equipment (normally 0.5)'\
            '\nRadFLight,0.7,  # Radiant heat fraction from light (normally 0.7)\n'\
            '\n#Urban climate parameters'\
            '\nh_ubl1,{},    # ubl height - day (m)'\
            '\nh_ubl2,{},      # ubl height - night (m)'\
            '\nh_ref,{},      # inversion height (m)'\
            '\nh_temp,{},       # temperature height (m)'\
            '\nh_wind,{},      # wind height (m)'\
            '\nc_circ,{},     # circulation coefficient (default = 1.2; Bruno (2012))'\
            '\nc_exch,{},       # exchange coefficient (default = 1; Bruno (2014))'\
            '\nmaxDay,150,     # max day threshold (W/m^2)'\
            '\nmaxNight,20,    # max night threshold (W/m^2)'\
            '\nwindMin,1,      # min wind speed (m/s)'\
            '\nh_obs,{},      # rural average obstacle height (m)'\
            .format(
                self._district.average_bldg_height,
                self._district.site_coverage_ratio,
                self._district.facade_to_site_ratio,
                self._district.fract_heat_to_canyon,
                self._district.characteristic_length,
                self._district.pavement_parameters.albedo,
                self._district.pavement_parameters.thickness,
                self._district.pavement_parameters.conductivity,
                self._district.pavement_parameters.volumetric_heat_capacity,
                self._district.traffic_parameters.sensible_heat,
                self._district._climate_zone + 1,
                self._district.grass_coverage_ratio,
                self._district.tree_coverage_ratio,
                veg_start,
                veg_end,
                self._district.vegetation_parameters.vegetation_albedo,
                self._epw_site_par.vegetation_coverage,
                self._district.vegetation_parameters.grass_latent_fraction,
                self._district.vegetation_parameters.tree_latent_fraction,
                str(traffic_matrix[0]).replace('[', '').replace(']', ''),
                str(traffic_matrix[1]).replace('[', '').replace(']', ''),
                str(traffic_matrix[2]).replace('[', '').replace(']', ''),
                bldg_type_mtx,
                month,
                day,
                n_day,
                self._sim_timestep,
                self._boundary_layer_par.day_boundary_layer_height,
                self._boundary_layer_par.night_boundary_layer_height,
                self._boundary_layer_par.inversion_height,
                self._epw_site_par.temp_measure_height,
                self._epw_site_par.wind_measure_height,
                self._boundary_layer_par.circulation_coefficient,
                self._boundary_layer_par.exchange_coefficient,
                self._epw_site_par.average_obstacle_height
            )

    def save_uwg_file(self, uwg_file_path=None):
        """Write the properties of the RunManager to a .uwg file.

        Args:
            uwg_file_path: Full file path to the .uwg file that you want to write.
                The default is set to go to an URBAN folder in the same
                directory as the existing rural EPW.

        Returns:
            uwg_file_path: The file path to the .uwg file.
        """
        start_folder, epw_name = os.path.split(self._epw_file)
        epw_name = epw_name.replace('.epw', '')
        if uwg_file_path is None:
            end_folder = '{}\\URBAN\\'.format(start_folder)
            name = '{}_URBAN.uwg'.format(epw_name)
        else:
            end_folder, name = os.path.split(uwg_file_path)
            if not name.lower().endswith('.uwg'):
                name = name + '.uwg'
        write_to_file_by_name(end_folder, name, self.uwg_file_string, True)

        uwg_file_path = os.path.join(end_folder, name)
        print ('.uwg file successfully written to: {}'.format(uwg_file_path))
        return uwg_file_path

    def run(self, urban_epw_path=None):
        """Run the UWG using the inputs to the RunManager.

        Args:
            urban_epw_path: Full file path to the morphed epw.
                The default is set to go to an URBAN folder in the same
                directory as the existing rural EPW.

        Returns:
            urban_epw_path: The file path to the morphed epw.
        """
        # check to see if UWG is installed
        assert uwg_installed is True, \
            'UWG must be installed to use the uwg.Runmanager.run() method. '\
            'Use "pip install uwg" to install.'

        # create a uwg_object from the dragonfly objects.
        uwg_object, urban_epw_path = self._create_uwg(urban_epw_path)
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

        return urban_epw_path

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
            veg_start, veg_end = self._get_start_end_vegetation()
            uwg_obj.vegStart = veg_start
            uwg_obj.vegEnd = veg_end

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

    def _get_start_end_vegetation(self):
        if self._district.vegetation_parameters.vegetation_start_month == 0 \
                or self._district.vegetation_parameters.vegetation_end_month == 0:
                    veg_start, veg_end = self._autocalc_start_end_vegetation()
        if self._district.vegetation_parameters.vegetation_start_month != 0:
            veg_start = self._district.vegetation_parameters.vegetation_start_month
        if self._district.vegetation_parameters.vegetation_end_month != 0:
            veg_end = self._district.vegetation_parameters.vegetation_end_month
        return veg_start, veg_end

    def _autocalc_start_end_vegetation(self, threshold_temp=10):
        epw_obj = EPW(self._epw_file)
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

    def to_json(self):
        """Create a UWG RunManager dictionary
        Results:
            {
                epw_file: list of Typology objects
                district: dragonfly district disct
                epw_site_par: epw site parameter dict
                boundary_layer_par: boundary layer parameter dict
                analysis_period: ladybug analysis period dict
                sim_timestep: simulation timestep in seconds
            }
        """
        return {
            'epw_file': self.epw_file,
            'district': self.district.to_json(),
            'epw_site_par': self.epw_site_par.to_json(),
            'boundary_layer_par': self.boundary_layer_par.to_json(),
            'analysis_period': self.analysis_period.to_json(),
            'sim_timestep': self.sim_timestep
            }

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
