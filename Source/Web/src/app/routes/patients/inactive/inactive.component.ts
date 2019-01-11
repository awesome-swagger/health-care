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
  compact as _compact
} from 'lodash';

@Component({
  selector: 'app-inactive',
  templateUrl: './inactive.component.html',
  styleUrls: ['./inactive.component.scss'],
})
export class InactivePatientsComponent implements OnDestroy, OnInit {

  public facilities = [];
  public facilitiesOpen = [];
  public activePatients = [];
  public activeServiceAreas = {};

  public toolXP1Open;
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

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
        this.facilities = facilities;
        this.facilities.forEach((facility, i) => {
          let inactivePatientsSub = this.store.Facility.detailRoute('get', facility.id, 'inactive_patients', {}, {})
            .subscribe(
              (inactivePatients: any) => {
                facility.inactivePatients = inactivePatients.results;
                console.log(facility);
              },
              (err) => {},
              () => {
                inactivePatientsSub.unsubscribe();
              }
            )
        });
      }
    )
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

}
