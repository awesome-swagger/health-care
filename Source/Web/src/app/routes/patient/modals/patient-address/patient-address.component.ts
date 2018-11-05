import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patient-address',
  templateUrl: './patient-address.component.html',
  styleUrls: ['./patient-address.component.scss'],
})
export class PatientAddressComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
