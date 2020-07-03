import { Component, OnInit } from "@angular/core";
import * as moment from 'moment';
import { cloneDeep } from 'lodash';

import { AuthService, StoreService } from "../../../services";
import { ModalService } from "../../../modules/modals";
import { PatientCreationService } from '../../../services/patient-creation.service';
import { Utils } from "../../../utils";

import { IApiResultsContainer } from "../../../models/api-results-container";
import { IBillingType } from "../../../models/billing_type";
import { ICarePlanRoles } from "../../../models/care-plan-roles";
import { IDiagnoses } from "../../../models/diagnoses";
import { IDiagnosis } from "../../../models/diagnosis";
import { IEmployee } from "../../../models/employee";
import { IFacility } from "../../../models/facility";
import { IFilteredResults } from "../../../models/filtered-results";
import { IHaveId } from "../../../models/ihave-id";
import { IInsurance } from "../../../models/insurance";
import { INewPatientDetails } from "../../../models/new-patient-details";
import { IOrganization } from "../../../models/organization";
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from "../../../models/patient-enrollment-modal-response";
import { IPotentialPatientEnrollmentDetailsComponentInitialData } from "../../../models/potential-patient-enrollment-details-component-initial-data";
import { IRole } from "../../../models/role";
import { ITypeahead } from "../../../models/typeahead";

@Component({
  selector: 'app-enrollment-details',
  templateUrl: './enrollment-details.component.html',
  styleUrls: ['./enrollment-details.component.scss'],
})
export class EnrollmentDetailsComponent implements OnInit {
  /** This should only be used for the initial data load then you should be using the internal newPatientDetails */
  public data: IPotentialPatientEnrollmentDetailsComponentInitialData;

  public billingTypes: Array<IBillingType>;
  public carePlanRoles: ICarePlanRoles = { display: 'None', open: false, roleIds: [], roles: {}, selectedIds: {} };
  public diagnoses: Array<IDiagnosis>;
  public diagnosesAction: ('add' | 'edit');
  public editingDiagnoses?: IDiagnoses;
  public employee: IEmployee;
  public filters: IFilteredResults = { billingPractioner: { array: [], search: '' }, careManager: { array: [], search: '' }, diagnosis: { array: [], search: '' } };
  public insurances: Array<IInsurance> = [];
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Cancel, step: PatientCreationStep.EnrollementDetails };
  public newPatientDetails: INewPatientDetails;
  public typeahead: ITypeahead = { billingPractioner: '', careManager: '', diagnosis: '' };

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private store: StoreService,
    public patientCreationService: PatientCreationService,
  ) {
    // Nothing here
  }

  public ngOnInit(): void {
    this.data = this.data || {};
    this.newPatientDetails = this.data.newPatientDetails || { carePlanRoles: {}, checked: { enroll: true, reimburses: false }, diagnoses: [], patient: { isPotential: true, isPreload: true } };
    if (!Utils.isNullOrUndefined(this.data.potentialPatient)) {
      const patient = this.data.potentialPatient;
      this.newPatientDetails.patient.patient = patient;

      Utils.convertObservableToPromise(this.store.Facility.readListPaged())
        .then((facilities: Array<IFacility>) => {
          facilities = facilities || [];
          this.newPatientDetails.facility = facilities.find(f => f.id === patient.facility[0]);
        });

      this.newPatientDetails.carePlan = patient.care_plan;
      this.newPatientDetails.checked.enroll = true;
      this.newPatientDetails.email = patient.email;
      this.newPatientDetails.firstName = patient.first_name;
      this.newPatientDetails.lastName = patient.last_name;
      this.newPatientDetails.phoneNumber = patient.phone;
      this.newPatientDetails.serviceArea = (patient.care_plan || {}).service_area;
      this.newPatientDetails.source = patient.source;
    }

    this.setEmployee('careManager', this.newPatientDetails.careManager);
    this.setEmployee('billingPractioner', this.newPatientDetails.billingPractioner);
    this.loadBillingTypes();
    this.loadInsurances();
    this.loadRoles();
    Utils.convertObservableToPromise(this.store.Diagnosis.readListPaged()).then((diagnoses: Array<IDiagnosis>) => this.diagnoses = diagnoses);
    Utils.convertObservableToPromise(this.auth.user$).then((user: IEmployee) => this.employee = user);
  }

  public addDiagnoses(): void {
    if (this.diagnosesAction === 'edit') {
      // Editing existing diagnoses
      this.editingDiagnoses.isModified = true;
      this.editingDiagnoses.date_identified = moment().format('YYYY-MM-DD');
      this.editingDiagnoses.diagnosing_practitioner = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
      this.editingDiagnoses.diagnosis_object = cloneDeep(this.newPatientDetails.diagnosis);
      this.editingDiagnoses.facility = this.newPatientDetails.facility.id;
      this.editingDiagnoses.is_chronic = this.newPatientDetails.chronic;
    } else {
      // Adding new diagnoses
      const diagnoses = {
        date_identified: moment().format('YYYY-MM-DD'),
        diagnosing_practitioner: `${this.employee.user.first_name} ${this.employee.user.last_name}`,
        diagnosis: this.newPatientDetails.diagnosis.id,
        diagnosis_object: cloneDeep(this.newPatientDetails.diagnosis),
        facility: this.newPatientDetails.facility.id,
        is_chronic: this.newPatientDetails.chronic,
        patient: (this.newPatientDetails.patient.patient || {}).id,
        type: 'N/A',
      };

      this.newPatientDetails.diagnoses.push(diagnoses);
    }

    this.unselectDiagnosis();
  }

  public carePlanRolesChanged(selected: boolean, roleId: string): void {
    let role = this.carePlanRoles.roles[roleId];
    (this.newPatientDetails.carePlanRoles[roleId] = this.newPatientDetails.carePlanRoles[roleId] || { role, selected }).selected = selected;
    if (!selected) {
      delete this.carePlanRoles.selectedIds[roleId];
    }

    const roleIds = Object.keys(this.carePlanRoles.selectedIds);
    if (roleIds.length === 0) {
      this.carePlanRoles.display = 'None';
      return;
    }

    if (roleIds.length === this.carePlanRoles.roleIds.length) {
      this.carePlanRoles.display = 'All';
      return;
    }

    const roleNames: Array<string> = [];
    for (let roleId of roleIds) {
      if (Utils.isNullOrUndefined(this.carePlanRoles.roles[roleId])) {
        continue;
      }

      role = this.carePlanRoles.roles[roleId];
      roleNames.push(role.name);
    }

    this.carePlanRoles.display = roleNames.sort().join(', ');
  }

  public compareFn(obj1: IHaveId | string, obj2: IHaveId | string): boolean {
    return Utils.areEqual(obj1, obj2);
  }

  public deleteDiagnoses(diagnoses: IDiagnoses, index: number): void {
    if (Utils.isNullOrUndefined(diagnoses) || index < -1 || index >= this.newPatientDetails.diagnoses.length) {
      return;
    }

    if (Utils.isNullOrWhitespace(diagnoses.id)) {
      this.newPatientDetails.diagnoses.splice(index, 1);
    } else {
      diagnoses.hidden = true;
    }
  }

  public editDiagnoses(diagnoses: IDiagnoses, index: number): void {
    if (Utils.isNullOrUndefined(diagnoses) || index < -1 || index >= this.newPatientDetails.diagnoses.length) {
      return;
    }

    diagnoses.hidden = true;
    this.editingDiagnoses = diagnoses;
    this.newPatientDetails.diagnosis = cloneDeep(this.editingDiagnoses.diagnosis_object);
    this.typeahead.diagnosis = this.editingDiagnoses.diagnosis_object.name;
    this.filters.diagnosis.array = [];
    this.filters.diagnosis.search = '';
    this.newPatientDetails.chronic = this.editingDiagnoses.is_chronic;
    this.diagnosesAction = 'edit';
  }

  public get isValidPotentialPatient(): boolean {
    return this.patientCreationService.isValidForEnrollment(this.newPatientDetails);
  }

  private loadBillingTypes(): void {
    Utils
      .convertObservableToPromise(this.store.BillingType.readListPaged())
      .then((billingTypes: Array<IBillingType>) => this.billingTypes = billingTypes.map(b => ({ isChronic: b.acronym === 'CCCM' || b.acronym === 'CCM', ...b })));
  }

  private loadInsurances(): void {
    Utils.convertObservableToPromise(this.auth.organization$)
      .then((org: IOrganization) => {
        if (Utils.isNullOrUndefined(org)) {
          return;
        }

        Utils.convertObservableToPromise(this.store.Organization.detailRoute('GET', org.id, 'insurances'))
          .then((response: IApiResultsContainer<Array<IInsurance>>) => this.insurances = response.results);
      });
  }

  private loadRoles(): void {
    this.newPatientDetails.carePlanRoles = this.newPatientDetails.carePlanRoles || {};
    Utils.convertObservableToPromise(this.store.ProviderRole.readListPaged())
      .then((roles: Array<IRole>) => {
        for (let role of roles) {
          const selected = !Utils.isNullOrUndefined(this.newPatientDetails.carePlanRoles[role.id]) && Utils.isTrueValue(this.newPatientDetails.carePlanRoles[role.id].selected);
          this.carePlanRoles.roleIds.push(role.id);
          this.carePlanRoles.roles[role.id] = role;
          this.newPatientDetails.carePlanRoles[role.id] = this.newPatientDetails.carePlanRoles[role.id] || { role, selected };
        }
      });
  }

  public move(option: 'Back' | 'Cancel' | 'Later' | 'Next'): void {
    if (option !== 'Cancel') {
      this.modalResponse.newPatientDetails = this.newPatientDetails;
    }

    this.modalResponse.action = PatientCreationAction[option];
    this.modals.close(this.modalResponse);
  }

  public openDiagnosesForm(): void {
    this.diagnosesAction = 'add';
  }

  public searchDiagnoses(): void {
    this.newPatientDetails.diagnosis = null;
    if (this.typeahead.diagnosis.length < 3 || this.typeahead.diagnosis === this.filters.diagnosis.search) {
      return;
    }

    this.filters.diagnosis.search = this.typeahead.diagnosis;
    const match = this.typeahead.diagnosis.toLowerCase();
    this.filters.diagnosis.array = this.diagnoses.filter(d => d.name.toLowerCase().indexOf(match) > -1);
  }

  public searchEmployeeCollection(searchCareManager: boolean): void {
    const prop = searchCareManager
      ? 'careManager'
      : 'billingPractioner';
    const searchProp = searchCareManager
      ? 'searchCareManagers'
      : 'searchBillingPractitioners';

    this.newPatientDetails[prop] = null;
    if (this.typeahead[prop].length < 3 || this.typeahead[prop] === this.filters[prop].search) {
      return;
    }

    this.filters[prop].search = this.typeahead[prop];
    this.filters[prop].array = this.patientCreationService[searchProp](this.typeahead[prop]);
  }

  public setDiagnosis(diagnosis: IDiagnosis): void {
    this.newPatientDetails.diagnosis = diagnosis;
    this.typeahead.diagnosis = diagnosis.name;
  }

  public setEmployee(employeeType: ('careManager' | 'billingPractioner'), employee: IEmployee): void {
    if (Utils.isNullOrUndefined(employee)) {
      return;
    }

    this.newPatientDetails[employeeType] = employee;
    this.typeahead[employeeType] = `${employee.user.first_name} ${employee.user.last_name}`;
  }

  public toggleAllCarePlanRoles(checked: boolean): void {
    if (checked) {
      this.carePlanRoles.display = 'All';
    } else {
      this.carePlanRoles.selectedIds = {};
      this.carePlanRoles.display = 'None';
    }

    this.carePlanRoles.roleIds.forEach(roleId => {
      (this.newPatientDetails.carePlanRoles[roleId] = this.newPatientDetails.carePlanRoles[roleId] || { role: this.carePlanRoles.roles[roleId], selected: checked }).selected = checked;
      if (checked) {
        this.carePlanRoles.selectedIds[roleId] = checked;
      }
    });

    this.carePlanRoles.open = false;
  }

  public unselectDiagnosis(): void {
    if (!Utils.isNullOrUndefined(this.editingDiagnoses)) {
      this.editingDiagnoses.hidden = false;
      this.editingDiagnoses = null;
    }

    this.diagnosesAction = null;
    this.newPatientDetails.diagnosis = null;
    this.newPatientDetails.chronic = null;
    this.typeahead.diagnosis = '';
  }
}
