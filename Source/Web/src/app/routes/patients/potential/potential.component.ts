import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment  from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent, EnrollmentComponent } from '../../../components/';
import { AuthService, StoreService } from '../../../services';

@Component({
  selector: 'app-potential',
  templateUrl: './potential.component.html',
  styleUrls: ['./potential.component.scss'],
})
export class PotentialPatientsComponent implements OnDestroy, OnInit {

  public facilities = [];
  public potentialPatients = [];

  private facilitiesSub = null;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.facilitiesSub = this.auth.facilities$.subscribe((facilities) => {
      if (facilities === null) {
        return;
      }
      this.facilities = facilities;
      let potentialPatientsSub = this.store.PotentialPatient.readListPaged({

      }).subscribe(
        (potentialPatients) => {
          console.log(potentialPatients);
          this.potentialPatients = potentialPatients;
        },
        (err) => {},
        () => {
          potentialPatientsSub.unsubscribe();
        }
      );
    });
  }

  public ngOnDestroy() {
    this.facilitiesSub.unsubscribe();
  }

  public addPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'add',
        patientKnown: false,
        patientInSystem: false,
        planKnown: false,
      },
      width: '576px',
    }).subscribe(() => {});
  }

  public enrollPotentialPatient(potentialPatient) {
    this.modals.open(EnrollmentComponent, {
      closeDisabled: true,
      width: '608px',
    }).subscribe(() => {});
  }

  public editPotentialPatient(potentialPatient) {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'edit',
        patientKnown: true,
        patientInSystem: true,
        planKnown: potentialPatient.care_plan.length > 0 ? true : false,
      },
      width: '576px',
    }).subscribe(() => {});
  }

  public removePotentialPatient(potentialPatient) {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove Patient?',
       body: 'Are you sure you want remove this patient from the list? This cannot be undone.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {

    });
  }

  public formatTimeAdded(time) {
    return moment(time).fromNow();
  }
}
