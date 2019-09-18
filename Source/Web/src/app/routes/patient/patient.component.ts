import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import * as moment from 'moment';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { filter as _filter, find as _find } from 'lodash';

import { AddDiagnosisComponent } from './modals/add-diagnosis/add-diagnosis.component';
import { Subscription } from 'rxjs';

import { AppConfig } from '../../app.config';
import { AuthService, NavbarService, StoreService, UtilsService } from '../../services';
import { CarePlanConsentComponent } from './modals/care-plan-consent/care-plan-consent.component';
import { DeleteMedicationComponent } from './modals/delete-medication/delete-medication.component';
import { FinancialDetailsComponent } from './modals/financial-details/financial-details.component';
import { MedicationComponent } from './modals/medication/medication.component';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { PatientAddressComponent } from './modals/patient-address/patient-address.component';
import { PatientCommunicationComponent } from './modals/patient-communication/patient-communication.component';
import { PatientCreationModalService } from '../../services/patient-creation-modal.service';
import { PatientEmergencyContactComponent } from './modals/patient-emergency-contact/patient-emergency-contact.component';
import { PatientProfileComponent } from './modals/patient-profile/patient-profile.component';
import { ProblemAreasComponent } from './modals/problem-areas/problem-areas.component';
import { ProcedureComponent } from './modals/procedure/procedure.component';
import { Utils } from '../../utils';

import { IAddPatientToPlanComponentData } from '../../models/add-patient-to-plan-component-data';
import { IApiResultsContainer } from '../../models/api-results-container';
import { IEmergencyContact } from '../../models/emergency-contact';
import { IEmployee } from '../../models/employee';
import { IPatient } from '../../models/patient';
import { IPatientCarePlan, IOverview } from '../../models/patient-interfaces';
import { IPatientEnrollmentResponse } from '../../models/patient-enrollment-modal-response';

class ImageSnippet {
  constructor(public src: string, public file: File) { }
}

@Component({
  selector: 'app-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss'],
})
export class PatientComponent implements OnDestroy, OnInit {
  @ViewChild('imageUpload') private imageUpload: ElementRef;

  private routeSub: Subscription = null;
  private userSub: Subscription = null;

  public carePlans: Array<IPatientCarePlan> = [];
  public editName;
  public emergencyContact: IEmergencyContact = null;
  public employee: IEmployee = null;
  public moment = moment;
  public nextCheckinTeamMember = null;
  public nextCheckinVisible = false;
  public patient: IPatient = null;
  public patientDiagnoses = [];
  public patientDiagnosesRaw = [];
  public patientMedications = [];
  public patientProcedures = [];
  public patientStats = null;
  public problemAreas = [];
  public teamListOpen = {};
  public tooltipPSOpen; re

  constructor(
    private auth: AuthService,
    private http: HttpClient,
    private modals: ModalService,
    private nav: NavbarService,
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
    public patientCreationModalService: PatientCreationModalService,
    public utils: UtilsService,
  ) {
    // Nothing here
  }

  public ngOnInit() {
    this.nav.normalState();
    this.routeSub = this.route.params.subscribe((params: Params) => {
      this
        .loadPatient(params.patientId)
        .then(() => {
          this.nav.addRecentPatient(this.patient);
          this.loadEmergencyContact();
          this.loadCarePlans(this.patient.id);
          this.loadProblemAreas(this.patient.id);
          this.loadPatientProcedures(this.patient.id);
          Utils.convertObservableToPromise(this.store.PatientStat.readListPaged())
            .then(res => this.patientStats = _find(res, stat => stat.mrn === this.patient.emr_code));
          this.getPatientDiagnoses(this.patient);
        })
        .catch(() => this.router.navigate(['/error']));
    });

    this.userSub = this.auth.user$.subscribe((user: IEmployee) => {
      if (Utils.isNullOrUndefined(user)) {
        return;
      }

      this.employee = user;
    });
  }

  public ngOnDestroy() {
    const unsub = (sub: Subscription) => (sub || { unsubscribe: () => null }).unsubscribe();
    unsub(this.routeSub);
    unsub(this.userSub);
  }

  public loadPatient(id: string): Promise<void> {
    return Utils.convertObservableToPromise<IPatient>(this.store.PatientProfile.read(id))
      .then(patient => this.patient = patient)
      .then(() => null);
  }

  public loadProblemAreas(patientId: string): void {
    const data = { patient: patientId };
    Utils.convertObservableToPromise(this.store.ProblemArea.readListPaged(data))
      .then((problemAreas: any) => this.problemAreas = problemAreas);
  }

  public loadCarePlans(patientId: string): void {
    Utils
      .convertObservableToPromise<Array<IPatientCarePlan>>(this.store.CarePlan.readListPaged({ patient: patientId }))
      .then((carePlans: Array<IPatientCarePlan>) => this.carePlans = carePlans)
      .then(() => {
        this.getCarePlanOverview(this.patient.id).then((overviews: Array<IOverview>) => {
          this.carePlans.forEach((carePlan) => {
            carePlan.overview = overviews.find((overviewObj) => overviewObj.plan_template.id === carePlan.plan_template.id);
            const allTeamMembers = carePlan.overview.care_team;
            // Get care manager
            carePlan.care_manager = allTeamMembers.filter((obj) => obj.is_manager)[0];
            // Get regular team members
            carePlan.team_members = allTeamMembers.filter((obj) => !obj.is_manager);
            // Get team member with closest check in date
            const sortedCT = this.sortTeamMembersByCheckin(allTeamMembers);
            if (sortedCT.length > 0) {
              this.nextCheckinTeamMember = sortedCT[0];
            }
          });
        });

        this.getPatientMedications(this.patient.id);
      });
  }

  public getCarePlanOverview(patientId: string): Promise<Array<IOverview>> {
    return Utils
      .convertObservableToPromise<IApiResultsContainer<Array<IOverview>>>(this.store.PatientProfile.detailRoute('get', patientId, 'care_plan_overview'))
      .then(response => response.results);
  }

  public loadEmergencyContact(): void {
    Utils.convertObservableToPromise<IApiResultsContainer<Array<IEmergencyContact>>>(this.store.PatientProfile.detailRoute('GET', this.patient.id, 'emergency_contacts'))
      .then((response: IApiResultsContainer<Array<IEmergencyContact>>) => this.emergencyContact = (response.results || [null])[0]);
  }

  public getCareTeam(plan) {
    return new Promise((resolve) => {
      this.store.CarePlan.detailRoute('GET', plan.id, 'care_team_members').subscribe((res: any) => {
        resolve(res);
      });
    });
  }

  public loadPatientProcedures(patientId: string): void {
    const data = { patient: patientId };
    Utils.convertObservableToPromise(this.store.PatientProcedure.readListPaged(data))
      .then(procedures => this.patientProcedures = procedures);
  }

  public getPatientDiagnoses(patient) {
    patient.diagnosis.forEach(d => {
      this.store.PatientDiagnosis.read(d).subscribe(
        (diagnosis: any) => {
          this.patientDiagnosesRaw.push(diagnosis);
          this.store.Diagnosis.read(diagnosis.diagnosis).subscribe(
            (res: any) => {
              res.patient_diagnosis = diagnosis;
              this.patientDiagnoses.push(res);
            }
          );
        }
      );
    });
  }

  public getPatientMedications(patientId) {
    this.store.PatientMedication.readListPaged({ patient: patientId }).subscribe(
      res => {
        this.patientMedications = res;
        this.carePlans.forEach(cp => {
          this.store.MedicationTaskTemplate.readListPaged({ plan__id: cp.id }).subscribe((res: any) => {
            res.forEach(taskTemplate => {
              const patientMedication = this.patientMedications.find(m => m.id === taskTemplate.patient_medication.id);

              if (patientMedication)
                patientMedication.task = taskTemplate;
            });
          });
        });
      }
    );
  }

  public formatTimeSince(time) {
    let momentTime = moment(time);
    let today = moment().startOf('day');
    if (momentTime.isSame(today, 'day')) {
      return 'Today';
    } else {
      return momentTime.fromNow();
    }
  }

  public timePillColor(plan) {
    if (!this.patient.payer_reimbursement || !plan.billing_type) {
      return null;
    }
    if (plan.billing_type.acronym === 'TCM') {
      return this.utils.timePillColorTCM(plan.created);
    } else {
      let timeCount = this.totalMinutes(plan.overview.time_spent_this_month);
      let allotted = plan.billing_type.billable_minutes;
      return this.utils.timePillColor(timeCount, allotted);
    }
  }

  public routeToHistory(patient, plan) {
    this.router.navigate(['/patient', patient.id, 'history', plan.id], {
      queryParams: {
        last_patient_interaction: true,
      }
    });
  }

  public progressInWeeks(plan: { created: moment.MomentInput, plan_template: { duration_weeks: number } }): number {
    if (!plan || !plan.created) {
      return 0;
    }

    return Math.min(plan.plan_template.duration_weeks, moment().diff(moment(plan.created), 'weeks'));
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
      (this.carePlans[planIndex] as any).billing_type = data.plan.billing_type;
    });
  }

  public openProblemAreas(plan) {
    const data = {
      closeDisabled: false,
      data: {
        patient: this.patient,
        plan: plan,
        problemAreas: this.problemAreasFilteredByPlan(plan.id),
      },
      width: '560px',
    };

    Utils.convertObservableToPromise(this.modals.open(ProblemAreasComponent, data))
      .then(() => this.loadProblemAreas(this.patient.id));
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
        });
      }
    });
  }

  public openConsentForm(plan) {
    this.modals.open(CarePlanConsentComponent, {
      data: {
        plan_id: plan,
      },
      width: '560px',
    }).subscribe(() => { });
  }

  public addPatientToPlan(patient) {
    const data: IAddPatientToPlanComponentData = {
      action: 'add',
      disableRemovePatient: true,
      enrollPatientChecked: true,
      facility: this.patient.facility,
      patient: patient
    };
    this.patientCreationModalService
      .openEnrollment_PotentialPatientDetails(data)
      .then((response: IPatientEnrollmentResponse) => {
        if (!Utils.isNullOrUndefined(response.patient)) {
          this.loadCarePlans(response.patient.id);
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
      data: {
        patient: this.patient,
      },
      width: '448px',
    }).subscribe((res) => {
      if (res) {
        this.patient = res;
      }
    });
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
        (res: any) => {
          this.patientDiagnoses.push(res);
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
          this.patientDiagnoses = this.patientDiagnoses.filter((d, i) => i !== index);

        });
      }
    });
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
        plans: this.carePlans,
      },
    }).subscribe((res) => {
      if (res) {
        this.patientMedications.push(res);
      }
    });
  }

  public editMedication(medication, i) {
    this.modals.open(MedicationComponent, {
      width: '576px',
      data: {
        type: 'edit',
        patient: this.patient,
        plans: this.carePlans,
        medication,
      }
    }).subscribe((res) => {
      if (res) {
        this.patientMedications[i] = res;
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
        this.router.navigate(['/patients', 'active']).then(() => { });
      });
    });
  }

  public confirmMakePatientActive() {
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Make Patient Active?',
        body: 'Are you sure you want to make this patient active again?',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
      this.store.PatientProfile.update(this.patient.id, {
        is_active: true,
      }).subscribe(() => {
        this.router.navigate(['/patients', 'active']).then(() => { });
      });
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
    if (this.patient && this.patient.user.birthdate) {
      return moment().diff(this.patient.user.birthdate, 'years');
    }
    return '';
  }

  public clickImageUpload() {
    const event = new MouseEvent('click');
    this.imageUpload.nativeElement.dispatchEvent(event);
  }

  public processUpload() {
    const file: File = this.imageUpload.nativeElement.files[0];
    const reader = new FileReader;

    reader.addEventListener('load', (event: any) => {
      const formData = new FormData();
      const selectedFile = new ImageSnippet(event.target.result, file);
      formData.append('image', selectedFile.file);
      this.http.request('PATCH', `${AppConfig.apiUrl}users/${this.patient.user.id}/`, {
        body: formData,
        headers: new HttpHeaders().set('Accept', 'application/json'),
      }).subscribe((res: any) => {
        this.patient.user.image = res.image_url;
      });
    });

    reader.readAsDataURL(file);

  }

  public numberFormat(num): string {
    if (num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
