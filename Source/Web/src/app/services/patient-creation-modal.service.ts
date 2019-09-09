import { Injectable } from '@angular/core';

import * as postData from '../models/post-data';
import { EnrollmentConsentComponent } from '../components/modals/enrollment-consent/enrollment-consent.component';
import { EnrollmentDetailsComponent } from '../components/modals/enrollment-details/enrollment-details.component';
import { EnrollmentPotentialPatientAddedComponent } from '../components/modals/enrollment-potential-patient-added/enrollment-potential-patient-added.component';
import { EnrollmentPotentialPatientDetailsComponent } from '../components/modals/enrollment-potential-patient-details/enrollment-potential-patient-details.component';
import { EnrollmentRequiredComponent } from '../components/modals/enrollment-required/enrollment-required.component';
import { ModalService } from '../modules/modals';
import { StoreService } from './store.service';
import { ToastService } from '../modules/toast';
import { Utils } from '../utils';

import { IAddPatientToPlanComponentData } from '../models/iadd-patient-to-plan-component-data';
import { ICarePlan } from '../models/care-plan';
import { IEmployee } from '../models/employee';
import { INewPatientDetails } from '../models/inew-patient-details';
import { IPatient } from '../models/patient';
import { IPatientEnrollmentModalResponse, IPatientEnrollmentResponse, PatientCreationAction, PatientCreationStep } from '../models/ipatient-enrollment-modal-response';
import { IPotentialPatient } from '../models/potential-patient';
import { IPotentialPatientEnrollmentDetailsComponentInitialData } from '../models/ipotential-patient-enrollment-details-component-initial-data';
import { IRole } from '../models/role';
import { IUser } from '../models/user';
import { IDiagnoses } from '../models/diagnoses';
import { IDiagnosis } from '../models/diagnosis';

@Injectable()
export class PatientCreationModalService {
  private readonly pw = 'password';
  private billingPractitionerRole: IRole = null;
  private careManagerRole: IRole = null;

  constructor(
    private modals: ModalService,
    private store: StoreService,
    private toast: ToastService
  ) {
    this.loadRoles();
  }

  private catchError<T>(message: string, error: Error | string, returnValue: T): Promise<T> {
    this.toast.error(message);
    console.error(error);

    return Promise.resolve(returnValue);
  }

  private completeEnrollment(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<IPatientEnrollmentResponse> {
    return Promise
      .resolve(null)
      .then(() => this.updatePhoneIfNeeded(newPatientDetails))
      .then(() => this.createPatientIfNeeded(newPatientDetails))
      .then(() => this.createCarePlan(newPatientDetails))
      .then(() => this.createCareTeamMemberIfNeeded(this.careManagerRole, newPatientDetails))
      .then(() => this.createCareTeamMemberIfNeeded(this.billingPractitionerRole, newPatientDetails))
      .then(() => this.createPlanConsentForm(newPatientDetails))
      .then(() => this.createDiagnosesIfNeeded(newPatientDetails))
      .then(() => this.deletePotentialPatientIfNeeded(newPatientDetails, potentialPatientId))
      .then(() => ({ potentialPatientId, patient: newPatientDetails.patient.patient as IPatient }));
  }

  private createCarePlan(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const postData: postData.ICarePlanApiPostData = {
      billing_practitioner: (newPatientDetails.billingPractioner || {}).id,
      billing_type: (newPatientDetails.planType || {}).id,
      patient: newPatientDetails.patient.patient.id,
      plan_start_date: newPatientDetails.enrollmentConsentDetails.planStartDate,
      plan_template: newPatientDetails.carePlan.id
    };

    return Utils
      .convertObservableToPromise<ICarePlan>(this.store.CarePlan.create(postData))
      .then((carePlan: ICarePlan) => newPatientDetails.carePlan = carePlan)
      .then(() => newPatientDetails);
  }

  private createCareTeamMemberIfNeeded(role: IRole, newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    let isManager: boolean;
    const careTeamMember: IEmployee = (isManager = role.id === this.careManagerRole.id)
      ? newPatientDetails.careManager
      : newPatientDetails.billingPractioner;

    if (Utils.isNullOrUndefined(careTeamMember)) {
      return Promise.resolve(null);
    }

    newPatientDetails.carePlan.careTeam = newPatientDetails.carePlan.careTeam || [];

    const postData: postData.ICareTeamMemberPostData = {
      employee_profile: careTeamMember.id,
      is_manager: isManager,
      plan: newPatientDetails.carePlan.id,
      role: role.id
    };

    return Utils.convertObservableToPromise<IEmployee>(this.store.CareTeamMember.create(postData))
      .then((member: IEmployee) => Utils.isNullOrUndefined(member) ? null : newPatientDetails.carePlan.careTeam.push(member))
      .then(() => newPatientDetails);
  }

  private createDiagnosesIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    if (Utils.isNullOrEmptyCollection(newPatientDetails.diagnoses)) {
      return Promise.resolve(newPatientDetails);
    }

    const promises: Array<Promise<IDiagnoses>> = [];
    const promise = new Promise<INewPatientDetails>(resolve => {
      (newPatientDetails.diagnoses || []).forEach(diagnoses => {
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
        .then(diagnoses => diagnoses.map(d => d.id))
        .then((diagnosis: Array<string>) => this.store.PatientProfile.update(newPatientDetails.patient.patient.id, { diagnosis }))
        .then(() => resolve(newPatientDetails))
        .then(() => newPatientDetails);
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

    return Utils.convertObservableToPromise<IPotentialPatient>(
      isPotentialPatient
        ? this.store.PotentialPatient.update(newPatientDetails.patient.patient.id, potentialPatientData)
        : this.store.PotentialPatient.create(potentialPatientData)
    ).catch(error => this.catchError('Failed to create/update potential patient', error, null));
  }

  private createPatientIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    if (!Utils.isNullOrUndefined(newPatientDetails.patient.patient)) {
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

    return this
      .getOrCreateUserId(newPatientDetails)
      .then((userId: string) => createPatientProfilePostData.user = userId)
      .then(() => Utils.convertObservableToPromise<IPatient>(this.store.PatientProfile.create(createPatientProfilePostData)))
      .then(patient => newPatientDetails.patient.patient = patient)
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

    return Utils.convertObservableToPromise<postData.IPlanConsentPostData>(this.store.PlanConsentForm.create(consentForm))
      .then(() => newPatientDetails);
  }

  private deletePotentialPatientIfNeeded(newPatientDetails: INewPatientDetails, potentialPatientId: string): Promise<INewPatientDetails> {
    if (Utils.isNullOrWhitespace(potentialPatientId)) {
      return Promise.resolve(newPatientDetails);
    }

    return Utils.convertObservableToPromise(this.store.PotentialPatient.destroy(potentialPatientId))
      .then(() => Promise.resolve(newPatientDetails))
      .catch(error => this.catchError(`Failed to delete potential patient with id: '${potentialPatientId}'`, error, newPatientDetails));
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

  private loadRoles(): void {
    Utils.convertObservableToPromise(this.store.ProviderRole.readListPaged())
      .then((roles: Array<IRole>) => {
        this.careManagerRole = roles.filter(x => x.name === 'Care Manager' || x.name === 'Care Team Manager')[0];
        this.billingPractitionerRole = roles.filter(x => x.name === 'Billing Practitioner')[0];
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

  private openEnrollment_PotentialPatientAddedModal(potentialPatient: IPotentialPatient, potentialPatientId?: string): Promise<IPatientEnrollmentResponse> {
    potentialPatientId = this.getPotentialPatientId(potentialPatient, null, potentialPatientId);

    if (!Utils.isNullOrWhitespace(potentialPatientId)) {
      return Promise.resolve({ potentialPatient, potentialPatientId });
    }

    return this
      .openModal(576, potentialPatient, EnrollmentPotentialPatientAddedComponent)
      .then(() => ({ potentialPatient, potentialPatientId }));
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

  private openModal<TComponent, TData>(width: number, data: TData, component: TComponent): Promise<IPatientEnrollmentModalResponse> {
    const modalData = {
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
    return this
      .createOrUpdatePotentialPatient(modalResponse.newPatientDetails)
      .then(potentialPatient => {
        if (!Utils.isNullOrUndefined(potentialPatient)) {
          return this.openEnrollment_PotentialPatientAddedModal(potentialPatient, potentialPatientId);
        }

        return Promise.resolve(null);
      });
  }

  private updatePhoneIfNeeded(newPatientDetails: INewPatientDetails): Promise<INewPatientDetails> {
    const patient = newPatientDetails.patient.patient as IPatient;

    if (Utils.isNullOrUndefined(patient)) {
      return Promise.resolve(newPatientDetails);
    }

    const hasSelectedPatientThatUpdatedThePhoneNumber =
      !Utils.isNullOrUndefined(patient)
      && !Utils.isNullOrUndefined(patient.user)
      && !patient.user.hasOwnProperty('patient_profile')
      && newPatientDetails.phoneNumber !== patient.user.phone;

    if (!hasSelectedPatientThatUpdatedThePhoneNumber) {
      return Promise.resolve(newPatientDetails);
    }

    let phone = patient.user.phone;
    phone = Utils.isNullOrWhitespace(phone) || phone.trim() === '-' ? null : phone;
    const postData = { phone: phone };
    return Utils
      .convertObservableToPromise(this.store.User.update(patient.user.id, postData))
      .then((user: IUser) => {
        if (Utils.isNullOrUndefined(user)) {
          console.warn('Failed to return an expected user object');
        }

        return newPatientDetails;
      });
  }

  private getOrCreateUserId(newPatientDetails: INewPatientDetails): Promise<string> {
    return this
      .getUserIfEmailMatches(newPatientDetails.email)
      .then((user: IUser) => {
        if (!Utils.isNullOrUndefined(user) && !Utils.isNullOrWhitespace(user.id)) {
          return user.id;
        }

        const createUserPostData: postData.ICreateUserPostData = {
          email: newPatientDetails.email,
          first_name: newPatientDetails.firstName,
          last_name: newPatientDetails.lastName,
          password1: this.pw,
          password2: this.pw
        };

        return Utils
          .convertObservableToPromise<{ pk: string }>(this.store.AddUser.createAlt(createUserPostData))
          .then((user: { pk: string }) => {
            console.log('userCreated', user);
            return user.pk;
          });
      });
  }

  private getUserIfEmailMatches(email: string): Promise<IUser> {
    if (Utils.isNullOrWhitespace(email)) {
      return Promise.resolve(null);
    }

    email = email.toLowerCase().trim();
    return Utils
      .convertObservableToPromise(this.store.PatientProfile.readListPaged())
      .then((patients: Array<IPatient>) => patients
        .filter(x => !Utils.isNullOrUndefined(x.user) && !Utils.isNullOrWhitespace(x.user.email))
        .map(x => ({ email: x.user.email.trim().toLowerCase(), user: x.user }))
      )
      .then((users: Array<{ email: string, user: IUser }>) => {
        const user = users.find(x => x.email === email);
        if (Utils.isNullOrUndefined(user)) {
          return null;
        }

        return user.user;
      });
  }
}
