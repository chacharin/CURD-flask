from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False  # Preserve key order in JSON

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Item {self.name}>"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name or not description:
        return jsonify({"error": "Name and description are required"}), 400
    
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    
    # Check if the request is from an API client (e.g., Streamlit) or a browser
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
        return jsonify({
            "message": "Item added successfully",
            "item": {"id": new_item.id, "name": new_item.name, "description": new_item.description}
        }), 201
    else:
        return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    item = Item.query.get_or_404(item_id)
    item.name = request.form.get('name')
    item.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    else:
        return redirect(url_for('index'))

@app.route('/api/items', methods=['GET'])
def get_items_api():
    items = Item.query.all()
    items_list = [{"id": item.id, "name": item.name, "description": item.description} 
                  for item in items]
    return jsonify(items_list)

if __name__ == '__main__':
    app.run(debug=True)
