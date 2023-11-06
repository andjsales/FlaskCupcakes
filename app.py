"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, Cupcake
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.init_app(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/api/cupcakes')
def list_all_cupcakes():
    """
    Get data about all cupcakes
    """
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def list_one_cupcake(cupcake_id):
    """
    Get data about a single cupcake    
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """
    Create a cupcake with flavor, size, rating and image data from the body of the request    
    """
    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """
    Update cupcake from data in request. 
    Return updated data.
    """
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """
    Delete cupcake and return confirmation message.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
