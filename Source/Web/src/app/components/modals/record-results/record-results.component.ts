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

  public user = null;
  public userRoles = [];
  public patient = null;
  public date = null;
  public carePlan = null;
  public tasks = [];
  public task = null;
  public totalMinutes = null;
  public teamMembers = [];
  public withSelected = [];
  public with = null;
  public syncToEHR = false;
  public notes = '';
  public patientEngagement = 0;
  public datePickerOptions = {
    relativeLeft: '0px',
    relativeTop: '48px'
  };

  private authSub = null;

  public tooltipRRM0Open;
  public tooltipRRM1Open;
  public tooltipRRM2Open;
  public showDate;
  public taskEditable;

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
      this.patient = this.data.patient;
      this.date = this.data.date ? this.data.date : moment();
      this.carePlan = this.data.carePlan;
      this.task = this.data.task;
      this.totalMinutes = this.data.totalMinutes;
      this.with = this.data.with;
      this.syncToEHR = this.data.syncToEHR;
      this.notes = this.data.notes;
      this.patientEngagement = this.data.patientEngagement;
      // Get care team
      this.getCareTeamMembers(this.carePlan.id).then((teamMembers: any) => {
      	this.userRoles = teamMembers.filter((obj) => {
      		return obj.employee_profile.user.id === this.user.user.id;
      	});
      	this.teamMembers = teamMembers.filter((obj) => {
      		return obj.employee_profile.user.id !== this.user.user.id;
      	});
      	this.getUserTaskTemplates(this.carePlan, this.userRoles).then((userTaskTemplates: any) => {
      		this.tasks = userTaskTemplates;
      	});
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

  public getUserTaskTemplates(plan, userRoles) {
    let promise = new Promise((resolve, reject) => {
      // Get team task templates for this care plan template type
      let teamTasksSub = this.store.TeamTaskTemplate.readListPaged({
        plan_template__id: plan.plan_template.id
      }).subscribe(
        (teamTasks) => {
          let userTaskTemplates = [];
          // If user has the manager role on the care plan, get task templates that are marked is_manager
          let hasManagerRole = userRoles.filter((obj) => obj.is_manager);
          if (hasManagerRole.length > 0) {
            let managerTasks = teamTasks.filter((obj) => obj.is_manager_task);
            userTaskTemplates = userTaskTemplates.concat(managerTasks);
          }
          // If user has roles on this care plan, get task templates that are marked for their roles
          userRoles.forEach((teamMemberObj, index, array) => {
            if (teamMemberObj.role) {
              let roleTasks = teamTasks.filter((obj) => obj.role && obj.role.id === teamMemberObj.role.id);
              userTaskTemplates = userTaskTemplates.concat(roleTasks);
            }
            if ((index + 1) === array.length) {
              resolve(userTaskTemplates);
            }
          });
        },
        (err) => reject(err),
        () => {
          teamTasksSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public setSelectedDay(e) {
    this.date = e;
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

  public clickClose() {
    this.modal.close(null);
  }

  public saveDisabled() {
    return (!this.task || !this.totalMinutes);
  }

  public clickSave() {
    this.modal.close({
      date: this.date,
      carePlan: this.carePlan,
      task: this.task,
      totalMinutes: this.totalMinutes,
      with: this.withSelected.map((obj) => obj.employee_profile.id),
      notes: this.notes,
      syncToEHR: this.syncToEHR,
      patientEngagement: this.patientEngagement,
    });
  }
}
