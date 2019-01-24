import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../../services';
import { ModalService } from '../../../../modules/modals';

@Component({
  selector: 'app-add-user',
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.scss'],
})
export class AddUserComponent implements OnInit {

  public data = null;
  public titles = [];
  public organizations = [];
  public specialties = [];

  public firstNameInput = '';
  public lastNameInput = '';
  public titleInput = null;
  public emailInput = '';
  public phoneInput = '';
  public organizationInput = null;
  public specialtyInput = null;
  public npiInput = '';

  public tooltipAUM0Open;

  constructor(
    public modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    this.getTitles().then((titles: any) => {
      this.titles = titles;
    });
    this.getOrganizations().then((organizations: any) => {
      this.organizations = organizations;
    });
    this.getSpecialties().then((specialties: any) => {
      this.specialties = specialties;
    });
  }

  public getTitles() {
    let promise = new Promise((resolve, reject) => {
      let titlesSub = this.store.ProviderTitle.readListPaged().subscribe(
        (titles) => {
          resolve(titles);
        },
        (err) => {
          reject(err);
        },
        () => {
          titlesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getOrganizations() {
    let promise = new Promise((resolve, reject) => {
      let organizationsSub = this.store.Organization.readListPaged().subscribe(
        (organizations) => {
          resolve(organizations);
        },
        (err) => {
          reject(err);
        },
        () => {
          organizationsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getSpecialties() {
    let promise = new Promise((resolve, reject) => {
      let specialtiesSub = this.store.ProviderSpecialty.readListPaged().subscribe(
        (specialties) => {
          resolve(specialties);
        },
        (err) => {
          reject(err);
        },
        () => {
          specialtiesSub.unsubscribe();
        }
      )
    });
    return promise;
  }

  public submit() {
    console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
    console.log(this.titleInput);
    console.log(this.specialtyInput);
    console.log(this.organizationInput);
    console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
    if (this.firstNameInput && this.lastNameInput && this.emailInput) {
      this.modals.close({
        firstName: this.firstNameInput,
        lastName: this.lastNameInput,
        email: this.emailInput,
        title: this.titleInput,
        specialty: this.specialtyInput,
        phone: this.phoneInput,
        npi: this.npiInput,
        employedBy: this.organizationInput,
        organization: this.organizationInput,
      })
    } else {
      this.modals.close('')
    }
  }
}
