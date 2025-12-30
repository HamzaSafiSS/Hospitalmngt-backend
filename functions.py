from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Patient, Doctor, Appointment
from schemas import AppointmentUpdate, CancelAppointmentRequest
from datetime import date, time

# ----------------- Patients -----------------
def ListPatient(db: Session):
    patients = db.query(Patient).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "case": p.case,
            "phone": p.phone,
            "address": p.address
        } for p in patients
    ]

def AddPatient(db: Session, id, name, age, gender, case, phone, address):
    if db.query(Patient).filter(Patient.id == id).first():
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    new_patient = Patient(
        id=id,
        name=name,
        age=age,
        gender=gender,
        case=case,
        phone=phone,
        address=address
    )
    db.add(new_patient)
    db.commit()
    return {"Message": "Patient Added Successfully"}

def ViewById(db: Session, patient_ID):
    patient = db.query(Patient).filter(Patient.id == patient_ID).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not exist")
    return {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "case": patient.case,
        "phone": patient.phone,
        "address": patient.address
    }

def SearchByName(db: Session, searchTerm):
    search_pattern = f"%{searchTerm}%"
    patients = db.query(Patient).filter(
        or_(
            Patient.name.ilike(search_pattern),
             # Assuming ID search is also desired as string, though ID is Integer in ORM.
             # If ID is strictly integer, casting might be needed or just skipping ID search if searchTerm is not int.
             # For now, keeping name search primarily. 
             # If user passes ID as string, we can try to cast or match if we change model to String.
             # The model defines ID as Integer.
             # Let's handle name search mainly, or exact ID match if digit.
        )
    ).all()
    
    # If generic search across textual fields is needed:
    if searchTerm.isdigit():
         id_match = db.query(Patient).filter(Patient.id == int(searchTerm)).first()
         if id_match and id_match not in patients:
             patients.append(id_match)

    return [
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "case": p.case,
            "phone": p.phone,
            "address": p.address
        } for p in patients
    ]

def UpdatePatient(db: Session, PatientName, PatientAge, PatientGender, PatientCase, PatientPhone, PatientAddress, patientID):
    patient = db.query(Patient).filter(Patient.id == patientID).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient with this ID does not exist")
    
    patient.name = PatientName
    patient.age = PatientAge
    patient.gender = PatientGender
    patient.case = PatientCase
    patient.phone = PatientPhone
    patient.address = PatientAddress
    
    db.commit()
    return {"Message": "Patient Information Successfully Updated"}

def DeletePatient(db: Session, patientid):
    patient = db.query(Patient).filter(Patient.id == patientid).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient with entered ID not exist")
    
    db.delete(patient)
    db.commit()
    return {"Message": "Patient Successfully Deleted"}


# ----------------- Doctors -----------------
def ListDoctors(db: Session):
    doctors = db.query(Doctor).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "age": d.age,
            "gender": d.gender,
            "speciality": d.speciality
        } for d in doctors
    ]

def AddDoctor(db: Session, doctorId, doctorName, doctorAge, doctorGender, doctorSpeciality):
    if db.query(Doctor).filter(Doctor.id == doctorId).first():
        raise HTTPException(status_code=400, detail="Doctor with this ID already exists.")
    
    new_doctor = Doctor(
        id=doctorId,
        name=doctorName,
        age=doctorAge,
        gender=doctorGender,
        speciality=doctorSpeciality
    )
    db.add(new_doctor)
    db.commit()
    return {"Message": "Doctor Successfully Added."}

def ViewDoctorById(db: Session, doctorid):
    doctor = db.query(Doctor).filter(Doctor.id == doctorid).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor with the provided ID not exist")
    return {
        "id": doctor.id,
        "name": doctor.name,
        "age": doctor.age,
        "gender": doctor.gender,
        "speciality": doctor.speciality
    }

def SearchDoctorByName(db: Session, searchTerm):
    search_pattern = f"%{searchTerm}%"
    doctors = db.query(Doctor).filter(Doctor.name.ilike(search_pattern)).all()
    if searchTerm.isdigit():
        id_match = db.query(Doctor).filter(Doctor.id == int(searchTerm)).first()
        if id_match and id_match not in doctors:
            doctors.append(id_match)

    return [
        {
            "id": d.id,
            "name": d.name,
            "age": d.age,
            "gender": d.gender,
            "speciality": d.speciality
        } for d in doctors
    ]

def UpdateDoctor(db: Session, newDoctorName, newDoctorAge, newDoctorGender, newDoctorSpeciality, doctorID):
    doctor = db.query(Doctor).filter(Doctor.id == doctorID).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor with this ID not exist")
    
    doctor.name = newDoctorName
    doctor.age = newDoctorAge
    doctor.gender = newDoctorGender
    doctor.speciality = newDoctorSpeciality
    
    db.commit()
    return {"Message": "Doctor Information Successfully Updated."}

def DeleteDoctor(db: Session, doctorid):
    doctor = db.query(Doctor).filter(Doctor.id == doctorid).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor with entered ID not exist")
    
    db.delete(doctor)
    db.commit()
    return {"Message": "Doctor Successfully Deleted."}


# ----------------- Appointments -----------------
def ListAppointments(db: Session):
    appointments = db.query(Appointment).all()
    return [
        {
            "id": a.id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "date": a.appointment_date,
            "time": a.appointment_time,
            "status": a.status
        } for a in appointments
    ]

def BookAppointment(db: Session, patientid, doctorid, date_val, time_val, status):
    if not db.query(Patient).filter(Patient.id == patientid).first():
        raise HTTPException(status_code=404, detail="Patient with entered ID not exist")
    if not db.query(Doctor).filter(Doctor.id == doctorid).first():
        raise HTTPException(status_code=404, detail="Doctor with entered ID not exist")

    # Check for duplicate appointment for the same doctor
    duplicate = db.query(Appointment).filter(
        Appointment.doctor_id == doctorid,
        Appointment.appointment_date == date_val,
        Appointment.appointment_time == time_val
    ).first()
    
    if duplicate:
        raise HTTPException(status_code=400, detail="This doctor already has an appointment at this date and time.")

    new_appointment = Appointment(
        patient_id=patientid,
        doctor_id=doctorid,
        appointment_date=date_val,
        appointment_time=time_val,
        status=status
    )
    db.add(new_appointment)
    db.commit()
    return {"Message": "Appointment Successfully Booked."}

def ViewAppointmentByID(db: Session, appointment_id):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not exist")
    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "date": appointment.appointment_date,
        "time": appointment.appointment_time,
        "status": appointment.status
    }

def ViewAppointmentsByPatientID(db: Session, patientid):
    appointments = db.query(Appointment).filter(Appointment.patient_id == patientid).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointment with entered Patient ID not exist.")
    return [
        {
            "id": a.id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "date": a.appointment_date,
            "time": a.appointment_time,
            "status": a.status
        } for a in appointments
    ]

def ViewAppointmentsByDoctorID(db: Session, doctorid):
    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctorid).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointment with entered Doctor ID not exist.")
    return [
        {
            "id": a.id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "date": a.appointment_date,
            "time": a.appointment_time,
            "status": a.status
        } for a in appointments
    ]

def UpdateAppointment(db: Session, patientid, number, data: AppointmentUpdate):
    appointments = db.query(Appointment).filter(Appointment.patient_id == patientid).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="Patient with entered ID does not exist or has no Appointment.")
    
    if number < 1 or number > len(appointments):
        raise HTTPException(status_code=400, detail="Invalid appointment number.")

    selected_app = appointments[number - 1]

    # Check for duplicate appointment for the same doctor, excluding current appointment
    duplicate = db.query(Appointment).filter(
        Appointment.doctor_id == selected_app.doctor_id,
        Appointment.appointment_date == data.date,
        Appointment.appointment_time == data.time,
        Appointment.id != selected_app.id
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="This doctor already has an appointment at this date and time.")

    selected_app.appointment_date = data.date
    selected_app.appointment_time = data.time
    selected_app.status = data.status
    
    db.commit()
    return {"Message": "Appointment Successfully Updated."}

def CancelAppointment(db: Session, request: CancelAppointmentRequest):
    appointments = db.query(Appointment).filter(Appointment.patient_id == request.patient_id).all()
    if not appointments:
        raise HTTPException(status_code=404, detail=f"Patient ID {request.patient_id} does not exist or has no appointments.")
    
    if request.appointment_number < 1 or request.appointment_number > len(appointments):
        raise HTTPException(status_code=400, detail="Invalid appointment number.")

    selected_app = appointments[request.appointment_number - 1]
    db.delete(selected_app)
    db.commit()
    return {"Message": "Appointment Successfully Deleted."}

def DeleteAppointmentByID(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not exist")
    
    db.delete(appointment)
    db.commit()
    return {"Message": "Appointment Successfully Deleted"}

def UpdateAppointmentByID(db: Session, appointment_id: int, data: AppointmentUpdate):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not exist")

    # Check for duplicate
    duplicate = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == data.date,
        Appointment.appointment_time == data.time,
        Appointment.id != appointment_id
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="This doctor already has an appointment at this date and time.")

    appointment.appointment_date = data.date
    appointment.appointment_time = data.time
    appointment.status = data.status
    
    db.commit()
    return {"Message": "Appointment Successfully Updated"}
