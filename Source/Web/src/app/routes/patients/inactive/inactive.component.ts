import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AuthService, StoreService } from '../../../services';
import {
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  filter as _filter,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean,
  sum as _sum,
  compact as _compact,
  find as _find
} from 'lodash';

@Component({
  selector: 'app-inactive',
  templateUrl: './inactive.component.html',
  styleUrls: ['./inactive.component.scss'],
})
export class InactivePatientsComponent implements OnDestroy, OnInit {

  public facilities = [];
  public facilitiesOpen = {};
  public activePatients = [];
  public activeServiceAreas = {};
  public employees = [];
  public employeeChecked = {};

  public toolXP1Open;
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

  public totalInactive:number = 0;
  public total:number = 0;
  public facilityTotals = {};
  public currentPage:number = 1;
  public facilityPages = {};

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.auth.facilities$.subscribe(
      (facilities) => {
        if (!facilities) {
          return;
        }
        this.facilities = facilities.filter(f => !f.is_affiliate);
        this.facilities.forEach(facility => {
          this.facilitiesOpen[facility.id] = false;
          this.getInactivePatients(facility.id).then((inactivePatients:any) => {
            this.totalInactive += inactivePatients.count;
            this.facilityPages[facility.id] = 1;
            this.facilityTotals[facility.id] = inactivePatients.count;
            facility.inactivePatients = inactivePatients.results;

            facility.inactivePatients.forEach(patient => {
              this.store.CarePlan.readListPaged({ patient: patient.id }).subscribe(plans => {
                patient.carePlans = plans;
                patient.carePlans.forEach(plan => {
                  this.store.CareTeamMember.readListPaged({ plan: plan.id }).subscribe(careTeamMembers => {
                    plan.careTeamMembers = careTeamMembers;
                  })
                })
              })
            })

          })
        });
        this.auth.user$.subscribe(user => {
          if (!user) return;

          if (user.facilities.length === 1) {
            this.facilitiesOpen[user.facilities[0].id] = true;
          }
        })
      }
    )

    this.store.EmployeeProfile.readListPaged().subscribe((res:any) => {
      this.employees = res;
      this.employees.forEach(e => {
        this.employeeChecked[e.id] = true;
      })
    })

  }

  private getInactivePatients(facilityId) {
    return new Promise((resolve, reject) => {
      let inactivePatientsSub = this.store.Facility.detailRoute('get', facilityId, 'patients', {}, { type: 'inactive' }).subscribe(
        (inactivePatients:any) => resolve(inactivePatients),
        err => reject(err),
        () => inactivePatientsSub.unsubscribe()
      )
    });
  }

  public ngOnDestroy() { }

  public confirmArchive() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Archive Patient?',
       body: 'Are you sure you want to archive this patient? This will revoke their access to CareAdopt. They would need to be sent a new invitation in order to use the app again.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public formatTimeFromNow(time) {
    return moment(time).fromNow();
  }

  get allPlans() {
    if (this.activePatients) {
      return _compact(_flattenDeep(_map(this.activePatients, p => p.care_plans)));
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

  public switchNthFacilityPage(n:number, by:number, to:number = 0) {
    if (this.facilities) {
      const facility = this.facilities[n];
      let inactivePatientsSub = this.store.Facility.detailRoute(
        'get',
        facility.id,
        'inactive_patients',
        {},
        {
          page: to || this.facilityPages[facility.id] + by,
        }
      ).subscribe(
        (inactivePatients: any) => {
          facility.inactivePatients = inactivePatients.results;
          if (to) {
            this.facilityPages[facility.id] = to;
          } else {
            this.facilityPages[facility.id] += by;
          }
        },
        (err) => {},
        () => {
          inactivePatientsSub.unsubscribe();
        },
      );
    }
  }

  public lastPage(total) {
    return Math.ceil(total/20);
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
