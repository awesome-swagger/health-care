import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import  { Subscription } from 'rxjs';
import * as moment from 'moment';
import {
  sumBy as _sumBy,
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  flattenDeep as _flattenDeep,
} from 'lodash';
import { AuthService, StoreService, UtilsService, } from '../../services';

@Component({
  selector: 'app-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class BillingComponent implements OnDestroy, OnInit {

  public moment = moment;

  public user = null;
  public organization = null;
  public isManager = false;
  public selectedMonth: moment.Moment = moment().startOf('month');
  public overviewStats = null;

  public billingPractitioners = [];

  public billingData = null;
  public patients = [];
  public facilities = [];
  public facilitiesShown = [];
  public selectedFacility = null;
  public facilitySearch = '';
  public serviceAreas = [];
  public serviceAreasShown = [];
  public selectedServiceArea = null;
  public serviceSearch = '';
  public selectedStatus = 'all';
  public employees = [];
  public employeesShown = [];
  public employeeSearch = '';
  public selectedEmployee = null;
  public planTypes = [];

  public syncTooltipOpen = false;
  public filterFacilitiesOpen = false;
  public filterServiceOpen = false;
  public filterStatusOpen = false;
  public employeeSearchOpen = false;
  public billablePatientsHelpOpen = false;
  public practitionerDropdownOpen = {};
  public detailsOpen = {};

  private authSub: Subscription = null;
  private orgSub: Subscription = null;
  private facilitiesSub: Subscription = null;

  constructor(
    private router: Router,
    private auth: AuthService,
    private store: StoreService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.authSub = this.auth.user$.subscribe((user) => {
      if (!user) {
        return;
      }
      this.user = user;
    });
    this.orgSub = this.auth.organization$.subscribe((organization) => {
      if (!organization) {
        return;
      }
      this.organization = organization;
      this.isManager = this.organization.is_manager;
      this.getBillingData();
    });
    this.facilitiesSub = this.auth.facilities$.subscribe((facilities) => {
      if (!facilities) {
        return;
      }
      this.facilities = facilities;
      this.facilitiesShown = this.facilities.concat();
    });
    let serviceAreasSub = this.store.ServiceArea.readListPaged().subscribe(
      (serviceAreas) => {
        this.serviceAreas = serviceAreas;
        this.serviceAreasShown = this.serviceAreas.concat();
      },
      (err) => {},
      () => {
        serviceAreasSub.unsubscribe();
      }
    );
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
    if (this.orgSub) {
      this.orgSub.unsubscribe();
    }
    if (this.facilitiesSub) {
      this.facilitiesSub.unsubscribe();
    }
  }

  public resolveActivityOverview(organizationId) {
    let promise = new Promise((resolve, reject) => {
      let params = {};
      if (this.selectedFacility !== null) {
        params['plan__patient__facility'] = this.selectedFacility.id;
      }
      if (this.selectedServiceArea !== null) {
        params['plan_template__service_area'] = this.selectedServiceArea.id;
      }
      params['activity_date__month'] = this.selectedMonth.month() + 1;
      params['activity_date__year'] = this.selectedMonth.year();
      let overviewSub = this.store.Organization.detailRoute('get', organizationId, 'billed_activities/overview', {}, params).subscribe(
        (data) => resolve(data),
        (err) => reject(err),
        () => {
          overviewSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public resolveBillingPractitioners(organizationId) {
    let promise = new Promise((resolve, reject) => {
      let params = {};
      if (this.selectedFacility !== null) {
        params['billed_plans__patient__facility'] = this.selectedFacility.id;
      }
      if (this.selectedServiceArea !== null) {
        params['billed_plans__plan_template__service_area'] = this.selectedServiceArea.id;
      }
      params['billed_plans__activities__activity_date__month'] = this.selectedMonth.month() + 1;
      params['billed_plans__activities__activity_date__year'] = this.selectedMonth.year();
      let bpSub = this.store.Organization.detailRoute('get', organizationId, 'billing_practitioners', {}, params).subscribe(
        (data: any) => resolve(data.results),
        (err) => reject(err),
        () => {
          bpSub.unsubscribe();
        }
      )
    });
    return promise;
  }

  public getBillingData() {
    this.resolveActivityOverview(this.organization.id).then((overviewStats: any) => {
      this.overviewStats = overviewStats;
    });
    this.resolveBillingPractitioners(this.organization.id).then((billingPractitioners: any) => {
      this.billingPractitioners = billingPractitioners.map((bp) => {
        let filteredPlans = bp.plans.filter((plan) => {
          if (this.selectedStatus === 'all') {
            return true;
          } else if (this.selectedStatus === 'not-billed') {
            return !plan.is_billed;
          } else if (this.selectedStatus === 'billed') {
            return plan.is_billed;
          } else {
            return true;
          }
        });
        bp.plans = filteredPlans;
        return bp;
      });
    });
  }

  public decrementMonth() {
    this.selectedMonth.add(-1, 'month');
    this.getBillingData();
  }

  public incrementMonth() {
    this.selectedMonth.add(1, 'month');
    this.getBillingData();
  }

  public filterFacilities() {
    this.facilitiesShown = this.facilities.filter((obj) => {
      return obj.name.toLowerCase().includes(this.facilitySearch.toLowerCase());
    });
  }

  public setSelectedFacility(facility) {
    this.selectedFacility = facility;
    this.filterFacilitiesOpen = false;
    this.getBillingData();
  }

  public filterServiceArea() {
    this.serviceAreasShown = this.serviceAreas.filter((obj) => {
      return obj.name.toLowerCase().includes(this.serviceSearch.toLowerCase());
    });
  }

  public setSelectedServiceArea(serviceArea) {
    this.selectedServiceArea = serviceArea;
    this.filterServiceOpen = false;
    this.getBillingData();
  }

  public setSelectedStatus(status) {
    this.selectedStatus = status;
    this.filterStatusOpen = false;
    this.getBillingData();
  }

  public filterEmployee() {
    this.employeesShown = this.employees.filter((obj) => {
      let fullNameWithTitle = `${obj.first_name} ${obj.last_name}, ${obj.title}`;
      return fullNameWithTitle.toLowerCase().includes(this.employeeSearch.toLowerCase());
    });
  }

  public setSelectedEmployee(employee) {
    this.selectedEmployee = employee;
    this.employeeSearch = `${employee.first_name} ${employee.last_name}, ${employee.title}`;
  }

  public getUniqueFacilities() {
    let facilities = this.billingPractitioners.map((bp) => {
      return bp.plans.map((plan) => plan.patient.facility);
    });
    facilities = _uniqBy(_flattenDeep(facilities), (obj) => obj.id);
    return facilities;
  }

  public getFacilityPractitioners(facilityId) {
    let practitioners = this.billingPractitioners.filter((obj) => {
      let facilityIds = obj.plans.map((plan) => plan.patient.facility.id);
      return facilityIds.includes(facilityId);
    });
    return practitioners;
  }

  public getPractitionerPlansAtFacility(practitionerId, facilityId) {
    let practitioner = this.billingPractitioners.find((obj) => obj.id === practitionerId);
    if (!practitioner) {
      return [];
    }
    return practitioner.plans.filter((obj) => {
      return obj.patient.facility.id === facilityId;
    });
  }

  public plansBilledCount(plans) {
    return plans.filter((obj) => obj.is_billed).length;
  }

  public facilityBillablePatientsCount(facilityId) {
    let practitioners = this.getFacilityPractitioners(facilityId);
    return _sumBy(practitioners, (obj) => {
      let plansCount = this.getPractitionerPlansAtFacility(obj.id, facilityId).length;
      return plansCount;
    });
  }

  public getBilledPercent(practitionerId, facilityId) {
    let calc = this.plansBilledCount(this.getPractitionerPlansAtFacility(practitionerId, facilityId)) /
              this.getPractitionerPlansAtFacility(practitionerId, facilityId).length;
    return calc * 100;
  }

  public markPlanBilled(plan) {
    let billSub = this.store.CarePlan.detailRoute('post', plan.id, 'bill_time').subscribe(
      (success) => {
        plan.is_billed = true;
      },
      (err) => {},
      () => {
        billSub.unsubscribe();
      }
    );
  }

  public minutesToHours(n) {
    let num = n;
    let hours = (num / 60);
    let rhours = Math.floor(hours);
    let minutes = (hours - rhours) * 60;
    let rminutes = Math.round(minutes);
    return `${rhours}:${rminutes}`;
  }

  public entriesSubtotal(entries) {
    return _sumBy(entries, (obj) => obj.subtotal);
  }

  public routeToPatient(id) {
    this.router.navigate(['/patient', id]);
  }

  public routeToUser(id) {
    this.router.navigate(['/user', id]);
  }
}
