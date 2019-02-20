import { Component, OnInit, OnDestroy } from '@angular/core';
import { StoreService, AuthService } from '../../services';
import { groupBy as _groupBy } from 'lodash';
import { PercentageGaugeComponent } from '../../components/graphs/percentage-gauge/percentage-gauge.component';
import { ActivePatientsGraphComponent } from '../../components/graphs/active-patients-graph/active-patients-graph.component';
import { PatientsEnrolledGraphComponent } from '../../components/graphs/patients-enrolled-graph/patients-enrolled-graph.component';
import * as moment from 'moment';
import { Subscription } from 'rxjs';
import patientsEnrolledData from './patientsEnrolledData';
import {
  filter as _filter,
  find as _find,
  map as _map,
} from 'lodash';
import { map } from 'd3';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit, OnDestroy {

  public org = null;
  public patients = null;
  public patientsGrouped = null;
  public employees = [];
  public employeeChecked = {};
  public facilities = [];
  public facilityChecked = {};

  public riskLevelBreakdown = null;
  public patientAdoption = null;
  public billingOverview = null;

  public analyticsData = null;

  public patientsEnrolledData = [];
  public filteredPatientsEnrolledData = patientsEnrolledData;

  public multiOpen;
  public dashTip1;
  public multi2Open;
  public multi3Open;

  public patientsEnrolledStart:moment.Moment = moment().subtract(5, 'M').startOf('M');
  public patientsEnrolledEnd:moment.Moment = moment();

  public datepickerOptions = {
     relativeTop: '-368px',
   };

  public constructor(
    private auth: AuthService,
    private store: StoreService,
  ) { }

  private organizationSub:Subscription = null;

  public ngOnInit() {
    this.store.PatientProfile.readListPaged().subscribe((res) => {
      this.patients = res;
      let patientGroupDefaults = {
        'pre-potential': null,
        'potential': null,
        'invited': null,
        'delinquent': null,
        'inactive': null,
        'active': null,
      };
      let groupedByStatus = _groupBy(res, obj => {
        return obj.status;
      });
      this.patientsGrouped = Object.assign({}, patientGroupDefaults, groupedByStatus);
    });

    this.organizationSub = this.auth.organization$.subscribe(
      org => {

        if (!org) return;
        this.org = org;
        this.store.EmployeeProfile.readList().subscribe((res) => {
          this.employees = res.results;
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
            console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
            console.log(this.patientAdoption);
            console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
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
      }
    )

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
    this.refreshRiskLevels();
  }

  public refreshRiskLevels() {
    if (this.org) {
      this.store.Organization.detailRoute('GET', this.org.id, 'patient_risk_levels', {}, {
        employees: _filter(Object.keys(this.employeeChecked), id => this.employeeChecked[id]).join(','),
      }).subscribe((res:any) => {
        this.riskLevelBreakdown = res;
      });
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

}
