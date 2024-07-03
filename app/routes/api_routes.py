from flask import Blueprint

bp = Blueprint('api', __name__)

@bp.route('/api/items', methods=['GET'])
def get_items():
    return {"items": ["item1", "item2"]}