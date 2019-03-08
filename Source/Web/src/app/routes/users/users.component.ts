import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { AuthService, StoreService } from '../../services';
import { uniqBy as _uniqBy, groupBy as _groupBy } from 'lodash';
import * as _ from 'lodash';
import { collectExternalReferences } from '@angular/compiler';
import { PopoverComponent } from '../../modules/popover';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
})
export class UsersComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public facilitiesSearch = '';
  private organizationSub: Subscription = null;
  private facilitesSub: Subscription = null;

  public total:number = 0;
  public facilityTotals = {};
  public currentPage:number = 1;
  public facilityPages = {};
  public allEmployees = [];

  public showInactive = false;
  public searchOpen = false;
  public organizationAccordionOpen = false;
  public facilityAccordionsOpen = [];
  public tooltipsOpen = [];

  public organizationChecked = true;
  public facilitiesChecked = {};
  public sortDirection = 'desc';
  public searchString = '';

  public facilitySelectOpen;

  constructor(
    private router: Router,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    // Get the organization that the user is logged in to from the auth service.
    this.organizationSub = this.auth.organization$.subscribe((organization) => {
      if (organization === null) {
        return;
      }
      this.organization = organization;
      if (!this.organization.is_manager) {
        this.router.navigate(['/error']);
      }
      let employeesSub = this.store.Organization.detailRoute('get', organization.id, 'employee_profiles').subscribe(
        (employees: any) => {
          this.total = employees.results.filter(e => e.status === 'active').length;
          this.organization.employees = employees.results;

          this.store.EmployeeProfile.readListPaged().subscribe(
            res => {
              this.allEmployees = res;
            }
          )
        },
        (err) => {},
        () => {
          employeesSub.unsubscribe();
        },
      )
      // Get the facilities for this organization from the auth service.
      this.facilitesSub = this.store.Organization.detailRoute('GET', organization.id, 'facilities').subscribe((facilities:any) => {
        if (facilities === null) {
          return;
        }
        this.facilities = facilities.results;
        this.facilities.forEach((facility, i) => {
          let employeesSub = this.store.Facility.detailRoute('get', facility.id, 'employee_profiles').subscribe(
            (employees: any) => {
              facility.employees = employees.results;
              this.facilitiesChecked[facility.id] = true;
              this.facilityPages[facility.id] = 1;
              this.facilityTotals[facility.id] = employees.count;
            },
            (err) => {},
            () => {
              employeesSub.unsubscribe();
            },
          );
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public routeToUserDetail(employee) {
    this.router.navigate(['/user', employee.id]);
  }

  public checkAllFacilities() {
    this.organizationChecked = true;
    this.facilities.forEach((facility) => {
      this.facilitiesChecked[facility.id] = true;
    });
  }

  public uncheckAllFacilities() {
    this.organizationChecked = false;
    this.facilities.forEach((facility) => {
      this.facilitiesChecked[facility.id] = false;
    });
  }

  public shownNthFacilityEmployeeCount(n) {
    if (this.facilities[n] && this.facilities[n].employees) {
      if (this.showInactive) {
        return this.facilities[n].employees.length;
      }
      return _.filter(this.facilities[n].employees, employee => employee.status !== 'inactive').length;
    }
    return 0;
  }

  get shownOrgEmployeesCount() {
    if (this.organization && this.organization.employees) {
      if (this.showInactive) {
        return this.organization.employees.length;
      }
      return _.filter(this.organization.employees, employee => employee.status !== 'inactive').length;
    }

    return 0;
  }

  get activeUsersCount() {
    if (this.organization && this.organization.employees) {
      return _.filter(this.organization.employees, employee => employee.status !== 'inactive').length;
    }
    return 0;
  }

  get searchEmployees() {
    if (this.organization && this.organization.employees) {
      return _.filter(this.organization.employees, employee => {
        const names = employee.full_name.split(' ');
        const nameMatches = _.map(names, name => name.slice(0, this.searchString.length).toLowerCase() === this.searchString.toLowerCase());
        return nameMatches.indexOf(true) > -1;
      });
    }

    return [];
  }

  public organizationSearchMatch() {
    return this.organization.name.toLowerCase().indexOf(this.facilitiesSearch) != -1;
  }

  public facilitySearchMatch(facility) {
    return facility.name.toLowerCase().indexOf(this.facilitiesSearch) != -1;
  }

  public usersFilteredBySearch() {

  }

  public switchPage(by:number, to:number = 0) {
    if (this.organization) {
      let employeesSub = this.store.Organization.detailRoute(
        'get',
        this.organization.id,
        'employee_profiles',
        {},
        { 
          page: to || this.currentPage + by
        }
      ).subscribe(
        (employees: any) => {
          this.organization.employees = employees.results;
          if (to) {
            this.currentPage = to;
          } else {
            this.currentPage += by;
          }
        },
        (err) => {},
        () => {
          employeesSub.unsubscribe();
        },
      )
    }
  }

  public switchNthFacilityPage(n:number, by:number, to:number = 0) {
    if (this.facilities) {
      const facility = this.facilities[n];
      let employeesSub = this.store.Facility.detailRoute(
        'get',
        facility.id,
        'employee_profiles',
        {},
        {
          page: to || this.facilityPages[facility.id] + by,
        }
      ).subscribe(
        (employees: any) => {
          facility.employees = employees.results;
          if (to) {
            this.facilityPages[facility.id] = to;
          } else {
            this.facilityPages[facility.id] += by;
          }
        },
        (err) => {},
        () => {
          employeesSub.unsubscribe();
        },
      );
    }
  }

  public get orgUserCountText() {
    if (!this.total) return 0;
    if (this.total <= 20) {
      return this.total;
    } else {
      const pageMin = 20*(this.currentPage - 1) + 1;
      const pageMax = 20*(this.currentPage - 1) + 20;
      return `${pageMin} - ${pageMax < this.total ? pageMax : this.total} of ${this.total}`
    }
  }

  public nthFacilityUserCountText(n) {
    const facility = this.facilities[n];
    if (this.facilityTotals[facility.id] <= 20) {
      return this.total;
    } else {
      const pageMin = 20*(this.facilityPages[facility.id] - 1) + 1;
      const pageMax = 20*(this.facilityPages[facility.id] - 1) + 20;
      return `${pageMin} - ${pageMax < this.facilityTotals[facility.id] ? pageMax : this.facilityTotals[facility.id]} of ${this.facilityTotals[facility.id]}`;
    }
  }

  public lastPage(total) {
    return Math.ceil(total/20);
  }

  public getAlso(facilityId, orgId, employeeId) {
    if (this.allEmployees && this.allEmployees.length) {
      const employee = _.find(this.allEmployees, e => e.id === employeeId);
      const alsoOrgs = _.filter(employee.organizations, o => o.id !== orgId);
      const alsoFacilities = _.filter(employee.facilities, f => f.id !== facilityId && !f.is_affiliate);

      return {
        facilities: _.map(alsoFacilities, f => f.name),
        orgs: _.map(alsoOrgs, o => o.name),
      }
    }
    return {facilities: [], orgs: []}
  }

  public filteredFacilities(is_affiliate) { return this.facilities.filter(f => f.is_affiliate === is_affiliate); }

  public facilityTypes = [
    { pluralName: 'Facilities', name: 'Facility', is_affiliate: false},
    { pluralName: 'Affiliates', name: 'Affiliate', is_affiliate: true}
  ]
}
