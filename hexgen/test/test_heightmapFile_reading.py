from unittest import TestCase

from hexgen.mapgen import default_params
from hexgen.heightmap import Heightmap


class TestHeightmapFileReading(TestCase):

    def setUp(self):
        params = default_params
        self.size = 100
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        params["size"] = self.size
        self.heightmap = Heightmap(params,False,heightmapFile)

    def test_init(self):
        self.assertEqual(len(self.heightmap.grid), self.size, "Grid size is incorrect")

    def test_wrap(self):
        self.assertEqual(
            self.heightmap.grid[1][0],
            self.heightmap.grid[1][-1],
            "Heightmap does not wrap horizontally",
        )
        self.assertEqual(
            self.heightmap.grid[-1][1],
            self.heightmap.grid[-1][-2],
            "Heightmap does not wrap vertically on the bottom",
        )

    def test_sealevel(self):
        self.assertEqual(
            self.heightmap.sealevel,
            0.0,
            "Heightmap sealevel should be 0 when loading from file",
        )

    def test_height_min(self):
        self.assertEqual(
            self.heightmap.lowest_height,
            0.0,
            "Minimim height should be 0 when loading from file",
        )

    def test_height_max(self):
        self.assertEqual(
            self.heightmap.highest_height,
            65157.0,
            "Maximum height should be 65157.0 when loading this file",
        )

    def test_height_avg(self):
        self.assertEqual(
            self.heightmap.average_height,
            3636.7816,
            "Average height should be 3636.7816 when loading this file",
        )
