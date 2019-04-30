import { Component, OnInit } from '@angular/core';
import {ModalService} from '../../../../modules/modals';
import {StoreService} from '../../../../services';

@Component({
  selector: 'app-patient-communication',
  templateUrl: './patient-communication.component.html',
  styleUrls: ['./patient-communication.component.scss'],
})
export class PatientCommunicationComponent implements OnInit {

  public selectedPreference = 'in_app_messaging';
  public email = '';
  public phone = '';
  public data = null;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.selectedPreference = this.data.patient.communication_preference;
      this.email = this.data.patient.communication_email;
      this.phone = this.data.patient.user.phone;
    }
  }

  public close() {
    this.modals.close(null);
  }

  public submit() {
    this.store.User.update(this.data.patient.user.id, {
      phone: this.phone,
    }).subscribe((user: any) => {
      this.store.PatientProfile.update(this.data.patient.id, {
        communication_preference: this.selectedPreference,
        communication_email: this.email,
      }).subscribe((patient: any) => {
        this.modals.close(patient);
      })
    })
  }

}
