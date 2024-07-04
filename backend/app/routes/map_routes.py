from flask import request, jsonify
from . import app
from .services import geocode_address


@app.route('/api/geocode', methods=['GET'])
async def geocode_handler():
    address = request.args.get('address')
    coordinates = await geocode_address(address)
    return jsonify({'coordinates': coordinates})


@app.route('/api/update_marker', methods=['POST'])
async def update_marker_handler():
    data = request.json

    print('Received new marker position:', data)
    return jsonify({'message': 'Marker position updated'})
