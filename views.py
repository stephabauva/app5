from flask import render_template, redirect, url_for, request
from models import db, Game
from app import app

@app.route("/")
def index():
    # Get all the games from the database
    games = Game.query.all()
    # Render the index.html template with the games data
    return render_template("index.html", games=games)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        # Render the create.html template
        return render_template("create.html")
    elif request.method == "POST":
        # Get the form data from the request
        name = request.form.get("name")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        # Create a new game object with the form data
        game = Game(name=name, genre=genre, rating=rating)
        # Add the game object to the database session
        db.session.add(game)
        # Commit the database session
        db.session.commit()
        # Redirect to the home page
        return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    # Get the game with the given id from the database
    game = Game.query.get_or_404(id)
    if request.method == "GET":
        # Render the update.html template with the game data
        return render_template("update.html", game=game)
    elif request.method == "POST":
        # Get the form data from the request
        name = request.form.get("name")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        # Update the game object with the form data
        game.name = name
        game.genre = genre
        game.rating = rating
        # Commit the database session
        db.session.commit()
        # Redirect to the home page
        return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    # Get the game with the given id from the database
    game = Game.query.get_or_404(id)
    # Delete the game object from the database session
    db.session.delete(game)
    # Commit the database session
    db.session.commit()
    # Redirect to the home page
    return redirect(url_for("index"))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = db.session.query(Game).filter(Game.name.like(f'%{query}%')).all()
        return render_template('search_results.html', results=results)
    return render_template('search.html')
