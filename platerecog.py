#-----------------------------------------------------------------------------#
# Este codigo construye una clase para reconocimiento de placas
#
# Dependencias: cv2, knn2, pytesseract, re
# Autores: Kenny Mendez, Jorge Ramos, Jonathan Romo, Adrian Villareal
#-----------------------------------------------------------------------------#


import cv2
from knn2 import principal
import re
import pytesseract
#import matplotlib.pyplot as plt


class ReconocePlaca:

	def __init__(self, filename, file_type = "filename"):

			self.resize_x = 600
			self.resize_y = 400

			self.lista_placas = None

			if file_type == "filename":
				self.img = cv2.imread(filename)
			elif file_type == "image":
				self.img = filename.copy()  # image

			self.img_re = cv2.resize(self.img.copy(), (self.resize_x, self.resize_y))
			self.gray = cv2.cvtColor(self.img_re.copy(), cv2.COLOR_BGR2GRAY)


			self.canny_low = 80
			self.canny_upp = 250

			self.dplate_x = 300
			self.dplate_y = 100

			self.posibles_textos = None

			#self.cascade_path = "haar_20_stages/cascade.xml"
			self.cascade_path = "haar_29_mx_plates_20_stages/cascade.xml"
			self.trained_cascade = None
			self.min_plates = 3



	def encuentra_placas(self, tipo_prep = "canny"):
		# Argumentos:
		# 	tipo_prep (1-Canny,2-Thresh tipo1 ,3 Thresh tipo2, 4.- Haar)

		# Salida:  list((x, y, w, h))

		img_re = self.img_re.copy()
		img_re_gr = cv2.cvtColor(img_re.copy(), cv2.COLOR_BGR2GRAY)


		# Segun el tipo de metodo
		if tipo_prep == "canny":
			mask = cv2.Canny(img_re_gr, self.canny_low, self.canny_upp)

		elif tipo_prep == "thresh1":
			_, mask = cv2.threshold(img_re_gr, 200, 255, cv2.THRESH_BINARY)

		elif tipo_prep == "thresh2":
			_, mask = cv2.threshold(img_re_gr, 140, 255, cv2.THRESH_BINARY)

		else:
			tipo_prep = "haar"  # establecemos como default

			self.trained_cascade = cv2.CascadeClassifier(self.cascade_path)
			plate_coords = self.trained_cascade.detectMultiScale(img_re_gr, 
				scaleFactor = 1.3, 
				minNeighbors = self.min_plates)

		
		h_list = []  # lista de placas (init)

		if tipo_prep == "haar":

			for (x,y,w,h) in plate_coords:

				h_list.append([x,y,w,h])
		else:

			# Buscamos contornos en las mascaras (canny, thresh1 o thresh2)
			_, contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_NONE)

			for contour in contours:

				[x,y,w,h] = cv2.boundingRect(contour)

				if 2*h > w:
					continue

				if w < 30 or h < 30:
					continue

				if h > 300 or w > 300:
					continue 

				h_list.append([x,y,w,h])


		self.lista_placas = h_list # lista de placas posibles

		#print("Usando " + tipo_prep + " en la imagen se encontraron " + 
		#	str(len(self.lista_placas)) + " posibles placas.")



	def redim_placa(self, x, y, w, h):

		img = self.img_re.copy()

		if y-4>0 and x-4>0 and y + h+4<100 and x + w+4<300:
			cropped = img[y-4 :y +  h+4 , x-4 : x + w+4]
		else:
			cropped = img[y-1 :y +  h+1 , x-1 : x + w+1]

		imgCropped = cv2.resize(cropped,(self.dplate_x, self.dplate_y))

		return imgCropped

	def elige_texto(self, text):
		
		text = re.sub(r'[^\w]', ' ', text)

		placa_text = None

		if len(text) > 4 and len(text) < 10:
			placa_text = text

		return placa_text
	def prep_haar(self):

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	# return a string
	def prep_knn(self, x, y, w, h):

		img = self.img_re.copy() # whole image

		img1 = img[y:y +  h , x: x + w]  # extract plate

		#plt.figure()
		#plt.imshow(img1, interpolation = "bicubic")

		# Resize the plate
		img2 = cv2.resize(img1.copy(),(self.dplate_x, self.dplate_y))

		imgGray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # get grayscale image
		imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)    
		imgBlurred = cv2.medianBlur(imgBlurred, 5)   
		imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
		                                      255,                                  # make pixels that pass the threshold full white
		                                      cv2.ADAPTIVE_THRESH_MEAN_C,       # use gaussian rather than mean, seems to give better results
		                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
		                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
		                                      2)  

		#Conseguimos los contornos de los caracteres y numeros de las placas considerando criterios de tamanos en la imagen 
		im2, contours, hierarchy = cv2.findContours(imgThresh,
			cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		h_list = []

		for contour in contours:
			[x,y,w,h] = cv2.boundingRect(contour)

			if h < 2*w:
				continue

			if w < 10 or h < 10:
				continue

			if w > 50:
				continue 

			h_list.append([x,y,w,h])


		# Ordenamos los rectangulos de izquierda a derecha
		x_s = []
		for i in range(0, len(h_list)):
		 	x_s.append(h_list[i][0])

		dic = dict(zip(x_s, h_list))
		# Reconocemos cada caracter dentro de los contornos obtenidos

		plate_chars = ""

		for key in sorted(dic):

			[xx,yy,ww,hh] = dic[key]
		  
			if yy-4>0 and xx-4>0 and yy + hh+4<100 and xx + ww+4<300:
				cropped = img2[yy-4 :yy +  hh+4 , xx-4 : xx + ww+4]
			else:
				cropped = img2[yy-1 :yy +  hh+1 , xx-1 : xx + ww+1]

			plate_chars = plate_chars + principal(cropped)

		return plate_chars


	def placa_ocr(self, tipo_ocr = "tesseract"):
		## tipo_ocr (tesseract, knn)

		texto_placa = None

		lista_texto = list()

		if tipo_ocr == "tesseract":

			bordersize = 10

			for x,y,w,h in self.lista_placas:
				imgCropped = self.redim_placa(x, y, w, h)		
				border = cv2.copyMakeBorder(imgCropped, top = bordersize, 
					bottom=bordersize, 
					left=bordersize, right=bordersize, 
					borderType = cv2.BORDER_CONSTANT, value=[255,255,255] )
				text0 = pytesseract.image_to_string(border)
				lista_texto.append(self.elige_texto(text0))

		elif tipo_ocr == "knn":
			
			# img = self.img_re.copy()

			for x1,y1,w1,h1 in self.lista_placas:

				plate_chars = self.prep_knn(x1, y1, w1, h1)
				
				lista_texto.append(self.elige_texto(plate_chars))

		# After all
		self.posibles_textos = lista_texto

	def is_number_plate(self, text):

		ltext = len(text)
		ans = False

		if ltext > 4 and ltext < 10:
			ans = True

		return ans
