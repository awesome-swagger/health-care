import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent } from '../../../components';
import { StoreService, AuthService } from '../../../services';
import { UtilsService } from '../../../services';
import { PopoverComponent } from '../../../modules/popover';
import {
  concat as _concat,
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  filter as _filter,
  find as _find,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean,
  sum as _sum,
  compact as _compact,
  get as _get,
} from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {

  public activePatients = [];
  public activeCount = 0;
  public activePatientsGrouped = [];
  public average = null;

  public facilities = [];
  public facilityOpen = {};
  public serviceAreas = [];
  public serviceAreaChecked = {};
  public carePlanTemplates = [];
  public carePlanTemplateChecked = {};

  public accordionsOpen = {};

  public employees = [];
  public employeeChecked = {};

  public openAlsoTip = {};
  public activeServiceAreas = {};
  public activeCarePlans = {};
  public activeUsers = {};
  public users = null;
  public toolAP1Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

  private authSub = null;

  constructor(
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private modals: ModalService,
    private store: StoreService,
    private utils: UtilsService,
  ) { }

  public ngOnInit() {

    this.authSub = this.auth.organization$.subscribe((org) => {
      if (org === null) return;
      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((facilities:any) => {
        this.facilities = facilities.results.filter(f => !f.is_affiliate);
        this.facilities.forEach(facility => {
          facility.avgRiskLevel = 0;
          facility.totalTime = '0:00';
          this.accordionsOpen[facility.id] = false;
          this.store.Facility.detailRoute('GET', facility.id, 'patients', {}, { type: 'active' }).subscribe((patients:any) => {
            facility.patients = patients.results;
            facility.patients.forEach(patient => {
              this.store.CarePlan.readListPaged({ patient: patient.id }).subscribe(plans => {
                patient.carePlans = plans;
                patient.carePlans.forEach(plan => {
                  plan.engagement = plan.engagement || 0;
                  plan.outcomes = plan.outcomes || 0;
                  plan.current_week = plan.current_week || 0;
                  plan.risk_level = plan.risk_level || 0;
                  plan.tasks_this_week = plan.tasks_this_week || 0;
                  this.store.CareTeamMember.readListPaged({ plan: plan.id }).subscribe(careTeamMembers => {
                    plan.careTeamMembers = careTeamMembers;
                  })
                })
              })
            })
          })
          this.auth.user$.subscribe(user => {
            if (!user) return;
            if (user.facilities.length === 1) {
              this.accordionsOpen[user.facilities[0].id] = true;
            }
          })
        })
      })

      this.store.EmployeeProfile.readListPaged().subscribe(users => {
        this.employees = users;
        users.forEach(user => {
          this.employeeChecked[user.id] = true;
        })

        this.route.params.subscribe(params => {
          if (!params) return;
          if (params.userId) {
            users.forEach(user => {
              this.employeeChecked[user.id] = false;
            })
            this.employeeChecked[params.userId] = true;
          }
        })
      })

    },
    )

    this.store.ServiceArea.readListPaged().subscribe(serviceAreas => {
      this.serviceAreas = serviceAreas;
      serviceAreas.forEach(area => {
        this.serviceAreaChecked[area.id] = true;
      })
    })

    this.store.CarePlanTemplate.readListPaged().subscribe(templates => {
      this.carePlanTemplates = templates
      templates.forEach(template => {
        this.carePlanTemplateChecked[template.id] = true;
      })
    })

    this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.store.CarePlan.detailRoute('GET', null, 'average', {}, {
        patient__facility__organization: org.id
      }).subscribe((res:any) => {
        this.average = res;
      })
    })

  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
  }

  public getPatients() {
    let promise = new Promise((resolve, reject) => {
      let patientsSub = this.store.PatientProfile.readListPaged({page: 1}).subscribe(
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

  public confirmRemovePatient(facility, patient, plan) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to remove this patient from this plan? This will negate their current progress. This cannot be undone.',
        cancelText,
        okText,
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === okText) {
        this.store.CarePlan.destroy(plan.id).subscribe(res => {
          const patientFacility = this.facilities.find(f => f.id === facility.id);
          const planPatient = _find(patientFacility.patients, p => p.id === patient.id);
          planPatient.carePlans = _filter(planPatient.carePlans, p => p.id !== plan.id);
        });
      }
    });
  }

  public addPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      data: {
        action: 'add',
        enrollPatientChecked: true,
        patientInSystem: true,
        planKnown: false,
      },
      width: '576px',
    }).subscribe(res => {
      if (!res) return;
      console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
      console.log(res);
      console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
      if (!(res.hasOwnProperty('patient') && res.hasOwnProperty('plan'))) {
        res.careTeamMembers = res.careTeam;
        res.engagement = res.engagement || 0;
        res.outcomes = res.outcomes || 0;
        res.current_week = res.current_week || 0;
        res.risk_level = res.risk_level || 0;
        res.tasks_this_week = res.tasks_this_week || 0;
        const facility = this.facilities.find(f => f.id === res.patient.facility.id)
        let patient = facility.patients.find(p => p.id === res.patient.id);
        if (!patient) {
          this.store.PatientProfile.read(res.patient.id).subscribe(patient => {
            if (facility.patients && facility.patients.length) {
              facility.patients.push(patient);
            } else {
              facility.patients = [patient];
            }
            this.store.CarePlan.readListPaged({ patient: patient.id }).subscribe(plans => {
              patient.carePlans = plans;
              patient.carePlans.forEach(plan => {
                this.store.CareTeamMember.readListPaged({ plan: plan.id }).subscribe(careTeamMembers => {
                  plan.careTeamMembers = careTeamMembers;
                })
              })
            })
          })
        } else {
          if (patient.carePlans && patient.carePlans.length) {
            patient.carePlans.push(res);
          } else {
            patient.carePlans = [res];
          }
        }
      }
      if (res.hasOwnProperty('patient') && res.hasOwnProperty('plan')) {
        res.plan.careTeamMembers = res.plan.careTeam;
        res.plan.engagement = res.plan.engagement || 0;
        res.plan.outcomes = res.plan.outcomes || 0;
        res.plan.current_week = res.plan.current_week || 0;
        res.plan.risk_level = res.plan.risk_level || 0;
        res.plan.tasks_this_week = res.plan.tasks_this_week || 0;
        res.patient.carePlans = [res.plan]
        const facility = this.facilities.find(f => f.id === res.patient.facility.id)
        if (facility.patients && facility.patients.length) {
          facility.patients.push(res.patient);
        } else {
          facility.patients = [res.patient];
        }
      }
    });
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
    if (patient && patient.carePlans) {
      const plans = patient.carePlans.slice();
      plans.splice(i, 1);
      return _map(plans, p => p.plan_template.name);
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
    Object.keys(this.activeCarePlans).forEach(area => {
      this.activeCarePlans[area] = status;
    })
  }

  public toggleAllUsers(status) {
    Object.keys(this.activeUsers).forEach(area => {
      this.activeUsers[area] = status;
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

  public hasActiveUser(plan) {
    if (plan.care_team_members && plan.care_team_members.length) {
      for (let i = 0; i < plan.care_team_members.length; i++) {
        if (this.activeUsers[plan.care_team_members[i].employee_profile.id]) {
          return true;
        }
      }
    } else {
      return this.showAllUsers;
    }
    return false;
  }

  public get showAllUsers() {
    return true;
  }

  public hasCheckedCareTeamMember(plan) {
    let result = false;
    if (plan.careTeamMembers) {
      plan.careTeamMembers.forEach(teamMember => {
        if (this.employeeChecked[teamMember.employee_profile.id] === true) {
          result = true;
        }
      })
    }
    return result;
  }

}

