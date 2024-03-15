#from config import get_db_object   

#from seminar import Seminar
#from config import get_app_object,get_request_object,get_jsonify
from Config import Configuration  # import class

setup=Configuration()   # setup is an object

db=setup.get_db_object()   # getting db obj from config class
request=setup.get_request_object()  # getting request obj from config class
jsonify=setup.get_jsonify()     # getting jsonify obj from config class

class Seminar(db.Model):
    __tablename__="seminar_info"
    
    #seminar  attribute
    
    seminar_id=db.Column(db.Integer,primary_key=True)
    seminar_topic=db.Column(db.String(255))
    seminar_speaker=db.Column(db.String(255))
    seminar_mode=db.Column(db.String(255))
    seminar_venue=db.Column(db.String(255))
    seminar_date=db.Column(db.String(255))
    seminar_time=db.Column(db.String(255))
    seminar_duration=db.Column(db.String(255))
    seminar_eligibility=db.Column(db.String(255))
    seminar_fees=db.Column(db.String(255))
    seminar_capacity=db.Column(db.String(255))
    seminar_poc=db.Column(db.String(255))
    seminar_url=db.Column(db.String(255))
    
    
    def to_json(self):
        return{
        "seminar_id":self.seminar_id,
        "seminar_topic":self.seminar_topic,
        "seminar_speaker":self.seminar_speaker,
        "seminar_mode":self.seminar_mode,
        "seminar_venue":self.seminar_venue,
        "seminar_date":self.seminar_date,
        "seminar_time":self.seminar_time,     #need to convert into string other wise showing error
        "seminar_duration":self.seminar_duration,
        "seminar_eligibility":self.seminar_eligibility,
        "seminar_fees":self.seminar_fees,
        "seminar_capacity":self.seminar_capacity,
        "seminar_poc":self.seminar_poc,
        "seminar_url":self.seminar_url,
        }
        
    def get_all_seminars(self):
        try:
        # fetching all the seminars object and storing in 
            seminars=Seminar.query.all()
       # seminar_list coantain [ {seminar_id1}, {seminar_id2}, {seminar_id3} ]
            seminar_list=[ seminar.to_json() for seminar in seminars ]
            return jsonify(seminar_list),200
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
    
    def get_seminar_by_id(self,seminar_id):
        try:
            # fetching single seminar object
            seminar=Seminar.query.get(seminar_id)
            if not seminar:
                return jsonify({"message":" seminar not found"}),404
            #if found than return in json format
            return jsonify(Seminar.to_json(seminar)),200   
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
        
    def add_seminar(self,data):
        #data = request.get_json()
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        try:
            # data that u want to inject into database
            seminar=Seminar(
                seminar_topic=data.get('seminar_topic'),
                seminar_speaker=data.get('seminar_speaker'),
                seminar_mode=data.get('seminar_mode'),
                seminar_venue=data.get('seminar_venue'),
                seminar_date=data.get('seminar_date'),
                seminar_time=data.get('seminar_time'),
                seminar_duration=data.get('seminar_duration'),
                seminar_eligibility=data.get('seminar_eligibility'),
                seminar_fees=data.get('seminar_fees'),
                seminar_capacity=data.get('seminar_capacity'),
                seminar_poc=data.get('seminar_poc'),
                seminar_url=data.get('seminar_url')
            )
            
            # add object that u want 
            db.session.add(seminar)  
            db.session.commit()
            return jsonify({'message': ' Seminar added successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_seminar(self,data):
        #data = request.get_json()
        # no data pass than
        if not data:    
            return jsonify({'message': 'Invalid JSON data'}), 400
        
        try:
            # data that u want to update into database
            
            seminar_id=data.get("seminar_id")
            seminar=Seminar.query.get(seminar_id)
            if not seminar:
                return jsonify({"message":"Seminar not found"}),404
            
            seminar.seminar_topic=data.get("seminar_topic"),
            seminar.seminar_speaker=data.get("seminar_speaker"),
            seminar.seminar_mode=data.get("seminar_mode"),
            seminar.seminar_venue=data.get("seminar_venue"),
            seminar.seminar_date=data.get("seminar_date"),   # date is replacing with 0000-00-00
            seminar.seminar_time=data.get("seminar_time"),
            seminar.seminar_duration=data.get("seminar_duration"),
            seminar.seminar_eligibility=data.get("seminar_eligibility"),
            seminar.seminar_fees=data.get("seminar_fees"),
            seminar.seminar_capacity=data.get("seminar_capacity"),
            seminar.seminar_poc=data.get("seminar_poc"),
            seminar.seminar_url=data.get("seminar_url")
            db.session.commit()
            return jsonify({'message': 'Seminar updated successfully'}), 200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
# Seminar_apis.py

#app4 = get_app_object()
#db=get_db_object()
#request=get_request_object()
#jsonify=get_jsonify()








