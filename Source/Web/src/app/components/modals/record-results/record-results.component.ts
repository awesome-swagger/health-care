import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import * as moment from 'moment';
import { AuthService, StoreService } from '../../../services';

@Component({
  selector: 'app-record-results',
  templateUrl: './record-results.component.html',
  styleUrls: ['./record-results.component.scss'],
})
export class RecordResultsComponent implements OnInit, OnDestroy {

  public data = null;

  public editing = false;
  public user = null;
  public patient = null;
  public date = null;
  public carePlan = null;
  public tasksLoaded = false;
  public teamTemplates = [];
  public selectedTeamTemplate = null;
  public taskEditable = true;
  public totalMinutes = null;
  public teamMembersLoaded = false;
  public teamMembers = [];
  public withSelected = [];
  public patientIncluded = false;
  public syncToEHR = false;
  public notes = '';
  public patientEngagement = 0;
  public datePickerOptions = {
    relativeLeft: '0px',
    relativeTop: '48px'
  };

  private authSub = null;

  public withOpen = false;
  public tasksOpen = false;
  public syncHelpOpen = false;
  public showDate = false;

  constructor(
    private modal: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (!this.data) {
      return;
    }
    this.authSub = this.auth.user$.subscribe((user) => {
      if (!user) return;
      this.user = user;
      this.editing = this.data.editing ? this.data.editing : false;
      this.taskEditable = this.data.taskEditable;
      this.patient = this.data.patient;
      this.date = this.data.date ? this.data.date : moment();
      this.carePlan = this.data.carePlan;
      this.totalMinutes = this.data.totalMinutes;
      this.syncToEHR = this.data.syncToEHR;
      this.notes = this.data.notes;
      this.patientIncluded = this.data.patientIncluded;
      this.patientEngagement = this.data.patientEngagement;
      // Get care team
      this.getCareTeamMembers(this.carePlan.id).then((teamMembers: any) => {
        this.teamMembersLoaded = true;
      	this.teamMembers = teamMembers.filter((obj) => {
      		return obj.employee_profile.user.id !== this.user.user.id;
      	});
        if (this.data.with) {
          this.withSelected = this.teamMembers.filter((obj) => {
            return this.data.with.includes(obj.employee_profile.id);
          });
        }
      });
      // Get Task Templates
      this.getTeamTemplates().then((teamTemplates: any) => {
        this.tasksLoaded = true;
        this.teamTemplates = teamTemplates;
        // If teamTemplateId is passed in data, set it as the selected task.
        if (this.data.teamTemplateId) {
          this.selectedTeamTemplate = this.teamTemplates.find((obj) => {
            return obj.id === this.data.teamTemplateId;
          });
        }
      });
    });
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
  }

  public getCareTeamMembers(planId) {
    let promise = new Promise((resolve, reject) => {
      let careTeamSub = this.store.CarePlan.detailRoute('get', planId, 'care_team_members', {}, {}).subscribe(
        (teamMembers: any) => resolve(teamMembers),
        (err) => reject(err),
        () => {
          careTeamSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getTeamTemplates() {
    let promise = new Promise((resolve, reject) => {
      // Get team task templates for this care plan template type
      let teamTemplatesSub = this.store.PlanTeamTemplate.readListPaged().subscribe(
        (teamTemplates) => resolve(teamTemplates),
        (err) => reject(err),
        () => {
          teamTemplatesSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public parseTime(time) {
    return time.format('HH:mm:00');
  }

  public setSelectedDay(e) {
    this.date.date(e.date());
    this.date.month(e.month());
    this.date.year(e.year());
  }

  public setSelectedTime(e) {
    let timeSplit = e.split(':');
    this.date.set({
      hour: timeSplit[0],
      minute: timeSplit[1],
    });
  }

  public setPatientEngagement(num) {
    this.patientEngagement = num;
  }

  public isSelectedMember(teamMember) {
    return this.withSelected.findIndex((obj) => obj.id === teamMember.id) > -1;
  }

  public toggleSelectedMember(teamMember) {
    let index = this.withSelected.findIndex((obj) => obj.id === teamMember.id);
    if (index > -1) {
      this.withSelected.splice(index, 1);
    } else {
      this.withSelected.push(teamMember);
    }
  }

  public formatSelectedMembers() {
    if (!this.withSelected || this.withSelected.length < 1) {
      return '';
    }
    let username = `${this.withSelected[0].employee_profile.user.first_name} ${this.withSelected[0].employee_profile.user.last_name}`;
    if (this.withSelected.length > 1) {
      return `${username}, +${this.withSelected.length - 1}`
    } else {
      return username;
    }
  }

  public clickClose() {
    this.modal.close(null);
  }

  public saveDisabled() {
    return (!this.date || !this.selectedTeamTemplate || !this.totalMinutes);
  }

  public clickSave() {
    this.modal.close({
      date: this.date,
      carePlan: this.carePlan,
      teamTemplate: this.selectedTeamTemplate.id,
      totalMinutes: this.totalMinutes,
      with: this.withSelected.map((obj) => obj.employee_profile.id),
      patientIncluded: this.patientIncluded,
      notes: this.notes,
      syncToEHR: this.syncToEHR,
      patientEngagement: this.patientEngagement,
    });
  }
}
