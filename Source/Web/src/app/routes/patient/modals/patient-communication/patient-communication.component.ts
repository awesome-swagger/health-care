import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patient-communication',
  templateUrl: './patient-communication.component.html',
  styleUrls: ['./patient-communication.component.scss'],
})
export class PatientCommunicationComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
