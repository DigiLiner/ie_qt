import unittest

def box_blur(src, radius):
    """
    Applies a box blur to a source image represented by a 2D list of RGBA tuples.
    This is the corrected version of the user's code.
    """
    if not src or (isinstance(src, list) and len(src) > 0 and not src[0]):
        return []
    h = len(src)
    w = len(src[0])
    # Create a destination image buffer with the same dimensions
    dst = [[(0, 0, 0, 0) for _ in range(w)] for _ in range(h)]

    if radius <= 0:
        # Return a copy of the source if radius is non-positive
        return [row[:] for row in src]

    for y in range(h):
        for x in range(w):
            # Define the bounding box for the blur kernel
            y0 = max(0, y - radius)
            y1 = min(h - 1, y + radius)
            x0 = max(0, x - radius)
            x1 = min(w - 1, x + radius)

            r_sum, g_sum, b_sum, a_sum = 0, 0, 0, 0
            count = 0
            
            # Iterate over the kernel area
            for yy in range(y0, y1 + 1):
                row = src[yy]
                for xx in range(x0, x1 + 1):
                    # This fixes the bug where 'xx' was used before definition and
                    # robustly checks for malformed data.
                    if isinstance(row, (list, tuple)) and len(row) > xx:
                        pixel = row[xx]
                        if isinstance(pixel, (list, tuple)) and len(pixel) == 4:
                            pr, pg, pb, pa = pixel
                            r_sum += pr
                            g_sum += pg
                            b_sum += pb
                            a_sum += pa
                            count += 1
            
            # Calculate the average and update the destination pixel
            if count > 0:
                dst[y][x] = (r_sum // count, g_sum // count, b_sum // count, a_sum // count)
            elif len(src[y]) > x and isinstance(src[y][x], (list, tuple)) and len(src[y][x]) == 4:
                # Fallback to original pixel if no valid neighbors were found.
                dst[y][x] = src[y][x]

    return dst


class TestBoxBlur(unittest.TestCase):
    """Unit tests for the box_blur function."""

    def test_simple_blur(self):
        """Test a basic 3x3 image with radius 1."""
        black = (0, 0, 0, 255)
        white = (255, 255, 255, 255)
        
        src_image = [
            [black, black, black],
            [black, white, black],
            [black, black, black]
        ]
        
        blurred_image = box_blur(src_image, 1)
        
        # Center pixel (1,1) is white, surrounded by 8 black pixels. Kernel size is 9.
        # Average is (255/9, 255/9, 255/9) -> (28, 28, 28)
        # Alpha is (255*9)/9 -> 255
        self.assertEqual(blurred_image[1][1], (28, 28, 28, 255))

        # Top-left corner (0,0) averages 4 pixels: (0,0), (0,1), (1,0), (1,1). Kernel size is 4.
        # 3 black, 1 white. Average is (255/4, 255/4, 255/4) -> (63, 63, 63)
        self.assertEqual(blurred_image[0][0], (63, 63, 63, 255))
        
        # Top-middle (0,1) averages 6 pixels. 5 black, 1 white. Kernel size is 6.
        # Average is (255/6, 255/6, 255/6) -> (42, 42, 42)
        self.assertEqual(blurred_image[0][1], (42, 42, 42, 255))

    def test_radius_zero(self):
        """Test with radius 0; should return an identical copy of the original image."""
        src_image = [
            [(10, 20, 30, 255), (40, 50, 60, 255)],
            [(70, 80, 90, 255), (100, 110, 120, 255)]
        ]
        original_image_copy = [row[:] for row in src_image]
        
        blurred_image = box_blur(src_image, 0)
        
        self.assertEqual(blurred_image, original_image_copy)
        self.assertIsNot(blurred_image, src_image)

    def test_single_pixel_image(self):
        """Test a 1x1 image; it should remain unchanged."""
        src_image = [[(100, 150, 200, 255)]]
        blurred_image = box_blur(src_image, 5)
        self.assertEqual(blurred_image, src_image)
        
    def test_empty_image(self):
        """Test with an empty image to ensure no errors."""
        self.assertEqual(box_blur([], 1), [])
        self.assertEqual(box_blur([[]], 1), [])

    def test_malformed_data(self):
        """Test an image with inconsistent row lengths and invalid pixel data."""
        black = (0, 0, 0, 255)
        
        src_image = [
            [black, black, black],
            [black, "not a pixel", black],
            [black, black]  # Note: This row is shorter than others
        ]
        
        blurred_image = box_blur(src_image, 1)

        # For pixel (1,1), the kernel includes 8 valid neighbors (all black) and 1 invalid center.
        # The 8 valid black pixels are averaged. Count is 8.
        # r,g,b sums are 0. a_sum = 8 * 255.
        # Result: (0 // 8, 0 // 8, 0 // 8, (8*255) // 8) -> (0, 0, 0, 255).
        self.assertEqual(blurred_image[1][1], (0, 0, 0, 255))

        # For pixel (0,0), kernel has 4 potential pixels.
        # (0,0) black, (0,1) black, (1,0) black, (1,1) invalid.
        # The average is of 3 black pixels. Result is black.
        self.assertEqual(blurred_image[0][0], (0, 0, 0, 255))
        
        # For pixel (2, 2), it's out of bounds of the original image data definition,
        # but the destination array is full-sized. The kernel will only include valid pixels.
        # Kernel for (2,2) would be (1,1),(1,2),(2,1).
        # (1,1) is invalid. (1,2) is black. (2,1) is black.
        # Average of 2 black pixels is black.
        self.assertEqual(blurred_image[2][2],(0, 0, 0, 255))


if __name__ == '__main__':
    unittest.main()
