import { Injectable } from '@angular/core';

import * as postData from '../models/post-data';
import { EnrollmentConsentComponent } from '../components/modals/enrollment-consent/enrollment-consent.component';
import { EnrollmentDetailsComponent } from '../components/modals/enrollment-details/enrollment-details.component';
import { EnrollmentMessagingComponent } from '../components/modals/enrollment-messaging';
import { EnrollmentPatientEnrolledComponent } from '../components/modals/enrollment-patient-enrolled/enrollment-patient-enrolled.component';
import { EnrollmentPotentialPatientAddedComponent } from '../components/modals/enrollment-potential-patient-added/enrollment-potential-patient-added.component';
import { EnrollmentPotentialPatientDetailsComponent } from '../components/modals/enrollment-potential-patient-details/enrollment-potential-patient-details.component';
import { EnrollmentRequiredComponent } from '../components/modals/enrollment-required/enrollment-required.component';
import { ModalService } from '../modules/modals';
import { StoreService } from './store.service';
import { ToastService } from '../modules/toast';
import { Utils, LogLevel } from '../utils';

import { IAddPatientToPlanComponentData } from '../models/add-patient-to-plan-component-data';
import { ICarePlan } from '../models/care-plan';
import { IDiagnoses } from '../models/diagnoses';
import { IEmployee } from '../models/employee';
import { INewPatientDetails } from '../models/new-patient-details';
import { IPatient } from '../models/patient';
import { IPatientEnrollmentModalResponse, IPatientEnrollmentResponse, PatientCreationAction, PatientCreationStep } from '../models/patient-enrollment-modal-response';
import { IPotentialPatient } from '../models/potential-patient';
import { IPotentialPatientEnrollmentDetailsComponentInitialData } from '../models/potential-patient-enrollment-details-component-initial-data';
import { IRole } from '../models/role';
import { IUser } from '../models/user';

@Injectable()
export class PatientCreationModalService {
  private readonly pw = 'password';
  private billingPractitionerRole: IRole = null;
  private careManagerRole: IRole = null;
  private logAction = <T>(message: string, action: () => Promise<T>, logResponse: boolean = false) => {
    return Promise.resolve()
      .then(() => Utils.logDebug(`starting_${message}`))
      .then(() => action())
      .then((response) => logResponse && Utils.logDebug(`response_${message}`, response))
      .then(() => Utils.logDebug(`complete_${message}`));
  };

  constructor(
    private modals: ModalService,
    private store: StoreService,
    private toast: ToastService
  ) {
    this.loadRoles();
  }

  private catchError<T>(message: string, error: Error | string, returnValue: T, reject: boolean = false): Promise<T> {
    Utils.logError(message, error, returnValue);
    if (reject) {
      return Promise.reject(message)
    }

    this.toast.error(message);
    return Promise.resolve(returnValue);
  }

  private completeEnrollment(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<IPatientEnrollmentResponse> {
    const data: {
      action?: () => Promise<void>,
      error?: Error | string,
      message: string,
      name: string,
      success?: boolean,
    } = {
      message: 'Creating/updating patient details',
      name: `${newPatientDetails.firstName} ${newPatientDetails.lastName}`
    };
    const action = () => Promise
      .resolve()
      .then(() => this.logAction('updatePhoneIfNeeded', () => this.updatePhoneIfNeeded(newPatientDetails)))
      .then(() => this.logAction('createPatientIfNeeded', () => this.createPatientIfNeeded(newPatientDetails), true))
      .then(() => data.message = 'Creating care plan')
      .then(() => this.logAction('createCarePlan', () => this.createCarePlan(newPatientDetails)))
      .then(() => data.message = 'Creating care manager/billing practitioner')
      .then(() => this.logAction('createCareTeamMemberIfNeeded_careManager', () => this.createCareTeamMemberIfNeeded(this.careManagerRole, newPatientDetails)))
      .then(() => this.logAction('createCareTeamMemberIfNeeded_billingPractitioner', () => this.createCareTeamMemberIfNeeded(this.billingPractitionerRole, newPatientDetails)))
      .then(() => data.message = 'Creating consent form')
      .then(() => this.logAction('createPlanConsentForm', () => this.createPlanConsentForm(newPatientDetails)))
      .then(() => data.message = 'Creating diagnoses')
      .then(() => this.logAction('createDiagnosesIfNeeded', () => this.createDiagnosesIfNeeded(newPatientDetails)))
      .then(() => this.logAction('deletePotentialPatientIfNeeded', () => this.deletePotentialPatientIfNeeded(newPatientDetails, potentialPatientId)))
      .then(() => data.message = 'Creating care team')
      .then(() => this.logAction('createOtherCareTeamRolesIfNeeded', () => this.createOtherCareTeamRolesIfNeeded(newPatientDetails)));
    data.action = action;

    return this
      .openModal(508, data, EnrollmentMessagingComponent, false)
      .then(() => {
        if (!Utils.isNullOrUndefined(data.error) || !data.success) {
          throw data.error || 'An unknown error has occurred while attempting to enroll the patient';
        }
      })
      .then(() => this.logAction('patientEnrolled_dispatchEvent_refreshPatientOverview', () => Promise.resolve(document.dispatchEvent(new Event('refreshPatientOverview')))))
      .then(() => this.openModal(508, newPatientDetails, EnrollmentPatientEnrolledComponent))
      .then(() => ({ potentialPatientId, patient: newPatientDetails.patient.patient as IPatient }))
      .catch(error => {
        this.modals.close(null);
        return this.catchError('Failed to complete patient enrollment', error, null);
      });
  }

  private createCarePlan(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const postData: postData.ICarePlanApiPostData = {
      billing_practitioner: (newPatientDetails.billingPractioner || {}).id,
      billing_type: (newPatientDetails.planType || {}).id,
      patient: newPatientDetails.patient.patient.id,
      plan_start_date: newPatientDetails.enrollmentConsentDetails.planStartDate,
      plan_template: newPatientDetails.carePlan.id
    };

    return Promise.resolve()
      .then(() => this.logAction('this.store.CarePlan.create', () => Utils
        .convertObservableToPromise<ICarePlan>(this.store.CarePlan.create(postData))
        .then((carePlan: ICarePlan) => newPatientDetails.carePlan = carePlan)
      ))
      .then(() => newPatientDetails);
  }

  private createCareTeamMemberIfNeeded(role: IRole, newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    let isManager: boolean;
    const careTeamMember: IEmployee = (isManager = role.id === this.careManagerRole.id)
      ? newPatientDetails.careManager
      : newPatientDetails.billingPractioner;

    if (Utils.isNullOrUndefined(careTeamMember)) {
      (Utils.logDebug('complete_NoCareTeamMemberCreated'));
      return Promise.resolve(null);
    }

    newPatientDetails.carePlan.careTeam = newPatientDetails.carePlan.careTeam || [];
    const postData: postData.ICareTeamMemberPostData = {
      employee_profile: careTeamMember.id,
      is_manager: isManager,
      plan: newPatientDetails.carePlan.id,
      role: role.id
    };

    return Promise.resolve()
      .then(() => this.logAction('this.store.CareTeamMember.create', () => {
        return Utils
          .convertObservableToPromise<IEmployee>(this.store.CareTeamMember.create(postData))
          .then((member: IEmployee) => {
            if (!Utils.isNullOrUndefined(member)) {
              newPatientDetails.carePlan.careTeam.push(member);
            }
          });
      }))
      .then(() => newPatientDetails);
  }

  private createDiagnosesIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    var notChronicPlan = () => {
      const planType = (newPatientDetails.planType || {}).acronym;
      return !(planType === 'CCM' || planType === 'CCCM');
    };

    if (!newPatientDetails.checked.reimburses || Utils.isNullOrEmptyCollection(newPatientDetails.diagnoses) || notChronicPlan()) {
      return this.logAction('noDiagnosesAdded', () => Promise.resolve())
        .then(() => newPatientDetails);
    }

    const totalDiagnoses = newPatientDetails.diagnoses.length;
    let counter = 0;
    const promises: Array<Promise<IDiagnoses>> = [];

    (Utils.logDebug(`starting_this.store.PatientDiagnosis.update/create => (0 of ${totalDiagnoses})`));
    const promise = new Promise<INewPatientDetails>(resolve => {
      newPatientDetails.diagnoses.forEach(diagnoses => {
        if (Utils.isNullOrWhitespace(diagnoses.patient)) {
          diagnoses.patient = newPatientDetails.patient.patient.id;
        }

        const fail = `Failed to create diagnoses: ${++counter}`;
        const message = `this.store.PatientDiagnosis.${(diagnoses.isModified ? 'update' : 'create')} => (${counter} of ${totalDiagnoses})`;
        const action = Utils.isTrueValue(diagnoses.isModified)
          ? this.store.PatientDiagnosis.update(diagnoses.id, diagnoses)
          : this.store.PatientDiagnosis.create(diagnoses);

        const p = Utils
          .convertObservableToPromise<IDiagnoses>(action)
          .then(newOrUpdatedDiagnoses => Object.assign(diagnoses, newOrUpdatedDiagnoses));

        promises.push(p);
      });

      Promise
        .all(promises)
        .then(diagnoses => diagnoses.filter(x => !Utils.isNullOrUndefined(x)).map(d => d.id))
        .then((diagnosis: Array<string>) => this
          .logAction(
            'updatingPatientProfile',
            () => Utils.convertObservableToPromise(this.store.PatientProfile.update(newPatientDetails.patient.patient.id, { diagnosis })),
            true
          )
        )
        .then(() => Utils.logDebug(`complete_this.store.PatientDiagnosis.update/create => (${totalDiagnoses} of ${totalDiagnoses})`))
        .then(() => resolve(newPatientDetails));
    });

    return promise;
  }

  private createOrUpdatePotentialPatient(newPatientDetails: INewPatientDetails): Promise<IPotentialPatient> {
    const isPotentialPatient = newPatientDetails.patient.isPotential && !Utils.isNullOrUndefined(newPatientDetails.patient.patient);
    const potentialPatientData: postData.IPotentialPatientPostData = {
      care_plan: newPatientDetails.carePlan.id,
      email: newPatientDetails.email,
      facility: [newPatientDetails.facility.id],
      first_name: newPatientDetails.firstName,
      last_name: newPatientDetails.lastName,
      phone: newPatientDetails.phoneNumber,
      source: newPatientDetails.source,
    };

    const action = () => Utils.convertObservableToPromise<IPotentialPatient>(
      isPotentialPatient
        ? this.store.PotentialPatient.update(newPatientDetails.patient.patient.id, potentialPatientData)
        : this.store.PotentialPatient.create(potentialPatientData)
    );

    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.store.PotentialPatient.create/Update'))
      .then(() => action())
      .then(potentialPatient => {
        (Utils.logDebug('complete_this.store.PotentialPatient.create/Update', potentialPatient));
        return potentialPatient;
      });
  }

  private createOtherCareTeamRolesIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const totalRoles = Object.keys(newPatientDetails.carePlanRoles).length;
    let counter = -1;
    const promises: Array<Promise<INewPatientDetails>> = [];
    let p = Promise.resolve()
      .then(() => Utils.logDebug(`starting_this.createCareTeamMemberIfNeeded => (${++counter} of ${totalRoles})`))
      .then(() => null);
    promises.push(p);

    const promise = new Promise<INewPatientDetails>((resolve) => {
      for (let roleIdProp in newPatientDetails.carePlanRoles) {
        const carePlanRole = newPatientDetails.carePlanRoles[roleIdProp];
        const role = carePlanRole.role;

        const action = () => !carePlanRole.selected || role.id === this.careManagerRole.id || role.id === this.billingPractitionerRole.id
          ? Promise.resolve(newPatientDetails)
          : this.createCareTeamMemberIfNeeded(role, newPatientDetails);

        p = Promise.resolve()
          .then(() => Utils.logDebug(`starting_this.createCareTeamMemberIfNeeded => (${++counter} of ${totalRoles})`))
          .then(() => action())
          .then(() => Utils.logDebug(`complete_this.createCareTeamMemberIfNeeded => (${counter} of ${totalRoles})`));

        promises.push(p);
      }

      Promise.all(promises)
        .then(() => Utils.logDebug(`complete_this.createCareTeamMemberIfNeeded => (${totalRoles} of ${totalRoles})`))
        .then(() => resolve(newPatientDetails))
        .then(() => newPatientDetails);
    });

    return promise;
  }

  private createPatientIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    if (!Utils.isTrueValue(newPatientDetails.patient.isPotential) && !Utils.isNullOrUndefined(newPatientDetails.patient.patient)) {
      (Utils.logDebug('complete_createPatientIfNeeded_patientAlreadyExists'));
      return Promise.resolve(newPatientDetails);
    }

    const createPatientProfilePostData: postData.ICreatePatientProfilePostData = {
      facility: newPatientDetails.facility.id,
      insurance: newPatientDetails.insurance && newPatientDetails.insurance.id,
      is_active: true,
      is_invited: false,
      payer_reimbursement: Utils.isTrueValue(newPatientDetails.checked.reimburses),
      user: null
    };

    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.getOrCreateUserId'))
      .then(() => this.getOrCreateUserId(newPatientDetails))
      .then((userId: string) => createPatientProfilePostData.user = userId)
      .then(() => (Utils.logDebug('createPatientProfilePostData', createPatientProfilePostData)))
      .then(() => Utils.convertObservableToPromise<IPatient>(this.store.PatientProfile.create(createPatientProfilePostData)))
      .then(patient => newPatientDetails.patient.patient = patient)
      .then(() => Utils.logDebug('createPatientIfNeeded.afterResponse', newPatientDetails))
      .then(() => Utils.logDebug('complete_this.getOrCreateUserId'))
      .then(() => newPatientDetails);
  }

  private createPlanConsentForm(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const consentForm: postData.IPlanConsentPostData = {
      plan: newPatientDetails.carePlan.id,
      verbal_consent: newPatientDetails.enrollmentConsentDetails.verbal_consent,
      seen_within_year: newPatientDetails.enrollmentConsentDetails.seen_within_year,
      discussed_co_pay: newPatientDetails.enrollmentConsentDetails.discussed_co_pay,
      will_use_mobile_app: newPatientDetails.enrollmentConsentDetails.will_use_mobile_app,
      will_interact_with_team: newPatientDetails.enrollmentConsentDetails.will_interact_with_team,
      will_complete_tasks: newPatientDetails.enrollmentConsentDetails.will_complete_tasks,
    };

    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.store.PlanConsentForm.create'))
      .then(() => Utils.convertObservableToPromise<postData.IPlanConsentPostData>(this.store.PlanConsentForm.create(consentForm)))
      .then(() => Utils.logDebug('complete_this.store.PlanConsentForm.create'))
      .then(() => newPatientDetails);
  }

  private deletePotentialPatientIfNeeded(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<INewPatientDetails> {
    if (Utils.isNullOrWhitespace(potentialPatientId)) {
      (Utils.logDebug('complete_deletePotentialPatientIfNeeded_potentialPatientNotSpecified'));
      return Promise.resolve(newPatientDetails);
    }

    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.store.PotentialPatient.destroy'))
      .then(() => Utils.convertObservableToPromise(this.store.PotentialPatient.destroy(potentialPatientId)))
      .then(() => Utils.logDebug('complete_this.store.PotentialPatient.destroy'))
      .then(() => newPatientDetails);
  }

  private getOrCreateUserId(newPatientDetails: INewPatientDetails): Promise<string> {
    (Utils.logDebug('starting_getOrCreateUserId'));

    return this
      .getUserIfEmailMatches(newPatientDetails.email)
      .then((user: IUser) => {
        if (!Utils.isNullOrUndefined(user) && !Utils.isNullOrWhitespace(user.id)) {
          (Utils.logDebug('complete_getOrCreateUserId_basedOnEmail'));
          return user.id;
        }

        const createUserPostData: postData.ICreateUserPostData = {
          email: newPatientDetails.email,
          first_name: newPatientDetails.firstName,
          last_name: newPatientDetails.lastName,
          password1: this.pw,
          password2: this.pw
        };

        let userId: string;
        return Promise.resolve()
          .then(() => Utils.logDebug('starting_this.store.AddUser.createAlt'))
          .then(() => Utils.convertObservableToPromise<{ pk: string }>(this.store.AddUser.createAlt(createUserPostData)))
          .then((user: { pk: string }) => userId = user.pk)
          .then(() => Utils.logDebug('complete_this.store.AddUser.createAlt'))
          .then(() => userId);
      });
  }

  private getPotentialPatientId(potentialPatient: IPotentialPatient, newPatientDetails: INewPatientDetails, potentialPatientId?: string): string {
    if (!Utils.isNullOrWhitespace(potentialPatientId)) {
      return potentialPatientId;
    }

    if (Utils.isNullOrUndefined(newPatientDetails) && !Utils.isNullOrUndefined(potentialPatient)) {
      newPatientDetails = <INewPatientDetails>{ checked: { enroll: false }, diagnoses: [], patient: { isPotential: true, patient: potentialPatient } };
    }

    if (
      Utils.isNullOrUndefined(newPatientDetails)
      || Utils.isNullOrUndefined(newPatientDetails.patient)
      || Utils.isNullOrUndefined(newPatientDetails.patient.patient)
      || !Utils.isTrueValue(newPatientDetails.patient.isPotential)
    ) {
      return null;
    }

    return newPatientDetails.patient.patient.id;
  }

  private getUserIfEmailMatches(email: string): Promise<IUser> {
    if (Utils.isNullOrWhitespace(email)) {
      return Promise.resolve()
        .then(() => Utils.logDebug('complete_getUserIfEmailMatches'))
        .then(() => null);
    }

    let result: IUser
    email = email.toLowerCase().trim();
    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.store.PatientProfile.readListPaged'))
      .then(() => Utils.convertObservableToPromise(this.store.PatientProfile.readListPaged()))
      .then((patients: Array<IPatient>) => patients
        .filter(x => !Utils.isNullOrUndefined(x.user) && !Utils.isNullOrWhitespace(x.user.email))
        .map(x => ({ email: x.user.email.trim().toLowerCase(), user: x.user }))
      )
      .then((users: Array<{ email: string, user: IUser }>) => {
        const user = users.find(x => x.email === email);
        if (!Utils.isNullOrUndefined(user)) {
          result = user.user
        }
      })
      .then(() => Utils.logDebug('complete_this.store.PatientProfile.readListPaged'))
      .then(() => result);
  }

  private loadRoles(): void {
    Promise.resolve()
      .then(() => Utils.convertObservableToPromise(this.store.ProviderRole.readListPaged()))
      .then((roles: Array<IRole>) => {
        const toLower = (val: string) => (val || '').toLowerCase();
        const filter = (opt1: string, opt2: string) => roles.find(x => {
          const name = toLower(x.name);
          return name === toLower(opt1) || name === toLower(opt2);
        });

        this.careManagerRole = filter('care manager', 'care team manager');
        this.billingPractitionerRole = filter('qualified practitioner', 'billing practitioner');
      });
  }

  private openEnrollment_EnrollmentConsent(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<IPatientEnrollmentResponse> {
    return this.openModal(608, newPatientDetails, EnrollmentConsentComponent)
      .then(modalResponse => this.processEnrollmentConsent(potentialPatientId, modalResponse));
  }

  /**
   * Open Enrollment Step 2 - Enrollment values (Care Plan & Billing employees, insurance, diagnoses, etc...)
   * @param data data required for creating a 
   * @param potentialPatientId
   */
  public openEnrollment_EnrollmentDetails(data: IPotentialPatientEnrollmentDetailsComponentInitialData, potentialPatientId?: string): Promise<IPatientEnrollmentResponse> {
    potentialPatientId = this.getPotentialPatientId(data.potentialPatient, data.newPatientDetails, potentialPatientId);

    return this
      .openModal(608, data, EnrollmentDetailsComponent)
      .then(modalResponse => this.processEnrollmentDetails(potentialPatientId, modalResponse));
  }

  private openEnrollment_EnrollmentRequired(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<IPatientEnrollmentResponse> {
    return this.openModal(576, newPatientDetails, EnrollmentRequiredComponent)
      .then((modalResponse) => this.processEnrollmentRequired(potentialPatientId, modalResponse));
  }

  private openEnrollment_PotentialPatientAddedModal(newPatientDetails: INewPatientDetails, potentialPatientId?: string): Promise<IPatientEnrollmentResponse> {
    const potentialPatient = newPatientDetails.patient.patient as IPotentialPatient;
    (Utils.logDebug('starting_openEnrollment_PotentialPatientAddedModal'));
    potentialPatientId = this.getPotentialPatientId(potentialPatient, null, potentialPatientId);
    const obj: IPatientEnrollmentResponse = { potentialPatient, potentialPatientId };

    if (Utils.isNullOrUndefined(potentialPatient)) {
      (Utils.logDebug('skipping_openEnrollment_PotentialPatientAddedModal', { potentialPatient, newPatientDetails }));
      return Promise.resolve(obj);
    }

    return this
      .openModal(576, newPatientDetails, EnrollmentPotentialPatientAddedComponent)
      .then(() => (Utils.logDebug('completing_openEnrollment_PotentialPatientAddedModal')))
      .then(() => (obj));
  }

  /**
   * Open Enrollment Step 1 - Patient Details
   * @param data Data required to preload control and set/lock selections
   * @param potentialPatientId The potential patient id if existing - Used to delete a potential patient when enrollment is completed
   */
  public openEnrollment_PotentialPatientDetails(data: IAddPatientToPlanComponentData, potentialPatientId?: string): Promise<IPatientEnrollmentResponse> {
    potentialPatientId = this.getPotentialPatientId(data.potentialPatient, data.newPatientDetails, potentialPatientId);

    return this
      .openModal(576, data, EnrollmentPotentialPatientDetailsComponent)
      .then(modalResponse => this.processPotentialPatientDetails(potentialPatientId, modalResponse));
  }

  private openModal<TComponent, TData>(width: number, data: TData, component: TComponent, blocking: boolean = true): Promise<IPatientEnrollmentModalResponse> {
    const modalData = {
      blocking,
      data: data,
      preventClose: true,
      width: `${width}px`
    };

    return Utils.convertObservableToPromise(this.modals.open(component, modalData));
  }

  private processEnrollmentConsent(potentialPatientId: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    const action = (modalResponse || { action: PatientCreationAction.Cancel, step: PatientCreationStep.PatientConsent }).action;
    let promise: Promise<IPatientEnrollmentResponse>;

    switch (action) {
      // User canceled the request - do and return nothing
      case PatientCreationAction.Cancel:
        promise = Promise.resolve({});
        break;

      case PatientCreationAction.Back:
        promise = this.openEnrollment_PotentialPatientDetails({ newPatientDetails: modalResponse.newPatientDetails }, potentialPatientId);
        break;

      case PatientCreationAction.Next:
        promise = this.rejectNotSupported(modalResponse);
        break;

      case PatientCreationAction.Later:
        promise = this.savePotentialPatientAndDisplayModalifNeeded(potentialPatientId, modalResponse);
        break;

      case PatientCreationAction.Complete:
        promise = this.completeEnrollment(modalResponse.newPatientDetails, potentialPatientId);
        break;

      default:
        promise = this.rejectNotDefined(modalResponse);
        break;
    }

    return promise;
  }

  private processEnrollmentDetails(potentialPatientId: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    const action = (modalResponse || { action: PatientCreationAction.Cancel, step: PatientCreationStep.EnrollementDetails }).action;
    let promise: Promise<IPatientEnrollmentResponse>;

    switch (action) {
      // User canceled the request - do and return nothing
      case PatientCreationAction.Cancel:
        promise = Promise.resolve({});
        break;

      case PatientCreationAction.Back:
        promise = this.openEnrollment_PotentialPatientDetails({ newPatientDetails: modalResponse.newPatientDetails }, potentialPatientId);
        break;

      case PatientCreationAction.Next:
        promise = this.openEnrollment_EnrollmentRequired(modalResponse.newPatientDetails, potentialPatientId);
        break;

      case PatientCreationAction.Later:
        // Clear data that should not be transmitted for a potential patient
        const npd = modalResponse.newPatientDetails;
        npd.checked.enroll = false;
        npd.checked.reimburses = false;
        npd.billingPractioner = null;
        npd.careManager = null;
        npd.chronic = null;
        npd.diagnoses = null;
        npd.diagnosis = null;
        npd.enrollmentConsentDetails = null;
        npd.insurance = null;
        npd.planType = null;
        for (let id in npd.carePlanRoles) {
          npd.carePlanRoles[id].selected = false;
        }
        Utils.logDebug('Saving potential patient...', npd);
        promise = this.savePotentialPatientAndDisplayModalifNeeded(potentialPatientId, modalResponse);
        break;

      case PatientCreationAction.Complete:
        promise = this.rejectNotSupported(modalResponse);
        break;

      default:
        promise = this.rejectNotDefined(modalResponse);
        break;
    }

    return promise;
  }

  private processEnrollmentRequired(potentialPatientId: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    const action = (modalResponse || { action: PatientCreationAction.Cancel, step: PatientCreationStep.EnrollmentRequired }).action;
    let promise: Promise<IPatientEnrollmentResponse>;

    switch (action) {
      // User canceled the request - do and return nothing
      case PatientCreationAction.Cancel:
      case PatientCreationAction.Back:
        promise = this.rejectNotSupported(modalResponse);
        break;

      case PatientCreationAction.Next:
        promise = this.openEnrollment_EnrollmentConsent(modalResponse.newPatientDetails, potentialPatientId);
        break;

      case PatientCreationAction.Later:
        promise = this.savePotentialPatientAndDisplayModalifNeeded(potentialPatientId, modalResponse);
        break;

      case PatientCreationAction.Complete:
        promise = this.rejectNotSupported(modalResponse);
        break;

      default:
        promise = this.rejectNotDefined(modalResponse);
        break;
    }

    return promise;
  }

  private processPotentialPatientDetails(potentialPatientId: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    const action = (modalResponse || { action: PatientCreationAction.Cancel, step: PatientCreationStep.PotentialPatientDetails }).action;
    let promise: Promise<IPatientEnrollmentResponse>;

    switch (action) {
      // User canceled the request - do and return nothing
      case PatientCreationAction.Cancel:
        promise = this.resolveCancel();
        break;

      case PatientCreationAction.Back:
        promise = this.rejectNotSupported(modalResponse);
        break;

      case PatientCreationAction.Next:
        promise = this.openEnrollment_EnrollmentDetails(modalResponse, potentialPatientId);
        break;

      case PatientCreationAction.Later:
        promise = this.rejectNotSupported(modalResponse);
        break;

      case PatientCreationAction.Complete:
        promise = this.savePotentialPatientAndDisplayModalifNeeded(potentialPatientId, modalResponse);
        break;

      default:
        promise = this.rejectNotDefined(modalResponse);
        break;
    }

    return promise;
  }

  private reject(reason: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    return Promise.reject({ action: PatientCreationAction[modalResponse.action], reason, modalResponse });
  }

  private rejectNotDefined(modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    return this.reject('Action was defined but not implemented!', modalResponse);
  }

  private rejectNotSupported(modalResponse): Promise<IPatientEnrollmentResponse> {
    return this.reject(`Operation not supported`, modalResponse);
  }

  private resolveCancel(): Promise<IPatientEnrollmentResponse> {
    return Promise.resolve({});
  }

  private savePotentialPatientAndDisplayModalifNeeded(potentialPatientId: string, modalResponse: IPatientEnrollmentModalResponse): Promise<IPatientEnrollmentResponse> {
    return Promise.resolve()
      .then(() => Utils.logDebug('starting_createOrUpdatePotentialPatient'))
      .then(() => this.createOrUpdatePotentialPatient(modalResponse.newPatientDetails))
      .then(potentialPatient => {
        if (Utils.isNullOrUndefined(potentialPatient)) {
          (Utils.logDebug('skipping_createOrUpdatePotentialPatient_noPotentialPatient', potentialPatient));
          return Promise.resolve(null);
        }

        modalResponse.newPatientDetails.patient.patient = potentialPatient;
        (Utils.logDebug('complete_createOrUpdatePotentialPatient', potentialPatient));

        return this.openEnrollment_PotentialPatientAddedModal(modalResponse.newPatientDetails, potentialPatientId);
      });
  }

  private updatePhoneIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const patient = newPatientDetails.patient.patient as IPatient;
    const newPhone = (newPatientDetails.phoneNumber || '').trim();

    if (
      Utils.isNullOrUndefined(patient)
      || Utils.isNullOrUndefined(patient.user)
      || patient.user.hasOwnProperty('patient_profile')
      || Utils.isNullOrWhitespace(newPhone)
      || (patient.user.phone || '').trim() === newPhone
    ) {
      (Utils.logDebug('complete_updatePhoneIfNeeded_notNeeded'))
      return Promise.resolve(newPatientDetails);
    }

    const postData = { phone: newPhone };
    return Promise.resolve()
      .then(() => Utils.logDebug('starting_this.store.User.update_phone'))
      .then(() => Utils.convertObservableToPromise(this.store.User.update(patient.user.id, postData)))
      .then((user: IUser) => {
        if (Utils.isNullOrUndefined(user)) {
          Utils.logWarn('Failed to return an expected user object');
        }
      })
      .then(() => Utils.logDebug('complete_this.store.User.update_phone'))
      .then(() => newPatientDetails);
  }
}
