import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent } from '../../../components';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-patient-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class PatientHistoryComponent implements OnDestroy, OnInit {

  public patient = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.id, params.planId);
      this.store.PatientProfile.read(params.id).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        },
        (err) => {},
        () => {},
      );
    });
  }

  public ngOnDestroy() { }

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
