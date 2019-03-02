import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-enrollment',
  templateUrl: './enrollment.component.html',
  styleUrls: ['./enrollment.component.scss'],
})
export class EnrollmentComponent implements OnInit {

  public data = null;

  public verbal_consent = false;
  public seen_within_year = false;
  public discussed_co_pay = false;
  public will_use_mobile_app = false;
  public will_interact_with_team = false;
  public will_complete_tasks = false;

  public email = '';
  public gender = '';
  public dob = '';
  public communicationPreference = 'In-App Messaging';

  public showEPStep2;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
  }

  public phoneNum(num) {
    return `(${num.slice(0,3)})${num.slice(3,6)}-${num.slice(6,num.length)}`
  }

  public get saveDisabled() {
    if (this.email && this.data.potentialPatient) {
      return false;
    }
    return true;
  }

  public close() {
    this.modals.close(null);
  }

  public save() {
    const patient = this.data.patient;
    this.store.AddUser.createAlt({
      email: this.email,
      first_name: patient.first_name,
      last_name: patient.last_name,
      password1: 'password',
      password2: 'password',
      gender: this.gender,
    }).subscribe(user => {
      this.store.PatientProfile.create({
        user: user.pk,
        facility: patient.facility[0],
        is_active: true,
        is_invited: false,
      }).subscribe(patientProfile => {
        this.store.CarePlan.create({
          patient: patientProfile.id,
          plan_template: patient.care_plan.id
        }).subscribe(plan => {
          this.store.PlanConsentForm.create({
            plan: plan.id,
            verbal_consent: this.verbal_consent,
            seen_within_year: this.seen_within_year,
            discussed_co_pay: this.discussed_co_pay,
            will_use_mobile_app: this.will_use_mobile_app,
            will_interact_with_team: this.will_interact_with_team,
            will_complete_tasks: this.will_complete_tasks,
          }).subscribe(res => {
            this.store.PotentialPatient.destroy(patient.id).subscribe(res => {
              this.modals.close({ patient: patient.id, facility: patient.facility[0] });
            })
          })
        })
      })
    }) 
  }

}
