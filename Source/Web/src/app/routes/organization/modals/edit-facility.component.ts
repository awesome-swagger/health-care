import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { AuthService, StoreService } from '../../../services';

@Component({
  selector: 'app-edit-facility',
  templateUrl: './edit-facility.component.html',
  styleUrls: ['./edit-facility.component.scss'],
})
export class EditFacilityComponent implements OnInit {

  public data = null;
  public organization = null;
  public action = '';
  public model = '';

  constructor(
    public modals: ModalService,
    public auth: AuthService,
    public store: StoreService,
  ) { }

  public ngOnInit() {
    this.action = this.data.type.replace(/^\w/, c => c.toUpperCase());
    if (this.data.isOrganization) {
      this.model = 'Organization';
    } else if (this.data.isAffiliate) {
      this.model = 'Affiliate';
    } else {
      this.model = 'Facility';
    }
    this.auth.organization$.subscribe((organization) => {
      if (!organization) {
        return;
      }
      this.organization = organization;
    });
  }

  public submit() {
    if (this.data.type === 'add') {
      if (this.data.isAffiliate) {
        this.data.facility.is_affiliate = true;
      } else {
        this.data.facility.is_affiliate = false;
      }
      this.data.facility.organization = this.organization.id;
      this.store.Facility.create(this.data.facility).subscribe(() => {});
      this.modals.close('created');
    } else if (this.data.type === 'edit') {
      if (this.data.isOrganization) {
        this.store.Organization.update(this.data.facility.id, this.data.facility, true).subscribe(() => {});
      } else {
        this.store.Facility.update(this.data.facility.id, this.data.facility, true).subscribe(() => {});
      }
      this.modals.close('updated');
    }
  }
}
