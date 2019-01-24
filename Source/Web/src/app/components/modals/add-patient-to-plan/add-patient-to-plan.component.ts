import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../services/store.service';
import { ModalService } from '../../../modules/modals';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-add-patient-to-plan',
  templateUrl: './add-patient-to-plan.component.html',
  styleUrls: ['./add-patient-to-plan.component.scss'],
})
export class AddPatientToPlanComponent implements OnInit {

  public data = null;
  public action = 'add';
  public patientKnown = false;
  public patientInSystem = false;
  public createDiagnosis = false;
  public planKnown = false;
  public patients = [];
  public selectedPatient = null;
  public payerReimburses = false;
  public enrollPatientChecked = false;
  public newDiagnosis = '';
  public newDiagnosisIsChronic = false;
  public serviceAreas = [];
  public selectedServiceArea = null;
  public carePlans = [];
  public selectedPlan = null;
  public planTypes = ['BHI', 'CCM', 'CCCM', 'CoCM', 'RPM', 'TCM'];
  public selectedPlanType = 'BHI';
  public diagnoses = [
    {
      name: 'Diabetes',
      original: false,
      chronic: true,
    }
  ];
  public editDiagnosisIndex = -1;
  public firstName = '';
  public lastName = '';
  public phoneNumber = '';

  public dropAPPM2Open;

  constructor(
    private store: StoreService,
    private modals: ModalService
  ) { }

  public ngOnInit() {
    console.log(this.data);
    this.data = this.data || {};
    if (this.data && Object.keys(this.data).length > 0) {
      this.action = this.data.action;
      this.patientKnown = this.data.patientKnown;
      this.patientInSystem = this.data.patientInSystem;
      this.planKnown = this.data.planKnown;
      if (this.patientKnown) {
        this.selectedPatient = this.data.patient;
      }
    }
    this.getPatients().then((patients: any) => {
      this.patients = patients;
    });
    this.getCarePlanTemplates().then((plans: any) => {
      this.carePlans = plans;
      this.getServiceAreas().then((serviceAreas: any) => {
        this.serviceAreas = serviceAreas;
        if (this.planKnown) {
          this.selectedPlan = this.carePlans.find((obj) => obj.id === this.data.planTemplate.id);
          this.selectedServiceArea = this.serviceAreas.find((obj) => obj.id === this.data.planTemplate.service_area.id);
        }
      });
    });
  }

  public getPatients() {
    return new Promise((resolve, reject) => {
        let patientsSub = this.store.PatientProfile.readListPaged().subscribe(
          (patients) => {
            resolve(patients);
          },
          (err) => {
            reject(err);
          },
          () => {
            patientsSub.unsubscribe();
          }
        )
    });
  }

  public getServiceAreas() {
    return new Promise((resolve, reject) => {
        let serviceAreasSub = this.store.ServiceArea.readListPaged().subscribe(
          (serviceAreas) => {
            resolve(serviceAreas);
          },
          (err) => {
            reject(err);
          },
          () => {
            serviceAreasSub.unsubscribe();
          }
        )
    });
  }

  public getCarePlanTemplates() {
    return new Promise((resolve, reject) => {
        let carePlanSub = this.store.CarePlanTemplate.readListPaged().subscribe(
          (plans) => {
            resolve(plans);
          },
          (err) => {
            reject(err);
          },
          () => {
            carePlanSub.unsubscribe();
          }
        )
    });
  }

  public carePlansFiltered() {
    if (!this.selectedServiceArea) {
      return [];
    }
    return this.carePlans.filter((obj) => obj.service_area.id === this.selectedServiceArea.id);
  }

  public selectedPatientName() {
    if (!this.selectedPatient) {
      return '';
    }
    return `${this.selectedPatient.user.first_name} ${this.selectedPatient.user.last_name}`;
  }

  public addDiagnosis() {
    this.createDiagnosis = !this.createDiagnosis
    this.diagnoses.push({
      name: this.newDiagnosis,
      original: false,
      chronic: this.newDiagnosisIsChronic,
    });
  }

  public editDiagnosis(index) {
    this.editDiagnosisIndex = index;
  }

  public clickClose() {
    this.modals.close(null);
  }

  public handleSubmit() {
    if (!this.enrollPatientChecked) {
      let potentialPatientSub = this.store.PotentialPatient.create({
        first_name: this.firstName,
        last_name: this.lastName,
        care_plan: this.selectedPlan.name,
        phone: this.phoneNumber,
        facility: [
  				"f96e8476-51bc-4cbc-b3b8-29ed0bf5c334"
			  ],
      }).subscribe(
        (data) => {
          this.modals.close(data);
        },
        (err) => {

        },
        () => {
          potentialPatientSub.unsubscribe();
        }
      )
    }
  }
}
