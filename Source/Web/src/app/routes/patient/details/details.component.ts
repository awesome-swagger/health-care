import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import {
  sumBy as _sumBy,
  filter as _filter,
  flatten as _flatten,
} from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent, GoalComponent, AddCTTaskComponent } from '../../../components';
import { NavbarService, StoreService, UtilsService } from '../../../services';
import { GoalCommentsComponent } from './modals/goal-comments/goal-comments.component';
import { DetailsMockData } from './detailsData';

@Component({
  selector: 'app-patient-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss'],
})
export class PatientDetailsComponent implements OnDestroy, OnInit {

  public moment = moment;

  private mockData = new DetailsMockData();

  public user = null;
  public patient = null;
  public carePlan = null;
  public isUsingMobile = true;
  public selectedDate = moment();
  public planGoals = [];
  public userTasks = [];
  public teamTasks = [];
  public patientTasks = [];
  public updatingPatientTasks = [];
  public patientTaskStatusChoices = ['done', 'missed', 'late'];
  public assessmentResults = [];
  public updatingAssessmentResults = [];
  public symptomResults = [];
  public updatingSymptomResults = [];
  public vitalResults = [];
  public updatingVitalResults = [];
  public messageQueues = [];

  public showDate = false;
  public goalAccordionOpen = false;
  public userTasksOpen = false;
  public teamTasksOpen = false;
  public patientTasksOpen = false;
  public assessmentResultsOpen = true;
  public symptomResultsOpen = false;
  public vitalsResultsOpen = false;
  public messagesOpen = false;
  public tooltipPD200Open;
  public tooltipPD300Open;
  public tooltipPD400Open;
  public tooltipPD401Open;
  public tooltipPD402Open;
  public tooltipPD500Open;
  public tooltipPD501Open;
  public tooltipPD502Open;
  public tooltipPD503Open;
  public tooltipPD504Open;
  public tooltipPD505Open;
  public tooltipPD506Open;
  public tooltipPD507Open;
  public tooltipPD508Open;
  public tooltipPD509Open;
  public tooltipPD510Open;
  public tooltipPD511Open;
  public tooltipPD512Open;
  public tooltipPD513Open;
  public tooltipPD600Open;
  public tooltipPD601Open;
  public tooltipPD602Open;
  public tooltipPD603Open;
  public tooltipPD700Open;
  public tooltipPD701Open;
  public tooltipPD702Open;
  public tooltipPD703Open;
  public tooltipPD800Open;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
          if (this.isUsingMobile) {
            this.updatingPatientTasks = this.getPatientTasks();
            this.updatingAssessmentResults = _flatten(this.getAssessmentResults().map((results) => results.questions));
            this.updatingSymptomResults = this.getSymptomResults();
            this.updatingVitalResults = _flatten(this.getVitalResults().map((results) => results.questions))
          }
        },
        (err) => {},
        () => {},
      );
      let carePlanSub = this.store.CarePlan.read(params.planId).subscribe(
        (carePlan: any) => {
          this.carePlan = carePlan;
          let messageSub = this.store.InfoMessageQueue.readListPaged().subscribe(
            (messageQueues) => {
              return this.messageQueues = _filter(messageQueues, m => m.plan_template.id === carePlan.plan_template.id);
            },
            err => {},
            () => messageSub.unsubscribe()
          );
        },
        err => {},
        () => carePlanSub.unsubscribe()
      );
    });
  }

  public ngOnDestroy() { }

  public getGoals() {
    return this.mockData.goals;
  }

  public getUserTasks(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.userTasks.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public getTeamTasks(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.careTeamTasks.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public getPatientTasks(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.patientTasks.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public getAssessmentResults(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.assessmentResults.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public getSymptomResults(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.symptomResults.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public getVitalResults(dateAsMoment = null) {
    if (!dateAsMoment) {
      dateAsMoment = moment();
    }
    return this.mockData.vitalResults.filter((obj) => {
      return dateAsMoment.isSame(obj.date, 'day');
    });
  }

  public goalsAverage() {
    if (!this.planGoals) {
      return 0;
    }
    let totalSum = _sumBy(this.planGoals, (obj) => {
      return obj.progress;
    });
    let average = (totalSum / this.planGoals.length) + .0;
    return Math.round(average * 10) / 10;
  }

  public goalsPercentage() {
    return Math.round((this.goalsAverage() / 5.0) * 100);
  }

  public goalPercentage(progress) {
    return (progress / 5.0) * 100;
  }

  public completedUserTasks() {
    return this.userTasks.filter((obj) => {
      return obj.status === 'done';
    }).length;
  }

  public userTasksPercentage() {
    return Math.round((this.completedUserTasks() / this.userTasks.length) * 100);
  }

  public completedTeamTasks() {
    return this.teamTasks.filter((obj) => {
      return obj.status === 'done';
    }).length;
  }

  public teamTasksPercentage() {
    return Math.round((this.completedTeamTasks() / this.teamTasks.length) * 100);
  }

  public completedPatientTasks() {
    return this.patientTasks.filter((obj) => {
      return obj.status === 'done';
    }).length;
  }

  public patientTasksPercentage() {
    return Math.round((this.completedPatientTasks() / this.patientTasks.length) * 100);
  }

  public outcomeAsssessments() {
    return this.assessmentResults.filter((obj) => obj.tracksOutcome);
  }

  public satisfactionAssessments() {
    return this.assessmentResults.filter((obj) => obj.tracksSatisfaction);
  }

  public totalOutcomeQuestions() {
    return _sumBy(this.outcomeAsssessments(), (obj) => obj.questions.length);
  }

  public totalSatisfactionQuestions() {
    return _sumBy(this.satisfactionAssessments(), (obj) => obj.questions.length);
  }

  public averageOutcomeScore() {
    let totalSum = _sumBy(this.outcomeAsssessments(), (obj) => {
      return _sumBy(obj.questions, (question) => question.outcome);
    });
    let average = (totalSum / this.totalOutcomeQuestions()) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageOutcomePercentage() {
    return Math.round((this.averageOutcomeScore() / 5.0) * 100);
  }

  public averageSatisfactionScore() {
    let totalSum = _sumBy(this.satisfactionAssessments(), (obj) => {
      return _sumBy(obj.questions, (question) => question.outcome);
    });
    let average = (totalSum / this.totalSatisfactionQuestions()) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageSatisfactionPercentage() {
    return Math.round((this.averageSatisfactionScore() / 5.0) * 100);
  }

  public outcomePercentage(outcome) {
    return (outcome / 5.0) * 100;
  }

  public averageSymptomRating() {
    let totalSum = _sumBy(this.symptomResults, (obj) => obj.rating);
    let average = (totalSum / this.symptomResults.length) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageSymptomPercent() {
    return Math.round((this.averageSymptomRating() / 5.0) * 100);
  }

  public ratingPercentage(rating) {
    return (rating / 5.0) * 100;
  }

  public floor(num) {
    return Math.floor(num);
  }

  public format24Hour(time) {
    let timeParse = time.split(":");
    let suffix = (timeParse[0] >= 12)? 'PM' : 'AM';
    let hours = (parseInt(timeParse[0]) > 12) ? parseInt(timeParse[0]) -12 : parseInt(timeParse[0]);
    hours = (hours == 0) ? 12 : hours;
    return `${hours}:${timeParse[1]} ${suffix}`;
  }

  public openRecordResults(task) {
    this.modals.open(RecordResultsComponent, {
     closeDisabled: true,
     data: {
       patient: this.patient,
       carePlan: this.carePlan,
       tasks: this.userTasks,
       task: task.id,
       totalMinutes: null,
       teamMembers: this.mockData.employees,
       with: null,
       syncToEHR: false,
       notes: '',
       patientEngagement: null,
     },
     width: '512px',
   }).subscribe((res) => {
     task.status = 'done';
   });
  }

  public addGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public updateGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        update: true,
        patientName: `${this.patient.user.first_name} ${this.patient.user.last_name}`
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public openGoalComments() {
    this.modals.open(GoalCommentsComponent, {
      closeDisabled: false,
      width: '512px',
    }).subscribe(() => {});
  }

  public addCTTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public nextDate() {
    this.setSelectedDay(this.selectedDate.add(1, 'days'));
  }

  public prevDate() {
    this.setSelectedDay(this.selectedDate.add(-1, 'days'));
  }

  public isViewingToday() {
    return this.selectedDate.isSame(moment().format('YYYY-MM-DD'), 'day');
  }

  public isViewingTomorrow() {
    return this.selectedDate.isSame(moment().add(1, 'days').format('YYYY-MM-DD'), 'day');
  }

  public isViewingYesterday() {
    return this.selectedDate.isSame(moment().add(-1, 'days').format('YYYY-MM-DD'), 'day');
  }

  public tableHeaderDate() {
    if (this.isViewingToday()) {
      return 'Today';
    } else if (this.isViewingYesterday()) {
      return 'Yesterday';
    } else if (this.isViewingTomorrow()) {
      return 'Tomorrow';
    } else {
      return this.selectedDate.format('MMM DD');
    }
  }

  public setSelectedDay(moment) {
    this.selectedDate = moment;
    this.planGoals = this.getGoals();
    this.userTasks = this.getUserTasks(moment);
    this.teamTasks = this.getTeamTasks(moment);
    this.patientTasks = this.getPatientTasks(moment);
    this.assessmentResults = this.getAssessmentResults(moment);
    this.symptomResults = this.getSymptomResults(moment);
    this.vitalResults = this.getVitalResults(moment);
  }

  public isUpdatingPatientTask(task) {
    return this.updatingPatientTasks.findIndex((obj) => obj.id === task.id) >= 0;
  }

  public clickUpdatePatientTask(task) {
    this.updatingPatientTasks.push(task);
  }

  public clickSavePatientTask(task) {
    let taskUpdateListIndex = this.updatingPatientTasks.findIndex((obj) => obj.id === task.id);
    this.updatingPatientTasks.splice(taskUpdateListIndex, 1);
  }

  public isUpdatingAssessmentResult(result) {
    return this.updatingAssessmentResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateAssessmentResult(result) {
    this.updatingAssessmentResults.push(result);
  }

  public clickSaveAssessmentResult(result) {
    let resultsListIndex = this.updatingAssessmentResults.findIndex((obj) => obj.id === result.id);
    this.updatingAssessmentResults.splice(resultsListIndex, 1);
  }

  public isUpdatingSymptomResult(result) {
    return this.updatingSymptomResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateSymptomResult(result) {
    this.updatingSymptomResults.push(result);
  }

  public clickSaveSymptomResult(result) {
    let resultsListIndex = this.updatingSymptomResults.findIndex((obj) => obj.id === result.id);
    this.updatingSymptomResults.splice(resultsListIndex, 1);
  }

  public formatVitalQuestionType(type: string) {
    if (!type) {
      return '';
    }
    if (type === 'boolean') {
      return 'True/False';
    } else if (type == 'float') {
      return 'Decimal';
    } else if (type === 'string') {
      return 'String';
    } else {
      return type;
    }
  }

  public routeToMessaging() {
    this.router.navigate(['/patient', this.patient.id, 'messaging', this.carePlan.id]);
  }
}
