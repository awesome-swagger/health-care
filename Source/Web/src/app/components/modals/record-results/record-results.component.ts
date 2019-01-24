import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-record-results',
  templateUrl: './record-results.component.html',
  styleUrls: ['./record-results.component.scss'],
})
export class RecordResultsComponent implements OnInit {

  public data = null;

  public tooltipRRM0Open;
  public tooltipRRM1Open;
  public tooltipRRM2Open;
  public showDate;
  public taskEditable;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
