from unittest import TestCase

from hexgen.mapgen import default_params
from hexgen.heightmap import Heightmap


class TestHeightmap(TestCase):

    def setUp(self):
        params = default_params
        self.size = 50
        params["size"] = self.size
        self.heightmap = Heightmap(params)

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


class TestHeightmapFileReading(TestCase):

    def setUp(self):
        params = default_params
        self.size = 100
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        params["size"] = self.size
        self.heightmap = Heightmap(params, False, heightmapFile)

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
            1.0,
            "Heightmap sealevel should be 1.0 when loading from file",
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
            255.0,
            "Maximum height should be 255.0 when loading this file",
        )

    def test_height_avg(self):
        self.assertEqual(
            self.heightmap.average_height,
            0.4436065175097276,
            "Average height should be 0.4436065175097276 when loading this file",
        )


class TestLandmaskFileReading(TestCase):

    def setUp(self):
        params = default_params
        self.size = 100
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        landMaskFile = "hexgen/test/orogen-landmask-0486ll4cxgegk2cs6um9hh.png"
        params["size"] = self.size
        self.heightmap = Heightmap(params, False, heightmapFile, landMaskFile)

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
            0.16802042801556422,
            "Sea level from land mask should be 0.16802042801556422 when loading from file",
        )


class TestCropping(TestCase):

    def setUp(self):
        params = default_params
        self.size = 100
        self.crop = [5000, 1400, 5701, 2084]
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        landMaskFile = "hexgen/test/orogen-landmask-0486ll4cxgegk2cs6um9hh.png"
        params["size"] = self.size
        params["crop"] = self.crop
        self.heightmap = Heightmap(params, False, heightmapFile, landMaskFile)

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
            0.008378101328286758,
            "Sea level from land mask should be 0.008378101328286758 when loading from file",
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
            240.2090296537094,
            "Maximum height should be 240.2090296537094 when loading this file",
        )

    def test_height_avg(self):
        self.assertEqual(
            self.heightmap.average_height,
            0.01156718505969914,
            "Average height should be 0.01156718505969914 when loading this file",
        )


class TestHeightmapSizes(TestCase):

    def setUp(self):
        params = default_params
        self.size = [100, 150]
        params["size"] = self.size
        self.heightmap = Heightmap(params)

    def test_init(self):
        self.assertEqual(len(self.heightmap.grid), self.size[0], "Grid height is incorrect")
        self.assertEqual(len(self.heightmap.grid[0]), self.size[1], "Grid width is incorrect")

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


class TestCroppingSizes(TestCase):

    def setUp(self):
        params = default_params
        self.size = (100,150)
        self.crop = [5000, 1400, 5701, 2084]
        heightmapFile = "hexgen/test/orogen-land-heightmap-0486ll4cxgegk2cs6um9hh.png"
        landMaskFile = "hexgen/test/orogen-landmask-0486ll4cxgegk2cs6um9hh.png"
        params["size"] = self.size
        params["crop"] = self.crop
        self.heightmap = Heightmap(params, False, heightmapFile, landMaskFile)

    def test_init(self):
        self.assertEqual(len(self.heightmap.grid), self.size[0], "Grid height is incorrect")
        self.assertEqual(len(self.heightmap.grid[0]), self.size[1], "Grid width is incorrect")

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
            0.008378101328286758,
            "Sea level from land mask should be 0.008378101328286758 when loading from file",
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
            240.2090296537094,
            "Maximum height should be 240.2090296537094 when loading this file",
        )

    def test_height_avg(self):
        self.assertEqual(
            self.heightmap.average_height,
            0.01156718505969914,
            "Average height should be 0.01156718505969914 when loading this file",
        )