import { Component, OnInit } from '@angular/core';
import { isNull } from 'util';

@Component({
  selector: 'app-enroll-patient',
  templateUrl: './enroll-patient.component.html',
  styleUrls: ['./enroll-patient.component.scss']
})
export class EnrollPatientComponent implements OnInit {

  constructor() { }

  public data = null;
  public step = 0;
  public stepName = [
    "Verbal Confirmation",
    "Patient Info"
  ]
  public box1 = false;
  public box2 = false;
  public box3 = false;
  public box4 = false;
  public box5 = false;
  public box6 = false;

  ngOnInit() {
  }

  clickNext() {
    if (this.box1 && this.box2 && this.box3 && this.box4 && this.box5 && this.box6) {
      this.step ++;
    }
  }

}
