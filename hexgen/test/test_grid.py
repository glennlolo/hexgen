from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from hexgen.grid import Grid, GridBoundsException
from hexgen.heightmap import Heightmap
from hexgen.hex import Hex
from hexgen.mapgen import default_params

import numpy as np

class TestGrid(TestCase):

    def setUp(self):
        self.params = default_params
        self.size = 50
        self.params["size"] = self.size
        self.heightmap = Heightmap(self.params)
        self.grid = Grid(self.heightmap, self.params)

    def test_init(self):
        self.assertEqual(self.grid.grid.shape[0], self.size, "Grid size is incorrect")
        self.assertEqual(self.grid.grid.shape[1], self.size, "Grid size is incorrect")
        self.assertEqual(self.grid.heightmap, self.heightmap, "Grid heightmap is incorrect")
        self.assertIsNone(self.grid.climateMap, "Climate map should be empty on default initialization")
        self.assertEqual(self.grid.sealevel, self.heightmap.sealevel, "Grid sealevel is incorrect")
        self.assertEqual(self.grid.average_height, self.heightmap.average_height, "Grid average height is incorrect")
        self.assertEqual(self.grid.highest_height, self.heightmap.highest_height, "Grid highest height is incorrect")
        self.assertEqual(self.grid.lowest_height, self.heightmap.lowest_height, "Grid lowest height is incorrect")
        self.assertEqual(self.grid.max_size, self.size, "Grid max size is incorrect")
        self.assertEqual(self.grid.centerLatitude, 0, "Grid center latitude should be 0 on default initialization")
        self.assertEqual(self.grid.latitudeRange, [90, -90], "Grid latitude range should be [-90, 90] on default initialization")

    def test_find_hex(self):
        with self.assertRaises(GridBoundsException):
            self.grid.find_hex(self.size, 0)
        with self.assertRaises(GridBoundsException):
            self.grid.find_hex(0, self.size)

    def test_calculate(self):
        self.grid.calculate()
        #Verify at the closest integer
        self.assertAlmostEqual(self.grid.avg_altitude, self.heightmap.average_height, 0, "Grid average altitude is incorrect")
        self.assertIsInstance(self.grid.hexes[0], Hex, "Grid hexes should be a list")
        #Verify the hexes are sorted by temperature
        self.assertTrue(all(self.grid.hexes[i].temperature <= self.grid.hexes[i + 1].temperature for i in range(len(self.grid.hexes) - 1)))
        #verify the clodest hexes are the 10% coldest hexes
        self.assertEqual(len(self.grid.coldest_hexes), int(self.size**2 * 0.10), "Grid coldest hexes should be %i" % int(self.size**2 * 0.10))

    def test_debug(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.grid = Grid(self.heightmap, self.params, debug=True)
            self.assertIn("Making grid", fake_out.getvalue())

class TestGridWithCrop(TestCase):

    def setUp(self):
        self.params = default_params
        self.size = 50
        self.params["size"] = self.size
        self.params["crop"] = True
        self.params["cropValue"] = [5000, 1400, 5701, 2084]
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        self.heightmap = Heightmap(self.params, False, heightmapFile)
        self.grid = Grid(self.heightmap, self.params)

    def test_init(self):
        self.assertEqual(self.grid.grid.shape[0], self.size, "Grid size is incorrect")
        self.assertEqual(self.grid.grid.shape[1], self.size, "Grid size is incorrect")
        self.assertEqual(self.grid.heightmap, self.heightmap, "Grid heightmap is incorrect")
        self.assertIsNone(self.grid.climateMap, "Climate map should be empty on default initialization")
        self.assertEqual(self.grid.sealevel, self.heightmap.sealevel, "Grid sealevel is incorrect")
        self.assertEqual(self.grid.average_height, self.heightmap.average_height, "Grid average height is incorrect")
        self.assertEqual(self.grid.highest_height, self.heightmap.highest_height, "Grid highest height is incorrect")
        self.assertEqual(self.grid.lowest_height, self.heightmap.lowest_height, "Grid lowest height is incorrect")
        self.assertEqual(self.grid.max_size, self.size, "Grid max size is incorrect")
        self.assertEqual(self.grid.centerLatitude, 13.447265625, "Grid center latitude is incorrect")
        self.assertEqual(self.grid.latitudeRange, [28.4765625, -1.58203125], "Grid latitude range is incorrect")

    def test_debug(self):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.grid = Grid(self.heightmap, self.params, debug=True)
                self.assertIn("Making grid", fake_out.getvalue())
                self.assertIn("Centering grid latitude at : 13.447265625, with range [28.4765625, -1.58203125]", fake_out.getvalue())

class TestGridWithClimateMap(TestCase):

    def setUp(self):
        self.params = default_params
        self.size = 50
        self.params["size"] = self.size
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        landMaskFile = "hexgen/test/orogen-landmask-0486ll4cxgegk2cs6um9hh.png"
        self.params["climateMapFile"] = "hexgen/test/orogen-climate-0486ll4cxgegk2cs6um9hh.png"
        self.heightmap = Heightmap(self.params, False, heightmapFile, landMaskFile)
        self.grid = Grid(self.heightmap, self.params)

    def test_climate_map(self):
        self.assertIsNotNone(self.grid.climateMap, "Climate map should not be None when provided")
        self.assertEqual(self.grid.climateMap.shape[0], self.size, "Climate map size is incorrect")
        self.assertEqual(self.grid.climateMap.shape[1], self.size, "Climate map size is incorrect")
        self.assertIsInstance(self.grid.climateMap[0][0], np.uint8, "Climate map values should be integers representing climate IDs")
        self.assertGreaterEqual(np.min(self.grid.climateMap), 0, "Climate map values should be non-negative integers")
        self.assertLessEqual(np.max(self.grid.climateMap), 30, "Climate map values should not be greater than the number of defined Koppen climates (30)")

class TestGridWithCropAndClimateMap(TestCase):

    def setUp(self):
        self.params = default_params
        self.size = 50
        self.params["size"] = self.size
        self.params["crop"] = True
        self.params["cropValue"] = [5000, 1400, 5701, 2084]
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        landMaskFile = "hexgen/test/orogen-landmask-0486ll4cxgegk2cs6um9hh.png"
        self.params["climateMapFile"] = "hexgen/test/orogen-climate-0486ll4cxgegk2cs6um9hh.png"
        self.heightmap = Heightmap(self.params, False, heightmapFile, landMaskFile)
        self.grid = Grid(self.heightmap, self.params)

    def test_climate_map(self):
        self.assertIsNotNone(self.grid.climateMap, "Climate map should not be None when provided")
        self.assertEqual(self.grid.climateMap.shape[0], self.size, "Climate map size is incorrect")
        self.assertEqual(self.grid.climateMap.shape[1], self.size, "Climate map size is incorrect")
        self.assertIsInstance(self.grid.climateMap[0][0], np.uint8, "Climate map values should be integers representing climate IDs")
        self.assertGreaterEqual(np.min(self.grid.climateMap), 0, "Climate map values should be non-negative integers")
        self.assertLessEqual(np.max(self.grid.climateMap), 30, "Climate map values should not be greater than the number of defined Koppen climates (30)")