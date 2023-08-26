import png


r = png.Reader("Img/Guard0.png")
data = r.read()
rows = list(data[2])
width = data[0]
height = data[1]

opaque_pixels = 0
for row in rows:
	for i in range(width):
		index = i * 4
		pixel = (row[index], row[index+1], row[index+2], row[index+3])
		# print(pixel)
		alpha = pixel[3]
		if alpha == 255:
			opaque_pixels += 1
print(opaque_pixels)
