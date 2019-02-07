import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { FinancialDetailsComponent } from './modals/financial-details/financial-details.component';
import { CarePlanConsentComponent } from './modals/care-plan-consent/care-plan-consent.component';
import { ProblemAreasComponent } from './modals/problem-areas/problem-areas.component';
import { DiagnosisComponent } from './modals/diagnosis/diagnosis.component';
import { ProcedureComponent } from './modals/procedure/procedure.component';
import { MedicationComponent } from './modals/medication/medication.component';
import { AddPatientToPlanComponent } from '../../components/modals/add-patient-to-plan/add-patient-to-plan.component';
import { PatientProfileComponent } from './modals/patient-profile/patient-profile.component';
import { PatientCommunicationComponent } from './modals/patient-communication/patient-communication.component';
import { PatientAddressComponent } from './modals/patient-address/patient-address.component';
import { PatientEmergencyContactComponent } from './modals/patient-emergency-contact/patient-emergency-contact.component';
import { DeleteMedicationComponent } from './modals/delete-medication/delete-medication.component';
import { DeleteDiagnosisComponent } from './modals/delete-diagnosis/delete-diagnosis.component';
import { NavbarService, StoreService } from '../../services';
import patientData from './patientdata.js';
import * as moment from 'moment';

@Component({
  selector: 'app-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss'],
})
export class PatientComponent implements OnDestroy, OnInit {

  public patient = null;
  public carePlans = [];
  public problemAreas = [];
  public patientProcedures = [];
  public teamListOpen = -1;

  public editName;
  public tooltipPSOpen;

  private routeSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private nav: NavbarService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.nav.normalState();
    this.routeSub = this.route.params.subscribe((params) => {
      this.getPatient(params.patientId).then((patient) => {
        this.patient = patient;
        this.nav.addRecentPatient(this.patient);
        this.getCarePlans(this.patient.id).then((carePlans: any) => {
          this.carePlans = carePlans;
        });
        this.getProblemAreas(this.patient.id).then((problemAreas: any) => {
          this.problemAreas = problemAreas;
        });
        this.getPatientProcedures(this.patient.id).then((patientProcedures: any) => {
          this.patientProcedures = patientProcedures;
          console.log(this.patientProcedures);
        });
      }).catch(() => {
        this.patient = patientData.patient;
        this.carePlans = patientData.carePlans;
      });
    });
  }

  public ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  public getPatient(id) {
    let promise = new Promise((resolve, reject) => {
      let patientSub = this.store.PatientProfile.read(id).subscribe(
        (patient) => {
          resolve(patient);
        },
        (err) => {
          reject(err);
        },
        () => {
          patientSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getProblemAreas(patientId) {
    let promise = new Promise((resolve, reject) => {
      let problemAreasSub = this.store.ProblemArea.readListPaged({
        patient: patientId,
      }).subscribe(
        (problemAreas) => resolve(problemAreas),
        (err) => reject(err),
        () => {
          problemAreasSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getCarePlans(patientId) {
    return new Promise((resolve, reject) => {
        let carePlanSub = this.store.PatientProfile.detailRoute('get', patientId, 'care_plans').subscribe(
          (plans) => {
            resolve(plans);
          },
          (err) => {
            reject(err);
          },
          () => {
            carePlanSub.unsubscribe();
          }
        )
    });
  }

  public getPatientProcedures(patientId) {
    let promise = new Promise((resolve, reject) => {
      let proceduresSub = this.store.PatientProcedure.readListPaged({
        patient: patientId,
      }).subscribe(
        (procedures) => resolve(procedures),
        (err) => reject(err),
        () => {
          proceduresSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public openFinancialDetails() {
    this.modals.open(FinancialDetailsComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public openProblemAreas() {
    this.modals.open(ProblemAreasComponent, {
      closeDisabled: true,
      data: {
        patient: this.patient,
        problemAreas: this.problemAreas,
      },
      width: '560px',
    });
  }

  public confirmPause() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Pause Plan?',
       body: 'Do you want to pause this plan? The patient won’t be able to record any progress while the plan is paused.',
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public confirmRemovePlan() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Delete Plan?',
       body: 'Are you sure you want to remove this plan? This will negate the patient\'s current progress. This cannot be undone.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public openConsentForm(plan) {
    this.modals.open(CarePlanConsentComponent, {
     closeDisabled: true,
     data: {
       plan_id: plan,
     },
     width: '560px',
   }).subscribe(() => {});
  }

  public addPatientToPlan(patient) {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'add',
        patientKnown: true,
        patient: patient,
        planKnown: false,
      },
      width: '576px',
    }).subscribe(() => {});
  }

  public editPatientProfile() {
    this.modals.open(PatientProfileComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }

  public editPatientCommunication() {
    this.modals.open(PatientCommunicationComponent, {
      closeDisabled: true,
      width: '448px',
    }).subscribe(() => {});
  }

  public editPatientAddress() {
    this.modals.open(PatientAddressComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public editPatientEmergencyContact() {
    this.modals.open(PatientEmergencyContactComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public addDiagnosis() {
    this.modals.open(DiagnosisComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }

  public editDiagnosis() {
    this.modals.open(DiagnosisComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }

  public deleteDiagnosis() {
    this.modals.open(DeleteDiagnosisComponent, {
      closeDisabled: true,
      width: '348px',
    }).subscribe(() => {});
  }

  public addProcedure() {
    this.modals.open(ProcedureComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe((procedureData) => {
      if (procedureData) {
        procedureData['patient'] = this.patient.id;
        this.store.PatientProcedure.create(procedureData).subscribe((newPatientProcedure) => {
          this.patientProcedures.push(newPatientProcedure);
        });
      }
    });
  }

  public editProcedure(patientProcedure) {
    this.modals.open(ProcedureComponent, {
      closeDisabled: true,
      data: {
        patientProcedure: patientProcedure,
      },
      width: '576px',
    }).subscribe((procedureData) => {
      if (procedureData) {
        this.store.PatientProcedure.update(patientProcedure.id, procedureData, true)
          .subscribe((updatedPatientProcedure) => {
            let index = this.patientProcedures.findIndex((obj) => obj.id === patientProcedure.id);
            this.patientProcedures[index] = updatedPatientProcedure;
          });
      }
    });
  }

  public deleteProcedure(patientProcedure) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Procedure?',
       body: 'Are you sure you want to remove this procedure?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === 'Continue') {
        this.store.PatientProcedure.destroy(patientProcedure.id).subscribe(
          (success) => {
            let index = this.patientProcedures.findIndex((obj) => obj.id === patientProcedure.id);
            this.patientProcedures.splice(index, 1);
          }
        );
      }
    // do something with result
    });
  }

  public addMedication() {
    this.modals.open(MedicationComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }

  public editMedication() {
    this.modals.open(MedicationComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }

  public deleteMedication() {
    this.modals.open(DeleteMedicationComponent, {
      closeDisabled: true,
      width: '348px',
    }).subscribe(() => {});
  }

  public confirmMakePatientInactive() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Make Patient Inactive?',
       body: 'Are you sure you want to make this patient inactive? This will negate the patient\'s current progress. This cannot be undone.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  get riskLevelText() {
    return this.carePlans.map((plan) => {
      if (plan.riskLevel >= 80) {
        return 'High Risk';
      } else if (plan.riskLevel >= 40) {
        return 'Some Risk';
      } else {
        return 'Low Risk';
      }
    })
  }

  get patientAge() {
    if (this.patient) {
      return moment().diff(this.patient.user.birthdate, 'years');
    }
    return '';
  }
}
