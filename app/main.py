import os
from fastapi import FastAPI, Depends, HTTPException 
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import date, time
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import engine         
from app.models import Base
from app.db import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.auth import hash_password, verify_password, create_access_token 
from pydantic import BaseModel
from app.auth import hash_password
from app.models import User, RoleEnum
from app.db import SessionLocal
from dotenv import load_dotenv

from fastapi import APIRouter, Query
from typing import List
from app.user import UserOut
from app.auth import require_role
from app.models import User
# Import functions
from app.functions import (
    ListPatient, AddPatient, ViewById, SearchByName, UpdatePatient, DeletePatient,
    ListDoctors, ViewDoctorById, SearchDoctorByName, UpdateDoctor, DeleteDoctor,
    ListAppointments, BookAppointment, ViewAppointmentsByPatientID, ViewAppointmentsByDoctorID,
    UpdateAppointment, CancelAppointment, DeleteAppointmentByID, UpdateAppointmentByID
)
from app.schemas import AppointmentUpdate, CancelAppointmentRequest
from app.auth import require_role

load_dotenv()

app = FastAPI(title="Hospital Management API")

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    create_default_admin()
    
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],         # allow GET, POST, PUT, DELETE
    allow_headers=["*"],
)

def create_default_admin():
    db = SessionLocal()
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if not existing_admin:
        new_admin = User(
            email=admin_email,
            password=hash_password(admin_password),
            role=RoleEnum.ADMIN
        )
        db.add(new_admin)
        db.commit()

    db.close()

# ----------------- Home -----------------
@app.get("/")
def home():
    return {"message": "Hospital Management API is running"}

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    users = (
        db.query(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return users

# ----------------- Admin -----------------

@app.post("/admin/create-admin")
def create_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    new_admin = User(
        email=user.email,
        password=hash_password(user.password),
        role=RoleEnum.ADMIN
    )
    db.add(new_admin)
    db.commit()
    return {"message": "Admin created"}


# ----------------- Patients -----------------
@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    return ListPatient(db)

class Patient(BaseModel):
    id: str  # Kept as str to match existing Pydantic models, but ORM uses Int (likely auto-casting or logic needed)
             # NOTE: Check if IDs are actually ints. Models.py says Integer. Pydantic says str.
             # We should probably align these, but keeping API contract for now if possible.
             # If passed as string "123", it parses to int 123 usually.
    name: Annotated[str, Field(pattern="^[A-Za-z ]+$")]
    age: Annotated[int, Field(ge=0, le=300)]
    gender: Annotated[str, Field(pattern="^(Male|Female|Other)$")]
    case: str
    phone: Annotated[str, Field(pattern=r"^(09\d{8}|\+2519\d{8})$")]
    address: str
    
@app.post("/patients")
def add_patient(patient: Patient, db: Session = Depends(get_db)):
    return AddPatient(db, patient.id, patient.name, patient.age, patient.gender, patient.case, patient.phone, patient.address)

@app.get("/patients/search")
def search_patients(searchTerm: str, db: Session = Depends(get_db)):
    return SearchByName(db, searchTerm)

@app.get("/patients/{patientID}")
def get_by_patient_id(patientID: str, db: Session = Depends(get_db)):
    return ViewById(db, patientID)

@app.put("/patients")
def update_patient(patient: Patient, db: Session = Depends(get_db)):
    return UpdatePatient(db, patient.name, patient.age, patient.gender, patient.case, patient.phone, patient.address, patient.id)

@app.delete("/patients/{patientid}")
def delete_patient(patientid: str, db: Session = Depends(get_db)):
    return DeletePatient(db, patientid)

# ----------------- Doctors -----------------
@app.get("/doctors")
def list_doctors(db: Session = Depends(get_db)):
    return ListDoctors(db)

class Doctor(BaseModel):
    id: str
    name: Annotated[str, Field(pattern="^[A-Za-z ]+$")]
    age: Annotated[int, Field(ge=25, le=300)]
    gender: Annotated[str, Field(pattern="^(Male|Female|Other)$")]
    speciality: str

@app.post("/admin/create-doctor")
def create_doctor(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    new_doctor = User(
        email=user.email,
        password=hash_password(user.password),
        role=RoleEnum.DOCTOR
    )
    db.add(new_doctor)
    db.commit()
    return {"message": "Doctor created"}

@app.post("/doctors")
def add_doctor(doctor: Doctor, db: Session = Depends(get_db)):
    return AddDoctor(db, doctor.id, doctor.name, doctor.age, doctor.gender, doctor.speciality)

@app.get("/doctors/search")
def search_doctors(searchTerm: str, db: Session = Depends(get_db)):
    return SearchDoctorByName(db, searchTerm)

@app.get("/doctors/{doctorid}")
def view_doctor_by_id(doctorid: str, db: Session = Depends(get_db)):
    return ViewDoctorById(db, doctorid)

@app.put("/doctors")
def update_doctor(doctor: Doctor, db: Session = Depends(get_db)):
    return UpdateDoctor(db, doctor.name, doctor.age, doctor.gender, doctor.speciality, doctor.id)

@app.delete("/doctors/{doctorid}")
def delete_doctor(doctorid: str, db: Session = Depends(get_db)):
    return DeleteDoctor(db, doctorid)

# ----------------- Appointments -----------------
@app.get("/appointments")
def list_appointments(db: Session = Depends(get_db)):
    return ListAppointments(db)

class Appointment(BaseModel):
    patient_id: str
    doctor_id: str
    date: date
    time: time
    status: str

@app.post("/appointments")
def book_appointment(appointment: Appointment, db: Session = Depends(get_db)):
    return BookAppointment(db, appointment.patient_id, appointment.doctor_id, appointment.date, appointment.time, appointment.status)

@app.get("/appointments/patient/{patientid}")
def appointment_by_patient_id(patientid: str, db: Session = Depends(get_db)):
    return ViewAppointmentsByPatientID(db, patientid)

@app.get("/appointments/doctor/{doctorid}")
def appointment_by_doctor_id(doctorid: str, db: Session = Depends(get_db)):
    return ViewAppointmentsByDoctorID(db, doctorid)

@app.get("/appointments/{appointmentid}")
def appointment_by_id(appointmentid: int, db: Session = Depends(get_db)):
    return ViewAppointmentByID(db, appointmentid)

@app.put("/appointments/{appointmentid}")
def update_appointment_by_id(appointmentid: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    return UpdateAppointmentByID(db, appointmentid, appointment)

@app.put("/appointments/{patientid}/{number}")
def update_appointment(patientid: str, number: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    return UpdateAppointment(db, patientid, number, appointment)

@app.delete("/appointments/{appointmentid}")
def delete_appointment(appointmentid: int, db: Session = Depends(get_db)):
    return DeleteAppointmentByID(db, appointmentid)

@app.delete("/appointments")
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):
    return CancelAppointment(db, request)

@app.get("/test")
def test():
    return {"status": "ok"}

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(new_user) # Here tracked by the SQLAlchemy Session it means it is still at pending level.
    db.commit() # lushes all pending changes to the database and permanently saves them
    db.refresh(new_user) # reloads the object from the database to get the latest data

    return {"message": "User created successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}