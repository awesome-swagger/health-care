import { Injectable } from '@angular/core';

import { StoreService } from './store.service';
import { Utils } from '../utils';

import { IDiagnoses } from '../models/diagnoses';
import { IDiagnosis } from '../models/diagnosis';
import { IEmployee } from '../models/employee';
import { INewPatientDetails } from '../models/new-patient-details';
import { IPatient } from '../models/patient';
import { IPatientProfileCarePlans } from '../models/patient-profile-careplans';
import { IPotentialPatient } from '../models/potential-patient';
import { IRole } from '../models/role';

@Injectable()
export class PatientCreationService {
  public billingPractitionerRole: IRole = null;
  public billingPractitioners: Array<ISearchableEmployee>;
  public careManagerRole: IRole = null;
  public careManagers: Array<ISearchableEmployee>;
  public employeesLoaded = false;

  constructor(
    private store: StoreService
  ) {
    this.loadRoles();
  }

  private filterAndConvertToSearchableEmployee(employees: Array<IEmployee>, searchForBillingManager: boolean): Array<ISearchableEmployee> {
    employees = employees || [];
    const filtered = searchForBillingManager
      ? employees.filter(x => Utils.isNullOrTrueValue(x.qualified_practitioner))
      : employees.filter(x => (x.roles || []).filter(r => r.id === (this.careManagerRole || {}).id).length > 0);

    return filtered.map<ISearchableEmployee>(e => ({ searchableName: `${(e.user || {}).first_name} ${(e.user || {}).last_name}`.trim().toLowerCase(), ...e }));
  }

  public getPatientDiagnoses(facilityId: string, diagnosesIds: Array<string>): Promise<Array<IDiagnoses>> {
    const collection: Array<IDiagnoses> = [];
    if (Utils.isNullOrEmptyCollection(diagnosesIds)) {
      return Promise.resolve(collection);
    }

    const promises: Array<Promise<number>> = [];
    const promise = new Promise<Array<IDiagnoses>>(resolve => {
      diagnosesIds.forEach(diagnosesId => {
        const p = this
          .getDiagnosesFromServer(facilityId, diagnosesId)
          .then((diagnoses: IDiagnoses) => Utils.isNullOrUndefined(diagnoses) ? null : collection.push(diagnoses));

        promises.push(p);
      });

      Promise
        .all(promises)
        .then(() => resolve(collection));
    });

    return promise;
  }

  private getDiagnosesFromServer(facilityId: string, diagnosisId: string): Promise<IDiagnoses> {
    return Utils
      .convertObservableToPromise(this.store.PatientDiagnosis.read(diagnosisId))
      .then((diagnoses: IDiagnoses) => diagnoses.facility === facilityId ? diagnoses : null)
      .then((diagnoses: IDiagnoses) => this.getDiagnosisFromServer(diagnoses));
  }

  private getDiagnosisFromServer(diagnoses: IDiagnoses): Promise<IDiagnoses> {
    if (Utils.isNullOrUndefined(diagnoses)) {
      return Promise.resolve(null);
    }

    return Utils
      .convertObservableToPromise(this.store.Diagnosis.read(diagnoses.diagnosis))
      .then((diagnosis: IDiagnosis) => diagnoses.diagnosis_object = diagnosis)
      .then(() => diagnoses);
  }

  /**
   * Returns a value indicating whether the patient id specified is currently enrolled in the selected plan
   * @param patient - Either a Potential or existing patient selected by user
   * @param serviceAreaId - The selected service area id
   * @param carePlanId - The selected care plan id 
   */
  public isPatientAlreadyEnrolledInPlan(patient: IPotentialPatient | IPatient, serviceAreaId: string, carePlanId: string): Promise<boolean> {
    patient = patient || {};
    const patientId = patient.id;
    if (
      !patient.hasOwnProperty('user')
      || Utils.isNullOrWhitespace(patientId)
      || Utils.isNullOrWhitespace(serviceAreaId)
      || Utils.isNullOrWhitespace(carePlanId)
    ) {
      return Promise.resolve(false);
    }

    return Utils.convertObservableToPromise<Array<IPatientProfileCarePlans>>(this.store.PatientProfile.detailRoute('get', patientId, 'care_plans'))
      .then((patientCarePlans: Array<IPatientProfileCarePlans>) => {
        const existingPlan = patientCarePlans.filter(x =>
          !Utils.isNullOrUndefined(x.plan_template)
          && !Utils.isNullOrUndefined(x.plan_template.service_area)
          && x.plan_template.id === carePlanId
          && x.plan_template.service_area.id === serviceAreaId
        );

        return existingPlan.length >= 1;
      });
  }

  /**
   * Returns a value indicating whether forms current state is valid for enrolling/saving a patient in the system
   * @param newPatientDetails - Details from the form regarding the patient enrollment
   * @param validateOnlyPatientDetails A value indicating that only the patient details should be validated at this time. (False by default)
   */
  public isValidForEnrollment(newPatientDetails: INewPatientDetails, validateOnlyPatientDetails: boolean = false): boolean {
    if (!newPatientDetails.checked.enroll || Utils.isNullOrUndefined(newPatientDetails.careManager)) {
      return false;
    }

    if (!validateOnlyPatientDetails && newPatientDetails.checked.reimburses) {
      if (
        Utils.isNullOrUndefined(newPatientDetails.insurance)
        || Utils.isNullOrUndefined(newPatientDetails.planType)
        || Utils.isNullOrUndefined(newPatientDetails.billingPractioner)
      ) {
        return false;
      }

      if (
        (newPatientDetails.planType.acronym === 'CCM' || newPatientDetails.planType.acronym === 'CCCM')
        && (newPatientDetails.diagnoses || []).filter(d => d.is_chronic).length < 2
      ) {
        return false;
      }
    }

    return this.isValidPotentialPatientDetails(newPatientDetails);
  }

  /**
   * Returns a value indicating whether the new patient details is valid at the current state
   * @param newPatientDetails - Patient details to be validated
   */
  public isValidPotentialPatientDetails(newPatientDetails: INewPatientDetails): boolean {
    return (
      !Utils.isNullOrWhitespace(newPatientDetails.firstName)
      && !Utils.isNullOrWhitespace(newPatientDetails.lastName)
      && !Utils.isNullOrWhitespace(newPatientDetails.phoneNumber)
      && Utils.isValidEmail(newPatientDetails.email)
      && !Utils.isNullOrUndefined(newPatientDetails.carePlan)
      && !Utils.isNullOrUndefined(newPatientDetails.facility)
      && !Utils.isNullOrWhitespace(newPatientDetails.source)
    );
  }

  private loadRoles(): void {
    Utils.convertObservableToPromise(this.store.ProviderRole.readListPaged())
      .then((roles: Array<IRole>) => this.setRoles(roles))
      .then(() => Utils.convertObservableToPromise(this.store.EmployeeProfile.readListPaged()))
      .then((employees: Array<IEmployee>) => this.setEmployees(employees));
  }

  /**
   * Search all billing practitioner names that match the specified text
   * @param searchText - Search text to match against
   */
  public searchBillingPractitioners(searchText: string): Array<IEmployee> {
    return this.searchEmployeeCollection(this.careManagers, searchText);
  }

  /**
   * Search all care manager names that match the specified text
   * @param searchText - Search text to match against
   */
  public searchCareManagers(searchText: string): Array<IEmployee> {
    return this.searchEmployeeCollection(this.careManagers, searchText);
  }

  private searchEmployeeCollection(collection: Array<ISearchableEmployee>, searchText: string): Array<IEmployee> {
    if (Utils.isNullOrWhitespace(searchText) || searchText.length < 3) {
      return null;
    }

    const match = searchText.toLowerCase();
    return collection.filter(e => e.searchableName.indexOf(match) > -1);
  }

  private setEmployees(employees: Array<IEmployee>): void {
    this.careManagers = this.filterAndConvertToSearchableEmployee(employees, false);
    this.billingPractitioners = this.filterAndConvertToSearchableEmployee(employees, true);
    this.employeesLoaded = true;
  }

  private setRoles(roles: Array<IRole>): void {
    const toLower = (val: string) => (val || '').toLowerCase();
    const filter = (opt1: string, opt2: string) => roles.find(x => {
      const name = toLower(x.name);
      return name === toLower(opt1) || name === toLower(opt2);
    });

    this.careManagerRole = filter('care manager', 'care team manager');
    this.billingPractitionerRole = filter('qualified practitioner', 'billing practitioner');
  }
}

interface ISearchableEmployee extends IEmployee {
  searchableName?: string;
}
