import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patient-emergency-contact',
  templateUrl: './patient-emergency-contact.component.html',
  styleUrls: ['./patient-emergency-contact.component.scss'],
})
export class PatientEmergencyContactComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
