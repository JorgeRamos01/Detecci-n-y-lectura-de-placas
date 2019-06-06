import platerecog as pr
import os
import cv2
import numpy as np
import sys



# TO RUN:
# python3 rpn_video.py


def detect_number_plate(frame):
	
	recog = pr.ReconocePlaca(filename = frame, file_type = "image")

	# Buscamos posibles placas
	recog.encuentra_placas(tipo_prep = placas_method)
	#plates_detected += (len(recog.lista_placas) > 0)

	# Buscamos posibles textos
	recog.placa_ocr(tipo_ocr = ocr_method)

			# Set dimensions
	frameWidth, frameHeight = np.shape(recog.gray)
	
	img_out = recog.img_re.copy()


	flag = True
	(tx, ty, tw, th) = (1, 1, 1, 1)
	ttext = ""

	for j in range(len(recog.posibles_textos)):
		

		x,y,w,h = recog.lista_placas[j]
		text = recog.posibles_textos[j]

		if text is not None and recog.is_number_plate(text):#  and flag:

			# If we only want the last label of the list
			(tx, ty, tw, th) = (x, y, w, h)
			ttext = text

			flag = False

			# Draw the rectangles and write the label
			cv2.rectangle(img_out, (x, y),(x + w, y + h), (0,0, 255), 4)

			cv2.putText(img = img_out, text = text, org = (int(0.2 * frameWidth),
				int(frameHeight * 0.5)), fontFace = cv2.FONT_HERSHEY_DUPLEX, 
				thickness = 3,
				fontScale = 3, color = (50, 255, 0))

	# cv2.rectangle(img_out, (tx, ty), (tx + tw, ty + th), (0,0, 255), 4)		
	# cv2.putText(img = img_out, text = ttext, org = (int(0.2 * frameWidth),
	# 		int(frameHeight * 0.5)), fontFace = cv2.FONT_HERSHEY_DUPLEX, 
	# 		thickness = 3,
	# 		fontScale = 3, color = (50, 255, 0))

	return(img_out)


placas_method = "haar"
ocr_method = "knn"

inputvideo = "video-1544648149.mp4"
outputvideo = "results/labeled_tests/" 

if len(sys.argv) > 1:

    placas_method = str(sys.argv[3])
    ocr_method = str(sys.argv[4])

    inputdir = str(sys.argv[1]) + "/"
    outputdir = str(sys.argv[2]) + "/"

## Define video to be created
width_ini = 576  # dimensions
height_ini = 320
fourcc = cv2.VideoWriter_fourcc(*'XVID')

name_out_vid = outputvideo + placas_method + "_" + ocr_method + "_" + inputvideo  + ".avi"
out_etiquetado = cv2.VideoWriter(name_out_vid, 
	fourcc, 30.0, (width_ini, height_ini))

## Open video to be processed

cap = cv2.VideoCapture(inputvideo)  # read video

estimated_nf = 6 * 30
id_frame = 0

while(cap.isOpened()):

	# print("Processing frame: " + str(i + 1) + " (", perc(i + 1, length), "%)")
	if id_frame >= estimated_nf:
		break

	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret == True:
		if frame is not None:
			process_frame = detect_number_plate(frame)
			process_frame2 = cv2.resize(process_frame, (width_ini, height_ini))
			out_etiquetado.write(process_frame2)

	id_frame += 1

out_etiquetado.release()
cap.release()

print("El video generado se guardó en: ", outputvideo)

cv2.destroyAllWindows()

