import platerecog as pr
import os



placas_method = "haar"
ocr_method = "tesseract"

inputdir = "../FUENTES/day_very_close_view_adrian/"
outputfile = "results/" + placas_method + "_" + ocr_method + ".txt"

if len(sys.argv) > 1:

    placas_method = str(sys.argv[3])
    ocr_method = str(sys.argv[4])

    inputdir = str(sys.argv[1])
    outputfile = str(sys.argv[2]) + "/" + placas_method + "_" + 
    ocr_method +  ".txt"


myf = open(outputfile, "w")

files = sorted(os.listdir(inputdir))  # get files from input directory
plates_detected = 0  # set descriptors
cont = 1

for filename in files:

	# Leemos imagen
	print("Processed ", round(100 * cont / len(files), 2), "%")
	recog = pr.ReconocePlaca(inputdir + filename)  # Creamos una instancia

	# Buscamos posibles placas
	recog.encuentra_placas(tipo_prep = placas_method)
	plates_detected += (len(recog.lista_placas) > 0)

	# Buscamos posibles textos
	recog.placa_ocr(tipo_ocr = ocr_method)


	line = ""
	for j in range(len(recog.posibles_textos)):
		if j > 0: line = line + ","

		text = recog.posibles_textos[j]
		line = line + str(text)

	myf.write(filename + " : " + line + "\n")
	cont += 1

print("Número de posibles placas detectadas: ", plates_detected)
myf.close()
