import { Component, OnInit } from '@angular/core';
import {ModalService} from '../../../../modules/modals';
import {StoreService} from '../../../../services';

@Component({
  selector: 'app-patient-address',
  templateUrl: './patient-address.component.html',
  styleUrls: ['./patient-address.component.scss'],
})
export class PatientAddressComponent implements OnInit {

  public data = null;

  public addr_city = '';
  public addr_state = '';
  public addr_street = '';
  public addr_suite = '';
  public addr_zip = '';
  public patient = null;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);

    if (this.data) {
      this.addr_city = this.data.patient.addr_city;
      this.addr_state = this.data.patient.addr_state;
      this.addr_zip = this.data.patient.addr_zip;
      this.addr_street = this.data.patient.addr_street;
      this.addr_suite = this.data.patient.addr_suite;
      this.patient = this.data.patient;
    }
  }

  public close() {
    this.modals.close(null);
  }

  public save() {
    const { addr_zip, addr_street, addr_suite, addr_city, addr_state } = this;
    this.store.PatientProfile.update(this.patient.id, {
      addr_zip, addr_street, addr_suite, addr_city, addr_state,
    }).subscribe(res => {
      this.modals.close(res);
    })
  }

}
