import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { AuthService, StoreService } from '../../services';
import { EditFacilityComponent } from './modals/edit-facility.component';
import { ToastService } from '../../modules/toast';

@Component({
  selector: 'app-organization',
  templateUrl: './organization.component.html',
  styleUrls: ['./organization.component.scss'],
})
export class OrganizationComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public affiliates = [];

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
  }

  public ngOnDestroy() {
    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public clickEditOrganization() {
    // NOTE: EditFacilityComponent is used for adding and editing facilities and organizations.
    this.modals.open(EditFacilityComponent, {
      closeDisabled: true,
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
      closeDisabled: true,
      data: {
        type: 'add',
        isAffiliate: isAffiliate,
        facility: {},
        isOrganization: false,
      },
      width: '512px',
    }).subscribe((res) => {
      this.facilities.push(res);
    });
  }

  public openEditFacility(facility) {
    this.modals.open(EditFacilityComponent, {
      closeDisabled: true,
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
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Are You Sure?',
        body: 'Are you sure you want to delete this facility? This would remove 28 user accounts and 468 active patients.',
        okText: 'Continue',
        cancelText: 'Cancel',
      },
      width: '440px',
    }).subscribe((res) => {
      if (res === 'Continue') {
        this.store.Facility.destroy(facility.id).subscribe();
        // TODO: Trigger a confirmation toast to undo.
      }
    });
  }
}
