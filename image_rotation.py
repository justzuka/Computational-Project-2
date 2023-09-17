import numpy as np
from scipy.interpolate import barycentric_interpolate
from PIL import Image
from math import floor
from math import ceil
import math

def rotate_vector(vector, angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    rotated_vector = np.dot(rotation_matrix, vector)
    return rotated_vector

angle = np.pi  / 6


image = Image.open("lines.jpg")

pixels = np.array(image)

height, width, rgb = pixels.shape

new_height = int(math.sqrt(height**2 + width**2))
new_width = new_height

print("Please wait..")

zoomed_image = np.full((new_width, new_height, 3), 0 , dtype=np.int32)


small_centre = np.array([height / 2, width / 2])
centre = np.array([new_height / 2, new_width / 2])


for x in range(new_height):
    for y in range(new_width):
        coord = np.array([x,y])
        sub = coord - centre
        rotated = rotate_vector(sub, angle)

        main_coord = rotated + small_centre

        sx = main_coord[0]
        sy = main_coord[1]

        avrg = np.array([0, 0, 0], dtype=np.float32)
        count = 0

        # interpolate on x
        low = floor(sy)
        high = ceil(sy)

        # low
        xx = [sx]
        xs = []
        ys = []


        for i in range(-2,3):
            xi = round(sx + i)

            if xi >= 0 and xi < height and low >=0 and low < width:
                xs.append(xi)
                ys.append(pixels[xi][low])
        
        xx = np.array(xx)
        xs = np.array(xs)
        ys = np.array(ys)

        if len(xx) == 0 or len(xs) == 0 or len(ys) ==0:
            pass
        else:
           
            count += 1
            avrg += barycentric_interpolate(xs, ys, xx)[0]
        
        # high

        xx = [sx]
        xs = []
        ys = []


        for i in range(-2,3):
            xi = round(sx + i)

            if xi >= 0 and xi < height and high >=0 and high < width:
                xs.append(xi)
                ys.append(pixels[xi][high])
        
        xx = np.array(xx)
        xs = np.array(xs)
        ys = np.array(ys)

        if len(xx) == 0 or len(xs) == 0 or len(ys) ==0:
            pass
        else:
            count += 1
            avrg += barycentric_interpolate(xs, ys, xx)[0]
        
        # interpolate on y
        
        low = floor(sx)
        high = ceil(sx)

        # low
        xx = [sy]
        xs = []
        ys = []


        for i in range(-2,3):
            xi = round(sy + i)

            if xi >= 0 and xi < width and low >=0 and low < height:
                xs.append(xi)
                ys.append(pixels[low][xi])
        
        xx = np.array(xx)
        xs = np.array(xs)
        ys = np.array(ys)

        if len(xx) == 0 or len(xs) == 0 or len(ys) ==0:
            pass
        else:
            count += 1
            avrg += barycentric_interpolate(xs, ys, xx)[0]
        
        # high
        xx = [sy]
        xs = []
        ys = []


        for i in range(-2,3):
            xi = round(sy + i)

            if xi >= 0 and xi < width and high >=0 and high < height:
                xs.append(xi)
                ys.append(pixels[high][xi])
        
        xx = np.array(xx)
        xs = np.array(xs)
        ys = np.array(ys)

        if len(xx) == 0 or len(xs) == 0 or len(ys) ==0:
            pass
        else:
            count += 1
            avrg += barycentric_interpolate(xs, ys, xx)[0]
        
        if count != 0:
            avrg /= count
        
        avrg = [int(x) for x in avrg]
        zoomed_image[x][y] = avrg
        


# ------------ SHOW ------------
zoomed_image_cropped = np.clip(zoomed_image, 0, 255)

zoomed_image_cropped = zoomed_image_cropped.astype(np.uint8)

zoomed_image_pil = Image.fromarray(zoomed_image_cropped)
zoomed_image_pil.show()