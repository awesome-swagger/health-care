import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-reassign-patients',
  templateUrl: './reassign-patients.component.html',
  styleUrls: ['./reassign-patients.component.scss'],
})
export class ReassignPatientsComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
