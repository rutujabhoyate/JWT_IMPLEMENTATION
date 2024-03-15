from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'RRR#122'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
jwt = JWTManager(app)




app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/firstdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    #role = db.Column(db.String(20))

# In-memory set to store blacklisted tokens
blacklisted_tokens = set()

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json() 
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        user_name = data["username"]
        password = data["password"]
        user = User.query.get(user_name)

        if not user:
            return jsonify({"message": "User not found"}), 404

        db_username = user.username
        db_password = user.password
        #db_role = user.role

        if db_username == user_name and db_password == password:
            access_token = create_access_token(identity=db_username, additional_claims={ "username": db_username})
            return jsonify(access_token=access_token), 201
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    
@app.route('/api/logout', methods=['POST'])
@jwt_required()
def api_logout():
    try:
        current_user = get_jwt_identity()
        jti = decode_token(get_jwt_identity())['jti']
        blacklisted_tokens.add(jti)
        return jsonify({"message": f"Logout successful for user {current_user}"}), 200
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

# This route requires a valid JWT for access.
@app.route('/auth', methods=['GET'])
@jwt_required()
def authorised():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


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




#  -------------------------Seminar----------------------------------
seminar_obj=Seminar()  # creating instance of seminar

#GET
@app.route("/api/all/seminars",methods=["GET"])
@jwt_required()
def api_get_all_seminar():
    try:
        return seminar_obj.get_all_seminars()    # calling func using seminar file
    except Exception as e:                   
        return jsonify({'message': f'Error {e}'}), 500
    
#GET
@app.route("/api/seminar/<int:seminar_id>",methods=["GET"])
@jwt_required()
def api_get_seminar_by_id(seminar_id):
    try:
        return seminar_obj.get_seminar_by_id(seminar_id=seminar_id)
          
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#POST
@app.route("/api/add/seminar",methods=["POST"])
@jwt_required()
def api_add_seminar():
    try:
        data=request.get_json()   # fetching json data
        return seminar_obj.add_seminar(data=data)     # passing  request data to  add seminar for adding in db
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    
#PUT
@app.route("/api/update/seminar",methods=["PUT"])
@jwt_required()
def api_update_seminar():
    try:
        data=request.get_json()   # fetching json data
        return seminar_obj.update_seminar(data=data)   # passing  request data to  update seminar in db
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500


#############################################################################################################################################################



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



internship_obj=Internship()  # creating instance of internship
#GET
@app.route("/api/all/internships",methods=["GET"])
@jwt_required()
def api_get_all_internships():
    try:
        return internship_obj.get_all_internships()
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

@app.route("/api/internship/<int:internship_id>",methods=["GET"])
@jwt_required()
def api_get_internship_by_id(internship_id):
    try:
        return internship_obj.get_internship_by_id(internship_id=internship_id)  # passing internship_id
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
        
#POST
@app.route("/api/add/internship",methods=["POST"])
@jwt_required()
def api_add_internship():
    try:
        data=request.get_json()
        return internship_obj.add_internship(data=data)
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#PUT
@app.route("/api/update/internship",methods=["PUT"])
@jwt_required()
def api_update_internship():
    try:
        data=request.get_json()
        return internship_obj.update_internship(data=data)
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
            



####################################################################################################################################################

class Scholarship(db.Model):
    __tablename__="scholarship_info"
    
    # scholarship attribute
    
    scholarship_id=db.Column(db.Integer,primary_key=True)
    scholarship_name=db.Column(db.String(255))
    scholarship_org=db.Column(db.String(255))
    scholarship_desc=db.Column(db.String(255))
    scholarship_eligibility=db.Column(db.String(255))
    scholarship_deadline=db.Column(db.String(255))
    scholarship_url=db.Column(db.String(255))
    scholarship_benefits=db.Column(db.String(255))
    scholarship_contact=db.Column(db.String(255))
    
    def to_json(self):
        return{
        "scholarship_id":self.scholarship_id,
        "scholarship_name":self.scholarship_name,
        "scholarship_org":self.scholarship_org,
        "scholarship_desc":self.scholarship_desc,
        "scholarship_eligibility":self.scholarship_eligibility,
        "scholarship_deadline":self.scholarship_deadline,
        "scholarship_url":self.scholarship_url,
        "scholarship_benefits":self.scholarship_benefits,
        "scholarship_contact":self.scholarship_contact,
        }
        
    def get_all_scholarships(self):
        try:
            # fetching all the scholarship object and storing in
            scholarships=Scholarship.query.all()
            # scholarship_list coantain [ {scholarship_id1}, {scholarship_id2}, {scholarship_id3} ]
            scholarships_list=[scholarship.to_json() for scholarship in scholarships ]
            return jsonify(scholarships_list),200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            return jsonify({'message': f'Error {e}'}), 500
    
    def get_scholarship_by_id(self,scholarship_id):
        try:
            # fetching single internship object
            scholarship=Scholarship.query.get(scholarship_id)
            if not scholarship:
                return jsonify({"message":" Scholarship not found"}),404
            #if found than return in json format
            return jsonify(Scholarship.to_json(scholarship)),200
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
        
    def add_scholarship(self,data):
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data.get()
        try:
            # data that u want to inject into database
            scholarship = Scholarship(
                scholarship_id = data.get("scholarship_id"),
                scholarship_name = data.get("scholarship_name"),
                scholarship_org = data.get("scholarship_org"),
                scholarship_desc= data.get("scholarship_desc"),
                scholarship_eligibility= data.get("scholarship_eligibility"),
                scholarship_deadline= data.get("scholarship_deadline"),
                scholarship_url= data.get("scholarship_url"),
                scholarship_benefits= data.get("scholarship_benefits"),
                scholarship_contact = data.get("scholarship_contact")
                )
            
            # add object that u want to add
            db.session.add(scholarship)  
            db.session.commit()
            return jsonify({'message': 'Scholarship created successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_scholarship(self,data):
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data that u want to update into database
        try:
            # fetching scholarship_id frn json data
            scholarship_id=data.get("scholarship_id")
            # below code return obj of that id
            scholarship=Scholarship.query.get(scholarship_id)
            #checking weather scholarship id exist in db before any update
            
            if not scholarship:
                return jsonify({"message": "Scholarship not found"}),404
            
            scholarship.scholarship_id = data.get("scholarship_id"),
            scholarship.scholarship_name = data.get("scholarship_name"),
            scholarship.scholarship_org = data.get("scholarship_org"),
            scholarship.scholarship_desc = data.get("scholarship_desc"),
            scholarship.scholarship_eligibility = data.get("scholarship_eligibility"),
            scholarship.scholarship_deadline = data.get("scholarship_deadline"),
            scholarship.scholarship_url= data.get("scholarship_url"),
            scholarship.scholarship_benefits = data.get("scholarship_benefits"),
            scholarship.scholarship_contact = data.get("scholarship_contact")
        
            db.session.commit()
            return jsonify({'message':'Scholarship updated successfully'}), 200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback()
            return jsonify({'message': f'Error {e}'}), 500

scholarship_obj=Scholarship() # creating instance

#GET
@app.route("/api/all/scholarships",methods=["GET"])
@jwt_required()
def api_get_all_scholarships():
    try:
        return scholarship_obj.get_all_scholarships()
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    
    
 

#GET
@app.route("/api/scholarship/<int:scholarship_id>",methods=["GET"])
@jwt_required()
def api_get_scholaraship_by_id(scholarship_id):
    try:
        return scholarship_obj.get_scholarship_by_id(scholarship_id=scholarship_id)  # passing scholarship id
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#POST
@app.route("/api/add/scholarship",methods=["POST"])
@jwt_required()
def api_add_scholarship():
    try:
        data=request.get_json()
        return scholarship_obj.add_scholarship(data=data) # passing data 
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    
    
    
#PUT
@app.route("/api/update/scholarship",methods=["PUT"])
@jwt_required()
def api_update_scholarship():
    try:
        data=request.get_json()
        return scholarship_obj.update_scholarship(data=data) # passing data that need to update
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500



    

#########################################################################################################################################################


class Job(db.Model):
    __tablename__="job_info"

    
    job_id=db.Column(db.Integer,primary_key=True)
    job_post=db.Column(db.String(255))
    job_org=db.Column(db.String(255))
    job_experience=db.Column(db.String(255))
    job_salary=db.Column(db.String(255))
    job_loc=db.Column(db.String(255))
    job_eligibility=db.Column(db.String(255))
    job_last_date=db.Column(db.String(255))
    job_mode=db.Column(db.String(255))
    job_skills=db.Column(db.String(255))
    job_desc=db.Column(db.String(255))
    job_url=db.Column(db.String(255))

    def to_json(self):
        return{
        "job_id":self.job_id,
        "job_post":self.job_post,
        "job_org":self.job_org,
        "job_experience":self.job_experience,
        "job_salary":self.job_salary,
        "job_loc":self.job_loc,
        "job_eligibility":self.job_eligibility,
        "job_last_date":self.job_last_date,
        "job_mode":self.job_mode,
        "job_skills":self.job_skills,
        "job_desc":self.job_desc,
        "job_url":self.job_url,
        }
        
    def get_all_jobs(self):
        try:
            # fetching all the internship object and storing in
            jobs=Job.query.all()
            # workshop_list coantain [ {job_id1}, {job_id2}, {job_id3} ]
            jobs_list=[job.to_json() for job in jobs ]
            return jsonify(jobs_list),200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            return jsonify({'message': f'Error {e}'}), 500
                            
    def get_job_by_id(self,job_id):
        try:
            # fetching single job object
            job=Job.query.get(job_id)
            if not job:
                return jsonify({"message":" Job not found"}),404
            #if found than return in json format
            return jsonify(Job.to_json(job)),200
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
        
    def add_job(self,data):
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data.get()
        try:
            # data that u want to inject into database
            job = Job(
                job_id=data.get("job_id"),
                job_post= data.get("job_post"),
                job_org = data.get("job_org"),
                job_experience= data.get("job_experience"),
                job_salary= data.get("job_salary"),
                job_loc= data.get("job_loc"),
                job_eligibility = data.get("job_eligibility"),
                job_last_date = data.get("job_last_date"),
                job_mode = data.get("job_mode"),
                job_skills = data.get("job_skills"),
                job_desc= data.get("job_desc"),
                job_url = data.get("job_url")
                )
            
            # add object that u want to add
            db.session.add(job)  
            db.session.commit()
            return jsonify({'message': 'Job created successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_job(self,data):
    # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data that u want to update into database
        try:
            # fetching workshop_id frn json data
            job_id=data.get("job_id")
            # below code return obj of that id
            job=Job.query.get(job_id)
            #checking weather workshop id exist in db before any update
            if not job :
                return jsonify({"message": "Job not found"}),404
            #updating
            job.job_id=data.get("job_id"),
            job.job_post= data.get("job_post"),
            job.job_org = data.get("job_org"),
            job.job_experience= data.get("job_experience"),
            job.job_salary= data.get("job_salary"),
            job.job_loc= data.get("job_loc"),
            job.job_eligibility = data.get("job_eligibility"),
            job.job_last_date = data.get("job_last_date"),
            job.job_mode = data.get("job_mode"),
            job.job_skills = data.get("job_skills"),
            job.job_desc= data.get("job_desc"),
            job.job_url = data.get("job_url")
            
            db.session.commit()
            return jsonify({'message': 'Job updated successfully'}), 200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback()
            return jsonify({'message': f'Error {e}'}), 500


job_obj=Job() # creating instance of job
#GET
@app.route("/api/all/jobs",methods=["GET"])
@jwt_required()
def api_get_all_jobs():
    try:
        return job_obj.get_all_jobs()
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#GET
@app.route("/api/job/<int:job_id>",methods=["GET"])
@jwt_required()
def api_get_job_by_id(job_id):
    try:
        return job_obj.get_job_by_id(job_id=job_id)  # passing job id
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#POST
@app.route("/api/add/job",methods=["POST"])
@jwt_required()
def api_add_job():
    try:
        data=request.get_json()
        return job_obj.add_job(data=data)  # passing data to add into db
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

    
#PUT
# not passing id through url need to pass inside json format
@app.route("/api/update/job",methods=["PUT"])
@jwt_required()
def api_update_job():
    try:
        data=request.get_json()
        return job_obj.update_job(data=data)  # passing data that need to update
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500


###########################################################################################################################################################################



class Workshop(db.Model):
    __tablename__="workshop_info"
    
    # workshop attribute

    workshop_id=db.Column(db.Integer,primary_key=True)
    workshop_title=db.Column(db.String(255))
    workshop_org=db.Column(db.String(255))
    workshop_trainer=db.Column(db.String(255))
    workshop_desc=db.Column(db.String(255))
    workshop_mode=db.Column(db.String(255))
    workshop_venue=db.Column(db.String(255))
    workshop_city=db.Column(db.String(255))
    workshop_date=db.Column(db.String(255))
    workshop_time=db.Column(db.String(255))
    workshop_target_audience=db.Column(db.String(255))
    workshop_fees=db.Column(db.String(255))
    workshop_seats=db.Column(db.String(255))
    workshop_url=db.Column(db.String(255))
    
    

 
    def to_json(self):
        return{
        "workshop_id":self.workshop_id,
        "workshop_title":self.workshop_title,
        "workshop_org":self.workshop_org,
        "workshop_trainer":self.workshop_trainer,
        "workshop_desc":self.workshop_desc,
        "workshop_mode":self.workshop_mode,
        "workshop_venue":self.workshop_venue,
        "workshop_city":self.workshop_city,
        "workshop_date":self.workshop_date,
        "workshop_time":self.workshop_time,   
        "workshop_target_audience":self.workshop_target_audience,
        "workshop_fees":self.workshop_fees,
        "workshop_seats":self.workshop_seats,
        "workshop_url":self.workshop_url
        }
    def get_all_workshops(self):
        try:
            # fetching all the workshop object and storing in
            workshops=Workshop.query.all()
            # workshop_list coantain [ {workshop_id1}, {workshop_id2}, {workshop_id3} ]
            workshops_list=[workshop.to_json() for workshop in workshops ]
            return jsonify(workshops_list),200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            return jsonify({'message': f'Error {e}'}), 500

    def get_workshop_by_id(self,workshop_id):
        try:
            # fetching single internship object
            workshop=Workshop.query.get(workshop_id)
            if not workshop:
                return jsonify({"message":" Workshop not found"}),404
            #if found than return in json format
            return jsonify(Workshop.to_json(workshop)),200
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
        
    def add_workshop(self,data):
     #   data = request.get_json()
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data.get()
        try:
            # data that u want to inject into database
            workshop=Workshop(
            workshop_id = data.get("workshop_id"),
            workshop_title = data.get("workshop_title"),
            workshop_org= data.get("workshop_org"),
            workshop_trainer = data.get("workshop_trainer"),
            workshop_desc = data.get("workshop_desc"),
            workshop_mode= data.get("workshop_mode"),
            workshop_venue= data.get("workshop_venue"),
            workshop_city = data.get("workshop_city"),
            workshop_date = data.get("workshop_date"),
            workshop_time = data.get("workshop_time"),
            workshop_target_audience = data.get("workshop_target_audience"),
            workshop_fees= data.get("workshop_fees"),
            workshop_seats = data.get("workshop_seats"),
            workshop_url = data.get("workshop_url")
            )
            
            # add object that u want to add
            db.session.add(workshop)  
            db.session.commit()
            return jsonify({'message': 'Workshop created successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_workshop(self,data):
        
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400
        # data that u want to update into database
        try:
            # fetching workshop_id frn json data
            workshop_id=data.get("workshop_id")
            # below code return obj of that id
            workshop=Workshop.query.get(workshop_id)
            #checking weather workshop id exist in db before any update
            if not workshop :
                return jsonify({"message": "Workshop not found"}),404
            #updating
            workshop.workshop_id = data.get("workshop_id")
            workshop.workshop_title = data.get("workshop_title")
            workshop.workshop_org= data.get("workshop_org")
            workshop.workshop_trainer = data.get("workshop_trainer")
            workshop.workshop_desc = data.get("workshop_desc")
            workshop.workshop_mode= data.get("workshop_mode")
            workshop.workshop_venue= data.get("workshop_venue")
            workshop.workshop_city = data.get("workshop_city")
            workshop.workshop_date = data.get("workshop_date")
            workshop.workshop_time = data.get("workshop_time")
            workshop.workshop_target_audience = data.get("workshop_target_audience")
            workshop.workshop_fees= data.get("workshop_fees")
            workshop.workshop_seats = data.get("workshop_seats")
            workshop.workshop_url = data.get("workshop_url")
            
            db.session.commit()
            return jsonify({'message': 'Workshop updated successfully'}), 200
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback()
            return jsonify({'message': f'Error {e}'}), 500


workshop_obj=Workshop()  # creating instance

#GET
@app.route("/api/all/workshops",methods=["GET"])
@jwt_required()
def api_get_all_workshops():
    try:
        return workshop_obj.get_all_workshops()
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#GET
@app.route("/api/workshop/<int:workshop_id>",methods=["GET"])
@jwt_required()
def api_get_workshop_by_id(workshop_id):
    try:
        return workshop_obj.get_workshop_by_id(workshop_id=workshop_id) # passing workshop id
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    

#POST
@app.route("/api/add/workshop",methods=["POST"])
@jwt_required()
def api_add_workshop():
    try:
        data=request.get_json()
        return workshop_obj.add_workshop(data=data)  # passing data
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    

#PUT
@app.route("/api/update/workshop",methods=["PUT"])
@jwt_required()
def api_update_workshop():
    try:
        data=request.get_json()
        return workshop_obj.update_workshop(data=data)
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

######################################################################################################################################################################


class Project(db.Model):
    __tablename__="project_info"
    
    #project attribute
    
    project_id=db.Column(db.Integer,primary_key=True)
    project_title=db.Column(db.String(255))
    project_desc=db.Column(db.String(255))
    project_company=db.Column(db.String(255))
    project_mentor=db.Column(db.String(255))
    project_start_date=db.Column(db.String(255))
    project_end_date=db.Column(db.String(255))
    project_duration=db.Column(db.String(255))
    
 
    def to_json(self):
         return{
        "project_id":self.project_id,
        "project_title":self.project_title,
        "project_desc":self.project_desc,
        "project_company":self.project_company,
        "project_mentor":self.project_mentor,
        "project_start_date":self.project_start_date,
        "project_end_date":self.project_end_date,
        "project_duration":self.project_duration
        }
    def get_all_projects(self):
        try:
            # fetching all the seminars object and storing in 
            projects=Project.query.all()
            # project_list coantain [ {project_id1},{ project_id2} } ]
            project_list=[ project.to_json() for project in projects ]
            
            return jsonify(project_list),200
    
        except Exception as e:
        
            return jsonify({'message': f'Error {e}'}), 500
        
    def get_project_by_id(self,project_id):
        try:
            # fetching single project object
            project=Project.query.get(project_id)
            if not project:
                return jsonify({"message":" Project not found"}),404
            #if found than return in json format
            return jsonify(Project.to_json(project)),200   
        except Exception as e:
            return jsonify({'message': f'Error {e}'}), 500
    
         
    def add_project(self,data):
        # no data pass than
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        try:
            # data that u want to inject into database
            project=Project(
                project_title=data.get("project_title"),
                project_desc=data.get("project_desc"),
                project_company=data.get("project_company"),
                project_mentor=data.get("project_mentor"),
                project_start_date=data.get("project_start_date"),
                project_end_date=data.get("project_end_date"),
                project_duration=data.get("project_duration")
                
            )
            # add object that u want 
            db.session.add(project)  
            db.session.commit()
            return jsonify({'message': 'Project added successfully'}), 201
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500
        
    def update_project(self,data):
       
        # no data pass than
        if not data:    
            return jsonify({'message': 'Invalid JSON data'}), 400
        
        # data that u want to update into database
        try:
            project_id=data.get("project_id")
            project=Project.query.get(project_id)
            if not project:
                return jsonify({"message":"Project not found"})
            
            # if project present than update
            project.project_title=data.get("project_title")
            project.project_desc=data.get("project_desc")
            project.project_company=data.get("project_company")
            project.project_mentor=data.get("project_mentor")
            project.project_start_date=data.get("project_start_date")
            project.project_end_date=data.get("project_end_date")
            project.duration=data.get("project_duration")
            db.session.commit()
            return jsonify({"message": "Project updated succcesfully"}),200
        
        except Exception as e:
            #this will bring session back to its state before the changes were made.
            db.session.rollback() 
            return jsonify({'message': f'Error {e}'}), 500


project_obj=Project() # creating instance of project

#GET
@app.route("/api/all/projects",methods=["GET"])
@jwt_required()
def api_get_all_projects():
    try:
        return project_obj.get_all_projects()
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

       
#GET
@app.route("/api/project/<int:project_id>",methods=["GET"])
@jwt_required()
def api_get_project_by_id(project_id):
    try:
        return project_obj.get_project_by_id(project_id=project_id)  # passing project_id
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500
    
#POST
@app.route("/api/add/project",methods=["POST"])
@jwt_required()
def api_add_project():
    try:
        data=request.get_json()
        return project_obj.add_project(data=data) # passing data 
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500

#PUT
@app.route("/api/update/project",methods=["PUT"])
@jwt_required()
def api_update_project():
    try:
        data=request.get_json()
        return project_obj.update_project(data=data) # passing data that need to be updated
    except Exception as e:
        return jsonify({'message': f'Error {e}'}), 500





####################################################################################################################################################



 
    




if __name__ == '__main__':
    app.run(debug=True)
