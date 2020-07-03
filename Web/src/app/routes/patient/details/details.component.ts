import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import {
  sumBy as _sumBy,
  filter as _filter,
  flatten as _flatten,
  flattenDeep as _flattenDeep,
  groupBy as _groupBy,
  uniqBy as _uniqBy,
  intersection as _intersection,
} from 'lodash';
import { ModalService } from '../../../modules/modals';
import { PopoverOptions } from '../../../modules/popover';
import { RecordResultsComponent, GoalComponent, AddCTTaskComponent, EditTaskComponent } from '../../../components';
import { AuthService, NavbarService, StoreService, TimeTrackerService, UtilsService } from '../../../services';
import { GoalCommentsComponent } from './modals/goal-comments/goal-comments.component';
import { Observable } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { Utils } from '../../../utils';

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
  public helpfulTTOpen: { [key: string]: boolean } = {};
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
    private timer: TimeTrackerService,
    private nav: NavbarService,
    public utils: UtilsService,
  ) {
    // Nothing yet
  }

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
            this.timer.startTimer(this.user, this.carePlan);
            this.getCareTeam(params.planId).then((teamMembers: any) => {
              this.careTeamMembers = teamMembers;
              this.refetchAllTasks(this.selectedDate).then(() => {
                this.assignRatingsToQuestions();
                this.detailsLoaded = true;
              }).catch(err => Utils.logError('ngOnInit.this.refetchAllTasks.promise.catch', err, user));
            });
            let messageSub = this.store.InfoMessageQueue.readListPaged().subscribe(
              (messageQueues) => {
                return this.messageQueues = _filter(messageQueues, m => m.plan_template.id === carePlan.plan_template.id);
              },
              (err) => Utils.logError('Failed to load message queue', err, user),
              () => messageSub.unsubscribe()
            );
          }).catch(err => Utils.logError('ngOnInit.this.getCarePlan.promise.catch', err, user));
        });
      });
    });
  }

  public ngOnDestroy() {
    this.timer.stopTimer();
    if (this.queryParamsSub) {
      this.queryParamsSub.unsubscribe();
    }
    if (this.routeParamsSub) {
      this.routeParamsSub.unsubscribe();
    }
    if (this.authUserSub) {
      this.authUserSub.unsubscribe();
    }
  }

  /***************************************************************************
  * API Promises
  ****************************************************************************/

  private apiPromise<T>(apiAction: () => Observable<T>): Promise<T> {
    const actionName = apiAction.toString();
    const caller = actionName.substring(actionName.indexOf('_this.') + 1);

    const promise = new Promise<T>((resolve, reject) => {
      const result = apiAction().subscribe(
        (data: T) => resolve(data),
        (err: HttpErrorResponse | Error) => {
          Utils.logWarn(`Failed to complete call: "${caller.substring(0, caller.indexOf('('))}"`, err);
          resolve(null);
          //reject(err);
        },
        () => result.unsubscribe()
      );
    });

    return promise;
  }

  public getPatientProfile(patientId: string | number): Promise<any> {
    return this.apiPromise(() => this.store.PatientProfile.read(patientId));
  }

  public getCarePlan(planId: string | number): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.read(planId));
  }

  public getCareTeam(planId: string | number): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.detailRoute('get', this.carePlan.id, 'care_team_members', {}, {}));
  }

  public getGoals(patient, planTemplate, start, end): Promise<any> {
    const params = {
      plan__patient: patient,
      goal_template__plan_template: planTemplate,
      start_on_datetime__lte: end,
    };

    return this.apiPromise(() => this.store.Goal.readListPaged(params));
  }

  public getAllTeamTasks(plan, date): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.detailRoute('get', plan.id, 'team_tasks_for_today', {}, { date: date }));
  }

  public getPatientTasks(patient, planTemplate, date): Promise<any> {
    const params = {
      plan_template: planTemplate,
      date: date,
      exclude_done: false,
    };

    return this.apiPromise(() => this.store.User.detailRoute('get', patient, 'tasks', {}, params));
  }

  public getAssessmentResults(plan, date): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.detailRoute('get', plan.id, 'assessment_results', {}, { date: date }));
  }

  public getSymptomResults(plan, date): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.detailRoute('get', plan.id, 'symptoms', {}, { date: date }));
  }

  public getVitalResults(plan, date): Promise<any> {
    return this.apiPromise(() => this.store.CarePlan.detailRoute('get', plan.id, 'vitals', {}, { date: date }));
  }

  public getCareMessages(planTemplate, start, end): Promise<any> {
    const params = {
      queue__plan_template: planTemplate,
      modified__lte: end,
      modified__gte: start,
    };

    return this.apiPromise(() => this.store.InfoMessage.readListPaged(params));
  }

  public refetchTeamTasks(formattedDate: string): Promise<any> {
    const teamTasksPromise = this.getAllTeamTasks(this.carePlan, formattedDate)
      .then((tasks: any) => {
        tasks = tasks || [];
        const userRoles = this.careTeamMembers.filter((teamMember) => teamMember.employee_profile.id === this.user.id);
        const userRoleIds = userRoles.filter((userRole) => userRole.role).map((userRole) => userRole.role.id);
        const userHasManagerRole = userRoles.filter((userRole) => userRole.is_manager === true).length > 0;
        this.userTasks = tasks.filter((task) => {
          if (!userRoles || userRoles.length === 0) {
            return false;
          }

          const taskRoles = task.roles.map((role) => role.id);
          if (!taskRoles || taskRoles.length === 0) {
            if (task.is_manager_task && userHasManagerRole) {
              return true;
            }
          } else {
            if (_intersection(userRoleIds, taskRoles).length > 0) {
              return true;
            }
          }

          return false;
        });

        this.teamTasks = tasks.filter((task) => !this.userTasks.includes(task));
        this.teamTasks.forEach((task) => task.responsible_person = this.getResponsiblePersonField(task));
      })
      .catch(err => Utils.logWarn('refetchTeamTasks.promise.catch', err));

    return teamTasksPromise;
  }

  public getResponsiblePersonField(task: { is_manager_task: boolean, roles: Array<{ id: number }> }): { is_manager_task: boolean, roles: Array<{ id: number }> } {
    const taskRoles = task.roles.map((role) => role.id);
    if (task.is_manager_task) {
      const teamManagers = this.careTeamMembers.filter((teamMember) => teamMember.is_manager);

      if (teamManagers.length > 0) {
        return teamManagers[0];
      }

      return null;
    }

    if (taskRoles.length > 0) {
      const qualifiedMembers = this.careTeamMembers.filter((teamMember) => teamMember.role && taskRoles.includes(teamMember.role.id));
      if (qualifiedMembers.length > 0) {
        return qualifiedMembers[0];
      }

      return null;
    }

    return null;
  }

  public refetchPatientTasks(formattedDate) {
    let patientTasksPromise = this.getPatientTasks(this.patient.user.id, this.carePlan.plan_template.id, formattedDate).then((tasks: any) => {
      this.patientTasks = tasks.tasks;
    });
    return patientTasksPromise;
  }

  public assignRatingsToQuestions() {
    this.assessmentResults.forEach((assessment) => {
      assessment.questions.forEach((question) => {
        let response = this.assessmentQuestionResponse(assessment, question);
        if (response) {
          question.response = response;
        } else {
          question.response = {
            question: question.prompt,
            question_id: question.id,
            rating: 0,
            occurrence: 'n/a',
            behavior: 'n/a',
            behavior_against_care_plan: 'n/a'
          };
        }
      });
    });
    this.symptomResults.forEach((symptom) => {
      symptom.default_symptoms.forEach((def) => {
        let rating = this.defaultSymptomRating(symptom, def);
        if (rating) {
          def.rating = rating;
        } else {
          def.rating = {
            rating: 0,
            behavior: 'n/a',
            behavior_against_care_plan: 'n/a',
            symptom: def,
          };
        }
      });
    });
    this.vitalResults.forEach((vital) => {
      vital.questions.forEach((question) => {
        let response = this.vitalQuestionResponse(vital, question);
        if (response) {
          question.response = response;
        } else {
          question.response = {
            question: question.prompt,
            question_id: question.id,
            answer: null,
            answer_type: question.answer_type,
            occurrence: 'n/a',
            behavior: 'n/a',
            behavior_against_care_plan: 'n/a'
          };
        }
      });
    });
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
    let teamTasksPromise = this.refetchTeamTasks(formattedDate).then();
    // let userTasksPromise = this.getUserTasks(this.carePlan.plan_template.id, formattedDate).then((tasks: any) => {
    //   this.userTasks = tasks.tasks.filter((obj) => obj.patient && obj.patient.id === this.patient.id);
    // });
    // this.teamTasks = [];
    // let teamTasksPromise = this.getAllTeamMemberTasks(this.carePlan.plan_template.id, formattedDate).then((teamMemberTasks: any) => {
    //   teamMemberTasks.forEach((tasks) => {
    //     this.teamTasks = this.teamTasks.concat(tasks.tasks.filter((obj) => obj.patient && obj.patient.id === this.patient.id));
    //   });
    // });
    let patientTasksPromise = this.refetchPatientTasks(formattedDate).then(() => {
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
    return Promise.all([goalsPromise, teamTasksPromise, patientTasksPromise, assessmentsPromise, symptomsPromise, vitalResultsPromise]);
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
      (data) => { },
      (err) => { },
      () => {
        if (!this.isUsingMobile) {
          this.setAllUpdatable();
        }
        updatePatientSub.unsubscribe();
      }
    );
  }

  public setSelectedDay(dateAsMoment) {
    if (!dateAsMoment || !this.patient || !this.carePlan) {
      return;
    }
    this.selectedDate = dateAsMoment;
    this.refetchAllTasks(dateAsMoment).then(() => {
      this.assignRatingsToQuestions();
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
      return _sumBy(assessment.responses, (response) => {
        return response.rating;
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
      return _sumBy(assessment.responses, (response) => {
        return response.rating;
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
    if (!this.symptomResults) {
      return 0;
    }
    let allRatings = _flattenDeep(this.symptomResults.map((obj) => { return obj.ratings }));
    if (allRatings.length === 0) {
      return 0;
    }
    let totalSum = _sumBy(allRatings, (obj) => { return obj.rating });
    let average = (totalSum / allRatings.length) + .0;
    return Math.round(average * 10) / 10;
  }

  public averageSymptomPercent() {
    return Math.round((this.averageSymptomRating() / 5.0) * 100);
  }

  public ratingPercentage(rating) {
    return (rating / 5.0) * 100;
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
      (err) => { },
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public assessmentQuestionResponse(assessment, question) {
    let res = assessment.responses.find((response) => {
      return response.question_id === question.id;
    });
    return res;
  }

  public isUpdatingAssessmentResult(question) {
    return this.updatingAssessmentResults.findIndex((obj) => obj.id === question.id) >= 0;
  }

  public clickUpdateAssessmentResult(question) {
    this.updatingAssessmentResults.push(question);
  }

  public clickSaveAssessmentResult(assessment, question) {
    if (!question.response || !question.response.rating) {
      return;
    }
    if (question.response.id) {
      let updateSub = this.store.AssessmentResponse.update(question.response.id, {
        rating: question.response.rating,
      }, true).subscribe(
        (res) => {
          let resultsListIndex = this.updatingAssessmentResults.findIndex((obj) => obj.id === question.id);
          this.updatingAssessmentResults.splice(resultsListIndex, 1);
          let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
          this.refetchPatientTasks(formattedDate).then(() => { })
        },
        (err) => { },
        () => {
          updateSub.unsubscribe();
        },
      );
    } else {
      let createSub = this.store.AssessmentResponse.create({
        assessment_task: assessment.task_id,
        assessment_question: question.id,
        rating: question.response.rating,
      }).subscribe(
        (res) => {
          let resultsListIndex = this.updatingAssessmentResults.findIndex((obj) => obj.id === question.id);
          this.updatingAssessmentResults.splice(resultsListIndex, 1);
          let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
          question.response.id = res.id;
          assessment.responses.push(question.response);
          this.refetchPatientTasks(formattedDate).then(() => { })
        },
        (err) => { },
        () => {
          createSub.unsubscribe();
        }
      );
    }
  }

  public defaultSymptomRating(symptom, def) {
    let rating = symptom.ratings.find((r) => {
      return r.symptom.id === def.id;
    });
    return rating;
  }

  public isUpdatingSymptomResult(result) {
    return this.updatingSymptomResults.findIndex((obj) => obj.id === result.id) >= 0;
  }

  public clickUpdateSymptomResult(result) {
    this.updatingSymptomResults.push(result);
  }

  public clickSaveSymptomResult(symptom, default_symptom) {
    if (!default_symptom.rating) {
      return;
    }
    if (default_symptom.rating.id) {
      let updateSub = this.store.SymptomRating.update(default_symptom.rating.id, {
        rating: default_symptom.rating.rating,
      }, true).subscribe(
        (res) => {
          let resultsListIndex = this.updatingSymptomResults.findIndex((obj) => obj.id === default_symptom.id);
          this.updatingSymptomResults.splice(resultsListIndex, 1);
        },
        (err) => { },
        () => {
          updateSub.unsubscribe();
        },
      );
    } else {
      let createSub = this.store.SymptomRating.create({
        symptom_task: symptom.task_id,
        symptom: default_symptom.id,
        rating: default_symptom.rating.rating,
      }).subscribe(
        (res) => {
          let resultsListIndex = this.updatingSymptomResults.findIndex((obj) => obj.id === default_symptom.id);
          this.updatingSymptomResults.splice(resultsListIndex, 1);
          let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
          default_symptom.rating.id = res.id;
          symptom.ratings.push(default_symptom.rating);
          this.refetchPatientTasks(formattedDate).then(() => { });
        },
        (err) => { },
        () => {
          createSub.unsubscribe();
        }
      );
    }
  }

  public vitalQuestionResponse(vital, question) {
    let res = vital.responses.find((response) => {
      return response.question_id === question.id;
    });
    return res;
  }

  public isUpdatingVitalResult(question) {
    return this.updatingVitalResults.findIndex((obj) => obj.id === question.id) >= 0;
  }

  public clickUpdateVitalResult(question) {
    this.updatingVitalResults.push(question);
  }

  public clickSaveVitalResult(vital, question) {
    if (!question.response) {
      return;
    }
    if (question.response.id) {
      let updateSub = this.store.VitalResponse.update(question.response.id, {
        response: question.response.answer,
      }, true).subscribe(
        (res) => {
          let resultsListIndex = this.updatingVitalResults.findIndex((obj) => obj.id === question.id);
          this.updatingVitalResults.splice(resultsListIndex, 1);
          let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
          this.refetchPatientTasks(formattedDate).then(() => { });
        },
        (err) => { },
        () => {
          updateSub.unsubscribe();
        },
      );
    } else {
      let createSub = this.store.VitalResponse.create({
        vital_task: vital.task_id,
        question: question.id,
        response: question.response.answer,
      }).subscribe(
        (res) => {
          let resultsListIndex = this.updatingVitalResults.findIndex((obj) => obj.id === question.id);
          this.updatingVitalResults.splice(resultsListIndex, 1);
          let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
          question.response.id = res.id;
          vital.responses.push(question.response);
          this.refetchPatientTasks(formattedDate).then(() => { });
        },
        (err) => { },
        () => {
          createSub.unsubscribe();
        }
      );
    }
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

  public routeToCareTeam() {
    this.router.navigate(['/patient', this.patient.id, 'team', this.carePlan.id]);
  }

  public getBehaviorIcon(behavior) {
    switch (behavior) {
      case 'increasing':
      case 'better':
        return 'ss-up iconLime';
      case 'decreasing':
      case 'worse':
        return 'ss-down iconRed'
      case 'equal':
      case 'new':
      case 'avg':
        return 'ss-hyphen';
      default:
        return 'ss-hyphen';
    }
  }

  /***************************************************************************
  * MODAL TRIGGERS
  ****************************************************************************/

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
                this.assignRatingsToQuestions();
                this.detailsLoaded = true;
              });
            },
            (err) => { },
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
      closeDisabled: false,
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
          (err) => { },
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
      overflow: 'auto',
      width: '512px',
    }).subscribe((res) => {
      Utils.logDebug('Goal Comments', res);
    });
  }

  public openRecordResults(task) {
    this.store.TeamTask.read(task.id).subscribe((taskObj) => {
      let hasPlanTemplate = !!taskObj.team_template;
      let teamTemplateId = null;
      if (hasPlanTemplate) {
        teamTemplateId = taskObj.team_template.id;
      }
      this.modals.open(RecordResultsComponent, {
        closeDisabled: false,
        data: {
          patient: this.patient,
          carePlan: this.carePlan,
          teamTemplateId: teamTemplateId,
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
          team_template: results.teamTemplate,
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
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-team',
        planId: this.carePlan.id,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (newTask) => {
        if (!newTask) return;
        setTimeout(() => {
          this.editTeamTask(newTask);
        }, 10);
      },
      (err) => { },
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editTeamTask(task) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-team',
        task: task,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        let formattedDate = this.selectedDate.utc().format('YYYY-MM-DD');
        this.refetchTeamTasks(formattedDate).then();
        if (!updatedTask) return;
      },
      (err) => { },
      () => {
        modalSub.unsubscribe();
      }
    );
  }
}
