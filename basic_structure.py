
#POST
@app.route("/api/",methods=["POST"])
def function_name():
    data = request.get_json()
    # no data pass than
    if not data:
        return jsonify({'message': 'Invalid JSON data'}), 400

    try:
        # data that u want to inject into database
        
        
        # add object that u want 
        db.session.add()  
        db.session.commit()
        return jsonify({'message': '  successfully'}), 201
    except Exception as e:
        #this will bring session back to its state before the changes were made.
        db.session.rollback() 
        return jsonify({'message': f'Error {e}'}), 500

#PUT
@app.route("/api/",methods=["PUT"])
def function_name():
    data = request.get_json()
    # no data pass than
    if not data:    
        return jsonify({'message': 'Invalid JSON data'}), 400
    
    
    try:
        # data that u want to update into database
        db.session.commit()
    
    except Exception as e:
        #this will bring session back to its state before the changes were made.
        db.session.rollback() 
        return jsonify({'message': f'Error {e}'}), 500
    
#GET
@app.route("/api/",methods=["GET"])
def function_name():
    try:
        #details = classname.query.get()
        if not details:
            return jsonify({"message":" not found"})
    
    #remaining part 
    #return jsonify({})    
    except Exception as e:
        #this will bring session back to its state before the changes were made.
        return jsonify({'message': f'Error {e}'}), 500