import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { AuthService, StoreService } from '../../services';
import { EditFacilityComponent } from './modals/edit-facility.component';
import { ToastService } from '../../modules/toast';
import * as moment from 'moment';
import {
  filter as _filter,
  find as _find
} from 'lodash';

@Component({
  selector: 'app-organization',
  templateUrl: './organization.component.html',
  styleUrls: ['./organization.component.scss'],
})
export class OrganizationComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public affiliates = [];
  public userCount = 0;
  public availableAccounts = 50;
  public availableAccountsLeft = 50;
  public openAlert = {
    users: false,
    date: false,
  };
  public renewalDate = null;
  public renewalDiff = 100;

  private organizationSub: Subscription = null;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.organizationSub = this.auth.organization$.subscribe(
      (organization) => {
        if (organization === null) {
          return;
        }
        this.organization = organization;

        this.renewalDate = moment('January 30, 2022'); // TODO: this should eventually be set on the org
        this.renewalDiff = this.renewalDate.diff(moment(), 'days');
        if (this.renewalDiff <= 90) {
          this.openAlert.date = true;
        }

        this.store.Facility.readListPaged({
          organization_id: organization.id
        }).subscribe(
          (facilities) => {
            this.facilities = facilities.filter((obj) => !obj.is_affiliate);
            this.affiliates = facilities.filter((obj) => obj.is_affiliate);
          }
        );
      }
    );

    let usersSub = this.store.EmployeeProfile.readListPaged().subscribe(
      users => {
        this.userCount = users.length;
        this.availableAccountsLeft = this.availableAccounts - this.userCount;
        if (this.availableAccountsLeft <= 5) {
          this.openAlert.users = true;
        }
      },
      err => {},
      () => usersSub.unsubscribe()
    )
  }

  public ngOnDestroy() {
    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public clickEditOrganization() {
    // NOTE: EditFacilityComponent is used for adding and editing facilities and organizations.
    this.modals.open(EditFacilityComponent, {
      closeDisabled: false,
      data: {
        type: 'edit',
        isAffiliate: false,
        facility: this.organization,
        isOrganization: true,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public openAddFacility(isAffiliate: boolean) {
    // NOTE: EditFacilityComponent is used for adding and editing facilities and organizations.
    this.modals.open(EditFacilityComponent, {
      closeDisabled: false,
      data: {
        type: 'add',
        isAffiliate: isAffiliate,
        facility: {},
        isOrganization: false,
      },
      width: '512px',
    }).subscribe((res) => {
      if (res.is_affiliate) {
        this.affiliates.push(res);
      } else {
        this.facilities.push(res);
      }
    });
  }

  public openEditFacility(facility) {
    this.modals.open(EditFacilityComponent, {
      closeDisabled: false,
      data: {
        type: 'edit',
        isAffiliate: facility.is_affiliate,
        facility: facility,
        isOrganization: false,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public deleteFacility(facility) {
    let patientsSub = this.store.Facility.detailRoute('get', facility.id, 'active_patients').subscribe(
      (patients: any) => {
        let usersSub = this.store.EmployeeProfile.readListPaged().subscribe(
          users => {
            const facilityUsers = _filter(users, u => _find(u.facilities, f => f.id === facility.id));
            this.modals.open(ConfirmModalComponent, {
              data: {
                title: 'Are You Sure?',
                body: `Are you sure you want to delete this facility? This would remove ${facilityUsers.length} user accounts and ${patients.results.length} active patients.`,
                okText: 'Continue',
                cancelText: 'Cancel',
              },
              width: '440px',
            }).subscribe((res) => {
              if (res === 'Continue') {
                this.store.Facility.destroy(facility.id).subscribe();
                this.affiliates = _filter(this.affiliates, a => a.id !== facility.id);
                this.facilities = _filter(this.facilities, a => a.id !== facility.id);
                // TODO: Trigger a confirmation toast to undo.
              }
            });
          },
          err => {},
          () => usersSub.unsubscribe()
        )
      },
      err => {},
      () => patientsSub.unsubscribe()
    )

  }

  public closeAlert(n) {
    this.openAlert[n] = false;
  }
}
