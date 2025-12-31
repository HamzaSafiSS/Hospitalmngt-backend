from db import get_connection
from functions import ListPatient
from functions import AddPatient
from functions import ViewById
from functions import SearchByName
from functions import UpdatePatient
from functions import DeletePatient
from functions import ListDoctors
from functions import AddDoctor
from functions import ViewDoctorById
from functions import SearchDoctorByName
from functions import UpdateDoctor
from functions import DeleteDoctor
from functions import ListAppointments
from functions import BookAppointment
from functions import ViewAppointmentByID
from functions import ViewAppointmentsByPatientID
from functions import ViewAppointmentsByDoctorID
from functions import UpdateAppointment
from functions import CancelAppointment
import sys

def ManagePatients():
    while True:
        print('\n--- Patient Management ---')
        print("1. List All Patients")
        print("2. Add Patient")
        print("3. View By Patient ID")
        print("4. Search Patients By Name")
        print("5. Update Patient")
        print("6. Delete Patient")
        print("7. Back")
        print("8. Exit")
        choice = int(input("Please enter the number of the service you need: "))
        if choice == 1:
            ListPatient()
        elif choice == 2:
            AddPatient()
        elif choice == 3:
            ViewById()
        elif choice == 4:
            SearchByName()
        elif choice == 5:
            UpdatePatient()
        elif choice == 6:
            DeletePatient()
        elif choice == 7:
            GetServices()
        elif choice == 8:
            sys.exit()


def ManageDoctors():
    while True:
        print('\n--- Doctors Management ---')
        print("1. List All Doctors")
        print("2. Add Doctor")
        print("3. View By Doctor ID")
        print("4. Search Doctor By Name")
        print("5. Update Doctor")
        print("6. Delete Doctor")
        print("7. Back")
        print("8. Exit")
        choice = int(input("Please enter the number of the service you need: "))
        if choice == 1:
            ListDoctors()
        elif choice == 2:
            AddDoctor()
        elif choice == 3:
            ViewDoctorById()
        elif choice == 4:
            SearchDoctorByName()
        elif choice == 5:
            UpdateDoctor()
        elif choice == 6:
            DeleteDoctor()
        elif choice == 7:
            GetServices()
        elif choice == 8:
            sys.exit()
def ManageAppointment():
    print("--- Appointment Management ---")
    print("1. List All Appointments")
    print("2. Book Appointment")
    print("3. View Appointment By ID")
    print("4. View Appointments By Patient ID")
    print("5. View Appointments By Doctor ID")
    print("6. Update Appointment")
    print("7. Cancel Appointment")
    print("8. Back")
    print("9. Exit")
    choice = int(input("Please Enter Service Number you want."))
    if choice == 1:
        ListAppointments()
    elif choice == 2:
        BookAppointment()
    elif choice == 3:
        ViewAppointmentByID()
    elif choice == 4:
        ViewAppointmentsByPatientID()
    elif choice == 5:
        ViewAppointmentsByDoctorID()
    elif choice == 6:
        UpdateAppointment()                           
    elif choice == 7:
        CancelAppointment()
    elif choice == 8:
        GetServices()
    elif choice == 9:
        sys.exit()
    
def GetServices():
    while True:
        print('\n -----Select Services You Want-----')
        print('1. Patients Management Services')
        print('2. Doctors Management Services')
        print('3. Appointment Services')
        
        choice = int(input("Please Enter Service Number You Want: "))
        if choice == 1:
            ManagePatients()
        elif choice == 2:
            ManageDoctors() 
        elif choice == 3:
            ManageAppointment()
GetServices()