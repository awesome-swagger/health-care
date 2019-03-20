import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent } from '../../../components';
import { StoreService, AuthService } from '../../../services';
import { UtilsService } from '../../../services';
import {
  uniqBy as _uniqBy,
  filter as _filter,
  find as _find,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean,
  sum as _sum,
  compact as _compact,
} from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-active',
  templateUrl: './active.component.html',
  styleUrls: ['./active.component.scss'],
})
export class ActivePatientsComponent implements OnDestroy, OnInit {

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
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private modals: ModalService,
    private store: StoreService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.authSub = this.auth.user$.subscribe((user) => {
      if (!user) return;
      this.employee = user;
      if (user.facilities.length === 1) {
        this.accordionsOpen[user.facilities[0].id] = true;
      }
      this.organizationSub = this.auth.organization$.subscribe((organization) => {
        if (!organization) return;
        this.getCarePlanAverage(organization.id).then((average: any) => {
          this.average = average;
        });
        this.getFacilitiesForOrganization(organization.id).then((facilities: any) => {
          this.facilities = facilities.results.filter(f => !f.is_affiliate);
          this.facilities = this.facilities.filter(f => user.facilities.find(fa => fa.id === f.id));
          this.facilities.forEach((facility) => {
            this.accordionsOpen[facility.id] = false;
            this.getFacilityCarePlans(facility.id).then((carePlans: any) => {
              facility.carePlans = carePlans.results;
            });
          });
          this.store.EmployeeProfile.readListPaged().subscribe((users) => {
            this.employees = users;
            users.forEach((user) => {
              this.employeeChecked[user.id] = true;
            })
            this.route.params.subscribe((params) => {
              if (!params) return;
              if (params.userId) {
                users.forEach(user => {
                  this.employeeChecked[user.id] = false;
                });
                this.employeeChecked[params.userId] = true;
              }
            });
          });
        });
      });
    });
    this.store.ServiceArea.readListPaged().subscribe((serviceAreas) => {
      this.serviceAreas = serviceAreas;
      serviceAreas.forEach((area) => {
        this.serviceAreaChecked[area.id] = true;
      });
    })
    this.store.CarePlanTemplate.readListPaged().subscribe((templates: any) => {
      this.carePlanTemplates = templates.sort((a, b) => {
        let textA = a.name.toUpperCase();
        let textB = b.name.toUpperCase();
        return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
      });
      templates.forEach((template) => {
        this.carePlanTemplateChecked[template.id] = true;
      });
    })
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public getCarePlanAverage(organizationId) {
    return new Promise((resolve, reject) => {
      let averageSub = this.store.CarePlan.detailRoute('GET', null, 'average', {}, {
        patient__facility__organization: organizationId
      }).subscribe(
        (average) => resolve(average),
        (err) => reject(err),
        () => averageSub.unsubscribe()
      );
    });
  }

  public getFacilitiesForOrganization(organizationId) {
    return new Promise((resolve, reject) => {
      let facilitiesSub = this.store.Organization.detailRoute('GET', organizationId, 'facilities').subscribe(
        (facilities) => resolve(facilities),
        (err) => reject(err),
        () => facilitiesSub.unsubscribe()
      );
    });
  }

  public getFacilityCarePlans(facilityId) {
    return new Promise((resolve, reject) => {
      let carePlansSub = this.store.Facility.detailRoute('get', facilityId, 'care_plans').subscribe(
        (carePlans) => resolve(carePlans),
        (err) => reject(err),
        () => carePlansSub.unsubscribe()
      );
    });
  }

  public getPatients() {
    return new Promise((resolve, reject) => {
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
  }

  public progressInWeeks(plan) {
    if (!plan || !plan.created) {
      return 0;
    }
    return moment().diff(moment(plan.created), 'weeks');
  }

  public get userFilterListText() {
    const checkedList = [];
    this.employees.forEach(e => {
      if (this.employeeChecked[e.id]) {
        checkedList.push(e);
      }
    })
    if (checkedList.length === 0) {
      return 'None';
    } else if (checkedList.length === this.employees.length) {
      return 'All';
    } else if (checkedList.length === 1) {
      return `${checkedList[0].user.first_name} ${checkedList[0].user.last_name}`
    } else {
      return `${checkedList[0].user.first_name} ${checkedList[0].user.last_name} (+${checkedList.length - 1})`
    }
  }

  public confirmRemovePatient(facility, plan) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to remove this patient from this plan? This will negate their current progress. This cannot be undone.',
        cancelText,
        okText,
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === okText) {
        this.store.CarePlan.destroy(plan.id).subscribe(() => {
          const patientFacility = this.facilities.find(f => f.id === facility.id);
          patientFacility.carePlans = _filter(patientFacility.carePlans, p => p.id !== plan.id)
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
      console.log(res);
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

  public routeToPatient(patient) {
    this.router.navigate(['patient', patient.id]).then(() => {});
  }

  public formatTime(minutes) {
    if (!minutes) return '0:00';
    const h = `${Math.floor(minutes / 60)}`;
    const m = `${minutes % 60}`;
    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`
  }

  public toggleAllServiceAreas(status) {
    Object.keys(this.serviceAreaChecked).forEach((area) => {
      this.serviceAreaChecked[area] = status;
    })
  }

  public toggleAllCarePlans(status) {
    Object.keys(this.carePlanTemplateChecked).forEach((area) => {
      this.carePlanTemplateChecked[area] = status;
    })
  }

  public toggleAllUsers(status) {
    Object.keys(this.employeeChecked).forEach((user) => {
      this.employeeChecked[user] = status;
    })
  }

  public timePillColor(plan) {
    if (!plan.patient.payer_reimbursement || !plan.billing_type) {
      return;
    }
    const allotted = plan.billing_type.billable_minutes;
    return this.utils.timePillColor(plan.time_count, allotted);
  }

  public facilityTimeCount(facility) {
    if (!facility.carePlans) {
      return 0;
    } else {
      let plans = facility.carePlans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
      return _sum(_map(plans, (plan) => plan.time_count));
    }
  }

  public avgFacilityTimeColor(facility) {
    if (facility.carePlans) {
      let plans = facility.carePlans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
      if (plans.length === 0) {
        return;
      }
      const avgTime = _sum(_map(plans, (p) => p.time_count)) / plans.length;
      const avgAllotted = _sum(_map(plans, (p) => p.billing_type.billable_minutes)) / plans.length;
      return this.utils.timePillColor(avgTime, avgAllotted);
    } else {
      return;
    }
  }

  public averageTimeMinutes() {
    let facilities = this.facilities.filter((facility) => facility.carePlans);
    let plans = _flattenDeep(_map(facilities, (facility) => facility.carePlans));
    plans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    if (plans.length === 0) {
      return;
    }
    let avgTime = _sum(_map(plans, (p) => p.time_count)) / plans.length;
    return Math.floor(avgTime);
  }

  public averageTimePercentage() {
    let facilities = this.facilities.filter((facility) => facility.carePlans);
    let plans = _flattenDeep(_map(facilities, (facility) => facility.carePlans));
    plans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    if (plans.length === 0) {
      return;
    }
    let avgTime = _sum(_map(plans, (p) => p.time_count)) / plans.length;
    let avgAlloted = _sum(_map(plans, (p) => p.billing_type.billable_minutes)) / plans.length;
    return this.utils.timePillColor(avgTime, avgAlloted);
  }

  public avgFacilityRiskLevel(facility) {
    let avg = _sum(_map(facility.carePlans, (p) => p.risk_level)) / facility.carePlans.length;
    return Math.floor(avg);
  }

  public hasCheckedCareTeamMember(plan) {
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

  public saSearchMatch(sa) {
    return sa.name.toLowerCase().indexOf(this.serviceAreaSearch.toLowerCase()) > -1;
  }

  public cpSearchMatch(cp) {
    return cp.name.toLowerCase().indexOf(this.carePlanSearch.toLowerCase()) > -1;
  }

  public showUserInFilter(user) {
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
    }
    else {
      return false;
    }
  }
}
