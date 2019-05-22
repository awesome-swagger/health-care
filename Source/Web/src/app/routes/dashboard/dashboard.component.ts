import { Component, OnInit, OnDestroy } from '@angular/core';
import { StoreService, AuthService } from '../../services';
import * as moment from 'moment';
import { Subscription } from 'rxjs';
import patientsEnrolledData from './patientsEnrolledData';
import {
  filter as _filter,
  find as _find,
  map as _map,
} from 'lodash';
import { map } from 'd3';
import {Router} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit, OnDestroy {

  public org = null;
  public user = null;
  public patients = null;
  public patientsGrouped = null;
  public employees = [];
  public employeeChecked = {};
  public facilities = [];
  public facilityChecked = {};
  public riskLevelChecked = {
    'on_track': true,
    'low_risk': true,
    'med_risk': true,
    'high_risk': true,
  };

  public riskLevelBreakdown = null;
  public patientAdoption = null;
  public billingOverview = null;

  public analyticsData = null;
  public patientOverview = null;

  public patientsEnrolledData = [];
  public filteredPatientsEnrolledData = patientsEnrolledData;

  public multiOpen;
  public dashTip1;
  public multi2Open;
  public multi3Open;

  public patientsEnrolledStart:moment.Moment = moment().subtract(5, 'M').startOf('M');
  public patientsEnrolledEnd:moment.Moment = moment();

  public topBillingStart:moment.Moment = moment().subtract('1', 'M').startOf('M');
  public topBillingEnd:moment.Moment = moment().subtract('1', 'M').endOf('M');

  public bottomBillingStart:moment.Moment = moment().subtract('2', 'M').startOf('M');
  public bottomBillingEnd:moment.Moment = moment().subtract('2', 'M').endOf('M');

  public datepickerOptions = {
     relativeTop: '-368px',
   };

  public constructor(
    private auth: AuthService,
    private router: Router,
    private store: StoreService,
  ) { }

  private organizationSub:Subscription = null;

  public ngOnInit() {

    this.organizationSub = this.auth.organization$.subscribe(
      (org) => {

        if (!org) return;
        this.org = org;
        this.store.EmployeeProfile.readListPaged({
          organization: this.org.id,
        }).subscribe((res) => {
          this.employees = res;
          this.employees.forEach(employee => {
            this.employeeChecked[employee.id] = false;
          })
          this.refreshRiskLevels()
        })

        this.store.Organization.detailRoute('GET', org.id, 'patients_enrolled_over_time').subscribe(
          (res:any) => {
            this.patientsEnrolledData = _map(Object.keys(res.graph), month => {
              return {
                month,
                enrolled: res.graph[month].enrolled_patients,
                billable: res.graph[month].billable_patients,
              }
            }).reverse();
            this.filterData();
          }
        )

        this.store.Organization.detailRoute('GET', org.id, 'patient_adoption').subscribe(
          (res:any) => {
            this.patientAdoption = res;
          }
        )

        this.store.Organization.detailRoute('GET', org.id, 'billed_activities/overview').subscribe(
          (res:any) => {
            this.billingOverview = res;
          }
        )

        this.store.Facility.readList({
          organization_id: org.id,
        }).subscribe((res) => {
          this.facilities = res.results;
          this.facilities.forEach(facility => {
            this.facilityChecked[facility.id] = true;
          })
        })
        this.store.Organization.detailRoute('GET', org.id, 'dashboard_analytics').subscribe(
          res => {
            this.analyticsData = res;
          }
        )
        this.store.PatientProfile.detailRoute('GET', null, 'overview', {}, {
          'facility__organization__id': this.org.id,
        }).subscribe(
          res => {
            this.patientOverview = res;
          }
        )
      }
    )

    this.auth.user$.subscribe(user => {
      if (!user) return;
      this.user = user;
    })

    this.filterData();

  }

  public ngOnDestroy() { }

  get defaultDates():[moment.Moment, moment.Moment] {
    const end = moment();
    const startMonth = end.clone().subtract(5, 'M');
    const start = startMonth.startOf('M');
    return [start, end];
  }

  public refreshAll() {
    setTimeout(() => {
      this.refreshRiskLevels();
    }, 0)
  }

  public refreshRiskLevels() {
    if (this.org) {
      let params = {};
      let employeesChecked = _filter(Object.keys(this.employeeChecked), id => this.employeeChecked[id]).join(',')
      if (employeesChecked.length > 0) {
        params['employees'] = employeesChecked;
        this.store.Organization.detailRoute('GET', this.org.id, 'patient_risk_levels', {}, params).subscribe((res:any) => {
          this.riskLevelBreakdown = res;
        });
      } else {
        this.store.Organization.detailRoute('GET', this.org.id, 'patient_risk_levels').subscribe(res => {
          this.riskLevelBreakdown = res;
        })
      }

    }
  }

  public toggleAllFilterList(list:any, state:boolean) {
    const keys = Object.keys(list);
    keys.forEach(key => {
     list[key] = state;
    })
    this.refreshAll();
  }

  public toggleAllUsers(state:boolean) {
    return this.toggleAllFilterList(this.employeeChecked, state);
  }

  public toggleAllFacilities(state:boolean) {
    return this.toggleAllFilterList(this.facilityChecked, state);
  }

  public filterData() {
    this.filteredPatientsEnrolledData = this.patientsEnrolledData
      .slice(
        this.patientsEnrolledData.indexOf(
          _find(this.patientsEnrolledData, d => d.month == this.patientsEnrolledStart.format('MMMM YYYY'))
        ),
        this.patientsEnrolledData.indexOf(
          _find(this.patientsEnrolledData, d => d.month == this.patientsEnrolledEnd.format('MMMM YYYY'))
        ),
      );
  }

  public get riskLevelPercent() {
    if (this.riskLevelBreakdown) {
      let { on_track, low_risk, med_risk, high_risk } = this.riskLevelBreakdown;
      const total = on_track + low_risk + med_risk + high_risk;
      on_track = Math.floor(on_track / total * 100);
      low_risk = Math.floor(low_risk / total * 100);
      med_risk = Math.floor(med_risk / total * 100);
      high_risk = Math.floor(high_risk / total * 100);
      return { on_track, low_risk, med_risk, high_risk };
    }
    return { on_track: 0, low_risk: 0, med_risk: 0, high_risk: 0 }
  }

  public routeToActive() {
    let employeesChecked = _filter(Object.keys(this.employeeChecked), id => this.employeeChecked[id]).join(',')
    if (employeesChecked.length > 0) {
      this.router.navigate(['/patients', 'active', employeesChecked]).then(() => {})
    } else {
      this.router.navigate(['/patients', 'active']).then(() => {})
    }
  }

  public showUserInFilter(user) {
    return true;
    // if (this.user) {
    //   return this.user.facilities.find(f => {
    //     let result = false;
    //     user.facilities.forEach(uf => {
    //       if (uf.id === f.id) {
    //         result = true;
    //       }
    //     })
    //     return result;
    //   })
    // }
    // else {
    //   return false;
    // }
  }

  public get userIsAdmin() {
    if (this.user) {
      return this.user.facilities_managed.length > 0 || this.user.organizations_managed.length > 0;
    }
    return false;
  }

  public toggleAllRiskLevels(status) {
    Object.keys(this.riskLevelChecked).forEach(r => {
      this.riskLevelChecked[r] = status;
    })
  }

}
