import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';

@Component({
  selector: 'app-record-results',
  templateUrl: './record-results.component.html',
  styleUrls: ['./record-results.component.scss'],
})
export class RecordResultsComponent implements OnInit {

  public data = null;

  public patient = null;
  public date = null;
  public carePlan = null;
  public task = null;
  public totalMinutes = null;
  public with = null;
  public syncToEHR = false;
  public notes = '';
  public patientEngagement = false;

  public tooltipRRM0Open;
  public tooltipRRM1Open;
  public tooltipRRM2Open;

  constructor(
    private modal: ModalService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.patient = this.data.patient;
      this.date = this.data.date;
      this.carePlan = this.data.carePlan;
      this.task = this.data.task;
      this.totalMinutes = this.data.totalMinutes;
      this.with = this.data.with;
      this.syncToEHR = this.data.syncToEHR;
      this.notes = this.data.notes;
      this.patientEngagement = this.data.patientEngagement;
    }
  }

  public clickClose() {
    this.modal.close(null);
  }

  public clickSave() {
    this.modal.close({
      
    });
  }
}
