import {Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
// noinspection ES6UnusedImports
import { TitleCasePipe } from '@angular/common'
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { FinancialDetailsComponent } from './modals/financial-details/financial-details.component';
import { CarePlanConsentComponent } from './modals/care-plan-consent/care-plan-consent.component';
import { ProblemAreasComponent } from './modals/problem-areas/problem-areas.component';
import { AddDiagnosisComponent } from './modals/add-diagnosis/add-diagnosis.component';
import { ProcedureComponent } from './modals/procedure/procedure.component';
import { MedicationComponent } from './modals/medication/medication.component';
import { AddPatientToPlanComponent } from '../../components';
import { PatientProfileComponent } from './modals/patient-profile/patient-profile.component';
import { PatientCommunicationComponent } from './modals/patient-communication/patient-communication.component';
import { PatientAddressComponent } from './modals/patient-address/patient-address.component';
import { PatientEmergencyContactComponent } from './modals/patient-emergency-contact/patient-emergency-contact.component';
import { DeleteMedicationComponent } from './modals/delete-medication/delete-medication.component';
import {AuthService, NavbarService, StoreService, UtilsService} from '../../services';
import * as moment from 'moment';
import {
  filter as _filter,
  find as _find
} from 'lodash';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {AppConfig} from '../../app.config';

class ImageSnippet {
  constructor(public src: string, public file: File) {}
}

@Component({
  selector: 'app-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss'],
})
export class PatientComponent implements OnDestroy, OnInit {

  @ViewChild('imageUpload') private imageUpload: ElementRef;

  public moment = moment;

  public patient = null;
  public carePlans = [];
  public patientDiagnoses = [];
  public patientDiagnosesRaw = [];
  public patientMedications = [];
  public nextCheckinTeamMember = null;
  public problemAreas = [];
  public patientProcedures = [];
  public teamListOpen = {};
  public patientStats = null;
  public emergencyContact = null;

  public editName;
  public tooltipPSOpen;
  public nextCheckinVisible = false;

  private routeSub = null;
  public employee = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private nav: NavbarService,
    private store: StoreService,
    public utils: UtilsService,
    private http: HttpClient,
    private auth: AuthService,
  ) { }

  public ngOnInit() {
    this.nav.normalState();
    this.routeSub = this.route.params.subscribe((params) => {
      this.getPatient(params.patientId).then((patient:any) => {
        this.patient = patient;
        this.nav.addRecentPatient(this.patient);
        this.getEmergencyContact();
        this.getCarePlans(this.patient.id).then((carePlans: any) => {
          this.carePlans = carePlans;
    			this.getCarePlanOverview(this.patient.id).then((overview: any) => {
            let overviewStats = overview.results;
            this.carePlans.forEach((carePlan) => {
              carePlan.overview = overviewStats.find((overviewObj) => overviewObj.plan_template.id === carePlan.plan_template.id);
              let allTeamMembers = carePlan.overview.care_team;
              // Get care manager
      				carePlan.care_manager = allTeamMembers.filter((obj) => {
      					return obj.is_manager;
      				})[0];
              // Get regular team members
      				carePlan.team_members = allTeamMembers.filter((obj) => {
      					return !obj.is_manager;
      				});
              // Get team member with closest check in date
              let sortedCT = this.sortTeamMembersByCheckin(allTeamMembers);
              if (sortedCT.length > 0) {
                this.nextCheckinTeamMember = sortedCT[0];
              }
            });
    			});
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
        this.router.navigate(['/error']).then(() => {});
        // this.patient = patientData.patient;
        // this.carePlans = patientData.carePlans;
      });
    });

    this.auth.user$.subscribe(user => {
      if (!user) return;
      this.employee = user;
    })
  }

  public ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  public getPatient(id) {
    return new Promise((resolve, reject) => {
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
  }

  public getProblemAreas(patientId) {
    return new Promise((resolve, reject) => {
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

  public getCarePlanOverview(patientId) {
    return new Promise((resolve, reject) => {
      let overviewSub = this.store.PatientProfile.detailRoute('get', patientId, 'care_plan_overview').subscribe(
        (overview) => resolve(overview),
        (err) => reject(err),
        () => {
          overviewSub.unsubscribe();
        }
      );
    });
  }

  public getEmergencyContact() {
    this.store.PatientProfile.detailRoute('GET', this.patient.id, 'emergency_contacts').subscribe((res:any) => {
      if (res.results[0]) {
        this.emergencyContact = res.results[0];
      } else {
        this.emergencyContact = {};
      }
    })
  }

  public getCareTeam(plan) {
    return new Promise((resolve) => {
        this.store.CarePlan.detailRoute('GET', plan.id, 'care_team_members').subscribe((res:any) => {
          resolve(res);
        })
    });
  }

  public getPatientProcedures(patientId) {
    return new Promise((resolve, reject) => {
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
  }

  public getPatientDiagnoses(patient) {
    patient.diagnosis.forEach(d => {
      this.store.PatientDiagnosis.read(d).subscribe(
        (diagnosis:any) => {
          this.patientDiagnosesRaw.push(diagnosis);
          this.store.Diagnosis.read(diagnosis.diagnosis).subscribe(
            (res:any) => {
              res.patient_diagnosis = diagnosis;
              this.patientDiagnoses.push(res);
            }
          );
        }
      )
    })
  }

  public getPatientMedications(patientId) {
    this.store.PatientMedication.readListPaged({ patient: patientId }).subscribe(
      res => {
        this.patientMedications = res;
      }
    )
  }

  public progressInWeeks(plan) {
    if (!plan || !plan.created) {
      return 0;
    }
    return moment().diff(moment(plan.created), 'weeks');
  }

  public isBefore3DaysAgo(dateAsMoment) {
    let threeDaysAgo = moment().subtract(3, 'days').startOf('day');
    return dateAsMoment.isBefore(threeDaysAgo);
  }

  public sortTeamMembersByCheckin(teamMembers) {
    // removes members without a checkin date set
    return teamMembers.filter((obj) => {
      return obj.next_checkin && !this.isBefore3DaysAgo(moment(obj.next_checkin));
    }).sort((left: any, right: any) => {
      left = moment(left.next_checkin).format();
      right = moment(right.next_checkin).format();
      return left - right;
    });
  }

  public problemAreasFilteredByPlan(planId) {
    if (!this.problemAreas) {
      return [];
    }
    return this.problemAreas.filter((obj) => obj.plan === planId);
  }

  public openFinancialDetails(plan) {
    let planIndex = this.carePlans.findIndex((planObj) => planObj.id === plan.id);
    this.modals.open(FinancialDetailsComponent, {
      closeDisabled: false,
      data: {
        patient: this.patient,
        plan: plan,
      },
      width: '532px',
    }).subscribe((data) => {
      if (!data) return;
      this.patient.payer_reimbursement = data.patient.payer_reimbursement;
      this.carePlans[planIndex].billing_type = data.plan.billing_type;
    });
  }

  public openProblemAreas(plan) {
    this.modals.open(ProblemAreasComponent, {
      closeDisabled: false,
      data: {
        patient: this.patient,
        plan: plan,
        problemAreas: this.problemAreasFilteredByPlan(plan.id),
      },
      width: '560px',
    }).subscribe(() => {
      this.getProblemAreas(this.patient.id).then((problemAreas: any) => {
        this.problemAreas = problemAreas;
      });
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
        this.store.CarePlan.destroy(planId).subscribe(() => {
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
        enrollPatientChecked: true,
        disableRemovePatient: true,
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
      width: '741px',
      data: {
        patient: this.patient,
      }
    }).subscribe((res) => {
      if (!res) return;
      this.patient = res;
    });
  }

  public editPatientCommunication() {
    this.modals.open(PatientCommunicationComponent, {
      width: '448px',
    }).subscribe(() => {});
  }

  public editPatientAddress() {
    this.modals.open(PatientAddressComponent, {
      width: '512px',
      data: {
        patient: this.patient,
      }
    }).subscribe((res) => {
      if (res) {
        this.patient = res;
      }
    });
  }

  public editPatientEmergencyContact() {
    this.modals.open(PatientEmergencyContactComponent, {
      data: {
        emergencyContact: this.emergencyContact,
        patient: this.patient,
      },
      width: '512px',
    }).subscribe((res) => {
      this.emergencyContact = res;
    });
  }

  public addDiagnosis() {
    this.modals.open(AddDiagnosisComponent, {
      width: '512px',
      data: {
        type: 'add',
        patient: this.patient,
      }
    }).subscribe((res) => {
      if (!res) return;
      this.store.Diagnosis.read(res.diagnosis).subscribe(
        (res:any) => {
          this.patientDiagnoses.push(res)
        }
      );
    });
  }

  public editDiagnosis(diagnosis) {
    this.modals.open(AddDiagnosisComponent, {
      data: {
        type: 'edit',
        patient: this.patient,
        diagnosis: diagnosis,
      },
      width: '576px',
    }).subscribe((res) => {
      if (res) {
        const d = this.patientDiagnoses.find(p => p.id === res.diagnosis);
        d.patient_diagnosis = res;
      }
    });
  }

  public deleteDiagnosis(diagnosis, index) {
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
        this.store.PatientDiagnosis.destroy(_find(this.patientDiagnosesRaw, d => d.diagnosis = diagnosis).id).subscribe(() => {
          this.patientDiagnoses = this.patientDiagnoses.filter((d, i) => i !== index)

        })
      }
    })
  }

  public addProcedure() {
    this.modals.open(ProcedureComponent, {
      width: '576px',
    }).subscribe((procedureData) => {
      if (procedureData) {
        procedureData['patient'] = this.patient.id;
        procedureData.attending_practitioner = procedureData.attending_practitioner.id;
        procedureData.facility = procedureData.facility.id;
        this.store.PatientProcedure.create(procedureData).subscribe((newPatientProcedure) => {
          this.patientProcedures.push(newPatientProcedure);
        });
      }
    });
  }

  public editProcedure(patientProcedure) {
    this.modals.open(ProcedureComponent, {
      data: {
        type: 'edit',
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
          () => {
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
        type: 'add',
        patient: this.patient,
      },
    }).subscribe((res) => {
      if (res) {
        this.patientMedications.push(res);
      }
    });
  }

  public editMedication(medication) {
    this.modals.open(MedicationComponent, {
      width: '576px',
      data: {
        type: 'edit',
        patient: this.patient,
        medication,
      }
    }).subscribe((res) => {
      if (res === 'delete') {
        this.patientMedications = this.patientMedications.filter(m => m.id !== medication.id);
      }
    });
  }

  public deleteMedication(id) {
    this.modals.open(DeleteMedicationComponent, {
      data: {
        medicationId: id,
      },
      width: '348px',
    }).subscribe((res) => {
      if (res) {
        if (!res) return;
        this.patientMedications = this.patientMedications.filter(m => m.id !== id);
      }
    });
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
      this.store.PatientProfile.update(this.patient.id, {
        is_active: false,
      }).subscribe(() => {
        this.router.navigate(['/patients', 'active']).then(() => {})
      })
    });
  }

  public confirmMakePatientActive() {
     this.modals.open(ConfirmModalComponent, {
     data: {
       title: 'Make Patient Inactive?',
       body: 'Are you sure you want to make this patient active again?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
      this.store.PatientProfile.update(this.patient.id, {
        is_active: true,
      }).subscribe(() => {
        this.router.navigate(['/patients', 'active']).then(() => {})
      })
    });
  }

  public totalMinutes(timeSpentStr) {
    if (!timeSpentStr) {
      return 0;
    }
    let timeCountSplit = timeSpentStr.split(":");
    let splitHours = parseInt(timeCountSplit[0]);
    let splitMinutes = parseInt(timeCountSplit[1]);
    let hours = splitHours;
    let minutes = splitMinutes;
    minutes = minutes + (hours * 60);
    return minutes;
  }

  get patientAge() {
    if (this.patient) {
      return moment().diff(this.patient.user.birthdate, 'years');
    }
    return '';
  }

  public clickImageUpload() {
    const event = new MouseEvent('click');
    this.imageUpload.nativeElement.dispatchEvent(event);
  }

  public processUpload() {
    const file : File = this.imageUpload.nativeElement.files[0];
    const reader = new FileReader;

    reader.addEventListener('load', (event:any) => {
      const formData = new FormData();
      const selectedFile = new ImageSnippet(event.target.result, file);
      formData.append('image', selectedFile.file);
      this.http.request('PATCH', `${AppConfig.apiUrl}users/${this.patient.user.id}/`, {
        body: formData,
        headers: new HttpHeaders().set('Accept', 'application/json'),
      }).subscribe((res:any) => {
        this.patient.user.image = res.image_url;
      })
    })

    reader.readAsDataURL(file);

  }
}
