import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent } from '../../../components';
import { NavbarService, StoreService } from '../../../services';
import mockData from './historyData';

@Component({
  selector: 'app-patient-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class PatientHistoryComponent implements OnDestroy, OnInit {

  public patient = null;
  public carePlan = null;
  public dateFilter = null;
  public actionChoices = [
    {
      display: 'Patient Interaction',
      value: 'interaction',
    },
    {
      display: 'Care Team Coordination',
      value: 'coordination',
    },
    {
      display: 'Notes',
      value: 'notes',
    },
  ];
  public selectedActions = [];
  public results = [];
  public selectedResult = null;

  public dateFilterOpen = false;
  public actionFilterOpen = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
          this.store.CarePlan.read(params.planId).subscribe(
            (carePlan) => {
              this.carePlan = carePlan;
              this.results = mockData.results;
              this.selectedResult = this.results[0];
              this.selectedActions = this.actionChoices.concat();
            },
            (err) => {},
            () => {},
          );
        },
        (err) => {},
        () => {},
      );
    });
  }

  public ngOnDestroy() { }

  public getEmployee(id) {
    return mockData.employees.find((obj) => obj.id === id);
  }

  public getTask(id) {
    return mockData.tasks.find((obj) => obj.id === id);
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

  public filteredResults() {
    return this.results.filter((result) => {
      let actionValues = this.selectedActions.map((obj) => obj.value);
      return actionValues.includes(this.getTask(result.task).category);
    });
  }

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      data: {
        patient: this.patient,
        carePlan: this.carePlan,
        task: null,
        totalMinutes: null,
        with: null,
        syncToEHR: false,
        notes: '',
        patientEngagement: null,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public editResults(result) {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      data: {
        patient: this.patient,
        carePlan: this.carePlan,
        task: this.getTask(result.task),
        totalMinutes: result.totalMinutes,
        with: result.with,
        syncToEHR: result.syncToEHR,
        notes: result.notes,
        patientEngagement: result.patientEngagement,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmDelete(result) {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Delete Record?',
       body: 'Are you sure you want to delete this history record?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }
}
