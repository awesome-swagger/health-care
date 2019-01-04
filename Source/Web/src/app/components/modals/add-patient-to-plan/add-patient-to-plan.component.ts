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
  public payerReimburses = false;
  public enrollPatientChecked = false;
  public planTypes = ['BHI', 'CCM', 'CCCM', 'CoCM', 'RPM', 'TCM'];
  public selectedPlanType = 'BHI';
  public selectedPlan = '';
  public newDiagnosis = '';
  public newDiagnosisIsChronic = false;
  public carePlans = null;
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

  constructor(
    private store: StoreService,
    private modals: ModalService
  ) { }

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

  public ngOnInit() {
    console.log(this.data);
    this.data = this.data || {};
    if (this.data && Object.keys(this.data).length > 0) {
      this.action = this.data.action;
      this.patientKnown = this.data.patientKnown;
      this.patientInSystem = this.data.patientInSystem;
      this.planKnown = this.data.planKnown;
    }

    this.getCarePlanTemplates().then((plans) => {
      this.carePlans = plans;
    })
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

  public handleSubmit() {
    if (!this.enrollPatientChecked) {
      let potentialPatientSub = this.store.PotentialPatient.create({
        first_name: this.firstName,
        last_name: this.lastName,
        care_plan: this.selectedPlan,
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
