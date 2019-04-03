import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import {
  sumBy as _sumBy,
  filter as _filter,
  flatten as _flatten,
  groupBy as _groupBy,
  uniqBy as _uniqBy,
} from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { PopoverOptions } from '../../../modules/popover';
import { RecordResultsComponent, GoalComponent, AddCTTaskComponent } from '../../../components';
import { AuthService, NavbarService, StoreService, UtilsService } from '../../../services';
import { GoalCommentsComponent } from './modals/goal-comments/goal-comments.component';

@Component({
  selector: 'app-patient-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss'],
})
export class PatientDetailsComponent implements OnDestroy, OnInit {

  public moment = moment;
  public objectKeys = Object.keys;

  public detailsLoaded = false;

  public user = null;
  public patient = null;
  public carePlan = null;
  public careTeamMembers = [];
  public isUsingMobile = true;

  public planGoals = [];
  public userTasks = [];
  public teamTasks = [];
  public patientTasks = [];
  public assessmentResults = [];
  public symptomResults = [];
  public vitalResults = [];
  public messageQueues = [];
  // Tracks what tasks, if any, are currently being updated.
  public updatingPatientTasks = [];
  public updatablePatientTaskTypes = ['patient_task', 'medication_task'];
  public patientTaskStatusChoices = ['done', 'missed'];
  public updatingAssessmentResults = [];
  public updatingSymptomResults = [];
  public updatingVitalResults = [];
  // Date picker options
  public selectedDate = moment();
  public showDate = false;
  public datePickerOptions: PopoverOptions = {
    relativeTop: '48px',
    relativeRight: '0px',
  };
  // Accordion open statuses
  public goalAccordionOpen = false;
  public userTasksOpen = false;
  public teamTasksOpen = false;
  public patientTasksOpen = false;
  public assessmentResultsOpen = false;
  public symptomResultsOpen = false;
  public vitalsResultsOpen = false;
  public messagesOpen = false;
  // Tooltip open statuses
  public goalUpdateTTOpen = false;
  public myTaskOccurTTOpen = false;
  public teamTaskOccurTTOpen = false;
  public patientTaskOccurTTOpen = false;
  public patientTaskAvgEngTTOpen = false;
  public patientTaskUpdateTTOpen = false;
  public symptomReportedTTOpen = false;
  public symptomVsPrevTTOpen = false;
  public symptomVsNextTTOpen = false;
  public symptomVsPlanTTOpen = false;
  public symptomUpdateTTOpen = false;
  public helpfulTTOpen = false;
  // Assessment and vital tooltips occur on multiple tables
  // so they are tied to the id of the vital or assessment
  public assmntOutcomeTTOpen: any = {};
  public assmntSatisfactionTTOpen: any = {};
  public assmntOccurTTOpen: any = {};
  public assmntVsPrevTTOpen: any = {};
  public assmntVsNextTTOpen: any = {};
  public assmntVsPlanTTOpen: any = {};
  public assmntUpdateTTOpen: any = {};
  public vitalReportedTTOpen: any = {};
  public vitalVsPrevTTOpen: any = {};
  public vitalVsNextTTOpen: any = {};
  public vitalVsPlanTTOpen: any = {};
  public vitalUpdateTTOpen: any = {};

  private queryParamsSub = null;
  private routeParamsSub = null;
  private authUserSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
    private nav: NavbarService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.queryParamsSub = this.route.queryParams.subscribe((params) => {
      if (params.show_my_tasks) {
        this.userTasksOpen = true;
      }
    });
    this.routeParamsSub = this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.authUserSub = this.auth.user$.subscribe((user) => {
        if (!user) {
          return;
        }
        this.user = user;
        this.getPatientProfile(params.patientId).then((patient: any) => {
          this.patient = patient;
          this.isUsingMobile = this.patient.is_using_mobile;
          this.nav.addRecentPatient(this.patient);
          this.getCarePlan(params.planId).then((carePlan: any) => {
        		this.carePlan = carePlan;
            this.getCareTeam(params.planId).then((teamMembers: any) => {
              this.careTeamMembers = teamMembers.filter((obj) => {
                return obj.employee_profile.user.id !== this.user.user.id;
              });
          		this.refetchAllTasks(this.selectedDate).then(() => {
                this.detailsLoaded = true;
              });
            });
        		let messageSub = this.store.InfoMessageQueue.readListPaged().subscribe(
        			(messageQueues) => {
        				return this.messageQueues = _filter(messageQueues, m => m.plan_template.id === carePlan.plan_template.id);
        			},
        			(err) => { },
        			() => messageSub.unsubscribe()
        		);
          });
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.queryParamsSub) {
      this.queryParamsSub.unsubscribe();
    }
    if (this.routeParamsSub) {
      this.routeParamsSub.unsubscribe();
    }
    if(this.authUserSub) {
      this.authUserSub.unsubscribe();
    }
  }

  public getPatientProfile(patientId) {
    let promise = new Promise((resolve, reject) => {
      let patientSub = this.store.PatientProfile.read(patientId).subscribe(
        (patient) => resolve(patient),
        (err) => reject(err),
        () => {
          patientSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getCarePlan(planId) {
    let promise = new Promise((resolve, reject) => {
      let planSub = this.store.CarePlan.read(planId).subscribe(
        (plan) => resolve(plan),
        (err) => reject(err),
        () => {
          planSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getCareTeam(planId) {
    let promise = new Promise((resolve, reject) => {
      let teamSub = this.store.CarePlan.detailRoute('get', this.carePlan.id, 'care_team_members', {}, {}).subscribe(
        (teamMembers: any) => resolve(teamMembers),
        (err) => reject(err),
        () => {
          teamSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getGoals(patient, planTemplate, start, end) {
    let promise = new Promise((resolve, reject) => {
      let goalsSub = this.store.Goal.readListPaged({
        plan__patient: patient,
        goal_template__plan_template: planTemplate,
        start_on_datetime__lte: end,
      }).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          goalsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getUserTasks(planTemplate, date) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.User.detailRoute('get', this.user.user.id, 'tasks', {}, {
        plan_template: planTemplate,
        plan: this.carePlan.id,
        date: date,
        exclude_done: false,
      }).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getTeamMemberTasks(teamMember, planTemplate, date) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.User.detailRoute('get', teamMember.employee_profile.user.id, 'tasks', {}, {
        plan_template: planTemplate,
        plan: this.carePlan.id,
        date: date,
        exclude_done: false,
      }).subscribe(
        (res: any) => {
          res.tasks.map((obj) => {
            obj['responsible_person'] = teamMember;
          });
          resolve(res);
        },
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getAllTeamMemberTasks(planTemplate, date) {
    let promises = _uniqBy(this.careTeamMembers, (obj) => obj.employee_profile.id)
      .map((obj) => this.getTeamMemberTasks(obj, planTemplate, date));
    return Promise.all(promises);
  }

  public getPatientTasks(patient, planTemplate, date) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.User.detailRoute('get', patient, 'tasks', {}, {
        plan_template: planTemplate,
        date: date,
        exclude_done: false,
      }).subscribe(
        (res: any) => resolve(res),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getAssessmentResults(plan, date) {
    let promise = new Promise((resolve, reject) => {
      let resultsSub = this.store.CarePlan.detailRoute('get', plan.id, 'assessment_results', {}, {
        date: date
      }).subscribe(
        (assessmentResults) => resolve(assessmentResults),
        (err) => reject(err),
        () => {
          resultsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getSymptomResults(plan, date) {
    let promise = new Promise((resolve, reject) => {
      let symptomsSub = this.store.CarePlan.detailRoute('get', plan.id, 'symptoms', {}, {
        date: date
      }).subscribe(
        (symptoms) => resolve(symptoms),
        (err) => reject(err),
        () => {
          symptomsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getVitalResults(plan, date) {
    let promise = new Promise((resolve, reject) => {
      let vitalsSub = this.store.CarePlan.detailRoute('get', plan.id, 'vitals', {}, {
        date: date
      }).subscribe(
        (vitals) => resolve(vitals),
        (err) => reject(err),
        () => {
          vitalsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getCareMessages(planTemplate, start, end) {
    let promise = new Promise((resolve, reject) => {
      let messagesSub = this.store.InfoMessage.readListPaged({
        queue__plan_template: planTemplate,
        modified__lte: end,
        modified__gte: start,
      }).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          messagesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public setAllUpdatable() {
    this.updatingPatientTasks = this.patientTasks.filter((obj) => this.isPatientTaskUpdatable(obj));
    this.assessmentResults.forEach((assessment) => {
      this.updatingAssessmentResults = this.updatingAssessmentResults.concat(assessment.questions);
    });
    this.updatingSymptomResults = this.symptomResults.concat();
    this.vitalResults.forEach((vital) => {
      this.updatingVitalResults = this.updatingVitalResults.concat(vital.questions);
    });
  }

  public toggleUsingMobile() {
    this.isUsingMobile = !this.isUsingMobile;
    let updatePatientSub = this.store.PatientProfile.update(this.patient.id, {
      is_using_mobile: this.isUsingMobile
    }, true).subscribe(
      (data) => {},
      (err) => {},
      () => {
        if (!this.isUsingMobile) {
          this.setAllUpdatable();
        }
        updatePatientSub.unsubscribe();
      }
    );
  }

  public refetchAllTasks(dateAsMoment) {
    if (!this.patient || !this.carePlan) {
      return;
    }
    this.detailsLoaded = false;
    let startOfDay = dateAsMoment.startOf('day').utc().toISOString();
    let endOfDay = dateAsMoment.endOf('day').utc().toISOString();
    let formattedDate = dateAsMoment.utc().format('YYYY-MM-DD');
    let goalsPromise = this.getGoals(this.patient.id, this.carePlan.plan_template.id, startOfDay, endOfDay).then((goals: any) => {
      this.planGoals = goals;
    });
    let userTasksPromise = this.getUserTasks(this.carePlan.plan_template.id, formattedDate).then((tasks: any) => {
      this.userTasks = tasks.tasks.filter((obj) => obj.patient && obj.patient.id === this.patient.id);
    });
    this.teamTasks = [];
    let teamTasksPromise = this.getAllTeamMemberTasks(this.carePlan.plan_template.id, formattedDate).then((teamMemberTasks: any) => {
      teamMemberTasks.forEach((tasks) => {
        this.teamTasks = this.teamTasks.concat(tasks.tasks.filter((obj) => obj.patient && obj.patient.id === this.patient.id));
      });
    });
    let patientTasksPromise = this.getPatientTasks(this.patient.user.id, this.carePlan.plan_template.id, formattedDate).then((tasks: any) => {
      this.patientTasks = tasks.tasks;
      if (!this.isUsingMobile) {
        this.updatingPatientTasks = this.patientTasks.filter((obj) => this.isPatientTaskUpdatable(obj));
      }
    });
    this.updatingAssessmentResults = [];
    let assessmentsPromise = this.getAssessmentResults(this.carePlan, formattedDate).then((assessments: any) => {
      this.assessmentResults = assessments.results;
      if (!this.isUsingMobile) {
        this.assessmentResults.forEach((assessment) => {
          this.updatingAssessmentResults = this.updatingAssessmentResults.concat(assessment.questions);
        });
      }
    });
    let symptomsPromise = this.getSymptomResults(this.carePlan, formattedDate).then((symptoms: any) => {
      this.symptomResults = symptoms.results;
      if (!this.isUsingMobile) {
        this.updatingSymptomResults = this.symptomResults.concat();
      }
    });
    let vitalResultsPromise = this.getVitalResults(this.carePlan, formattedDate).then((vitals: any) => {
      this.vitalResults = vitals.results;
      if (!this.isUsingMobile) {
        this.vitalResults.forEach((vital) => {
          this.updatingVitalResults = this.updatingVitalResults.concat(vital.questions);
        });
      }
    });
    return Promise.all([goalsPromise, userTasksPromise, teamTasksPromise, patientTasksPromise, assessmentsPromise, symptomsPromise, vitalResultsPromise]);
  }

  public setSelectedDay(dateAsMoment) {
    if (!dateAsMoment || !this.patient || !this.carePlan) {
      return;
    }
    this.selectedDate = dateAsMoment;
    this.refetchAllTasks(dateAsMoment).then(() => {
      this.detailsLoaded = true;
    });
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

  public goalsAverage() {
    if (!this.planGoals || this.planGoals.length === 0) {
      return 0;
    }
    let totalSum = _sumBy(this.planGoals, (obj) => {
      return obj.latest_progress ? obj.latest_progress.rating : 0;
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
      return obj.state === 'done';
    }).length;
  }

  public userTasksPercentage() {
    return Math.round((this.completedUserTasks() / this.userTasks.length) * 100);
  }

  public completedTeamTasks() {
    return this.teamTasks.filter((obj) => {
      return obj.state === 'done';
    }).length;
  }

  public teamTasksPercentage() {
    return Math.round((this.completedTeamTasks() / this.teamTasks.length) * 100);
  }

  public completedPatientTasks() {
    return this.patientTasks.filter((obj) => {
      return obj.state === 'done';
    }).length;
  }

  public patientTasksPercentage() {
    return Math.round((this.completedPatientTasks() / this.patientTasks.length) * 100);
  }

  public totalOutcomeQuestions() {
    let outcomeAssessments = this.assessmentResults.filter((assessment) => assessment.tracks_outcome);
    let questionsCount = _sumBy(outcomeAssessments, (assessment) => assessment.questions.length);
    return questionsCount;
  }

  public totalSatisfactionQuestions() {
    let satisfactionAssessments = this.assessmentResults.filter((assessment) => assessment.tracks_satisfaction);
    let questionsCount = _sumBy(satisfactionAssessments, (assessment) => assessment.questions.length);
    return questionsCount;
  }

  public averageOutcomeScore() {
    let outcomeAssessments = this.assessmentResults.filter((assessment) => assessment.tracks_outcome);
    let totalSum = _sumBy(outcomeAssessments, (assessment) => {
      return _sumBy(assessment.questions, (question) => {
        return question.rating;
      });
    });
    let average = (totalSum / this.totalOutcomeQuestions()) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageOutcomePercentage() {
    return Math.round((this.averageOutcomeScore() / 5.0) * 100);
  }

  public averageSatisfactionScore() {
    let satisfactionAssessments = this.assessmentResults.filter((assessment) => assessment.tracks_satisfaction);
    let totalSum = _sumBy(satisfactionAssessments, (assessment) => {
      return _sumBy(assessment.questions, (question) => {
        return question.rating;
      });
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
    let totalSum = _sumBy(this.symptomResults, (obj) => obj.rating.rating);
    let average = (totalSum / this.symptomResults.length) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageSymptomPercent() {
    return Math.round((this.averageSymptomRating() / 5.0) * 100);
  }

  public ratingPercentage(rating) {
    return (rating / 5.0) * 100;
  }

  public addGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: false,
      data: {
        creatingTemplate: true,
      },
      width: '512px',
    }).subscribe(
      (results) => {
        if (results !== null) {
          let createSub = this.store.GoalTemplate.create({
            name: results.name,
            plan_template: this.carePlan.plan_template.id,
            description: results.description,
            focus: results.focus,
            duration_weeks: results.duration_weeks,
            start_on_day: results.start_on_day,
          }).subscribe(
            (goal) => {
              this.refetchAllTasks(this.selectedDate).then(() => {
                this.detailsLoaded = true;
              });
            },
            (err) => {},
            () => {
              createSub.unsubscribe();
            }
          );
        }
      }
    );
  }

  public updateGoal(goal) {
    let goalIndex = this.planGoals.findIndex((obj) => {
      return obj.id === goal.id;
    });
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        update: true,
        patientName: `${this.patient.user.first_name} ${this.patient.user.last_name}`,
        goal: goal,
      },
      width: '512px',
    }).subscribe((results) => {
      if (!results) {
        return;
      }
      // create goal progress instance
      this.store.GoalProgress.create({
        goal: goal.id,
        rating: results.progress,
      }).subscribe((newProgress) => {
        // TODO: Update individual goal, rather than goal template for all of this plan type.
        let updateSub = this.store.GoalTemplate.update(goal.goal_template.id, {
          name: results.name,
          description: results.description,
          focus: results.focus,
          duration_weeks: results.duration_weeks,
          start_on_day: results.start_on_day,
        }, true).subscribe(
          (updatedGoal) => {
            this.planGoals[goalIndex].goal_template = updatedGoal;
            this.planGoals[goalIndex].latest_progress = newProgress;
          },
          (err) => {},
          () => {
            updateSub.unsubscribe();
          }
        );
      });
    });
  }

  public openGoalComments(goal) {
    this.modals.open(GoalCommentsComponent, {
      closeDisabled: false,
      data: {
        user: this.user.user,
        patient: this.patient,
        goal: goal,
      },
      width: '512px',
    }).subscribe((res) => {
      console.log(res);
    });
  }

  public openRecordResults(task) {
    this.store.TeamTask.read(task.id).subscribe((taskObj) => {
      this.modals.open(RecordResultsComponent, {
        closeDisabled: false,
        data: {
          patient: this.patient,
          carePlan: this.carePlan,
          teamTaskId: taskObj.team_task_template,
          taskEditable: false,
          totalMinutes: null,
          with: null,
          syncToEHR: false,
          notes: '',
          patientEngagement: null,
        },
        width: '512px',
      }).subscribe((results) => {
        if (!results) {
          return;
        }
        this.store.BilledActivity.create({
          plan: this.carePlan.id,
          activity_datetime: results.date,
          members: [
            this.user.id,
          ].concat(results.with),
          team_task_template: results.teamTaskTemplate,
          patient_included: results.patientIncluded,
          sync_to_ehr: results.syncToEHR,
          added_by: this.user.id,
          notes: results.notes,
          time_spent: results.totalMinutes,
        }).subscribe((res) => {
          this.store.TeamTask.update(task.id, {
            status: 'done',
          }, true).subscribe((res) => {
            task.state = 'done';
          });
        });
      });
    });
  }

  public addCTTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      width: '384px',
    }).subscribe(() => {});
  }

  public isUpdatingPatientTask(task) {
    return this.updatingPatientTasks.findIndex((obj) => obj.id === task.id) >= 0;
  }

  public isPatientTaskUpdatable(task) {
    return this.updatablePatientTaskTypes.includes(task.type);
  }

  public clickUpdatePatientTask(task) {
    this.updatingPatientTasks.push(task);
  }

  public clickSavePatientTask(task) {
    let storeModel = null;
    if (task.type === 'patient_task') {
      storeModel = this.store.PatientTask;
    } else if (task.type === 'medication_task') {
      storeModel = this.store.MedicationTask;
    }
    if (!storeModel) {
      return;
    }
    let updateSub = storeModel.update(task.id, {
      status: task.state,
    }, true).subscribe(
      (res) => {
        let taskUpdateListIndex = this.updatingPatientTasks.findIndex((obj) => obj.id === task.id);
        this.updatingPatientTasks.splice(taskUpdateListIndex, 1);
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public isUpdatingAssessmentResult(result) {
    return this.updatingAssessmentResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateAssessmentResult(result) {
    this.updatingAssessmentResults.push(result);
  }

  public clickSaveAssessmentResult(result) {
    let updateSub = this.store.AssessmentResponse.update(result.id, {
      rating: result.rating,
    }, true).subscribe(
      (res) => {
        let resultsListIndex = this.updatingAssessmentResults.findIndex((obj) => obj.id === result.id);
        this.updatingAssessmentResults.splice(resultsListIndex, 1);
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public isUpdatingSymptomResult(result) {
    return this.updatingSymptomResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateSymptomResult(result) {
    this.updatingSymptomResults.push(result);
  }

  public clickSaveSymptomResult(result) {
    let updateSub = this.store.SymptomRating.update(result.rating.id, {
      rating: result.rating.rating,
    }, true).subscribe(
      (res) => {
        let resultsListIndex = this.updatingSymptomResults.findIndex((obj) => obj.id === result.id);
        this.updatingSymptomResults.splice(resultsListIndex, 1);
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public isUpdatingVitalResult(result) {
    return this.updatingVitalResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateVitalResult(result) {
    this.updatingVitalResults.push(result);
  }

  public clickSaveVitalResult(result) {
    let updateSub = this.store.VitalResponse.update(result.id, {
      response: result.answer,
    }, true).subscribe(
      (res) => {
        let resultsListIndex = this.updatingVitalResults.findIndex((obj) => obj.id === result.id);
        this.updatingVitalResults.splice(resultsListIndex, 1);
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public formatTaskType(type: string) {
    return type.toLowerCase().replace('_task', '').replace('patient', 'task');
  }

  public floor(num) {
    return Math.floor(num);
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
