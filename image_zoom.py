import numpy as np
from scipy.interpolate import barycentric_interpolate
from PIL import Image
zoom = 2
image = Image.open("forest1.jpg")
image.show()
pixels = np.array(image)

height, width, rgb = pixels.shape

new_height = int(height * zoom)
new_width = int(width * zoom)

zoomed_image = np.full((new_width, new_height, 3), -1 , dtype=np.int32)
print("Please wait..")
for x in range(height):
    for y in range(width):
        new_x = x * zoom
        new_y = y * zoom
        zoomed_image[new_x][new_y] = pixels[x][y]



for x in range(0, new_height, 2):
    for i in range(0, new_width - 7, 7):
    
        xs = []
        ys = []
        xx = []
        for k in range(i, i + 7):
            if zoomed_image[x][k][0] != -1:
                xs.append(k)
                ys.append(zoomed_image[x][k])
            else:
                xx.append(k)
        if xx == [] or xs == [] or ys == []:
          
            continue
        
        interpolated = barycentric_interpolate(xs, ys, xx)
        
        
        for i in range(len(xx)):
            zoomed_image[x][xx[i]] = interpolated[i]


for y in range(0, new_width, 2):
    for i in range(0, new_height - 7, 7):
    
        xs = []
        ys = []
        xx = []

        for k in range(i, i + 7):
            if zoomed_image[k][y][0] != -1:
                xs.append(k)
                ys.append(zoomed_image[k][y])
            else:
                xx.append(k)
        if xx == [] or xs == [] or ys == []:
          
            continue
        
        interpolated = barycentric_interpolate(xs, ys, xx)
        
        
        for i in range(len(xx)):
            zoomed_image[xx[i]][y] = interpolated[i]

coord = [(1,0), (-1,0), (0, 1) , (0, -1)]
for x in range(1, new_height, 2):
    for y in range(1, new_width , 2):
        avrg = np.array([0,0,0])
        count = 0
        for xi,yi in coord:
            if x + xi < new_height and y + yi < new_width:
                avrg += np.array(zoomed_image[x + xi][y + yi])
                count += 1  
        avrg = avrg.astype(np.float32)
        avrg /= count
        avrg = [int(x) for x in avrg]
        zoomed_image[x][y] = avrg

for x in range(1, new_height):
    for y in range(1, new_width):
        if zoomed_image[x][y][0] == -1:
            avrg = np.array([0,0,0])
            count = 0
            for xi,yi in coord:
                if x + xi < new_height and y + yi < new_width:
                    avrg += np.array(zoomed_image[x + xi][y + yi])
                    count += 1  
            avrg = avrg.astype(np.float32)
            avrg /= count
            avrg = [int(x) for x in avrg]
            zoomed_image[x][y] = avrg
        

zoomed_image_cropped = np.clip(zoomed_image, 0, 255)

# Convert the array to integers
zoomed_image_cropped = zoomed_image_cropped.astype(np.uint8)

zoomed_image_pil = Image.fromarray(zoomed_image_cropped)
zoomed_image_pil.show()









