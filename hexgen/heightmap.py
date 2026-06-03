import math
import random
import numpy as np
from PIL import Image, ImageFilter


class Heightmap:

    def __init__(self, params, debug=False, heightmapFile="", landMaskFile=""):
        self.params = params

        self.size = params.get("size")
        if isinstance(self.size, int):
            #If their is only one value for size, we consider the heightmap to be square
            self.height = self.size
            self.width = self.size
        elif isinstance(self.size, tuple) and len(self.size) == 2:
            self.width = self.size[0]
            self.height = self.size[1]
        else:
            raise ValueError("Size parameter must be a single value or a tuple of two values (height, width)")

        self.grid = np.ndarray((self.height, self.width), dtype=float)
        if heightmapFile == "":
            # start making the heightmap
            self.grid[0][0] = random.randint(0, 255)
            self.grid[self.height - 1][0] = random.randint(0, 255)
            self.grid[0][self.width - 1] = random.randint(0, 255)
            self.grid[self.height - 1][self.width - 1] = random.randint(0, 255)
            self._subdivide(0, 0, self.height - 1, self.width - 1)

            # compute average and record top height
            avg = []
            m = []
            for g in self.grid:
                m.append(max(g))
                avg.append(sum(g) / float(len(g)))

            self.highest_height = max(m)
            self.lowest_height = min(m)
            self.average_height = sum(avg) / float(len(avg))
            sea_percent = params.get("sea_percent")
            self.sealevel = round(self.average_height * (sea_percent * 2 / 100))

            if sea_percent == 100:
                self.sealevel = 255

            if debug:
                print("Sea level at {} or {}%".format(self.sealevel, sea_percent))
        else:
            # load heightmap from file
            print("Loading heightmap from file: {}".format(heightmapFile))
            im = Image.open(heightmapFile)
            self.fullMapSize = im.size  # Get the full map size
            if params.get("crop") != []:
                print(
                    "Cropping heightmap with coordinates: {}".format(params.get("crop"))
                )
                im = im.crop(params.get("crop"))
            if debug:
                im.show()
            imSize = im.size  # Get the width and height of the image
            factor = (math.floor(imSize[0] / self.width), math.floor(imSize[1] / self.height))  # Calculate the scaling factor
            pix = im.get_flattened_data()  # Get the pixel data of the image
            maxPix = max(pix)  # Get the maximum pixel value to normalize the heightmap
            for i in range(self.height):
                for j in range(self.width):
                    p = []
                    # Construct the pixels of the original image
                    for k in range(factor[0]):
                        p.append(
                            pix[
                                int(i * factor[1] * imSize[0] + (k + j * factor[0])) : int(
                                    (i + 1) * factor[1] * imSize[0] + (k + j * factor[0])
                                ) : imSize[0]
                            ]
                        )
                    # Average the pixel values to get the height value for the heightmap
                    self.grid[i][j] = np.mean(p) * 255 / maxPix
            self.highest_height = np.max(self.grid)
            self.lowest_height = np.min(self.grid)
            self.average_height = np.median(self.grid)
            if landMaskFile == "":
                # By default use 0.0 as default sea level
                self.sealevel = 1.0
                if debug:
                    print(
                        "Sea level defaulting at {} for heightmap file".format(
                            self.sealevel
                        )
                    )
            else:
                # Use LandMaskFile if their is one provided to compute sea shores height
                print(
                    "Loading land mask to compute shores from file: {}".format(
                        landMaskFile
                    )
                )
                imMask = Image.open(landMaskFile)
                if params.get("crop") != []:
                    print(
                        "Cropping LandMask with coordinates: {}".format(
                            params.get("crop")
                        )
                    )
                    imMask = imMask.crop(params.get("crop"))
                imContour = imMask.filter(
                    ImageFilter.CONTOUR
                )  # Find the edges of the land mask to compute the shores
                imContour = imContour.crop(
                    [1, 1, imContour.size[0] - 1, imContour.size[1] - 1]
                )  # Crop the contour to remove the black border
                pixContour = imContour.get_flattened_data()  # Get the contours pixels
                if debug:
                    imContour.show()
                contourHeight = []
                for i in range(self.height):
                    for j in range(self.width):
                        # Construct the pixels of the original image
                        for k in range(factor[0]):
                            p = pixContour[
                                int(i * factor[1] * imSize[0] + (k + j * factor[0])) : int(
                                    (i + 1) * factor[1] * imSize[0] + (k + j * factor[0])
                                ) : imSize[0]
                            ]
                            if any(slice == (0, 0, 0, 255) for slice in p):
                                contourHeight.append(
                                    self.grid[i][j]
                                )  # Get the height values of the shores to compute the sea level
                                break
                self.sealevel = np.median(
                    contourHeight
                )  # The sea level is equal to the one of the
                if debug:
                    print(
                        "Sea level median at {} for landMask file".format(self.sealevel)
                    )

    def height_at(self, x, y):
        return self.grid[x][y]

    def _adjust(self, xa, ya, x, y, xb, yb):
        """fix the sides of the map"""
        if self.grid[x][y] == 0:
            d = math.fabs(xa - xb) + math.fabs(ya - yb)
            ROUGHNESS = self.params.get("roughness")
            v = (self.grid[xa][ya] + self.grid[xb][yb]) / 2.0 + (
                random.random() - 0.5
            ) * d * ROUGHNESS
            c = int(math.fabs(v) % 257)
            if y == 0:
                self.grid[x][self.height - 1] = c
            if x == 0 or x == self.width - 1:
                if y < self.height - 1:
                    self.grid[x][self.height - 1 - y] = c
            range_low, range_high = self.params.get("height_range")
            if c < range_low:
                c = range_low
            elif c > range_high:
                c = range_high
            self.grid[x][y] = c

    def _subdivide(self, x1, y1, x2, y2):
        """subdivide the heightmap iterate"""
        if not ((x2 - x1 < 2.0) and (y2 - y1 < 2.0)):
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)

            v = int(
                (
                    self.grid[x1][y1]
                    + self.grid[x2][y1]
                    + self.grid[x2][y2]
                    + self.grid[x1][y2]
                )
                / 4
            )
            range_low, range_high = self.params.get("height_range")
            if v < range_low:
                v = range_low
            elif v > range_high:
                v = range_high
            self.grid[x][y] = v

            self._adjust(x1, y1, x, y1, x2, y1)
            self._adjust(x2, y1, x2, y, x2, y2)
            self._adjust(x1, y2, x, y2, x2, y2)
            self._adjust(x1, y1, x1, y, x1, y2)

            self._subdivide(x1, y1, x, y)
            self._subdivide(x, y1, x2, y)
            self._subdivide(x, y, x2, y2)
            self._subdivide(x1, y, x, y2)
