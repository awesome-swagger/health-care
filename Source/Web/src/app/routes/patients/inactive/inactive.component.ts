import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AuthService, StoreService } from '../../../services';

@Component({
  selector: 'app-inactive',
  templateUrl: './inactive.component.html',
  styleUrls: ['./inactive.component.scss'],
})
export class InactivePatientsComponent implements OnDestroy, OnInit {

  public facilities = [];
  public facilitiesOpen = [];

  public toolXP1Open;
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;

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
}
