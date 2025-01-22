import os
from flask import Flask, request, render_template, send_from_directory
import face_recognition

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def Predict(imagePath, referenceImagePath, tolerance=0.4):
    """
    Compare l'image donnée avec une image de référence et retourne si c'est la même personne.
    """
    try:
        # Charger l'image de référence
        reference_image = face_recognition.load_image_file(referenceImagePath)
        reference_encoding = face_recognition.face_encodings(reference_image)

        if not reference_encoding:
            return "Aucun visage trouvé dans l'image de référence."

        # Charger l'image d'entrée
        input_image = face_recognition.load_image_file(imagePath)
        input_encoding = face_recognition.face_encodings(input_image)

        if not input_encoding:
            return "Aucun visage trouvé dans l'image d'entrée."

        # Comparer les encodages avec la tolérance définie
        matches = face_recognition.compare_faces([reference_encoding[0]], input_encoding[0], tolerance=tolerance)

        # Calculer la distance faciale pour des diagnostics supplémentaires
        distance = face_recognition.face_distance([reference_encoding[0]], input_encoding[0])[0]

        # Log des détails pour le débogage
        print(f"Distance calculée : {distance}, Tolérance utilisée : {tolerance}")

        if matches[0]:
            return f"Même personne (distance : {distance:.2f})."
        else:
            return f"Personne différente (distance : {distance:.2f})."
    except Exception as e:
        print("Erreur dans la fonction Predict :", e)
        return "Une erreur s'est produite lors de l'analyse."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')

    # Créer le répertoire si nécessaire
    if not os.path.isdir(target):
        os.mkdir(target)

    # Récupérer les fichiers envoyés par l'utilisateur
    reference_file = request.files.get("reference_file")
    input_file = request.files.get("file")

    # Vérification des fichiers
    if not reference_file or not input_file:
        print("Fichiers manquants !")
        return "Les fichiers nécessaires ne sont pas fournis.", 400

    # Définir les chemins de sauvegarde
    reference_path = os.path.join(target, reference_file.filename)
    input_path = os.path.join(target, input_file.filename)

    try:
        # Sauvegarder les fichiers sur le serveur
        reference_file.save(reference_path)
        input_file.save(input_path)
        print("Fichiers sauvegardés :", reference_path, input_path)

        # Appeler la fonction Predict pour comparer les images
        result = Predict(input_path, reference_path, tolerance=0.4)
        return render_template("result.html", message=result)
    except Exception as e:
        # Gérer les erreurs et afficher les logs
        print("Erreur lors du traitement des fichiers :", e)
        return "Une erreur s'est produite : {}".format(str(e)), 500


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run(debug=True)
