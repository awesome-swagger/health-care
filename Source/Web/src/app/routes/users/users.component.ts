import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { AuthService, StoreService } from '../../services';
import { uniqBy as _uniqBy, groupBy as _groupBy } from 'lodash';

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

  public showInactive = false;
  public searchOpen = false;
  public organizationAccordionOpen = false;
  public facilityAccordionsOpen = [];
  public tooltipsOpen = [];

  public organizationChecked = true;
  public facilitiesChecked = {};

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
          this.organization.employees = employees.results;
        },
        (err) => {},
        () => {
          employeesSub.unsubscribe();
        },
      )
      // Get the facilities for this organization from the auth service.
      this.facilitesSub = this.auth.facilities$.subscribe((facilities) => {
        if (facilities === null) {
          return;
        }
        this.facilities = facilities;
        this.facilities.forEach((facility, i) => {
          let employeesSub = this.store.Facility.detailRoute('get', facility.id, 'employee_profiles').subscribe(
            (employees: any) => {
              facility.employees = employees.results;
              this.facilitiesChecked[facility.id] = true;
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

  public organizationSearchMatch() {
    return this.organization.name.toLowerCase().indexOf(this.facilitiesSearch) != -1;
  }

  public facilitySearchMatch(facility) {
    return facility.name.toLowerCase().indexOf(this.facilitiesSearch) != -1;
  }

  public usersFilteredBySearch() {

  }
}
