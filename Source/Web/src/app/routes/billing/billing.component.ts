import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import  { Subscription } from 'rxjs';
import * as moment from 'moment';
import {
  sumBy as _sumBy,
  uniqBy as _uniqBy,
  uniq as _uniq,
  groupBy as _groupBy,
  flattenDeep as _flattenDeep,
} from 'lodash';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, StoreService, SessionStorageService, UtilsService, } from '../../services';

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
  public loadingBillingData = true;
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
  public loadingEmployees = true;
  public employeeSearch = '';
  public selectedEmployees = [];
  public planTypes = [];

  public syncTooltipOpen = false;
  public filterFacilitiesOpen = false;
  public filterServiceOpen = false;
  public filterStatusOpen = false;
  public employeeSearchOpen = false;
  public employeesDropOptions: PopoverOptions = {
    relativeTop: '80px',
    relativeRight: '0px',
  };
  public billablePatientsHelpOpen = false;
  public practitionerDropdownOpen = {};
  public detailsOpen = {};

  private authSub: Subscription = null;
  private orgSub: Subscription = null;
  private facilitiesSub: Subscription = null;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private auth: AuthService,
    private store: StoreService,
    private session: SessionStorageService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.route.queryParams.subscribe((qparams) => {
      if (qparams.from_dashboard) {
        this.selectedEmployees = [];
        let dashboardEmployeesSelected = this.session.getObj('dashboardEmployeesSelected');
        if (dashboardEmployeesSelected && dashboardEmployeesSelected.length > 0) {
          this.selectedEmployees = dashboardEmployeesSelected;
        }
      }
      this.authSub = this.auth.user$.subscribe((user) => {
        if (!user) {
          return;
        }
        this.user = user;
        if (qparams.from_patient_dashboard) {
          this.selectedEmployees = [this.user.id];
        }
      });
      this.orgSub = this.auth.organization$.subscribe((organization) => {
        if (!organization) {
          return;
        }
        this.organization = organization;
        this.isManager = this.organization.is_manager;
        this.getEmployees(this.organization.id).then((employees: any) => {
          this.employees = employees;
        });
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
    });
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

  public getEmployees(organizationId) {
    this.loadingEmployees = true;
    return new Promise((resolve, reject) => {
      let employeesSub = this.store.EmployeeProfile.readListPaged({
        organization: organizationId
      }).subscribe(
        (employees) => {
          this.loadingEmployees = false;
          resolve(employees);
        },
        (err) => reject(err),
        () => {
          employeesSub.unsubscribe();
        }
      );
    });
  }

  public resolveActivityOverview(organizationId) {
    let promise = new Promise((resolve, reject) => {
      let params = {};
      if (this.selectedFacility !== null) {
        params['plan__patient__facility'] = this.selectedFacility.id;
      }
      if (this.selectedServiceArea !== null) {
        params['plan__plan_template__service_area'] = this.selectedServiceArea.id;
      }
      params['activity_datetime__month'] = this.selectedMonth.month() + 1;
      params['activity_datetime__year'] = this.selectedMonth.year();
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
      params['billed_plans__activities__activity_datetime__month'] = this.selectedMonth.month() + 1;
      params['billed_plans__activities__activity_datetime__year'] = this.selectedMonth.year();
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
    this.loadingBillingData = true;
    let overviewPromise = this.resolveActivityOverview(this.organization.id).then((overviewStats: any) => {
      this.overviewStats = overviewStats;
    });
    let practitionersPromise = this.resolveBillingPractitioners(this.organization.id).then((billingPractitioners: any) => {
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
    Promise.all([overviewPromise, practitionersPromise]).then(() => {
      this.loadingBillingData = false;
    });
  }

  public decrementMonth() {
    this.selectedMonth.add(-1, 'month');
    this.getBillingData();
  }

  public incrementMonthDisabled() {
    return this.selectedMonth.get('month') === moment().get('month');
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

  public filterEmployees() {
    return this.employees.concat().filter((obj) => {
      let fullName = `${obj.user.first_name} ${obj.user.last_name}`;
      return fullName.toLowerCase().includes(this.employeeSearch.toLowerCase());
    });
  }

  public employeesShown() {
    if (this.employeeSearch && this.employeeSearch.length > 0) {
      return this.filterEmployees();
    } else {
      return this.employees.concat();
    }
  }

  public toggleEmployeeSelected(employee) {
    if (this.isEmployeeSelected(employee)) {
      let index = this.selectedEmployees.indexOf(employee.id);
      this.selectedEmployees.splice(index, 1);
    } else {
      this.selectedEmployees.push(employee.id);
    }
  }

  public checkAllEmployees() {
    this.selectedEmployees = this.employees.map((emp) => emp.id);
  }

  public uncheckAllEmployees() {
    this.selectedEmployees = [];
  }

  public isEmployeeSelected(employee) {
    if (this.selectedEmployees.length === 0) {
      return true;
    }
    return this.selectedEmployees.includes(employee.id);
  }

  public formatSelectedUsers() {
    if (this.selectedEmployees.length === 0 || this.selectedEmployees.length === this.employees.length) {
      return 'All';
    } else {
      return this.selectedEmployees.length + ' Users';
    }
  }

  public getUniqueFacilities() {
    let facilities = this.billingPractitioners.map((bp) => {
      return bp.plans.map((plan) => plan.patient.facility);
    });
    facilities = _uniqBy(_flattenDeep(facilities), (obj) => obj.id);
    return facilities;
  }

  public planContainsSelectedEmployees(plan) {
    if (!this.selectedEmployees || this.selectedEmployees.length === 0) {
      return true;
    }
    let planUserIds = [plan.care_manager.id];
    let uniqueDetailsUsers = _uniq(plan.details_of_service.map((details) => {
      return details.added_by.id;
    }));
    planUserIds = planUserIds.concat(uniqueDetailsUsers);
    return this.selectedEmployees.filter((emp) => -1 !== planUserIds.indexOf(emp)).length > 0;
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
      return obj.patient.facility.id === facilityId && this.planContainsSelectedEmployees(obj);
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

  public getActionType(details) {
    if (details.team_template) {
      return details.team_template.name;
    } else {
      return 'Patient Data Review';
    }
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
