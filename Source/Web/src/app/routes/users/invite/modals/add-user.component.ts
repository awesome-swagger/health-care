import { Component, OnInit } from '@angular/core';
import { StoreService, AuthService } from '../../../../services';
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
  public employedByInput = null;
  public facilityInput = null;
  public specialtyInput = null;
  public npiInput = '';
  public organization = null;
  public facilities = [];

  public tooltipAUM0Open;

  constructor(
    public auth: AuthService,
    public modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    if (this.data && this.data.user) {
      console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
      console.log(this.data.user);
      console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
      this.firstNameInput = this.data.user.firstName;
      this.lastNameInput = this.data.user.lastName;
      this.titleInput = this.data.user.title;
      this.emailInput = this.data.user.email;
      this.specialtyInput = this.data.user.specialty;
      this.employedByInput = this.data.user.employedBy;
      this.facilityInput = this.data.user.facility;
      this.npiInput = this.data.user.npi;
    }
    this.getTitles().then((titles: any) => {
      this.titles = titles;
    });
    this.getOrganizations().then((organizations: any) => {
      this.organizations = organizations;
    });
    this.getSpecialties().then((specialties: any) => {
      this.specialties = specialties;
    });

    this.auth.organization$.subscribe(org => {
      if (!org) return;

      this.organization = org;
      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((res:any) => {
        this.facilities = res.results;
      })
    })
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

  public filteredFacilities(is_affiliate) {
    return this.facilities.filter(f => f.is_affiliate === is_affiliate);
  }

  public compareFn(c1, c2) {
    return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

  public close() {
    this.modals.close(null);
  }

  public submit() {
    if (this.firstNameInput && this.lastNameInput && this.emailInput) {
      this.modals.close({
        firstName: this.firstNameInput,
        lastName: this.lastNameInput,
        title: this.titleInput,
        email: this.emailInput,
        employedBy: this.employedByInput,
        facility: this.facilityInput,
        specialty: this.specialtyInput,
        npi: this.npiInput,
      })
    } else {
      this.modals.close('')
    }
  }
}
