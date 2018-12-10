import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent } from '../../../components';
import { StoreService } from '../../../services';
import { uniqBy as _uniqBy, groupBy as _groupBy } from 'lodash';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {

  public activePatients = [];
  public activePatientsGrouped = [];

  public accordionsOpen = [];

  public toolAP1Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;

  constructor(
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.activePatients = [];
    this.activePatientsGrouped = [];
    this.getPatients().then((patients: any) => {
      this.activePatients = patients;
      this.activePatientsGrouped = this.groupPatientsByFacility(patients);
      console.log(this.uniqueFacilities());
      console.log(this.activePatientsGrouped);
    });
  }

  public ngOnDestroy() { }

  public getPatients() {
    let promise = new Promise((resolve, reject) => {
      let patientsSub = this.store.PatientProfile.readListPaged().subscribe(
        (patients) => {
          resolve(patients);
        },
        (err) => {
          reject(err);
        },
        () => {
          patientsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public groupPatientsByStatus(patients) {
    let patientGroupDefaults = {
      'potential': null,
      'invited': null,
      'inactive': null,
      'active': null,
    };
    let groupedByStatus = _groupBy(patients, (obj) => {
      return obj.status;
    });
    return Object.assign({}, patientGroupDefaults, groupedByStatus);
  }

  public groupPatientsByFacility(patients) {
    let groupedByFacility = _groupBy(patients, (obj) => {
      return obj.facility.id;
    });
    return groupedByFacility;
  }

  public confirmRemovePatient() {
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to remove this patient from this plan? This will negate their current progress. This cannot be undone.',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => { });
  }

  public addPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'add',
        patientKnown: false,
        patientInSystem: true,
        planKnown: false,
      },
      width: '576px',
    }).subscribe(() => { });
  }

  public uniqueFacilities() {
    return _uniqBy(this.activePatients.map((obj) => { return obj.facility; }), 'id');
  }

  public getPatientsForFacility(facility) {
    return this.activePatientsGrouped[facility.id];
  }

  public routeToPatient(patient) {
    this.router.navigate(['patient', patient.id, 'overview']);
  }
}
