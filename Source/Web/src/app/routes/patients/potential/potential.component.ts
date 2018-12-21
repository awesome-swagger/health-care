import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment  from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent, EnrollmentComponent } from '../../../components/';
import { AuthService, StoreService } from '../../../services';
import {
  uniq as _uniq,
  map as _map
} from 'lodash';

@Component({
  selector: 'app-potential',
  templateUrl: './potential.component.html',
  styleUrls: ['./potential.component.scss'],
})
export class PotentialPatientsComponent implements OnDestroy, OnInit {

  public facilities = [];
  public potentialPatients = [];
  public activeCarePlans = {};
  public users = null;

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
          this.carePlans.forEach((p) => {
            this.activeCarePlans[p] = true;
          })
        },
        (err) => {},
        () => {
          potentialPatientsSub.unsubscribe();
        }
      );
    });

    let employeesSub = this.store.EmployeeProfile.readListPaged().subscribe(
      (employees) => {
        this.users = employees;
      },
      (err) => {

      },
      () => {
        employeesSub.unsubscribe();
      }
    )
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
    }).subscribe((data) => {
      this.potentialPatients.push(data)
    });
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

  get carePlans() {
    if (this.potentialPatients && this.potentialPatients.length) {
      return _uniq(_map(this.potentialPatients, p => p.care_plan));
    }
    return [];
  }
}
