import platerecog as pr

wdir = "data/"
filename = wdir + "33.JPG"
#filename = wdir + "67.JPG"
filename = wdir + "HPIM1040.JPG"
filename = wdir + "ej_real_01.jpg"

# Leemos imagen
recog = pr.ReconocePlaca(filename)

# Buscamos posibles placas

#recog.encuentra_placas(tipo_prep = "canny")
#recog.encuentra_placas(tipo_prep = "thresh1")
recog.encuentra_placas(tipo_prep = "canny")

print(recog.lista_placas)

# Buscamos posibles textos

print("Con Tesseract")
recog.placa_ocr(tipo_ocr = "tesseract")

for texto in recog.posibles_textos:
	print(texto)


print("Con KNN")
recog.placa_ocr(tipo_ocr = "knn")

for texto in recog.posibles_textos:
	print(texto)