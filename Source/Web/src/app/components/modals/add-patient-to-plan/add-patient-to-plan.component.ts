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
  public planKnown = false;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
    this.action = this.data.action;
    this.patientKnown = this.data.patientKnown;
    this.patientInSystem = this.data.patientInSystem;
    this.planKnown = this.data.planKnown;
  }
}
