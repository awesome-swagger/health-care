import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { compact as _compact, filter as _filter, find as _find, flattenDeep as _flattenDeep, map as _map, mean as _mean, sum as _sum, uniqBy as _uniqBy } from 'lodash';
import { Router, ActivatedRoute } from '@angular/router';

import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { StoreService, AuthService } from '../../../services';
import { UtilsService } from '../../../services';
import { PatientCreationModalService } from '../../../services/patient-creation-modal.service';
import { Utils } from '../../../utils';

import { IFacility } from '../../../models/facility';
import { IAddPatientToPlanComponentData } from '../../../models/iadd-patient-to-plan-component-data';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {
  public average = null;
  public averageaverage;
  public facilities = [];
  public facilityOpen = {};
  public serviceAreas = [];
  public serviceAreaChecked = {};
  public carePlanTemplates = [];
  public carePlanTemplateChecked = {};
  public facilityPage = {};
  public facilityTotal = {};
  public facilityPageCount = {};
  public accordionsOpen: { [key: string]: boolean } = {};
  public tooltip2Open: { [key: string]: boolean } = {};
  public employees = [];
  public employeeChecked = {};
  public employee = null;
  public openAlsoTip = {};
  public activeServiceAreas = {};
  public activeUsers = {};
  public users = null;
  public toolAP1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;
  public serviceAreaSearch = '';
  public carePlanSearch = '';
  private authSub = null;
  private organizationSub = null;

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
  }

  public ngOnInit(): void {
    this.authSub = this.auth.user$.subscribe((user) => {
      if (!user) {
        return;
      }

      this.employee = user;
      if (user.facilities.length === 1) {
        this.accordionsOpen[user.facilities[0].id] = true;
      }

      this.organizationSub = this.auth.organization$.subscribe((organization) => {
        if (!organization) {
          return;
        }

        this.getCarePlanAverage(organization.id).then((average: any) => this.average = average);
        this.getFacilitiesForOrganization(organization.id).then((facilities: any) => {
          this.facilities = facilities.results.filter(f => !f.is_affiliate);
          this.facilities = this.facilities.filter(f => user.facilities.find(fa => fa.id === f.id));
          this.facilities.forEach((facility) => {
            this.accordionsOpen[facility.id] = false;
            this.facilityPage[facility.id] = 1;
            this.getFacilityCarePlans(facility.id).then((carePlans: any) => {
              facility.carePlans = carePlans.results;
              this.facilityTotal[facility.id] = carePlans.count;
              this.facilityPageCount[facility.id] = this.getPageCount(carePlans.count);
            });
          });

          this.store.EmployeeProfile.readListPaged().subscribe((users) => {
            this.employees = users;
            users.forEach((user) => this.employeeChecked[user.id] = true);
            this.route.params.subscribe((params) => {
              if (!params) {
                return;
              }

              if (params.userId) {
                const ids = params.userId.split(',');
                users.forEach(user => this.employeeChecked[user.id] = false);
                ids.forEach(id => this.employeeChecked[id] = true);
                this.employeeChecked[params.userId] = true;
              }
            });
          });
        });
      });
    });

    this.store.ServiceArea.readListPaged().subscribe((serviceAreas) => {
      this.serviceAreas = serviceAreas;
      serviceAreas.forEach((area) => this.serviceAreaChecked[area.id] = true);
    });

    this.store.CarePlanTemplate.readListPaged().subscribe((templates: any) => {
      this.carePlanTemplates = templates.sort((a, b) => {
        const textA = a.name.toUpperCase();
        const textB = b.name.toUpperCase();

        return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
      });

      templates.forEach((template) => this.carePlanTemplateChecked[template.id] = true);
    });
  }

  public ngOnDestroy(): void {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }

    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public getCarePlanAverage(organizationId: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      let averageSub = this.store.CarePlan.detailRoute('GET', null, 'average', {}, {
        patient__facility__organization: organizationId
      }).subscribe(
        (average) => resolve(average),
        (err) => reject(err),
        () => averageSub.unsubscribe()
      );
    });
  }

  public getPatientsOverview(organizationId: string): Promise<any> {
    const promise = new Promise<any>((resolve, reject) => {
      const params = {
        'facility__organization__id': organizationId
      };

      const patientsSub = this.store.PatientProfile.listRoute('GET', 'overview', {}, params).subscribe(
        patients => resolve(patients),
        err => reject(err),
        () => patientsSub.unsubscribe()
      );
    });

    return promise;
  }

  public getFacilitiesForOrganization(organizationId: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      const facilitiesSub = this.store.Organization.detailRoute('GET', organizationId, 'facilities').subscribe(
        facilities => resolve(facilities),
        err => reject(err),
        () => facilitiesSub.unsubscribe()
      );
    });
  }

  public getFacilityCarePlans(facilityId: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      const params = {
        page: this.facilityPage[facilityId]
      };
      const carePlansSub = this.store.Facility.detailRoute('get', facilityId, 'care_plans', {}, params).subscribe(
        (carePlans) => resolve(carePlans),
        (err) => reject(err),
        () => carePlansSub.unsubscribe()
      );
    });
  }

  public getPatients(): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      const patientsSub = this.store.PatientProfile.readListPaged({ page: 1 }).subscribe(
        patients => resolve(patients),
        err => reject(err),
        () => patientsSub.unsubscribe()
      );
    });
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
    this.employees.forEach(e => {
      if (this.employeeChecked[e.id]) {
        checkedList.push(e);
      }
    });

    if (checkedList.length === 0) {
      return 'None';
    }

    if (checkedList.length === this.employees.length) {
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
    // TODO: FIX THIS
    const data: IAddPatientToPlanComponentData = {
      action: 'add',
      enrollPatientChecked: true,
      facility: facility
    };

    this.patientCreationModalService
      .openEnrollment_PotentialPatientDetails(data)
      .then((response) => {
        if (Utils.isNullOrUndefined(response)) {
          return;
        }

        console.log('TODO: Fix this', response);
        // TODO: FIX THIS
        //if (!(res.hasOwnProperty('patient') && res.hasOwnProperty('plan'))) {
        //  res.careTeamMembers = res.careTeam;
        //  res.engagement = res.engagement || 0;
        //  res.outcomes = res.outcomes || 0;
        //  res.current_week = res.current_week || 0;
        //  res.risk_level = res.risk_level || 0;
        //  res.tasks_this_week = res.tasks_this_week || 0;
        //  const facility = this.facilities.find(f => f.id === res.patient.facility.id);
        //  const patient = facility.patients.find(p => p.id === res.patient.id);
        //  if (!patient) {
        //    this.store.PatientProfile.read(res.patient.id).subscribe(patient => {
        //      if (facility.patients && facility.patients.length) {
        //        facility.patients.push(patient);
        //      } else {
        //        facility.patients = [patient];
        //      }

        //      this.store.CarePlan.readListPaged({ patient: patient.id }).subscribe(plans => {
        //        patient.carePlans = plans;
        //        patient.carePlans.forEach(plan => {
        //          this.store.CareTeamMember
        //            .readListPaged({ plan: plan.id })
        //            .subscribe(careTeamMembers => plan.careTeamMembers = careTeamMembers);
        //        });
        //      });
        //    });
        //  } else {
        //    if (patient.carePlans && patient.carePlans.length) {
        //      patient.carePlans.push(res);
        //    } else {
        //      patient.carePlans = [res];
        //    }
        //  }
        //}

        //if (res.hasOwnProperty('patient') && res.hasOwnProperty('plan')) {
        //  res.plan.careTeamMembers = res.plan.careTeam;
        //  res.plan.engagement = res.plan.engagement || 0;
        //  res.plan.outcomes = res.plan.outcomes || 0;
        //  res.plan.current_week = res.plan.current_week || 0;
        //  res.plan.risk_level = res.plan.risk_level || 0;
        //  res.plan.tasks_this_week = res.plan.tasks_this_week || 0;
        //  res.patient.carePlans = [res.plan];
        //  const facility = this.facilities.find(f => f.id === res.patient.facility.id);
        //  if (facility.patients && facility.patients.length) {
        //    facility.patients.push(res.patient);
        //  } else {
        //    facility.patients = [res.patient];
        //  }
        //}
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

  public toggleAllServiceAreas(status: boolean | string): void {
    Object.keys(this.serviceAreaChecked).forEach((area) => this.serviceAreaChecked[area] = status);
  }

  public toggleAllCarePlans(status: boolean | string): void {
    Object.keys(this.carePlanTemplateChecked).forEach((area) => this.carePlanTemplateChecked[area] = status);
  }

  public toggleAllUsers(status: {}): void {
    Object.keys(this.employeeChecked).forEach((user) => this.employeeChecked[user] = status);
  }

  public timePillColor(plan: IPillColorPlan): string {
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

  public hasCheckedCareTeamMember(plan: { care_team_employee_ids: Array<string> }): boolean {
    if (!this.employees) {
      return true;
    }
    let result = false;
    if (plan.care_team_employee_ids) {
      plan.care_team_employee_ids.forEach((employeeId) => {
        if (this.employeeChecked[employeeId] === true) {
          result = true;
        }
      })
    }
    return result;
  }

  public saSearchMatch(sa: { name: string }): boolean {
    return sa.name.toLowerCase().indexOf(this.serviceAreaSearch.toLowerCase()) > -1;
  }

  public cpSearchMatch(cp: { name: string }): boolean {
    return cp.name.toLowerCase().indexOf(this.carePlanSearch.toLowerCase()) > -1;
  }

  public showUserInFilter(user: { facilities: Array<{ id: string }> }): boolean {
    if (this.employee) {
      return this.employee.facilities.find(f => {
        let result = false;
        user.facilities.forEach(uf => {
          if (uf.id === f.id) {
            result = true;
          }
        })
        return result;
      })
    } else {
      return false;
    }
  }

  public getPageCount(count: number): number {
    return Math.ceil(count / 20);
  }

  public navigatePages(facilityId: string, to: any): void {
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

interface IPillColorPlan {
  billing_type: {
    acronym: string,
    billable_minutes: number
  },
  created: string,
  patient: {
    payer_reimbursement: any
  },
  time_count: number
}
