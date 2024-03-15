from Config import Configuration  # import class

setup=Configuration()   # setup is an object

db=setup.get_db_object()   # getting db obj from config class
request=setup.get_request_object()  # getting request obj from config class
jsonify=setup.get_jsonify()     # getting jsonify obj from config class
#from internship import Internship



class Internship(db.Model):
    __tablename__="internship_info"
    # internship attribute
    internship_id=db.Column(db.Integer,primary_key=True)
    internship_title=db.Column(db.String(255))
    internship_dept=db.Column(db.String(255))
    internship_org=db.Column(db.String(255))
    internship_desc=db.Column(db.String(255))
    internship_loc=db.Column(db.String(255))
    internship_startdate=db.Column(db.String(255))
    internship_lastdate=db.Column(db.String(255))
    internship_duration=db.Column(db.String(255))
    internship_stipend=db.Column(db.String(255))
    internship_eligibility=db.Column(db.String(255))
    internship_mode=db.Column(db.String(255))
    internship_skills=db.Column(db.String(255))
    internship_poc=db.Column(db.String(255))
    internship_url=db.Column(db.String(255))
    
    def to_json(self):
         return{
           "internship_id":self.internship_id,
           "internship_title":self.internship_title,
           "internship_dept":self.internship_dept,
           "internship_org":self.internship_org,
           "internship_desc":self.internship_desc,
           "internship_loc":self.internship_loc,
           "internship_startdate":self.internship_startdate,
           "internship_lastdate":self.internship_lastdate,
           "internship_duration":self.internship_duration,
           "internship_stipend":self.internship_stipend,
           "internship_eligibility":self.internship_eligibility,
           "internship_mode":self.internship_mode,
           "internship_skills":self.internship_skills,
           "internship_poc":self.internship_poc,
           "internship_url":self.internship_url
           }
         
    def get_all_internships(self):
        try:
            # fetching all the internship object and storing in 
            internships=Internship.query.all()
            # internshipe_list coantain [ {inter_id1}, {inter_id2}, {inter_id3} ]
            internships_list=[ internship.to_json() for internship in internships ]
            
            return jsonify(internships_list),200
    
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            return jsonify({'message': f'Error {e}'}), 500
        
    def get_internship_by_id(self,internship_id):
        try:
            # fetching single internship object
            internship=Internship.query.get(internship_id)
            if not internship:
                return jsonify({"message":" Internship not found"}),404
            #if found than return in json format
            return jsonify(Internship.to_json(internship)),200   
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
        
    def add_internship(self,data):
       # data = request.get_json()
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data.get()
        try:
            # data that u want to inject into database
            internship=Internship(
            #internship_id = data.get("internship_id"),
            internship_title = data.get("internship_title"),
            internship_dept = data.get("internship_dept"),
            internship_org =  data.get("internship_org"),
            internship_desc = data.get("internship_desc"),
            internship_loc = data.get("internship_loc"),
            internship_startdate = data.get("internship_startdate"),
            internship_lastdate = data.get("internship_lastdate"),
            internship_duration = data.get("internship_duration"),
            internship_stipend = data.get("internship_stipend"),
            internship_eligibility = data.get("internship_eligibility"),
            internship_mode = data.get("internship_mode"),
            internship_skills = data.get("internship_skills"),
            internship_poc = data.get("internship_poc"),
            internship_url = data.get("internship_url")
            )
            
            # add object that u want to add
            db.session.add(internship)  
            db.session.commit()
            return jsonify({'message': 'Internship created successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_internship(self,data):
       # data = request.get_json()
        # no data pass than
        if not data:    
            return jsonify({'message': 'Invalid JSON data'}), 400
        
        # data that u want to update into database
        try:
            # fetching internship_id frn json data
            internship_id=data.get("internship_id")
            # below code return obj of that id
            internship=Internship.query.get(internship_id)
            #checking weather internshipe id exist in db before any update
            if not internship :
                return jsonify({"message": "internship not found"}),404
            #updating
            #internship_id = data.get("internship_id"),
            internship.internship_title = data.get("internship_title")
            internship.internship_dept = data.get("internship_dept ")
            internship.internship_org = data.get("internship_org")
            internship.internship_desc = data.get("internship_desc")
            internship.internship_loc = data.get("internship_loc")
            internship.internship_startdate= data.get("internship_startdate")
            internship.internship_lastdate = data.get("internship_lastdate ")
            internship.internship_duration = data.get("internship_duration")
            internship.internship_stipend = data.get("internship_stipend")
            internship.internship_eligibility = data.get("internship_eligibility")
            internship.internship_mode = data.get("internship_mode")
            internship.internship_skills = data.get("internship_skills")
            internship.internship_poc = data.get("internship_poc")
            internship.internship_url = data.get("internship_url")
                
            db.session.commit()
            return jsonify({'message': 'Internship updated successfully'}), 200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500







 

    




	

