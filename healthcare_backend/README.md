HOW TO RUN:
1)Clone the Repository

git clone https://github.com/Abhishek708844/Healthcare.git

cd Healthcare

2) Create AND OPEN Virtual Environment

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

 3) NAVIGATE TO root DIRECTORY SAME AS MANAGE.PY

 cd healthcare_backend  


 4) Install Dependencies

 pip install -r requirements.txt


 5) Create a .env file in the project root same as manage.py:
 
 .env TEMPLATE

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5433
SECRET_KEY=your-super-secret-django-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


 6) Run Migrations

python manage.py makemigrations
python manage.py migrate


7) RUN SERVER

python manage.py runserver


8) CHECK ALL ENDPOINTS IN POSTMAN 

API Endpoints


Authentication
POST /api/auth/register/ - User registration

POST /api/auth/login/ - User login (get JWT token)



Patients
POST /api/patients/ - Create patient (Authenticated)

GET /api/patients/ - List patients (Authenticated)

GET /api/patients/{id}/ - Get patient details

PUT /api/patients/{id}/ - Update patient

DELETE /api/patients/{id}/ - Delete patient




Doctors
POST /api/doctors/ - Create doctor (Authenticated)

GET /api/doctors/ - List all doctors

GET /api/doctors/{id}/ - Get doctor details

PUT /api/doctors/{id}/ - Update doctor

DELETE /api/doctors/{id}/ - Delete doctor





Patient-Doctor Mapping
POST /api/mappings/ - Assign doctor to patient

GET /api/mappings/ - List all mappings

GET /api/mappings/{patient_id}/ - Get doctors for a patient

DELETE /api/mappings/{id}/ - Remove assignment
