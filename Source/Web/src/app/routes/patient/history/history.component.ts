import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent } from '../../../components';
import { AuthService, NavbarService, StoreService } from '../../../services';
import { HistoryMockData } from './historyData';

@Component({
  selector: 'app-patient-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class PatientHistoryComponent implements OnDestroy, OnInit {

  public moment = moment;

  public mockData = new HistoryMockData();

  public user = null;
  public patient = null;
  public carePlan = null;
  public careTeamMembers = [];
  public dateFilter = moment();
  public actionChoices = [
    {
      display: 'Care Plan Review',
      value: 'care_plan_review',
    },
    {
      display: 'Phone Call',
      value: 'phone_call',
    },
    {
      display: 'Notes',
      value: 'notes',
    },
    {
      display: 'Face to Face',
      value: 'face_to_face',
    },
    {
      display: 'Message',
      value: 'message',
    }
  ];
  public datePickerOptions = {
    relativeLeft: '0px',
    relativeTop: '48px'
  };
  public selectedActions = [];
  public billedActivities = [];
  public selectedActivity = null;

  public dateFilterOpen = false;
  public actionFilterOpen = false;

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
    				// Get care team
    				this.getCareTeamMembers(params.planId).then((teamMembers: any) => {
    					this.careTeamMembers = teamMembers.filter((obj) => {
    						return obj.employee_profile.user.id !== this.user.user.id;
    					});
    					this.selectedActions = this.actionChoices.concat();
    					// Get billed activities
    					this.getBilledActivities().then((billedActivities: any) => {
    						this.billedActivities = billedActivities;
    						this.selectedActivity = this.billedActivities[0];
    					});
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

  public getBilledActivities() {
    let promise = new Promise((resolve, reject) => {
      let billedActivitiesSub = this.store.BilledActivity.readListPaged({
        // TODO: Filters to get only billed activities for this care plan
        activity_date: this.dateFilter.format('YYYY-MM-DD'),
      }).subscribe(
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
    this.dateFilter = e;
    this.dateFilterOpen = false;
    // Get billed activities
    this.getBilledActivities().then((billedActivities: any) => {
      this.billedActivities = billedActivities;
      this.selectedActivity = this.billedActivities[0];
    });
  }

  public isActionChecked(action) {
    return this.selectedActions.findIndex((obj) => {
      return obj.value === action.value;
    }) > -1;
  }

  public checkAllActions() {
    this.selectedActions = this.actionChoices.concat();
  }

  public uncheckAllActions() {
    this.selectedActions = [];
  }

  public toggleAction(action) {
    if (!this.isActionChecked(action)) {
      this.selectedActions.push(action);
    } else {
      let index = this.selectedActions.findIndex((obj) => obj.value === action.value);
      this.selectedActions.splice(index, 1);
    }
  }

  public filteredBilledActivities() {
    return this.billedActivities.filter((activity) => {
      let actionValues = this.selectedActions.map((obj) => obj.value);
      return actionValues.includes(activity.activity_type);
    });
  }

  public formatActivityType(type) {
    return type.replace(/_/g, ' ');
  }

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      data: {
        patient: this.patient,
        carePlan: this.carePlan,
        tasks: this.mockData.tasks, // TODO: Get tasks for user
        task: null,
        totalMinutes: null,
        teamMembers: this.careTeamMembers,
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
        activity_type: 'care_plan_review', // TODO: activity type
        members: [
          this.user.id, // TODO: user selected in "with" field.
        ],
        sync_to_ehr: results.syncToEHR,
        added_by: this.user.id,
        notes: results.notes,
        time_spent: results.totalMinutes,
      }).subscribe(
        (newResult) => {
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
        patient: this.patient,
        carePlan: this.carePlan,
        date: moment(result.activity_date),
        tasks: this.mockData.tasks, // TODO: Get tasks for user
        task: null,
        totalMinutes: result.time_spent,
        teamMembers: this.careTeamMembers,
        with: null, // TODO: Autofill with field
        syncToEHR: result.sync_to_ehr,
        notes: result.notes,
        patientEngagement: 0, // TODO: Autofill patient engagement.
      },
      width: '512px',
    }).subscribe((results) => {
      if (!results) {
        return;
      }
      let updateSub = this.store.BilledActivity.update(result.id, {
        activity_type: 'care_plan_review', // TODO: activity type
        members: [
          this.user.id, // TODO: user selected in "with" field.
        ],
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
    }).subscribe(() => {
      let index = this.billedActivities.findIndex((obj) => obj.id === result.id);
      this.billedActivities = this.billedActivities.splice(index, 1);
    });
  }
}
