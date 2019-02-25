import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { FinancialDetailsComponent } from './modals/financial-details/financial-details.component';
import { CarePlanConsentComponent } from './modals/care-plan-consent/care-plan-consent.component';
import { ProblemAreasComponent } from './modals/problem-areas/problem-areas.component';
import { AddDiagnosisComponent } from './modals/add-diagnosis/add-diagnosis.component';
import { EditDiagnosisComponent } from './modals/edit-diagnosis/edit-diagnosis.component';
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
import {
  filter as _filter,
  find as _find
} from 'lodash';
import { st } from '@angular/core/src/render3';

@Component({
  selector: 'app-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss'],
})
export class PatientComponent implements OnDestroy, OnInit {

  public patient = null;
  public carePlans = [];
  public patientDiagnoses = [];
  public patientDiagnosesRaw = [];
  public patientMedications = [];
  public problemAreas = [];
  public patientProcedures = [];
  public teamListOpen = -1;
  public patientStats = null;

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
      this.getPatient(params.patientId).then((patient:any) => {
        this.patient = patient;
        this.nav.addRecentPatient(this.patient);
        this.getCarePlans(this.patient.id).then((carePlans: any) => {
          this.carePlans = carePlans;
          this.carePlans.forEach(plan => {
            this.getCareTeam(plan).then(res => {
              plan.careTeam = res;
            });
          })
        });
        this.getProblemAreas(this.patient.id).then((problemAreas: any) => {
          this.problemAreas = problemAreas;
        });
        this.getPatientProcedures(this.patient.id).then((patientProcedures: any) => {
          this.patientProcedures = patientProcedures;
        });

        this.store.PatientStat.readListPaged().subscribe(res => {
          this.patientStats = _find(res, stat => stat.mrn === patient.emr_code);
        })

        this.getPatientDiagnoses(this.patient);

        this.getPatientMedications(this.patient.id);
        
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
        let carePlanSub = this.store.CarePlan.readListPaged({patient: patientId}).subscribe(
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

  public getCareTeam(plan) {
    return new Promise((resolve, reject) => {
        this.store.CarePlan.detailRoute('GET', plan.id, 'care_team_members').subscribe((res:any) => {
          resolve(res);
        })
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

  public getPatientDiagnoses(patient) {
    patient.diagnosis.forEach(d => {
      this.store.PatientDiagnosis.read(d).subscribe(
        (res:any) => {
          this.patientDiagnosesRaw.push(res);
          this.store.Diagnosis.read(res.diagnosis).subscribe(
            (res:any) => {
              this.patientDiagnoses.push(res)
            }
          );
        }
      )
    })
  }

  public getPatientMedications(patientId) {
    this.store.PatientMedication.readListPaged({ patient: patientId }).subscribe(
      res => {
        console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
        console.log(res);
        console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
        this.patientMedications = res;
      }
    )
  }

  public openFinancialDetails() {
    this.modals.open(FinancialDetailsComponent, {
      width: '384px',
    }).subscribe(() => {});
  }

  public openProblemAreas() {
    this.modals.open(ProblemAreasComponent, {
      data: {
        patient: this.patient,
        problemAreas: this.problemAreas,
      },
      width: '560px',
    });
  }

  public confirmPause() {
    this.modals.open(ConfirmModalComponent, {
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

  public confirmRemovePlan(planId) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
     data: {
       title: 'Delete Plan?',
       body: 'Are you sure you want to remove this plan? This will negate the patient\'s current progress. This cannot be undone.',
       cancelText,
       okText,
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === okText) {
        this.store.CarePlan.destroy(planId).subscribe(res => {
          this.carePlans = _filter(this.carePlans, plan => plan.id !== planId);
        })
      }
    });
  }

  public openConsentForm(plan) {
    this.modals.open(CarePlanConsentComponent, {
     data: {
       plan_id: plan,
     },
     width: '560px',
   }).subscribe(() => {});
  }

  public addPatientToPlan(patient) {
    this.modals.open(AddPatientToPlanComponent, {
      data: {
        action: 'add',
        patientKnown: true,
        patient: patient,
        planKnown: false,
        facility: this.patient.facility,
      },
      width: '576px',
    }).subscribe((plan) => {
      if (plan) {
        this.carePlans.push(plan);
      }
    });
  }

  public editPatientProfile() {
    this.modals.open(PatientProfileComponent, {
      width: '576px',
    }).subscribe(() => {});
  }

  public editPatientCommunication() {
    this.modals.open(PatientCommunicationComponent, {
      width: '448px',
    }).subscribe(() => {});
  }

  public editPatientAddress() {
    this.modals.open(PatientAddressComponent, {
      width: '512px',
    }).subscribe(() => {});
  }

  public editPatientEmergencyContact() {
    this.modals.open(PatientEmergencyContactComponent, {
      width: '512px',
    }).subscribe(() => {});
  }

  public addDiagnosis() {
    this.modals.open(AddDiagnosisComponent, {
      width: '512px',
      data: {
        patient: this.patient,
      }
    }).subscribe((res) => {
        this.store.Diagnosis.read(res.diagnosis).subscribe(
          (res:any) => {
            this.patientDiagnoses.push(res)
          }
        );
    });
  }

  public editDiagnosis() {
    this.modals.open(EditDiagnosisComponent, {
      width: '576px',
    }).subscribe(() => {});
  }

  public deleteDiagnosis(diagnosis) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
      width: '384px',
      data: {
        okText,
        cancelText,
        title: 'Delete Diagnosis?',
        body: `Do you want to remove the diagnosis of ${diagnosis.name} from ${this.patient.user.first_name} ${this.patient.user.last_name}?`,
      }
    }).subscribe(res => {
      if (res === okText) {
        this.store.PatientDiagnosis.destroy(_find(this.patientDiagnosesRaw, d => d.diagnosis = diagnosis).id).subscribe(() => {})
      }
    })
  }

  public addProcedure() {
    this.modals.open(ProcedureComponent, {
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
      width: '576px',
      data: {
        patient: this.patient,
      },
    }).subscribe((res) => {
      if (res) {
        this.patientMedications.push(res);
      }
    });
  }

  public editMedication() {
    this.modals.open(MedicationComponent, {
      width: '576px',
    }).subscribe(() => {});
  }

  public deleteMedication(id) {
    this.modals.open(DeleteMedicationComponent, {
      width: '348px',
    }).subscribe((

    ) => {});
  }

  public confirmMakePatientInactive() {
    this.modals.open(ConfirmModalComponent, {
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

  public riskLevelText(level) {
    if (level >= 90) {
      return 'On Track';
    } else if (level >= 70) {
      return 'Low Risk';
    } else if (level >= 50) {
      return 'Med Risk'
    } else {
      return 'High Risk';
    }
  }

  get patientAge() {
    if (this.patient) {
      return moment().diff(this.patient.user.birthdate, 'years');
    }
    return '';
  }
}
