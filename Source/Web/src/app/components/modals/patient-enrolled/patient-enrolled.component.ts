import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patient-enrolled',
  templateUrl: './patient-enrolled.component.html',
  styleUrls: ['./patient-enrolled.component.scss'],
})
export class PatientEnrolledComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
