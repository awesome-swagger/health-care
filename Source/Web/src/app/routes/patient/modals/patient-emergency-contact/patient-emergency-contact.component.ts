import { Component, OnInit } from '@angular/core';
import {ModalService} from '../../../../modules/modals';
import {StoreService} from '../../../../services';

@Component({
  selector: 'app-patient-emergency-contact',
  templateUrl: './patient-emergency-contact.component.html',
  styleUrls: ['./patient-emergency-contact.component.scss'],
})
export class PatientEmergencyContactComponent implements OnInit {

  public data = null;

  public name = '';
  public relationship = '';
  public phone = '';
  public email = '';

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data && this.data.emergencyContact &&  Object.keys(this.data.emergencyContact).length > 0) {
      const contact = this.data.emergencyContact;
      this.name = `${contact.first_name} ${contact.last_name}`;
      this.relationship = contact.relationship;
      this.phone = contact.phone;
      this.email = contact.email;
    }
  }

  public save() {
    if (this.data && this.data.emergencyContact &&  Object.keys(this.data.emergencyContact).length > 0) {
       this.store.PatientProfile.detailRoute('PUT', this.data.patient.id, `emergency_contacts/${this.data.emergencyContact.id}`, {
        first_name: this.name.split(' ')[0],
        last_name: this.name.split(' ')[1],
        relationship: this.relationship,
        phone: this.phone,
        email: this.email,
      }).subscribe((res:any) => {
        this.modals.close(res);
      })
    } else {
      this.store.PatientProfile.detailRoute('POST', this.data.patient.id, 'emergency_contacts', {
        first_name: this.name.split(' ')[0],
        last_name: this.name.split(' ')[1],
        relationship: this.relationship,
        phone: this.phone,
        email: this.email,
      }).subscribe((res:any) => {
        this.modals.close(res);
      })
    }
  }

  public close() {
    this.modals.close(null);
  }

}
