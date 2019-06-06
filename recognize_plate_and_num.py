import platerecog as pr
import os
import cv2
import numpy as np
import sys



# TO RUN:
# python3 recognize_plate_and_num.py test_img/ results/labeled_tests haar knn

placas_method = "haar"
ocr_method = "knn"

inputdir = "test_img/"
outputdir = "results/labeled_tests/"

if len(sys.argv) > 1:

    placas_method = str(sys.argv[3])
    ocr_method = str(sys.argv[4])

    inputdir = str(sys.argv[1]) + "/"
    outputdir = str(sys.argv[2]) + "/" #+ placas_method + "_" + 
    #ocr_method +  ".txt"



files = sorted(os.listdir(inputdir))  # get files from input directory
plates_detected = 0  # set descriptors
cont = 1

for filename in files:

	# Leemos imagen
	print("image: ", inputdir + filename + "\n")

	print("Processed ", round(100 * cont / len(files), 2), "%")
	recog = pr.ReconocePlaca(inputdir + filename)  # Creamos una instancia

	

	# Buscamos posibles placas
	recog.encuentra_placas(tipo_prep = placas_method)
	plates_detected += (len(recog.lista_placas) > 0)

	# Buscamos posibles textos
	recog.placa_ocr(tipo_ocr = ocr_method)

			# Set dimensions
	frameWidth, frameHeight = np.shape(recog.gray)
	
	img_out = recog.img_re.copy()

	for j in range(len(recog.posibles_textos)):
		

		x,y,w,h = recog.lista_placas[j]
		text = recog.posibles_textos[j]

		cv2.rectangle(img_out, (x, y),(x + w, y + h), (0,0, 255), 4)

		if text is not None and recog.is_number_plate(text):

			cv2.putText(img = img_out, text = text, org = (int(0.2 * frameWidth),
				int(frameHeight / 2)), fontFace = cv2.FONT_HERSHEY_DUPLEX, 
				thickness = 3,
				fontScale = 3, color = (50, 255, 0))


	methods = placas_method + "_" + ocr_method + "_"
	
	cv2.imwrite(outputdir + "/" + methods + filename, img_out)
	cont += 1

print("Número de posibles placas detectadas: ", plates_detected)
