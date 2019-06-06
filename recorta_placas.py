import platerecog as pr
import os
import cv2
import sys


# Process command line arguments

# To run: python3 recorta_placas.py test_img results/real_tests haar

# python3 recorta_placas.py test_img/ results/real_test_v2 haar

path = "../FUENTES/day_very_close_view_adrian/"

placas_method = "thresh1"

outputdir = "plates/" + placas_method + "/"

if len(sys.argv) > 1:
    
    # file_to_load = sys.argv[1]
    path = str(sys.argv[1])
    placas_method = str(sys.argv[3])
    outputdir = str(sys.argv[2]) + placas_method + "/"




#ocr_method = "tesseract"
#outputfile = "plates/" + placas_method + "_" + ocr_method + ".txt"
#myf = open(outputfile, "w")

cont = 1
files = os.listdir(path)

#print(files)

plates_detected = 0

for filename in sorted(files):

	# Leemos imagen
	# print(path + filename)
	print("Processed ", round(100 * cont / len(files), 2), "%")

	#print(path + filename)

	recog = pr.ReconocePlaca(path + filename)

	# Buscamos posibles placas
	recog.encuentra_placas(tipo_prep = placas_method)
	plates_detected += (len(recog.lista_placas) > 0)

	id_plate = 1

	for x,y,w,h in recog.lista_placas:

		cv2.imwrite(outputdir + filename + "_" + str(id_plate) + ".JPG", 
			recog.img_re[y:(y+h),x:(x+w),:])

		id_plate += 1

	cont += 1

print("Número de posibles placas detectadas: ", plates_detected)
#myf.close()
