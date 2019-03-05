import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';
import { AuthService, StoreService } from '../../../../../services';

@Component({
  selector: 'app-edit-user-details',
  templateUrl: './edit-user-details.component.html',
  styleUrls: ['./edit-user-details.component.scss'],
})
export class EditUserDetailsComponent implements OnInit {

  public data = null;

  public org = null;
  public employedBy = null;
  public specialty = null;
  public npi = '';
  public phone = '';
  public affiliates = [];
  public specialties = [];

  public tooltipEUDMOpen;

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    if (this.data) {
      this.employedBy = this.data.employedBy;
      this.specialty = this.data.specialty;
      this.npi = this.data.npi;
      this.phone = this.data.phone;
    }

    this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.org = org;

      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((res:any) => {
        this.affiliates = res.results.filter(f => f.is_affiliate);
      })

      this.store.ProviderSpecialty.readListPaged().subscribe(res => {
        this.specialties = res;
      })

    })

  }

  public compareFn(c1, c2) {
    return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

  public close() {
    this.modals.close(null);
  }

  public save() {
    if (this.employedBy.id !== this.data.employedBy.id && this.data.employedBy.hasOwnProperty('is_affiliate')) {
      this.data.employee.facilities = this.data.employee.facilities.filter(f => f.id !== this.data.employedBy.id);
    } else if (this.employedBy.id !== this.data.employedBy.id && this.employedBy.hasOwnProperty('is_affiliate')) {
      this.data.employee.facilities.push(this.employedBy)
    }
    const facilities = this.data.employee.facilities.map(f => f.id);
    let organizations;
    if (!this.employedBy.hasOwnProperty('is_affiliate')) {
      organizations = [this.employedBy.id];
    } else {
      organizations = this.data.employee.organizations.map(o => o.id);
    }

    this.store.EmployeeProfile.update(this.data.employee.id, {
      facilities,
      organizations,
      specialty: this.specialty.id,
      npi_code: this.npi,
    }).subscribe(res => {
      if (this.phone !== this.data.phone) {
        this.store.User.update(this.data.employee.user.id, {
          phone: this.phone
        }).subscribe(() => {
          res.user.phone = this.phone;
          this.modals.close(res);
        })
      } else {
        this.modals.close(res);
      }
    })

  }

}
