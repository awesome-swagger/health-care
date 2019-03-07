import { Component, OnInit } from '@angular/core';
import { AuthService, StoreService } from '../../../../services';
import { ModalService } from '../../../../modules/modals';

@Component({
  selector: 'app-patient-profile',
  templateUrl: './patient-profile.component.html',
  styleUrls: ['./patient-profile.component.scss'],
})
export class PatientProfileComponent implements OnInit {

  public data = null;

  public birthYear = '';
  public birthMonth = '';
  public birthDay = '';
  public gender = '';

  public insurances = [];
  public selectedInsurance = null;
  public selectedSecondaryInsurance = null;

  public mrn = '';
  public ethnicity = '';
  public cognitiveAbility = '';

  public heightFeet = '';
  public heightInches = '';

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);

    if (this.data && this.data.patient) {
      this.birthYear = this.data.patient.user.birthdate.split('-')[0]
      this.birthMonth = this.data.patient.user.birthdate.split('-')[1]
      this.birthDay = this.data.patient.user.birthdate.split('-')[2]
      this.gender = this.data.patient.user.gender;
      this.selectedInsurance = this.data.patient.insurance;
      this.selectedSecondaryInsurance = this.data.patient.secondary_insurance;
      this.mrn = this.data.patient.mrn;
      this.heightFeet = this.data.patient.height_feet;
      this.heightInches = this.data.patient.height_inches;
      this.ethnicity = this.data.patient.ethnicity.toLowerCase();
      this.cognitiveAbility = this.data.patient.cognitive_ability.toLowerCase();
    }

    this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.store.Organization.detailRoute('GET', org.id, 'insurances').subscribe((res:any) => {
        this.insurances = res.results;
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
    this.store.User.update(this.data.patient.user.id, {
      birthdate: `${this.birthYear}-${this.birthMonth}-${this.birthDay}`,
      gender: this.gender,
    }).subscribe(user => {
      this.store.PatientProfile.update(this.data.patient.id, {
        insurance: this.selectedInsurance.id,
        secondary_insurance: this.selectedSecondaryInsurance.id,
        mrn: this.mrn,
        height_feet: this.heightFeet,
        height_inches: this.heightInches,
        ethnicity: this.ethnicity,
        cognitive_ability: this.cognitiveAbility,
      }).subscribe(patient => {
        this.modals.close(patient);
      })
    })
  }

}
