import { Component, EventEmitter, Input, Output, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { find as _find } from 'lodash';
import * as moment from 'moment';
import { ModalService } from '../../modules/modals';
import { ToastService } from '../../modules/toast';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, LocalStorageService, StoreService, UtilsService } from '../../services';
import { ProblemAreasComponent } from '../../routes/patient/modals/problem-areas/problem-areas.component';
import { FinancialDetailsComponent } from '../../routes/patient/modals/financial-details/financial-details.component';

@Component({
  selector: 'app-patient-header',
  templateUrl: './patient-header.component.html',
  styleUrls: ['./patient-header.component.scss']
})
export class PatientHeaderComponent implements OnInit, OnDestroy {

  public moment = moment;

  public _currentPage = null;
  public employee = null;
  public isCollapsed = false;
  public isCareTeamMember = false;
  public employeeCTRoles = [];
  public patient = null;
  public carePlans = [];
  public patientPlansOverview = null;
  public selectedPlan = null;
  public selectedPlanOverview = null;
  public allTeamMembers = [];
  public careTeamMembers = [];
  public careManager = null;
  public problemAreas = [];
  public editCheckin = false;
  public myCheckinDate: moment.Moment = null;
  public checkinRevertValue: moment.Moment = null;
  public nextCheckinTeamMember = null;

  @Output()
  public onPlanChange = new EventEmitter<any>();

  public planSelectOpen = false;
  public teamListOpen = false;
  public planSelectOptions: PopoverOptions = {};
  public datePickerOptions: PopoverOptions = {
    relativeTop: '48px',
    relativeRight: '0px',
  };

  private routeSub = null;
  private employeeSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private toast: ToastService,
    private auth: AuthService,
    private store: StoreService,
    private local: LocalStorageService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.routeSub = this.route.params.subscribe((params) => {
      this.employeeSub = this.auth.user$.subscribe((employee) => {
        if (!employee) {
          return;
        }
        this.employee = employee;
        this.getPatient(params.patientId).then((patient: any) => {
          this.patient = patient;
        });
        this.getCarePlans(params.patientId).then((carePlans: any) => {
          this.carePlans = carePlans;
          this.selectedPlan = carePlans.find((obj) => {
            return obj.id === params.planId;
          });
          this.getCarePlanOverview(params.patientId).then((overview: any) => {
            this.patientPlansOverview = overview.results;
            this.selectedPlanOverview = this.getOverviewForPlanTemplate(this.selectedPlan.plan_template.id);
            this.allTeamMembers = this.selectedPlanOverview.care_team;
            // Get care manager
            this.careManager = this.allTeamMembers.filter((obj) => {
              return obj.is_manager;
            })[0];
            // Get regular team members
            this.careTeamMembers = this.allTeamMembers.filter((obj) => {
              return !obj.is_manager;
            });
            let employeeCTRoles = this.allTeamMembers.filter((obj) => {
              return obj.employee_profile.id === this.employee.id;
            });
            this.isCareTeamMember = !!employeeCTRoles[0];
            this.employeeCTRoles = employeeCTRoles;
            // Set next checkin date and time
            if (this.isCareTeamMember && this.employeeCTRoles) {
              if (this.employeeCTRoles[0].next_checkin) {
                if (this.isBefore3DaysAgo(moment(this.employeeCTRoles[0].next_checkin))) {
                  return;
                }
                this.myCheckinDate = moment(this.employeeCTRoles[0].next_checkin);
              }
            }
            // Get team member with closest check in date
            let sortedCT = this.sortTeamMembersByCheckin(this.allTeamMembers);
            if (sortedCT.length > 0) {
              this.nextCheckinTeamMember = sortedCT[0];
            }
          });
          this.getProblemAreas(params.patientId).then((problemAreas: any) => {
            this.problemAreas = problemAreas;
          });
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.routeSub) {
      this.routeSub.unsubscribe();
    }
    if (this.employeeSub) {
      this.employeeSub.unsubscribe();
    }
  }

  public getPatient(patientId) {
    let promise = new Promise((resolve, reject) => {
      let fetchSub = this.store.PatientProfile.read(patientId).subscribe(
        (patient) => resolve(patient),
        (err) => reject(err),
        () => {
          fetchSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getCarePlans(patientId) {
    let promise = new Promise((resolve, reject) => {
      let carePlansSub = this.store.CarePlan.readListPaged({
        patient: patientId,
      }).subscribe(
        (carePlans) => resolve(carePlans),
        (err) => reject(err),
        () => {
          carePlansSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getCarePlanOverview(patientId) {
    let promise = new Promise((resolve, reject) => {
      let overviewSub = this.store.PatientProfile.detailRoute('get', patientId, 'care_plan_overview').subscribe(
        (overview) => resolve(overview),
        (err) => reject(err),
        () => {
          overviewSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getProblemAreas(patient) {
    let promise = new Promise((resolve, reject) => {
      let problemAreasSub = this.store.ProblemArea.readListPaged({
        plan: this.selectedPlan.id,
      }).subscribe(
        (problemAreas) => resolve(problemAreas),
        (err) => reject(err),
        () => {
          problemAreasSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getOverviewForPlanTemplate(planTemplateId) {
    return this.patientPlansOverview.find((obj) => obj.plan_template.id === planTemplateId);
  }

  public formatTimeSince(time) {
    let momentTime = moment(time);
    let today = moment().startOf('day');
    if (momentTime.isSame(today, 'day')) {
      return 'Today';
    } else {
      return momentTime.fromNow();
    }
  }

  public routeToHistory(patient, plan) {
    this.router.navigate(['/patient', patient.id, 'history', plan.id], {
      queryParams: {
        last_patient_interaction: true,
      }
    });
  }

  public changeSelectedPlan(plan) {
    this.router.navigate(['/patient', this.patient.id, this.currentPage, plan.id]);
  }

  public routeToPatientHistory() {
    this.router.navigate(['/patient', this.patient.id, 'history', this.selectedPlan.id]);
  }

  public openProblemAreas() {
    this.modals.open(ProblemAreasComponent, {
      closeDisabled: false,
      data: {
        patient: this.patient,
        plan: this.selectedPlan,
        problemAreas: this.problemAreas,
      },
      width: '560px',
    }).subscribe((res) => {
      this.getProblemAreas(this.patient.id).then((problemAreas: any) => {
        this.problemAreas = problemAreas;
      });
    });
  }

  public openFinancialDetails() {
    this.modals.open(FinancialDetailsComponent, {
      closeDisabled: false,
      data: {
        patient: this.patient,
        plan: this.selectedPlan,
      },
      width: '532px',
    }).subscribe((res) => {
      if (!res) return;
      this.patient.payer_reimbursement = res.patient.payer_reimbursement;
      this.selectedPlan.billing_type = res.plan.billing_type;
    });
  }

  public progressInWeeks(plan: { created: moment.MomentInput, plan_template: { duration_weeks: number } }): number {
    if (!plan || !plan.created) {
      return 0;
    }

    return Math.min(plan.plan_template.duration_weeks, moment().diff(moment(plan.created), 'weeks'));
  }

  public parseTime(time) {
    return time.format('HH:mm:00');
  }

  public timePillColor(plan) {
    if (!this.patient.payer_reimbursement || !plan.billing_type) {
      return null;
    }
    if (plan.billing_type.acronym === 'TCM') {
      return this.utils.timePillColorTCM(plan.created);
    } else {
      let overview = this.getOverviewForPlanTemplate(this.selectedPlan.plan_template.id);
      let timeCount = this.totalMinutes(overview.time_spent_this_month);
      let allotted = plan.billing_type.billable_minutes;
      return this.utils.timePillColor(timeCount, allotted);
    }
  }

  public totalMinutes(timeSpentStr) {
    if (!timeSpentStr) {
      return 0;
    }
    let hours = 0;
    let minutes = 0;
    let timeCountSplit = timeSpentStr.split(":");
    let splitHours = parseInt(timeCountSplit[0]);
    let splitMinutes = parseInt(timeCountSplit[1]);
    hours = splitHours;
    minutes = splitMinutes;
    minutes = minutes + (hours * 60);
    return minutes;
  }

  public isBefore3DaysAgo(dateAsMoment) {
    let threeDaysAgo = moment().subtract(3, 'days').startOf('day');
    if (dateAsMoment.isBefore(threeDaysAgo)) {
      return true;
    }
    return false;
  }

  public sortTeamMembersByCheckin(teamMembers) {
    // removes members without a checkin date set
    return teamMembers.filter((obj) => {
      return obj.next_checkin && !this.isBefore3DaysAgo(moment(obj.next_checkin));
    }).sort((left: any, right: any) => {
      left = moment(left.next_checkin).format();
      right = moment(right.next_checkin).format();
      return left - right;
    });
  }

  public clickEditCheckin() {
    if (!this.myCheckinDate) {
      this.myCheckinDate = moment().add(1, 'd');
      this.myCheckinDate.set({
        hour: 12,
        minute: 0,
        second: 0,
      });
      this.checkinRevertValue = null;
    } else {
      this.checkinRevertValue = this.myCheckinDate.clone();
    }
    this.editCheckin = true;
  }

  public setCheckinDate(e: moment.Moment) {
    this.myCheckinDate.date(e.date());
  }

  public setCheckinTime(e) {
    let timeSplit = e.split(':');
    this.myCheckinDate.set({
      hour: timeSplit[0],
      minute: timeSplit[1],
    });
  }

  public revertCheckin() {
    this.editCheckin = false;
    this.myCheckinDate = this.checkinRevertValue;
    this.checkinRevertValue = null;
  }

  public checkExistingCheckinId() {
    return new Promise((resolve, reject) => {
      let planDay = moment(this.selectedPlan.created).diff(moment(), 'days');
      this.store.PlanTeamTemplate.readListPaged({
        plan: this.selectedPlan.id,
      }).subscribe(
        (tasks) => {
          // return true if plan has a checkin task that isn't past the current due time
          for (let i = 0; i < tasks.length; i++) {
            if (tasks[i].name === 'Patient Check-in') {
              let isAfterNow = moment(this.selectedPlan.created).add(tasks[i].start_on_day, 'days').isAfter(moment());
              if (isAfterNow) {
                resolve(tasks[i].id);
              }
            }
          }
          resolve(null);
        },
      );
    });
  }

  public saveCheckin() {
    if (!this.myCheckinDate) {
      return;
    }
    this.editCheckin = null;
    this.checkinRevertValue = null;
    this.checkExistingCheckinId().then((checkinId: any) => {
      let startOnDay = this.myCheckinDate.diff(moment(this.selectedPlan.created), 'days');
      let appearTime = this.myCheckinDate.format('HH:mm') + ':00';
      let dueTime = this.myCheckinDate.clone().add(4, 'hours').format('HH:mm') + ':00';
      if (checkinId) {
        this.store.PlanTeamTemplate.update(checkinId, {
          custom_start_on_day: startOnDay,
          custom_appear_time: appearTime,
          custom_due_time: dueTime,
        }, true).subscribe();
      } else {
        this.store.PlanTeamTemplate.create({
          custom_name: 'Patient Check-in',
          custom_start_on_day: startOnDay,
          custom_frequency: 'once',
          custom_repeat_amount: 1,
          custom_appear_time: appearTime,
          custom_due_time: dueTime,
          plan: this.selectedPlan.id,
        }).subscribe();
      }
    });
    this.employeeCTRoles.forEach((obj) => {
      let updateSub = this.store.CareTeamMember.update(obj.id, {
        next_checkin: this.myCheckinDate.toISOString()
      }, true).subscribe(
        (success) => {
          obj.next_checkin = success.next_checkin;
        },
        (err) => { },
        () => {
          // Recalculate next checkin in overview section
          // Get team member with closest check in date
          let sortedCT = this.sortTeamMembersByCheckin(this.allTeamMembers);
          if (sortedCT.length > 0) {
            this.nextCheckinTeamMember = sortedCT[0];
          }
          updateSub.unsubscribe();
        }
      );
    });
  }

  public toggleCollapsed() {
    let collapsedPatientHeaders = this.local.getObj('collapsed-patient-headers');
    let index = collapsedPatientHeaders.findIndex((obj) => obj === this.currentPage);
    if (index > 0) {
      collapsedPatientHeaders.splice(index, 1);
      this.local.setObj('collapsed-patient-headers', collapsedPatientHeaders);
      this.isCollapsed = false;
    } else {
      collapsedPatientHeaders.push(this.currentPage);
      this.local.setObj('collapsed-patient-headers', collapsedPatientHeaders);
      this.isCollapsed = true;
    }
  }

  @Input()
  public get currentPage() {
    return this._currentPage;
  }

  public set currentPage(value) {
    this._currentPage = value;
    let collapsedPatientHeaders = this.local.getObj('collapsed-patient-headers');
    if (!collapsedPatientHeaders) {
      this.local.setObj('collapsed-patient-headers', ['messaging', 'history']);
      if (this._currentPage !== 'messaging' || this._currentPage !== 'history')
        this.isCollapsed = false;
    }
    if (collapsedPatientHeaders.includes(this._currentPage)) {
      this.isCollapsed = true;
    }
  }
}
