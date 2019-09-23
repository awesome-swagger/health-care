import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { compact as _compact, filter as _filter, find as _find, flattenDeep as _flattenDeep, map as _map, mean as _mean, sum as _sum, uniqBy as _uniqBy } from 'lodash';
import { Router, ActivatedRoute, Params } from '@angular/router';

import * as models from '../../../models/add-patient-models';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { PatientCreationModalService } from '../../../services/patient-creation-modal.service';
import { StoreService, AuthService } from '../../../services';
import { Utils, LogLevel } from '../../../utils';
import { UtilsService } from '../../../services';

import { IAddPatientToPlanComponentData } from '../../../models/add-patient-to-plan-component-data';
import { IApiResultsContainer } from '../../../models/api-results-container';
import { IEmployee } from '../../../models/employee';
import { IFacility } from '../../../models/facility';
import { IOrganization } from '../../../models/organization';
import { IPatientEnrollmentResponse } from '../../../models/patient-enrollment-modal-response';
import { IServiceArea } from '../../../models/service-area';
import { Subscription } from 'rxjs';
import { StringIndexable } from '../../../models/types';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {
  private authSub: Subscription = null;
  private orgSub: Subscription = null;
  private routeSub: Subscription = null;

  public average: models.ICarePlanAverage = null;
  public carePlanSearch: string = '';
  public carePlanTemplateChecked: StringIndexable<boolean> = {};
  public carePlanTemplates: Array<models.IPlanTemplate> = [];
  public employee: IEmployee = null;
  public employeeChecked: StringIndexable<boolean> = {};
  public employeeProfiles: Array<models.IEmployeeProfile> = [];
  public facilities: Array<models.IFacilityWithCarePlans> = [];
  public facilityOpen: StringIndexable<boolean> = {};
  public facilityPage: StringIndexable<number> = {};
  public facilityPageCount: StringIndexable<number> = {};
  public facilityTotal: StringIndexable<number> = {};
  public multi2Open: boolean = null;
  public multi3Open: boolean = null;
  public multi4Open: boolean = null;
  public openAlsoTip: StringIndexable<boolean> = {};
  public serviceAreaChecked: StringIndexable<boolean> = {};
  public serviceAreas: Array<IServiceArea> = [];
  public serviceAreaSearch: string = '';
  public toolAP1Open: boolean = null;
  public tooltip2Open: StringIndexable<boolean> = {};

  constructor(
    public auth: AuthService,
    public modals: ModalService,
    public patientCreationModalService: PatientCreationModalService,
    public route: ActivatedRoute,
    public router: Router,
    public store: StoreService,
    public utilsService: UtilsService
  ) {
    // Nothing yet
    Utils.minimumLoggingLevel = LogLevel.debug;
  }

  public ngOnInit(): void {
    this.authSub = this.auth.user$.subscribe((user: IEmployee) => {
      if (Utils.isNullOrUndefined(user)) {
        return;
      }

      this.employee = user;
      if ((user.facilities || []).length === 1) {
        this.facilityOpen[user.facilities[0].id] = true;
      }

      this.orgSub = this.auth.organization$.subscribe((organization: IOrganization) => {
        if (Utils.isNullOrUndefined(organization)) {
          return;
        }

        this.loadCarePlanAverage(organization.id);
        Utils.convertObservableToPromise<IApiResultsContainer<Array<IFacility>>>(this.store.Organization.detailRoute('GET', organization.id, 'facilities'))
          .then((facilities: IApiResultsContainer<Array<IFacility>>) => {
            this.facilities = facilities.results.filter(f => !f.is_affiliate);
            this.facilities = this.facilities.filter(f => user.facilities.find(fa => fa.id === f.id));

            this.facilities.forEach((facility) => {
              this.facilityOpen[facility.id] = false;
              this.facilityPage[facility.id] = 1;
              this.loadFacilityCarePlans(facility);
            });
          });

        Utils.convertObservableToPromise<Array<models.IEmployeeProfile>>(this.store.EmployeeProfile.readListPaged())
          .then((employeeProfiles) => {
            this.employeeProfiles = employeeProfiles;
            employeeProfiles.forEach((user) => this.employeeChecked[user.id] = true);
            this.routeSub = this.route.params.subscribe((params) => {
              if (!params) {
                return;
              }

              if (params.userId) {
                const ids = params.userId.split(',');
                employeeProfiles.forEach(user => this.employeeChecked[user.id] = false);
                ids.forEach(id => this.employeeChecked[id] = true);
                this.employeeChecked[params.userId] = true;
              }
            });
          });
      });
    });

    Utils.convertObservableToPromise(this.store.ServiceArea.readListPaged())
      .then((serviceAreas: Array<IServiceArea>) => {
        this.serviceAreas = serviceAreas;
        serviceAreas.forEach((area) => this.serviceAreaChecked[area.id] = true);
      });

    Utils.convertObservableToPromise(this.store.CarePlanTemplate.readListPaged())
      .then((templates: Array<models.IPlanTemplate>) => {
        this.carePlanTemplates = Utils.sort(templates.map(t => ({ ...t, sortName: t.name.toLowerCase() })), true, 'sortName');
        templates.forEach((template) => this.carePlanTemplateChecked[template.id] = true);
      });
  }

  private loadFacilityCarePlans(facility: models.IFacilityWithCarePlans): void {
    this.getFacilityCarePlans(facility.id)
      .then((carePlans: IApiResultsContainer<Array<models.IActivePatientCarePlans>>) => {
        facility.carePlans = carePlans.results;
        this.facilityTotal[facility.id] = carePlans.count;
        this.facilityPageCount[facility.id] = Math.ceil(carePlans.count / 20);
      });
  }

  public ngOnDestroy(): void {
    const unsubscribe = (sub: Subscription) => (sub || { unsubscribe: () => null }).unsubscribe();

    unsubscribe(this.authSub);
    unsubscribe(this.orgSub);
    unsubscribe(this.routeSub);
  }

  public loadCarePlanAverage(organizationId: string): void {
    const params = { patient__facility__organization: organizationId };
    Utils
      .convertObservableToPromise<models.ICarePlanAverage>(this.store.CarePlan.detailRoute('GET', null, 'average', {}, params))
      .then((average: models.ICarePlanAverage) => {
        average = average || {};
        average.average_engagement = average.average_engagement || 0;
        average.average_outcome = average.average_outcome || 0;
        average.risk_level = average.risk_level || 0;
        average.riskLevelText = this.utilsService.getRiskLevelText(average.risk_level);
        this.average = average;
      });
  }

  public getFacilityCarePlans(facilityId: string): Promise<IApiResultsContainer<Array<models.IActivePatientCarePlans>>> {
    const params = { page: this.facilityPage[facilityId] };
    return Utils
      .convertObservableToPromise<IApiResultsContainer<Array<models.IActivePatientCarePlans>>>(this.store.Facility.detailRoute('get', facilityId, 'care_plans', {}, params))
      .then((carePlans) => carePlans);
  }

  public progressInWeeks(plan: { created: moment.MomentInput, plan_template: { duration_weeks: number } }): number {
    if (!plan || !plan.created) {
      return 0;
    }

    const diff = moment().diff(moment(plan.created), 'weeks') + 1;
    if (diff < plan.plan_template.duration_weeks) {
      return diff;
    }

    return plan.plan_template.duration_weeks;
  }

  public get userFilterListText(): string {
    const checkedList = [];
    this.employeeProfiles.forEach(e => {
      if (this.employeeChecked[e.id]) {
        checkedList.push(e);
      }
    });

    if (checkedList.length === 0) {
      return 'None';
    }

    if (checkedList.length === this.employeeProfiles.length) {
      return 'All';
    }

    if (checkedList.length === 1) {
      return `${checkedList[0].user.first_name} ${checkedList[0].user.last_name}`
    }

    return `${checkedList[0].user.first_name} ${checkedList[0].user.last_name} (+${checkedList.length - 1})`
  }

  public confirmRemovePatient(facility: { id: string }, plan: { id: string }) {
    const modalData = {
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to remove this patient from this plan? This will negate their current progress. This cannot be undone.',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px',
    };

    this.modals.open(ConfirmModalComponent, modalData).subscribe((res) => {
      if (res === modalData.data.okText) {
        this.store.CarePlan.destroy(plan.id).subscribe(() => {
          const patientFacility = this.facilities.find(f => f.id === facility.id);
          patientFacility.carePlans = _filter(patientFacility.carePlans, p => p.id !== plan.id);
        });
      }
    });
  }

  public addPatientToPlan(facility: IFacility = null): void {
    const data: IAddPatientToPlanComponentData = {
      action: 'add',
      enrollPatientChecked: true,
      facility: facility
    };

    this.patientCreationModalService
      .openEnrollment_PotentialPatientDetails(data)
      .then((response: IPatientEnrollmentResponse) => {
        if (Utils.isNullOrUndefined((response || {}).patient)) {
          return;
        }

        document.dispatchEvent(new Event('refreshPatientOverview'));
        const facility = this.facilities.find(f => f.id === (response.patient.facility || {}).id);
        if (!Utils.isNullOrUndefined(facility)) {
          this.loadFacilityCarePlans(facility);
        }
      });
  }

  public routeToPatient(patient: { id: string }): void {
    this.router.navigate(['patient', patient.id]);
  }

  public formatTime(minutes: number): string {
    if (!minutes) {
      return '0:00';
    }

    const h = `${Math.floor(minutes / 60)}`;
    const m = `${minutes % 60}`;

    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`;
  }

  public toggleAllServiceAreas(status: boolean): void {
    Object.keys(this.serviceAreaChecked).forEach((area) => this.serviceAreaChecked[area] = status);
  }

  public toggleAllCarePlans(status: boolean): void {
    Object.keys(this.carePlanTemplateChecked).forEach((area) => this.carePlanTemplateChecked[area] = status);
  }

  public toggleAllUsers(status: boolean): void {
    Object.keys(this.employeeChecked).forEach((user) => this.employeeChecked[user] = status);
  }

  public timePillColor(plan: models.IPillColorPlan): string {
    if (!plan.patient.payer_reimbursement || !plan.billing_type) {
      return null;
    }

    if (plan.billing_type.acronym === 'TCM') {
      return this.utilsService.timePillColorTCM(plan.created);
    }

    const allotted = plan.billing_type.billable_minutes;
    return this.utilsService.timePillColor(plan.time_count, allotted);
  }

  public facilityTimeCount(facility: { carePlans: Array<{ billing_type: boolean, patient: { payer_reimbursement: boolean } }> }): number {
    if (!facility.carePlans) {
      return 0;
    }

    let plans = facility.carePlans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    return _sum(_map(plans, (plan) => plan.time_count));
  }

  public avgFacilityTimeColor(facility): string {
    if (!facility.carePlans || facility.carePlans.length < 1) {
      return null;
    }

    let billablePlans = facility.carePlans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    billablePlans = billablePlans.filter((plan) => plan.billing_type.acronym !== 'TCM');
    if (billablePlans.length < 1) {
      return null;
    }

    const avgTime = _sum(_map(billablePlans, (p) => p.time_count)) / billablePlans.length;
    const avgAllotted = _sum(_map(billablePlans, (p) => p.billing_type.billable_minutes)) / billablePlans.length;
    if (avgAllotted < 1) {
      return null;
    }

    return this.utilsService.timePillColor(avgTime, avgAllotted);
  }

  public averageTimeMinutes(): number {
    const facilities = this.facilities.filter((facility) => facility.carePlans);
    let plans = _flattenDeep(_map(facilities, (facility) => facility.carePlans));
    plans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    if (plans.length === 0) {
      return;
    }

    const avgTime = _sum(_map(plans, (p) => p.time_count)) / plans.length;
    return Math.floor(avgTime);
  }

  public averageTimePercentage(): string {
    const facilities = this.facilities.filter((facility) => facility.carePlans);
    const plans = _flattenDeep(_map(facilities, (facility) => facility.carePlans));
    const billablePlans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    if (billablePlans.length < 1) {
      return null;
    }

    const avgTime = _sum(_map(billablePlans, (p) => p.time_count)) / billablePlans.length;
    const avgAllotted = _sum(_map(billablePlans, (p) => p.billing_type.billable_minutes)) / billablePlans.length;
    if (avgAllotted < 1) {
      return null;
    }

    return this.utilsService.timePillColor(avgTime, avgAllotted);
  }

  public avgFacilityRiskLevel(facility: { carePlans: Array<{ risk_level: number }> }): number {
    const avg = _sum(_map(facility.carePlans, (p) => p.risk_level)) / facility.carePlans.length;
    return Math.floor(avg);
  }

  public hasCheckedCareTeamMember(plan: { id?: string, care_team_employee_ids?: Array<string>, patient?: { full_name?: string } }): boolean {
    if (Utils.isNullOrEmptyCollection(this.employeeProfiles) || Utils.isNullOrEmptyCollection(plan.care_team_employee_ids)) {
      return true;
    }

    const employeeIds = plan.care_team_employee_ids;
    return employeeIds
      .map(employeeId => this.employeeChecked[employeeId])
      .some(checked => checked === true);
  }

  public saSearchMatch(sa: { name: string }): boolean {
    return sa.name.toLowerCase().indexOf(this.serviceAreaSearch.toLowerCase()) > -1;
  }

  public cpSearchMatch(cp: { name: string }): boolean {
    return cp.name.toLowerCase().indexOf(this.carePlanSearch.toLowerCase()) > -1;
  }

  public showUserInFilter(user: { facilities: Array<{ id: string }> }): boolean {
    if (Utils.isNullOrUndefined(this.employee)) {
      return false;
    }

    const userFacility = this.employee.facilities.find(f => !Utils.isNullOrUndefined(user.facilities.find(uf => uf.id === f.id)));
    return !Utils.isNullOrUndefined(userFacility);
  }

  public navigatePages(facilityId: string, to: number): void {
    this.facilityPage[facilityId] = to;
    this.getFacilityCarePlans(facilityId).then((carePlans: any) => {
      const facility = this.facilities.find(f => f.id === facilityId);
      facility.carePlans = carePlans.results;
    });
  }

  public get activePatientsCount(): number {
    let total = 0;
    this.facilities.forEach(f => {
      if (this.facilityTotal[f.id]) {
        total += this.facilityTotal[f.id];
      }
    });

    return total;
  }
}
