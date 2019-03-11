import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  filter as _filter,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean
} from 'lodash';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { HttpService, StoreService, AuthService } from '../../../services';
import { AppConfig } from '../../../app.config';
import { ReminderEmailComponent } from './modals/reminder-email/reminder-email.component';
import { AddPatientToPlanComponent } from '../../../components';

@Component({
  selector: 'app-invited',
  templateUrl: './invited.component.html',
  styleUrls: ['./invited.component.scss'],
})
export class InvitedPatientsComponent implements OnDestroy, OnInit {

  public invitedPatients = [];
  public invitedPatientsGrouped = [];
  public activeServiceAreas = {};
  public activeCarePlans = {};
  public openAlsoTip = {};
  public toolIP1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

  public facilityAccordOpen = {};

  public facilities = [];
  public employees = [];
  public employeeChecked = {};
  public userSearch:string = '';

  constructor(
    private auth: AuthService,
    private router: Router,
    private modals: ModalService,
    private http: HttpService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.invitedPatients = [];
    this.invitedPatientsGrouped = [];
    this.store.Facility.readListPaged().subscribe((res:any) => {

      this.facilities = res.filter(f => !f.is_affiliate);

      this.facilities.forEach(f => {
        this.facilityAccordOpen[f.id] = false;
      })

      this.auth.user$.subscribe(user => {
        if (!user) return;

        if (user.facilities.length === 1) {
          this.facilityAccordOpen[user.facilities[0].id] = true;
          let employeeSub = this.auth.user$.subscribe(
            user => {
              if (!user) return;
              if (user.facilities.length === 1) {
                this.facilityAccordOpen[user.facilities[0].id] = true;
              }
            },
            () => {},
            () => {
              employeeSub.unsubscribe();
            }
          )
        }
      })

      this.facilities.forEach(facility => {
        this.getPatients(facility).then((patients: any) => {
          facility.invitedPatients = patients.results;
          facility.invitedPatients.forEach(patient => {
            this.store.CarePlan.readListPaged({patient: patient.id}).subscribe(plans => {
              patient.carePlans = plans;
              patient.carePlans.forEach(plan => {
                this.store.CareTeamMember.readListPaged({ plan: plan.id }).subscribe(careTeamMembers => {
                  plan.careTeamMembers = careTeamMembers;
                })
              })
            })
          })
        });
      })
    })

    this.store.EmployeeProfile.readListPaged().subscribe((res:any) => {
      this.employees = res;
      this.employees.forEach(e => {
        this.employeeChecked[e.id] = true;
      })
    })

  }

  public ngOnDestroy() { }

  public get totalInvited() {
    if (this.facilities) {
      let result = 0;
      this.facilities.forEach(f => {
        if (f.invitedPatients) {
          result += f.invitedPatients.length;
        }
      })
      return result;
    }
    return 0;
  }

  public getPatients(facility) {
    let promise = new Promise((resolve, reject) => {
      let patientsSub = this.store.Facility.detailRoute('GET', facility.id, 'patients', {}, { type: 'invited' }).subscribe(
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

  public getAlsoPlans(i, patient) {
    if (patient && patient.carePlans) {
      const plans = patient.carePlans.slice();
      plans.splice(i, 1);
      return _map(plans, p => p.plan_template.name);
    }
    return [];
  }

  public getPatientsForFacility(facility) {
    return this.invitedPatientsGrouped[facility.id];
  }

  public groupPatientsByFacility(patients) {
    let groupedByFacility = _groupBy(patients, (obj) => {
      return obj.facility.id;
    });
    return groupedByFacility;
  }

  get allPlans() {
    if (this.invitedPatients) {
      return _flattenDeep(_map(this.invitedPatients, p => p.care_plans));
    }
  }

  get allServiceAreas() {
    const plans = this.allPlans;
    return _uniqBy(_map(plans, p => p.service_area));
  }

  get allCarePlans() {
    const plans = _filter(this.allPlans, p => this.activeServiceAreas[p.service_area]);
    return _uniqBy(_map(plans, p => p.name));
  }


  public uniqueFacilities() {
    return _uniqBy(this.invitedPatients.map((obj) => { return obj.facility; }), 'id');
  }

  public daysSinceEnroll(patient) {
    const dateJoined = moment(patient.user.date_joined);
    const now = moment();
    return now.diff(dateJoined, 'days');
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

  public reminderEmail(patient) {
    let modalSub = this.modals.open(ReminderEmailComponent, {
      data: {
        patient: patient,
      },
      width: '512px',
    }).subscribe(
      (response) => {
        if (!response) {
          return;
        }
        let url = AppConfig.apiUrl + 'reminder_email';
        let postSub = this.http.post(url, {
          patient: response.patient.id,
          subject: response.subject,
          message: response.message,
        }).subscribe(
          (success) => {
            console.log('Successfully sent email');
          },
          (err) => {
            console.log(err);
          },
          () => {
            postSub.unsubscribe();
          }
        );
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
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
    }).subscribe()
  }

  public confirmRemovePatient(facility, patient, plan) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Remove Patient?',
       body: 'Are you sure you want to revoke this patient’s invitation? This cannot be undone.',
       cancelText,
       okText,
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === okText) {
        this.store.CarePlan.destroy(plan.id).subscribe(res => {
          const facility = this.facilities.find(f => f.id === facility.id);
          const patient = facility.invitedPatients.find(p => p.id === patient.id);
          patient.carePlans = patient.carePlans.filter(p => p.id !== plan.id);
        })
      }
    });
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

  public userSearchMatch(user) {
    return `${user.user.first_name} ${user.user.last_name}`.toLowerCase().indexOf(this.userSearch) > -1;
  }

  public toggleAllUsers(status) {
    Object.keys(this.employeeChecked).forEach(id => {
      this.employeeChecked[id] = status;
    })
  }
}
