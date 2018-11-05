import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../../services';

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
  public titleInput: string = null;
  public emailInput = '';
  public phoneInput = '';
  public organizationInput: string = null;
  public specialtyInput: string = null;
  public npiInput = '';

  constructor(
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
}
