from pydantic import BaseModel
from datetime import date,time
class AppointmentUpdate(BaseModel):
    date: date
    time: time
    status: str

class CancelAppointmentRequest(BaseModel):
    patient_id: str
    appointment_number: int
    