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
  public dateFilter = null;
  public actionFilter = '';
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
  public results = [];
  public selectedResult = null;

  public showDatePH;
  public multiOpenPH;

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
          this.results = mockData.results;
          this.selectedResult = this.results[0];
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

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public editResults() {
    this.modals.open(RecordResultsComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmDelete() {
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
