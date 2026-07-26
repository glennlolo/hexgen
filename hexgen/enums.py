from enum import Enum
from hexgen.constants import TERRAIN_BARREN, TERRAIN_TERRAN, TERRAIN_OCEANIC


class SuperEnum(Enum):
    """Adds an id property that gets the order of an enum member in the class"""

    def __init__(self, *args):
        for key, value in enumerate(args):
            for namekey, name in enumerate(self.__keys__):
                if key == namekey:
                    setattr(self, name, value)

    def to_dict(self):
        """converts an enum member to a dict"""
        rep = dict([(key, getattr(self, key)) for key in self.__keys__])
        rep["name"] = self.name
        return rep

    @classmethod
    def get(cls, id_):
        idx = [
            item for item in list(cls.__members__) if getattr(cls[item], "id") == id_
        ]
        if idx is not None and len(idx) > 0:
            return cls[idx[0]]
        else:
            return None

    @classmethod
    def items(cls):
        return list(cls.__members__)

    @classmethod
    def pluck(cls, key="name"):
        return [getattr(cls[x], key) for x in list(cls.__members__)]

    @classmethod
    def dump(cls):
        return [cls[x].to_dict() for x in list(cls.__members__)]

    @classmethod
    def all(cls):
        return [cls[x].to_dict() for x in list(cls.__members__)]

    @classmethod
    def members(cls):
        return [cls[x].name for x in list(cls.__members__)]

    @classmethod
    def list(cls):
        return [cls[x] for x in list(cls.__members__)]


# https://jsfiddle.net/ajfu7em8/1/
class Biome(SuperEnum):
    __keys__ = ["id", "code", "title", "color", "base_fertility", "color_satellite"]

    lifeless = (13, "l", "Lifeless", (200, 200, 200), 0, (150, 150, 150))

    # terran
    arctic = (1, "a", "Arctic", (224, 224, 224), 1, (132, 152, 159))
    tundra = (2, "u", "Tundra", (114, 153, 128), 15, (52, 55, 44))
    alpine_tundra = (3, "p", "Alpine Tundra", (97, 130, 106), 10, (59, 60, 42))
    desert = (4, "d", "Desert", (237, 217, 135), 5, (94, 78, 52))
    shrubland = (5, "s", "Shrubland", (194, 210, 136), 20, (58, 47, 21))
    savanna = (6, "S", "Savanna", (219, 230, 158), 80, (66, 53, 28))
    grasslands = (7, "g", "Grasslands", (166, 223, 106), 150, (45, 46, 22))
    boreal_forest = (8, "b", "Boreal Forest", (28, 94, 74), 30, (36, 41, 29))
    temperate_forest = (9, "t", "Temperate Forest", (76, 192, 0), 100, (40, 37, 19))
    temperate_rainforest = (
        10,
        "T",
        "Temperate Rainforest",
        (89, 129, 89),
        100,
        (42, 38, 21),
    )
    tropical_forest = (11, "r", "Tropical Forest", (96, 122, 34), 70, (32, 39, 21))
    tropical_rainforest = (12, "R", "Tropical Rainforest", (0, 70, 0), 60, (26, 33, 16))

    # BARREN
    # color: grey if no atmosphere ( less than 0.003 earth pressure),
    #   red if atmosphere (greater than 0.003 earth pressure),
    #   tan if atmosphere and water
    # - highlands   light
    # - lowlands    dark
    barren_dusty = (14, "bld", "Barren Drylands", (87, 26, 27), 0)

    barren = (16, "bld", "Barren Drylands", (43, 44, 35), 0)
    barren_wet = (21, "bw", "Barren Wetland", (77, 36, 37), 0, (22, 51, 61))

    barren_ice_caps = (18, "bi", "Barren Ice Caps", (242, 228, 216), 0)

    # VOLCANIC
    # color: greyish light brown with red lava flows
    # - lava plains     red
    # - highlands       ligh
    # - lowlands        dark
    volcanic_liquid = (19, "mo", "Lava Fields", (217, 0, 0), 0)
    volcanic_molten_river = (19, "mo", "Lavaflow", (207, 10, 10), 0, (207, 10, 10))
    volcanic_solid = (20, "so", "Basaltic Plains", (40, 28, 25), 0)

    # ocean biomes?
    # estuary
    # coral reef
    # deep ocean
    # inland sea
    # mediterranean
    # arctic_ocean


class OceanType(SuperEnum):
    __keys__ = ["id", "title"]

    water = (1, "Water")
    magma = (2, "Magma")
    hydrocarbons = (3, "Hydrocarbons")


class HexResourceRating(SuperEnum):
    """((1 + 1) * 60/1000 ) / (60 ^ 2) * 10000"""

    __keys__ = ["id", "title", "rarity", "multiplier"]

    poor = (1, "Poor", 10, 4)
    average = (2, "Average", 6, 3)
    rich = (3, "Rich", 3, 2)
    abundant = (4, "Abundant", 1, 1)


class HexResourceType(SuperEnum):
    __keys__ = ["id", "rarity", "title", "material", "yield", "color"]

    iron_vein = (1, 15, "Iron Vein", 1000, "commonmetals", (100, 0, 0))
    copper_vein = (2, 15, "Copper Vein", 1000, "commonmetals", (0, 100, 0))
    silver_vein = (3, 15, "Silver Vein", 1000, "commonmetals", (0, 0, 100))
    lead_vein = (4, 15, "Lead Vein", 1000, "commonmetals", (100, 0, 100))
    aluminum_vein = (5, 15, "Aluminum Vein", 1000, "commonmetals", (50, 150, 50))
    tin_vein = (6, 15, "Tin Vein", 1000, "commonmetals", (150, 50, 50))
    titanium_vein = (7, 15, "Titanium Vein", 1000, "commonmetals", (200, 50, 200))
    magnesium_vein = (8, 15, "Magnesium Vein", 1000, "commonmetals", (50, 200, 50))

    gold_ore_deposit = (9, 1, "Gold Ore Deposit", 500, "preciousmetals", (255, 0, 0))
    chromite_ore_deposit = (
        10,
        3,
        "Chromite Ore Deposit",
        500,
        "preciousmetals",
        (255, 255, 0),
    )
    monazite_ore_deposit = (
        11,
        5,
        "Monazite Ore Deposit",
        500,
        "preciousmetals",
        (0, 0, 255),
    )
    bastnasite_ore_deposit = (
        12,
        4,
        "Bastnasite Ore Deposit",
        500,
        "preciousmetals",
        (0, 125, 200),
    )
    xenotime_ore_deposit = (
        13,
        1,
        "Xenotime Ore Deposit",
        500,
        "preciousmetals",
        (200, 125, 0),
    )

    graphite_deposit = (14, 10, "Graphite Deposit", 1500, "carbon", (0, 0, 0))
    coal_deposit = (15, 30, "Coal Deposit", 1500, "carbon", (255, 255, 255))

    quartz_deposit = (16, 7, "Quartz Vein", 1000, "silicon", (80, 80, 80))

    uranium_ore_deposit = (17, 1, "Uranium Ore Deposit", 10, "uranium", (255, 50, 50))


class HexEdge(SuperEnum):
    __keys__ = ["id", "title", "short", "arrow"]
    east = (1, "East", "E", "→")
    north_east = (2, "North East", "NE", "↗")
    north_west = (3, "North West", "NW", "↖")
    west = (4, "West", "W", "←")
    south_west = (5, "South West", "SW", "↙")
    south_east = (6, "South East", "SE", "↘")


class MapType(SuperEnum):
    __keys__ = ["id", "title", "colors"]

    terran = (1, "Terran", TERRAIN_TERRAN)
    barren = (2, "Barren", TERRAIN_BARREN)
    gas = (3, "Gas", None)
    volcanic = (4, "Volcanic", TERRAIN_BARREN)
    oceanic = (5, "Oceanic", TERRAIN_OCEANIC)
    glacial = (6, "Barren", TERRAIN_BARREN)


class HexType(Enum):
    land = "Land"  # hex over or at sealevel
    ocean = "Ocean"  # hex under sealevel


class HexSurface(SuperEnum):
    """needed for temperature calculations"""

    __keys__ = ["id", "specific_heat", "albedo"]
    water_fresh = (1, 1.00, 0.0)  # water without salt
    water_sea = (2, 0.94, 0.0)  # water with salt
    granite = (3, 0.19, 0.0)  # continental crust in volcanically active planets
    basalt = (4, 0.20, 0.0)  # volcanic basaltic rock
    soil_wet = (5, 0.35, 0.0)  # soil with organic materials
    soil_dry = (6, 0.19, 0.0)  # desert soil
    soil_barren = (7, 0.10, 0.0)  # barren soil
    ice_warm = (8, 0.50, 0.0)  # ice warmer than -10 degrees F
    ice_cold = (9, 0.40, 0.0)  # ice warmer than -100 deg F to -10 deg F


class HexFeature(Enum):
    """Each hex can have multiple HexFeatures"""

    lake = "Lake"  # The terminus to a river if it didn't reach sealevel
    glacier = "Glacier"  # A water hex with a very low surface temperature

    # randomly placed
    volcano = "Volcano"  # Volcano: 1 hex or 2-ring or 3-ring
    lava_flow = "Lava Flow"
    crater = "Crater"  # depression of size 2-ring or 3-ring

    # bodies of water
    sea = "Sea"
    ocean = "Ocean"


class GeoformType(SuperEnum):
    """A grouping of like geographic features"""

    __keys__ = ["id", "title", "color"]

    # water
    ocean = (1, "Ocean", (0, 0, 255))  # > 100 water hexes
    sea = (2, "Sea", (50, 50, 200))  # < 100 water hexes
    strait = (
        3,
        "Strait",
        (100, 100, 150),
    )  # a water hex with land on opposite sides and water in between them
    lake = (4, "Lake", (0, 0, 100))  # a group of up to 3 water hexes
    bay = (10, "Bay", (50, 50, 150))

    # land
    isthmus = (
        5,
        "Isthmus",
        (100, 150, 100),
    )  # a land hex with water on opposite sides and land in between them
    small_island = (6, "Small Island", (200, 255, 200))  # < 25 land hexes
    large_island = (7, "Large Island", (100, 255, 100))  # < 100 land hexes
    continent = (8, "Continent", (0, 255, 0))  # > 100 land hexes
    peninsula = (9, "Peninsula", (0, 200, 0))  # group of land separated by an isthmus


class EdgeDirection(Enum):
    north = "North"
    south = "South"
    north_west = "North West"
    north_east = "North East"
    south_west = "South West"
    south_east = "South East"


class HexSide(Enum):
    east = "East"
    west = "West"
    north_west = "North West"
    north_east = "North East"
    south_west = "South West"
    south_east = "South East"

    def branching(self, direction):
        """Returns the hex sides that fork from this edge direction"""
        if self is HexSide.east or self is HexSide.west:
            if direction is EdgeDirection.north:
                return HexSide.south_west, HexSide.south_east
            else:  # elif direction is EdgeDirection.south:
                return HexSide.north_west, HexSide.north_east
        elif self is HexSide.south_east:
            if direction is EdgeDirection.north_east:
                return HexSide.west, HexSide.south_west
            else:  # elif direction is EdgeDirection.south_west:
                return HexSide.east, HexSide.north_east
        elif self is HexSide.south_west:
            if direction is EdgeDirection.north_west:
                return HexSide.east, HexSide.south_east
            else:  # elif direction is EdgeDirection.south_east:
                return HexSide.west, HexSide.north_west
        elif self is HexSide.north_west:
            if direction is EdgeDirection.south_west:
                return HexSide.east, HexSide.north_east
            else:  # elif direction is EdgeDirection.north_east:
                return HexSide.west, HexSide.south_west
        elif self is HexSide.north_east:
            if direction is EdgeDirection.north_west:
                return HexSide.east, HexSide.south_east
            else:  # elif direction is EdgeDirection.south_east:
                return HexSide.north_west, HexSide.west
        raise Exception(
            "Branching invalid, Side: {}, Direction: {}".format(self, direction)
        )


class Zones(SuperEnum):
    __keys__ = ["id", "title", "color", "map_key", "incr"]

    arctic_circle = (1, "Artic Circle", (150, 150, 250), "N", 0.60)
    northern_temperate = (2, "Northern Temperate", (150, 250, 150), "A", 0.90)
    northern_subtropics = (3, "Nothern Subtropics", (150, 250, 200), "B", 0.60)
    northern_tropics = (4, "Northern Tropics", (230, 150, 150), "C", 0.30)
    southern_tropics = (5, "Southern Tropics", (250, 180, 150), "D", 0.30)
    southern_subtropics = (6, "Southern Subtropics", (150, 250, 200), "E", 0.60)
    southern_temperate = (7, "Southern Temperate", (150, 250, 150), "F", 0.90)
    antarctic_circle = (8, "Antarctic Circle", (150, 150, 250), "S", 0.60)


class Hemisphere(Enum):
    northern = "Northern"
    southern = "Southern"


class Season(Enum):
    winter = "Winter"
    spring = "Spring"
    summer = "Summer"
    autumn = "Autumn"


class KoppenClimate(SuperEnum):
    __keys__ = ["id", "code", "title", "color", "description"]

    default = (0, "XX", "Default", (255, 255, 255), "Default climate")
    tropical_rainforest = (
        1,
        "Af",
        "Tropical Rainforest",
        (0, 0, 255),
        "Rainforest climate",
    )
    tropical_monsoon = (2, "Am", "Tropical Monsoon", (0, 182, 255), "Monsoon climate")
    tropical_dry_winter_savanna = (
        3,
        "Aw",
        "Tropical Savanna, dry winter",
        (142, 214, 253),
        "Savanna dry winter climate",
    )
    arid_desert_hot = (4, "BWh", "Arid Desert Hot", (255, 0, 0), "Hot desert climate")
    arid_desert_cold = (
        5,
        "BWk",
        "Arid Desert Cold",
        (255, 202, 202),
        "Cold desert climate",
    )
    arid_steppe_hot = (
        6,
        "BSh",
        "Arid Steppe Hot",
        (251, 211, 0),
        "Hot semi-arid climate",
    )
    arid_steppe_cold = (
        7,
        "BSk",
        "Arid Steppe Cold",
        (255, 238, 167),
        "Cold semi-arid climate",
    )
    temperate_dry_winter_hot_summer = (
        8,
        "Cwa",
        "Temperate Dry Winter, Hot Summer",
        (202, 255, 202),
        "Moonsoon-influenced humid subtropical climate",
    )
    temperate_dry_winter_warm_summer = (
        9,
        "Cwb",
        "Temperate Dry Winter, Warm Summer",
        (167, 229, 167),
        "Subtropical highland climate or Moonsoon-influenced temperate oceanic climate",
    )
    temperate_dry_winter_cold_summer = (
        10,
        "Cwc",
        "Temperate Dry Winter, Cold Summer",
        (124, 202, 124),
        "Cold subtropical highland climate or Moonsoon-influenced temperate oceanic climate",
    )
    temperate_humid_subtropical = (
        11,
        "Cfa",
        "Temperate Humid Subtropical",
        (229, 255, 151),
        "Humid subtropical climate",
    )
    temperate_oceanic = (
        12,
        "Cfb",
        "Temperate Oceanic",
        (167, 255, 151),
        "Temperate oceanic climate or subtropical highland climate",
    )
    temperate_subpolar_oceanic = (
        13,
        "Cfc",
        "Temperate Subpolar Oceanic",
        (124, 229, 0),
        "Subpolar oceanic climate",
    )
    temperate_dry_summer_hot_summer = (
        14,
        "Csa",
        "Temperate Dry Summer, Hot Summer",
        (255, 255, 0),
        "Mediterranean climate, hot summer",
    )
    temperate_dry_summer_warm_summer = (
        15,
        "Csb",
        "Temperate Dry Summer, Warm Summer",
        (229, 229, 0),
        "Mediterranean climate, warm summer",
    )
    temperate_dry_summer_cold_summer = (
        16,
        "Csc",
        "Temperate Dry Summer, Cold Summer",
        (202, 202, 0),
        "Mediterranean climate, cold summer",
    )
    continental_humid_hot_summer = (
        17,
        "Dfa",
        "Continental Humid Hot Summer",
        (0, 255, 255),
        "Hot-summer humid continental climate",
    )
    continental_humid_warm_summer = (
        18,
        "Dfb",
        "Continental Humid Warm Summer",
        (129, 229, 255),
        "Warm-summer humid continental climate",
    )
    continental_humid_cold = (
        19,
        "Dfc",
        "Continental Humid Cold",
        (0, 186, 186),
        "Subarctic climate",
    )
    continental_humid_very_cold = (
        20,
        "Dfd",
        "Continental Humid Very Cold",
        (0, 142, 163),
        "Extremely cold subarctic climate",
    )
    continental_dry_winter_hot_summer = (
        21,
        "Dsa",
        "Continental Dry Winter, Hot Summer",
        (243, 188, 255),
        "Mediterranean-influenced hot-summer humid continental climate",
    )
    continental_dry_winter_warm_summer = (
        22,
        "Dsb",
        "Continental Dry Winter, Warm Summer",
        (218, 159, 238),
        "Mediterranean-influenced warm-summer humid continental climate",
    )
    continental_dry_winter_cold_summer = (
        23,
        "Dsc",
        "Continental Dry Winter, Cold Summer",
        (188, 124, 211),
        "Mediterranean-influenced subarctic climate",
    )
    continental_dry_winter_very_cold = (
        24,
        "Dsd",
        "Continental Dry Winter, Very Cold",
        (159, 88, 179),
        "Mediterranean-influenced extremely cold subarctic climate",
    )
    continental_dry_summer_hot_summer = (
        25,
        "Dwa",
        "Continental Dry Summer, Hot Summer",
        (214, 216, 255),
        "Moonsoon-influenced hot-summer humid continental climate",
    )
    continental_dry_summer_warm_summer = (
        26,
        "Dwb",
        "Continental Dry Summer, Warm Summer",
        (175, 182, 229),
        "Moonsoon-influenced warm-summer humid continental climate",
    )
    continental_dry_summer_cold_summer = (
        27,
        "Dwc",
        "Continental Dry Summer, Cold Summer",
        (147, 151, 229),
        "Moonsoon-influenced subarctic climate",
    )
    continental_dry_summer_very_cold = (
        28,
        "Dwd",
        "Continental Dry Summer, Very Cold",
        (124, 0, 192),
        "Moonsoon-influenced extremely cold subarctic climate",
    )
    polar_tundra = (29, "ET", "Polar Tundra", (218, 218, 218), "Tundra climate")
    polar_ice_cap = (30, "EF", "Polar Ice Cap", (172, 172, 172), "Ice cap climate")

    @classmethod
    def get_colors(cls):
        """Returns a list of colors for all climate types"""
        return [cls[x].color for x in list(cls.__members__)]

    def toBiome(cls):
        """Returns the biome associated with this climate type"""
        if cls in [
            KoppenClimate.tropical_rainforest,
        ]:
            return Biome.tropical_rainforest
        elif cls in [
            KoppenClimate.tropical_monsoon,
        ]:
            return Biome.tropical_forest
        elif cls in [
            KoppenClimate.tropical_dry_winter_savanna,
        ]:
            return Biome.savanna
        elif cls in [
            KoppenClimate.arid_desert_hot,
            KoppenClimate.arid_desert_cold,
        ]:
            return Biome.desert
        elif cls in [
            KoppenClimate.temperate_dry_winter_hot_summer,
            KoppenClimate.temperate_dry_winter_warm_summer,
            KoppenClimate.temperate_dry_winter_cold_summer,
            KoppenClimate.temperate_oceanic,
            KoppenClimate.temperate_subpolar_oceanic,
            KoppenClimate.temperate_dry_summer_hot_summer,
            KoppenClimate.temperate_dry_summer_warm_summer,
            KoppenClimate.temperate_dry_summer_cold_summer,
        ]:
            return Biome.temperate_forest
        elif cls in [
            KoppenClimate.temperate_humid_subtropical,
        ]:
            return Biome.temperate_rainforest
        elif cls in [
            KoppenClimate.arid_steppe_hot,
            KoppenClimate.arid_steppe_cold,
            KoppenClimate.continental_dry_winter_hot_summer,
            KoppenClimate.continental_dry_winter_warm_summer,
            KoppenClimate.continental_dry_summer_hot_summer,
            KoppenClimate.continental_dry_summer_warm_summer,
        ]:
            return Biome.grasslands
        elif cls in [
            KoppenClimate.continental_humid_hot_summer,
            KoppenClimate.continental_humid_warm_summer,
        ]:
            return Biome.shrubland
        elif cls in [
            KoppenClimate.continental_humid_cold,
            KoppenClimate.continental_dry_winter_cold_summer,
            KoppenClimate.continental_dry_summer_cold_summer,
        ]:
            return Biome.boreal_forest
        elif cls in [
            KoppenClimate.continental_dry_summer_very_cold,
            KoppenClimate.continental_dry_winter_very_cold,
            KoppenClimate.continental_humid_very_cold,
        ]:
            return Biome.alpine_tundra
        elif cls in [
            KoppenClimate.polar_tundra,
        ]:
            return Biome.tundra
        elif cls in [
            KoppenClimate.polar_ice_cap,
        ]:
            return Biome.arctic

        return Biome.lifeless
