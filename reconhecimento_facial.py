import os
import cv2
import face_recognition


#Recebe 1 caso exista algum rosto na câmera, para ser usado como paramêtro para a planilha
validador_planilha = 0

# Procura em uma pasta específica o número de imagens, sempre nomeados com: rosto_salvo_i
# Onde i = número da imagem, sempre em ordem crescente começando do 0
imagens_referencia = []
for arquivo in os.listdir("<caminho para as imagens>"):
    # Verifica se o arquivo é uma imagem
    if arquivo.endswith(".jpg"):
        imagem_referencia = face_recognition.load_image_file(os.path.join("<caminho para as imagens>", arquivo))
        features_referencia = face_recognition.face_encodings(imagem_referencia)[0]
        imagens_referencia.append(features_referencia)
imagens_referencia = [face_recognition.face_encodings(face_recognition.load_image_file(os.path.join("<caminho para as imagens>", f"rosto_salvo_{i}.jpg")))[0] for i in range(len(imagens_referencia))]

# Conecta a webcam
webcam = cv2.VideoCapture(0)
def camera():
    validador = False
    while webcam.isOpened():
        validacao, frame = webcam.read()
        if not validacao:
            break

        # Converte a imagem da webcam para o padrão RGB
        imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Rosto", frame)

        # Encontra todos os rostos na imagem da webcam
        rostos = face_recognition.face_locations(imagem)

        # Extrai as features faciais de cada rosto encontrado
        features_rostos = face_recognition.face_encodings(imagem, rostos)

        # Compara as features faciais da imagem de referência com as encontradas na imagem da webcam
        for features_rosto in features_rostos:
            for features_referencia in imagens_referencia:
                distancia = face_recognition.face_distance([features_referencia], features_rosto)
                if distancia < 0.6:
                    validador = True
                    return validador
                
        if cv2.waitKey(1) == 27:  # ESC
            break

# Libera a memória
if camera() == True:
    validador_planilha = 1

webcam.release()
cv2.destroyAllWindows()
