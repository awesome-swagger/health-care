import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent } from '../../../components';
import { StoreService } from '../../../services';
import { UtilsService } from '../../../services';
import {
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  filter as _filter,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean,
  sum as _sum,
  compact as _compact
} from 'lodash';
import * as moment from 'moment';
import patientsData from './patients-data';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {

  public activePatients = [];
  public activePatientsGrouped = [];

  public accordionsOpen = [];

  public openAlsoTip = {};
  public activeServiceAreas = {};
  public activeCarePlans = {};
  public users = null;
  public toolAP1Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

  constructor(
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.activePatients = [];
    this.activePatientsGrouped = [];
    this.getPatients().then((patients: any) => {
      // patients = patientsData.results; // TODO: remove
      this.activePatients = _filter(patients, p => p.is_active);
      this.activePatientsGrouped = this.groupPatientsByFacility(patients);

      this.activePatients.forEach((patient, i) => {
        let carePlanSub = this.store.PatientCarePlans(patient.id).read().subscribe(
          (plans) => {
            this.activePatients[i].care_plans = plans.map((plan) => {
              return {
                name: plan.plan_template.name,
                service_area: plan.plan_template.service_area || "Undefined",
                current_week: plan.current_week || 0,
                total_weeks: plan.plan_template.duration_weeks || 0,
                time_in_minutes: plan.time || 0,
                engagement: plan.engagement || 0,
                outcomes: plan.outcomes || 0,
                risk_level: plan.risk_level || 0,
                next_check_in: plan.next_check_in || 0,
                tasks_this_week: plan.tasks_this_week || 0,
              }
            });
            this.allServiceAreas.forEach(serviceArea => {
              this.activeServiceAreas[serviceArea] = true;
            });
            this.allCarePlans.forEach(carePlan => {
              this.activeCarePlans[carePlan] = true;
            });
          },
          (err) => {

          },
          () => {
            carePlanSub.unsubscribe();
          }
        )
      })

      console.log(this.uniqueFacilities());
      console.log(this.activePatientsGrouped);
    });

    let employeesSub = this.store.EmployeeProfile.readListPaged().subscribe(
      (employees) => {
        this.users = employees;
      },
      (err) => {

      },
      () => {
        employeesSub.unsubscribe();
      }
    )
  }

  public ngOnDestroy() { }

  public getPatients() {
    let promise = new Promise((resolve, reject) => {
      let patientsSub = this.store.PatientProfile.readListPaged().subscribe(
        (patients) => {
          resolve(patients);
        },
        (err) => {
          reject(err);
        },
        () => {
          patientsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public groupPatientsByStatus(patients) {
    let patientGroupDefaults = {
      'potential': null,
      'invited': null,
      'inactive': null,
      'active': null,
    };
    let groupedByStatus = _groupBy(patients, (obj) => {
      return obj.status;
    });
    return Object.assign({}, patientGroupDefaults, groupedByStatus);
  }

  public groupPatientsByFacility(patients) {
    let groupedByFacility = _groupBy(patients, (obj) => {
      return obj.facility.id;
    });
    return groupedByFacility;
  }

  public confirmRemovePatient() {
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to remove this patient from this plan? This will negate their current progress. This cannot be undone.',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => { });
  }

  public addPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'add',
        patientKnown: false,
        patientInSystem: true,
        planKnown: false,
      },
      width: '576px',
    }).subscribe(() => { });
  }

  public uniqueFacilities() {
    return _uniqBy(this.activePatients.map((obj) => { return obj.facility; }), 'id');
  }

  public getPatientsForFacility(facility) {
    return this.activePatientsGrouped[facility.id];
  }

  public routeToPatient(patient) {
    this.router.navigate(['patient', patient.id]);
  }

  public getAlsoPlans(i, patient) {
    if (patient && patient.care_plans) {
      const plans = patient.care_plans.slice();
      plans.splice(i, 1);
      return _map(plans, p => p.name);
    }
    return [];
  }

  public formatTime(minutes) {
    if (!minutes) return '';
    const h = `${Math.floor(minutes / 60) || ''}`;
    const m = `${minutes % 60}`;
    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`
  }

  public riskLevelText(x) {
    if (x < 50) {
      return 'High Risk';
    } else if (x < 70) {
      return 'Med Risk';
    } else if (x <= 90) {
      return 'Low Risk';
    } else {
      return 'On Track';
    }
  }

  get allPlans() {
    if (this.activePatients) {
      return _compact(_flattenDeep(_map(this.activePatients, p => p.care_plans)));
    }
  }

  get avgTimeInMinutes() {
    return Math.floor(_mean(_map(this.allPlans, p => p.time_in_minutes)));
  }

  get avgEngagement() {
    return Math.floor(_mean(_map(this.allPlans, p => p.engagement)))
  }

  get avgOutcomes() {
    return Math.floor(_mean(_map(this.allPlans, p => p.outcomes)))
  }

  get avgRiskLevel() {
    return Math.floor(_mean(_map(this.allPlans, p => p.risk_level)))
  }

  public facilityPlans(i) {
    if (this.getPatientsForFacility(i)) {
      return _compact(_flattenDeep(_map(this.getPatientsForFacility(i), p => p.care_plans)));
    }
  }

  public avgFacilityTimeInMinutes(i) {
    return Math.floor(_mean(_map(this.facilityPlans(i), p => p.time_in_minutes)));
  }

  public avgFacilityRiskLevel(i) {
    return Math.floor(_mean(_map(this.facilityPlans(i), p => p.risk_level)));
  }

  get allServiceAreas() {
    const plans = this.allPlans;
    return _uniqBy(_map(plans, p => p.service_area));
  }

  get allCarePlans() {
    const plans = _filter(this.allPlans, p => this.activeServiceAreas[p.service_area]);
    return _uniqBy(_map(plans, p => p.name));
  }

  public toggleAllServiceAreas(status) {
    Object.keys(this.activeServiceAreas).forEach(area => {
      this.activeServiceAreas[area] = status;
    })
  }

  public toggleAllCarePlans(status) {
    Object.keys(this.activeServiceAreas).forEach(area => {
      this.activeServiceAreas[area] = status;
    })
  }

  public timePillColor(plan) {
    const allotted = plan.allotted_time || 30;
    return this.utils.timePillColor(plan.time_in_minutes, allotted);
  }

  public avgTimePillColor() {
    const avgTime = _sum(_map(this.allPlans, p => p.time_in_minutes)) / this.allPlans.length;
    const avgAllotted = _sum(_map(this.allPlans, p => p.allotted_time || 30)) / this.allPlans.length;
    return this.utils.timePillColor(avgTime, avgAllotted);
  }

  public avgFacilityTimeColor(facility) {
    if (this.facilityPlans(facility)) {
      const avgTime = _sum(_map(this.facilityPlans(facility), p => p.time_in_minutes)) / this.facilityPlans(facility).length;
      const avgAllotted = _sum(_map(this.facilityPlans(facility), p => p.allotted_time || 30)) / this.facilityPlans(facility).length;
      return this.utils.timePillColor(avgTime, avgAllotted);
    }
  }
}
