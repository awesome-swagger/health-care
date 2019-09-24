import { Component, OnInit } from "@angular/core";
import { uniqWith } from 'lodash';

import { ModalService } from "../../../modules/modals";
import { PatientCreationService } from "../../../services/patient-creation.service";
import { StoreService } from "../../../services";
import { Utils } from "../../../utils";

import { IAddPatientToPlanComponentData } from "../../../models/add-patient-to-plan-component-data";
import { IBasicUser } from "../../../models/basic-user";
import { ICarePlan } from "../../../models/care-plan";
import { IEmployee } from "../../../models/employee";
import { IFacility } from "../../../models/facility";
import { IFilteredResults } from "../../../models/filtered-results";
import { IHaveId } from "../../../models/ihave-id";
import { INewPatientDetails } from "../../../models/new-patient-details";
import { IPatient } from '../../../models/patient';
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from "../../../models/patient-enrollment-modal-response";
import { IPotentialPatient } from "../../../models/potential-patient";
import { ISearchablePatient } from "../../../models/searchable-patient";
import { IServiceArea } from "../../../models/service-area";
import { ITypeahead } from "../../../models/typeahead";
import { IDiagnoses } from "../../../models/diagnoses";

@Component({
  selector: 'app-enrollment-potential-patient-details',
  templateUrl: './enrollment-potential-patient-details.component.html',
  styleUrls: ['./enrollment-potential-patient-details.component.scss'],
})
export class EnrollmentPotentialPatientDetailsComponent implements OnInit {
  public alreadyEnrolled: boolean = false;
  public careManagerPlaceHolder = 'Loading...';
  public carePlans: Array<ICarePlan>;
  public data: IAddPatientToPlanComponentData;
  public facilities: Array<IFacility> = [];
  public filteredCarePlans: Array<ICarePlan>;
  public filteredFacilities: Array<IFacility>;
  public filters: IFilteredResults = { careManager: { array: [], search: '' }, patients: { array: [], search: '' } };
  public matchingPatient: ISearchablePatient;
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Cancel, step: PatientCreationStep.PotentialPatientDetails };
  public newPatientDetails: INewPatientDetails = { carePlanRoles: {}, checked: {}, diagnoses: [], patient: { isPotential: false, isPreload: false } };
  public patients: Array<IPatient> = [];
  public potentialPatients: Array<IPotentialPatient> = [];
  public searchablePatients: Array<ISearchablePatient> = [];
  public serviceAreas: Array<IServiceArea> = [];
  public typeahead: ITypeahead = { careManager: '', patient: '' };

  constructor(
    private modals: ModalService,
    public patientCreationService: PatientCreationService,
    private store: StoreService,
  ) {
    // Nothing yet
  }

  public ngOnInit(): void {
    this.data = this.data || {};

    let facilityId: string;
    if (!Utils.isNullOrUndefined(this.data.newPatientDetails)) {
      this.newPatientDetails = this.data.newPatientDetails;
      this.setPhone();
      facilityId = (this.data.newPatientDetails.facility || {}).id;
      if (!Utils.isNullOrUndefined(this.newPatientDetails.careManager) && !Utils.isNullOrUndefined(this.newPatientDetails.careManager.user)) {
        this.typeahead.careManager = `${this.newPatientDetails.careManager.user.first_name} ${this.newPatientDetails.careManager.user.last_name}`;
      }
    } else {
      facilityId = ((this.data.potentialPatient || {}).facility || [null])[0] || ((this.data.facility || { id: null }).id);
      const patient: ISearchablePatient = this.convertToSearchablePatient(this.data.potentialPatient || this.data.patient);
      this.setPatient(patient, true);
    }

    Promise.all([
      this.loadPatients(facilityId),
      this.loadPotentialPatients(facilityId)
    ]).then(() => {
      this.searchablePatients = [
        ...this.patients.map<ISearchablePatient>(this.convertToSearchablePatient),
        ...this.potentialPatients.map<ISearchablePatient>(this.convertToSearchablePatient)
      ];
    });

    this.loadFacilities(facilityId);
    this.loadCarePlansAndServiceAreas(this.data.carePlan || (this.data.potentialPatient || {}).care_plan);
  }

  public cancel(): void {
    this.modals.close(this.modalResponse);
  }

  public clearEmail(): void {
    this.matchingPatient = null;
    this.newPatientDetails.email = null;
  }

  public compareFn(obj1: IHaveId | string, obj2: IHaveId | string): boolean {
    return Utils.areEqual(obj1, obj2);
  }

  private convertToSearchablePatient(patient: IPatient | IPotentialPatient): ISearchablePatient {
    patient = patient || {};

    if (patient.hasOwnProperty('care_plan')) {
      const p = patient as IPotentialPatient;
      const name = `${p.first_name} ${p.last_name}`.trim();
      return <ISearchablePatient>{
        email: (p.email || '').toLowerCase(),
        id: p.id,
        image: null,
        isPotentialPatient: true,
        name: name,
        nameLower: name.toLowerCase(),
        patient: p
      };
    }

    if (patient.hasOwnProperty('user')) {
      const p = patient as IPatient;
      const name = `${p.user.first_name} ${p.user.last_name}`.trim();
      return <ISearchablePatient>{
        email: (p.user.email || '').toLowerCase(),
        id: p.id,
        image: p.user.image,
        isPotentialPatient: false,
        name: name,
        nameLower: name.toLowerCase(),
        patient: p
      };
    }

    return null;
  }

  public get isValidPotentialPatientForm(): boolean {
    return this.patientCreationService.isValidPotentialPatientDetails(this.newPatientDetails);
  }

  public get isValidForSaveOrNext(): boolean {
    return this.patientCreationService.isValidForEnrollment(this.newPatientDetails, true);
  }

  private loadCarePlansAndServiceAreas(preloadedCarePlan: ICarePlan = null): void {
    const hasPlan = !Utils.isNullOrUndefined(preloadedCarePlan);
    const hasServiceArea = hasPlan && !Utils.isNullOrUndefined(preloadedCarePlan.service_area);
    if (hasPlan) {
      this.newPatientDetails.carePlan = preloadedCarePlan;
    }

    if (hasServiceArea) {
      this.newPatientDetails.serviceArea = preloadedCarePlan.service_area;
    }

    const plansLoaded = Utils.convertObservableToPromise(this.store.CarePlanTemplate.readListPaged())
      .then((carePlans: Array<ICarePlan>) => this.carePlans = carePlans);

    const serviceAreasLoaded = Utils.convertObservableToPromise(this.store.ServiceArea.readListPaged())
      .then((serviceAreas: Array<IServiceArea>) => this.serviceAreas = serviceAreas);

    Promise.all([plansLoaded, serviceAreasLoaded])
      .then(() => {
        this.serviceAreas.forEach(s => s.uiCarePlans = this.carePlans.filter(x => x.service_area.id === s.id));
        this.updateFilteredCarePlan();
      });
  }

  private loadFacilities(facilityId: string): void {
    Utils.convertObservableToPromise(this.store.Facility.readListPaged())
      .then((facilities: Array<IFacility>) => {
        this.facilities = facilities || [];
        this.filteredFacilities = this.facilities.filter(x => !x.is_affiliate);
        if (!Utils.isNullOrWhitespace(facilityId)) {
          this.newPatientDetails.facility = this.facilities.find(f => f.id === facilityId);
        }
      });
  }

  private loadPatients(facilityId: string): Promise<void> {
    return Utils.convertObservableToPromise(this.store.PatientProfile.readListPaged())
      .then((patients: Array<IPatient>) => {
        patients = patients || [];
        this.patients = !Utils.isNullOrWhitespace(facilityId)
          ? patients.filter(p => p.facility.id === facilityId)
          : patients;
      });
  }

  public loadPatientFacilityDiagnoses(): void {
    if (Utils.isNullOrUndefined(this.newPatientDetails.patient.patient)) {
      return;
    }

    this.patientCreationService
      .getPatientDiagnoses(this.newPatientDetails.facility.id, (this.newPatientDetails.patient.patient as IPatient).diagnosis)
      .then((diagnoses: Array<IDiagnoses>) => this.newPatientDetails.diagnoses = diagnoses);
  }

  private loadPotentialPatients(facilityId: string): Promise<void> {
    return Utils.convertObservableToPromise(this.store.PotentialPatient.readListPaged())
      .then((potentialPatients: Array<IPotentialPatient>) => {
        potentialPatients = potentialPatients || [];
        this.potentialPatients = uniqWith<Array<IPotentialPatient>>(potentialPatients, (a, b) => a.first_name === b.first_name && a.last_name === b.last_name);
        if (!Utils.isNullOrWhitespace(facilityId)) {
          this.potentialPatients = this.potentialPatients.filter(p => p.facility[0] === facilityId);
        }
      });
  }

  public save(): void {
    if (!this.isValidPotentialPatientForm) {
      return;
    }

    this.modalResponse.newPatientDetails = this.newPatientDetails;
    this.modalResponse.action = this.newPatientDetails.checked.enroll
      ? PatientCreationAction.Next
      : PatientCreationAction.Complete;

    this.modals.close(this.modalResponse);
  }

  public searchCareManagers(): void {
    this.newPatientDetails.careManager = null;
    if (this.typeahead.careManager.length < 3 || this.typeahead.careManager === this.filters.careManager.search) {
      return;
    }

    this.filters.careManager.search = this.typeahead.careManager;
    this.filters.careManager.array = this.patientCreationService.searchCareManagers(this.typeahead.careManager);
  }

  public searchPatients(): void {
    if (this.typeahead.patient.length < 3 || this.typeahead.patient === this.filters.patients.search) {
      return;
    }

    this.filters.patients.search = this.typeahead.patient;
    const lowerSearchText = this.typeahead.patient.toLowerCase();
    this.filters.patients.array = Utils.sort(this.searchablePatients.filter(u => u.nameLower.indexOf(lowerSearchText) > -1), true, 'nameLower');
  }

  public setCareManager(employee: IEmployee): void {
    this.newPatientDetails.careManager = employee;
    this.typeahead.careManager = `${employee.user.first_name} ${employee.user.last_name}`;
  }

  public setMatchingPatient(): void {
    this.setPatient(this.matchingPatient);
    this.matchingPatient = null;
  }

  public setPatient(selectedPatient: ISearchablePatient, isPreload: boolean = false): void {
    if (Utils.isNullOrUndefined(selectedPatient)) {
      return;
    }

    this.newPatientDetails.name = selectedPatient.name;
    this.newPatientDetails.patient = {
      isPotential: selectedPatient.isPotentialPatient,
      isPreload,
      patient: selectedPatient.patient
    };

    let user: IBasicUser = null;

    if (selectedPatient.isPotentialPatient) {
      const patient = selectedPatient.patient as IPotentialPatient;
      const firstFacility = (patient.facility || [''])[0];
      this.newPatientDetails.facility = this.facilities.find(f => f.id === firstFacility);
      user = patient;
    } else {
      const patient = selectedPatient.patient as IPatient;
      this.newPatientDetails.facility = patient.facility;
      user = patient.user;

      this.loadPatientFacilityDiagnoses();
    }

    this.setPhone(user);
    this.newPatientDetails.email = user.email;
    this.newPatientDetails.firstName = user.first_name;
    this.newPatientDetails.lastName = user.last_name;
    this.newPatientDetails.source = user.source;
    this.verifyPatientPlanEnrollment();
  }

  private setPhone(user: IBasicUser = {}): void {
    const phone = this.newPatientDetails.phoneNumber || user.phone;
    this.newPatientDetails.phoneNumber = Utils.isNullOrWhitespace(phone) || phone.trim() === '-' ? null : phone;
  }

  public unselectPatient(): void {
    for (let prop in this.typeahead) {
      this.typeahead[prop] = '';
    }

    for (let prop in this.filters) {
      this.filters[prop].array = [];
      this.filters[prop].search = null;
    }

    this.alreadyEnrolled = false;
    const npd = this.newPatientDetails;
    npd.name = null;
    npd.email = null;
    npd.firstName = null;
    npd.lastName = null;
    npd.source = null;
    npd.patient = { isPotential: false, isPreload: false, patient: null };
    npd.diagnoses = [];

    if (Utils.isNullOrUndefined(this.data.facility) && Utils.isNullOrWhitespace(this.data.facilityId)) {
      npd.facility = null;
    }

    if (Utils.isNullOrUndefined(this.data.carePlan)) {
      npd.carePlan = null;
      npd.serviceArea = null;
    }
  }

  public updateFilteredCarePlan(clearCarePlan: boolean = false): void {
    if (clearCarePlan) {
      this.newPatientDetails.carePlan = null;
    }

    if (Utils.isNullOrEmptyCollection(this.carePlans) || Utils.isNullOrEmptyCollection(this.serviceAreas)) {
      return;
    }

    this.filteredCarePlans = (this.newPatientDetails.serviceArea || {}).uiCarePlans || [];

    if (Utils.isNullOrUndefined(this.newPatientDetails.carePlan)) {
      this.newPatientDetails.carePlan = this.filteredCarePlans[0];
    }
  }

  public verifyEmail(): void {
    if (Utils.isNullOrWhitespace(this.newPatientDetails.email)) {
      return;
    }

    this.matchingPatient = this.searchablePatients.find(p => p.email === this.newPatientDetails.email.toLowerCase());
    if (!Utils.isNullOrUndefined(this.matchingPatient)) {
      Utils.logDebug('Found matching patient', this.matchingPatient);
    }
  }

  public verifyPatientPlanEnrollment(): void {
    const serviceAreaId = (this.newPatientDetails.serviceArea || {}).id;
    const carePlanId = (this.newPatientDetails.carePlan || {}).id;

    this.patientCreationService
      .isPatientAlreadyEnrolledInPlan(this.newPatientDetails.patient.patient, serviceAreaId, carePlanId)
      .then((isEnrolled: boolean) => this.alreadyEnrolled = isEnrolled);
  }
}
