import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-medication',
  templateUrl: './medication.component.html',
  styleUrls: ['./medication.component.scss'],
})
export class MedicationComponent implements OnInit {

  public data = null;

  public showDate;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
