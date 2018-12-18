import { Component, OnInit } from '@angular/core';

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
  public newDiagnosis = '';
  public newDiagnosisIsChronic = false;
  public diagnoses = [
    {
      name: 'Diabetes',
      original: false,
      chronic: true,
    }
  ];
  public editDiagnosisIndex = -1;

  constructor() {

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

  public ngOnInit() {
    console.log(this.data);
    this.data = this.data || {};
    if (this.data && Object.keys(this.data).length > 0) {
      this.action = this.data.action;
      this.patientKnown = this.data.patientKnown;
      this.patientInSystem = this.data.patientInSystem;
      this.planKnown = this.data.planKnown;
    }
  }
}
