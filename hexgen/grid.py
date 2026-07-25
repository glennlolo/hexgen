import math
from PIL import Image
import numpy as np
from hexgen.hex import Hex
from hexgen.enums import KoppenClimate
from hexgen.constants import OROGEN_KOPPEN_DEFAULT_COLORS

class GridBoundsException(Exception):
    pass


class Grid:
    def __init__(self, heightmap, params, debug=False):
        self.heightmap = heightmap
        self.sealevel = heightmap.sealevel
        self.params = params
        self.average_height = heightmap.average_height
        self.highest_height = heightmap.highest_height
        self.lowest_height = heightmap.lowest_height
        self.max_size = np.max([self.heightmap.height, self.heightmap.width])
        
        self.climateMap = None #By default no climate map is loaded

        self.avg_altitude = 0

        self.hexes = []
        self.coldest_hexes = []

        if debug:
            print("Making grid")
        self.num_ocean_hexes = 0
        self.grid = np.ndarray(
            (self.heightmap.height, self.heightmap.width), dtype=object
        )
        for y in range(self.heightmap.width):
            for x in range(self.heightmap.height):
                self.grid[x][y] = Hex(self, x, y, self.heightmap.height_at(x, y))
                if self.grid[x][y].is_water:
                    self.num_ocean_hexes += 1

        if self.params.get("crop"):
            # if their is cropping, then change center latitude of the grid
            crop = self.params.get("cropValue")
            # The center latitude is obtained by a three rule
            self.centerLatitude = (
                (
                    self.heightmap.fullMapSize[1] / 2
                    - (crop[1] + (crop[3] - crop[1]) / 2)
                )
                * 90
                / (self.heightmap.fullMapSize[1] / 2)
            )
            self.latitudeRange = [
                (self.heightmap.fullMapSize[1] / 2 - crop[1])
                * 90
                / (self.heightmap.fullMapSize[1] / 2),
                (self.heightmap.fullMapSize[1] / 2 - crop[3])
                * 90
                / (self.heightmap.fullMapSize[1] / 2),
            ]
            if debug:
                print(
                    "Centering grid latitude at : {}, with range {}".format(
                        self.centerLatitude, self.latitudeRange
                    )
                )
        else:
            self.centerLatitude = 0.0
            self.latitudeRange = [90, -90]

        if params.get("climateMapFile") != "":
            # Load climate map from file and store it in the grid
            if debug:
                print("Loading climate map from file: {}".format(params.get("climateMapFile")))
            im = Image.open(params.get("climateMapFile"))
            if params["crop"]:
                im = im.crop(params.get("cropValue"))
            if debug:
                im.show()
            imMap = im.get_flattened_data()
            imSize = im.size
            self.climateMap = np.zeros((self.grid.shape[0], self.grid.shape[1]), dtype=int)
            KoppenClimateColors = KoppenClimate.get_colors()
            if self.heightmap.factor == (None, None):
                # Need to calculate the factor for climate map scaling
                self.heightmap.factor = (
                                math.floor(imSize[0] / self.grid.shape[1]),
                                math.floor(imSize[1] / self.grid.shape[0]),
                            )  # Calculate the scaling factor
            for i in range(self.grid.shape[0]):
                for j in range(self.grid.shape[1]):
                    p = []
                    for k in range(self.heightmap.factor[0]):
                        p.extend(
                            imMap[
                                int(
                                    i * self.heightmap.factor[1] * imSize[0] + (k + j * self.heightmap.factor[0])
                                ) : int(
                                    (i + 1) * self.heightmap.factor[1] * imSize[0]
                                    + (k + j * self.heightmap.factor[0])
                                ) : imSize[
                                    0
                                ]
                            ]
                        )
                    uniqValues, uniqCounts = np.unique(p, axis=0, return_counts=True)
                    climateHex = tuple(uniqValues[np.argmax(uniqCounts)].tolist()) #Get the most present color
                    
                    if tuple(climateHex[0:3]) in KoppenClimateColors:
                        self.climateMap[i][j] = KoppenClimate.default.get(KoppenClimateColors.index(climateHex[0:3])).id
                    elif tuple(climateHex[0:3]) in OROGEN_KOPPEN_DEFAULT_COLORS:
                        self.climateMap[i][j] = KoppenClimate.default.id #Get default climate for zones not needing it
                    else:
                        raise Exception("Color {} at {}, {} in climate map is not a valid KoppenClimate color".format(climateHex[0:3], i, j))
            if debug:
                climateMapColor = np.zeros((self.grid.shape[0], self.grid.shape[1], 3), dtype=np.uint8)
                for x in range(self.grid.shape[0]):
                    for y in range(self.grid.shape[1]):
                        climateMapColor[x][y] = KoppenClimate.default.get(self.climateMap[x][y]).color
                im = Image.fromarray(climateMapColor, mode="RGB")
                im.show()

        self.calculate()

    @property
    def size(self):
        return self.params.get("size")

    def find_hex(self, x, y):
        """Finds a hex and a x and y coordinate"""
        try:
            return self.grid[x][y]
        except IndexError:
            raise GridBoundsException("Invalid coordinates {}, {}".format(x, y))

    def calculate(self):
        # run through the grid, calculate the edges
        alt = 0
        hexes = []
        for y in range(self.heightmap.width):
            for x in range(self.heightmap.height):
                self.grid[x][y].calculate()
                alt += self.grid[x][y].altitude
                hexes.append(self.grid[x][y])
        self.avg_altitude = round(alt / math.pow(self.max_size, 2))

        self.hexes = sorted(hexes, key=lambda x: x.temperature)

        number = round(len(self.hexes) * 0.10)
        self.coldest_hexes = self.hexes[:number]
