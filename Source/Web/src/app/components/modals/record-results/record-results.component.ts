import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import * as moment from 'moment';

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
  public tasks = [];
  public task = null;
  public totalMinutes = null;
  public teamMembers = [];
  public with = null;
  public syncToEHR = false;
  public notes = '';
  public patientEngagement = false;

  public tooltipRRM0Open;
  public tooltipRRM1Open;
  public tooltipRRM2Open;
  public showDate;
  public taskEditable;

  constructor(
    private modal: ModalService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.patient = this.data.patient;
      this.date = this.data.date ? this.data.date : moment();
      this.carePlan = this.data.carePlan;
      this.tasks = this.data.tasks;
      this.task = this.data.task;
      this.totalMinutes = this.data.totalMinutes;
      this.teamMembers = this.data.teamMembers;
      this.with = this.data.with;
      this.syncToEHR = this.data.syncToEHR;
      this.notes = this.data.notes;
      this.patientEngagement = this.data.patientEngagement;
    }
  }

  public setSelectedDay(e) {
    this.date = e;
  }

  public setPatientEngagement(num) {
    this.patientEngagement = num;
  }

  public clickClose() {
    this.modal.close(null);
  }

  public saveDisabled() {
    return (!this.task || !this.totalMinutes || !this.patientEngagement);
  }

  public clickSave() {
    this.modal.close({
      date: this.date,
      carePlan: this.carePlan,
      task: this.task,
      totalMinutes: this.totalMinutes,
      with: this.with,
      notes: this.notes,
      syncToEHR: this.syncToEHR,
      patientEngagement: this.patientEngagement,
    });
  }
}
