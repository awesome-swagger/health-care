import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent } from '../../../components';
import { AuthService, NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-patient-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class PatientHistoryComponent implements OnDestroy, OnInit {

  public moment = moment;

  public user = null;
  public userRoles = [];
  public patient = null;
  public carePlan = null;
  public careTeamMembers = [];
  public dateFilter = moment();
  public taskTypeChoices = [
    {
      display: 'Care Team Coordination',
      value: 'coordination',
    },
    {
      display: 'Patient Interaction',
      value: 'interaction',
    },
    {
      display: 'Notes',
      value: 'notes',
    }
  ];
  public teamTaskChoices = [];
  public selectedTasks = [];
  public datePickerOptions = {
    relativeLeft: '0px',
    relativeTop: '48px'
  };
  public billedActivities = [];
  public activitiesLoaded = false;
  public selectedActivity = null;

  public dateFilterOpen = false;
  public taskFilterOpen = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
    	this.nav.patientDetailState(params.patientId, params.planId);
    	// Get auth user
    	this.auth.user$.subscribe((user) => {
    		if (!user) {
    			return;
    		}
    		// Get patient
    		this.getPatient(params.patientId).then((patient: any) => {
    			this.patient = patient;
    			this.nav.addRecentPatient(this.patient);
    			this.user = user;
    			// Get care plan
    			this.getCarePlan(params.planId).then((carePlan: any) => {
    				this.carePlan = carePlan;
            this.getTaskTemplates().then((taskTemplates: any) => {
              this.teamTaskChoices = taskTemplates;
            });
            // Get billed activities
            this.getBilledActivities().then((billedActivities: any) => {
              this.billedActivities = billedActivities;
              this.selectedActivity = this.billedActivities[0];
              this.activitiesLoaded = true;
            });
    			});
    		});
    	});
    });
  }

  public ngOnDestroy() { }

  public getPatient(patientId) {
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

  public getTaskTemplates() {
    let promise = new Promise((resolve, reject) => {
      let teamTasksSub = this.store.TeamTaskTemplate.readListPaged().subscribe(
        (teamTasks) => resolve(teamTasks),
        (err) => reject(err),
        () => {
          teamTasksSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getBilledActivities(taskTemplate = null) {
    let promise = new Promise((resolve, reject) => {
      let params = {
        plan: this.carePlan.id,
      };
      if (this.dateFilter) {
        let endOfDay = this.dateFilter.clone().endOf('day');
        params['activity_datetime__lte'] = endOfDay.toISOString();
      }
      if (taskTemplate) {
        params['team_task_template'] = taskTemplate.id;
      }
      let billedActivitiesSub = this.store.BilledActivity.readListPaged(params).subscribe(
        (billedActivities) => {
          resolve(billedActivities);
        },
        (err) => reject(err),
        () => {
          billedActivitiesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getCarePlan(planId) {
    let promise = new Promise((resolve, reject) => {
      let carePlanSub = this.store.CarePlan.read(planId).subscribe(
        (carePlan) => resolve(carePlan),
        (err) => reject(err),
        () => {
          carePlanSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public setSelectedDay(e) {
    if (e.isSame(this.dateFilter, 'day')) {
      return;
    }
    this.dateFilter = e;
    this.dateFilterOpen = false;
    // Get billed activities
    this.getBilledActivities().then((billedActivities: any) => {
      this.billedActivities = billedActivities;
      this.selectedActivity = this.billedActivities[0];
      this.activitiesLoaded = true;
    });
  }

  public formatTaskType(taskType) {
    let match = this.taskTypeChoices.find((obj) => {
      return obj.value === taskType;
    });
    if (match) {
      return match.display;
    } else {
      return taskType;
    }
  }

  public isTaskChecked(task) {
    return this.selectedTasks.findIndex((obj) => {
      return obj.id === task.id;
    }) > -1;
  }

  public checkAllTasks() {
    this.selectedTasks = this.teamTaskChoices.concat();
  }

  public uncheckAllTasks() {
    this.selectedTasks = [];
  }

  public toggleTask(task) {
    if (!this.isTaskChecked(task)) {
      this.selectedTasks.push(task);
    } else {
      let index = this.selectedTasks.findIndex((obj) => obj.id === task.id);
      this.selectedTasks.splice(index, 1);
    }
  }

  public filteredBilledActivities() {
    return this.billedActivities.filter((activity) => {
      // let actionValues = this.selectedActions.map((obj) => obj.value);
      // return actionValues.includes(activity.activity_type);
      return true;
    }).sort((left: any, right: any) => {
      left = moment(left.created).format();
      right = moment(right.created).format();
      return left - right;
    });
  }

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: false,
      data: {
        patient: this.patient,
        carePlan: this.carePlan,
        taskEditable: true,
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
      // Create billed activity record
      let createSub = this.store.BilledActivity.create({
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
      }).subscribe(
        (newResult) => {
          // check if date is current date, if it is push it to the list, if not, switch to the new date
          this.billedActivities.push(newResult);
          this.selectedActivity = newResult;
        },
        (err) => {},
        () => {
          createSub.unsubscribe();
        }
      );
    });
  }

  public editResults(result) {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      data: {
        editing: true,
        taskEditable: true,
        patient: this.patient,
        carePlan: this.carePlan,
        date: moment(result.activity_datetime),
        teamTaskId: result.team_task_template ? result.team_task_template.id : null,
        patientIncluded: result.patient_included,
        totalMinutes: result.time_spent,
        with: result.members.map((member) => member.id),
        syncToEHR: result.sync_to_ehr,
        notes: result.notes,
        patientEngagement: null,
      },
      width: '512px',
    }).subscribe((results) => {
      if (!results) return;
      let updateSub = this.store.BilledActivity.update(result.id, {
        activity_datetime: results.date,
        members: [
          this.user.id,
        ].concat(results.with),
        team_task_template: results.teamTaskTemplate,
        patient_included: results.patientIncluded,
        sync_to_ehr: results.syncToEHR,
        notes: results.notes,
        time_spent: results.totalMinutes,
      }, true).subscribe(
        (updatedResult) => {
          let resultIndex = this.billedActivities.findIndex((obj) => obj.id === result.id);
          this.billedActivities[resultIndex] = updatedResult;
          this.selectedActivity = this.billedActivities[resultIndex];
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public confirmDelete(result) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Record?',
       body: 'Are you sure you want to delete this history record?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe((modalResult) => {
      if (!modalResult) return;
      if (modalResult.toLowerCase() === 'continue') {
        this.store.BilledActivity.destroy(result.id).subscribe(
          (success) => {
            let index = this.billedActivities.findIndex((obj) => obj.id === result.id);
            this.billedActivities.splice(index, 1);
          },
          (err) => {},
          () => {},
        );
      }
    });
  }
}
