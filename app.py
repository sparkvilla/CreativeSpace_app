import json
import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageOps

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
SONGS_FILE = "data/projects.json"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to load songs from JSON
def load_songs():
    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Function to save songs to JSON
def save_songs(songs):
    with open(SONGS_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4)


@app.route("/")
def index():
    songs = load_songs()
    return render_template("index.html", songs=songs)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        songs = load_songs()

        song_title = request.form["song_title"]
        song_file = request.files["song_file"]
        song_image = request.files.get("song_image")
        song_lyrics = request.form.get("song_lyrics", "")
        tags = request.form.get("tags", "").split(",")  # Tags as comma-separated values
        participants = request.form.get("participants", "").split(
            ","
        )  # Participants as CSV

        if song_file:
            audio_filename = song_file.filename
            song_file.save(os.path.join(app.config["UPLOAD_FOLDER"], audio_filename))
        else:
            return "Error: No audio file uploaded", 400

        if song_image:
            image_filename = song_image.filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
            song_image.save(image_path)

            # Open and process the image
            with Image.open(image_path) as img:
                # Make image square by cropping the center
                min_side = min(img.size)  # Get smallest dimension (to crop square)
                img = ImageOps.fit(
                    img, (min_side, min_side), Image.LANCZOS
                )  # Crop to square

                # Resize to desired size (300x300)
                img = img.resize((300, 300), Image.LANCZOS)

                # Save the final image
                img.save(image_path)
        else:
            image_filename = "default.jpg"

        new_song = {
            "id": len(songs) + 1,
            "title": song_title,
            "name": os.path.splitext(audio_filename)[0],
            "image": image_filename,
            "audio": audio_filename,
            "lyrics": song_lyrics,
            "tags": tags,
            "participants": participants,
        }

        songs.append(new_song)
        save_songs(songs)

        return redirect(url_for("index"))

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
