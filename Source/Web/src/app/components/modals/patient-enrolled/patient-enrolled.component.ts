import { Component, OnInit } from '@angular/core';
import {StoreService} from '../../../services';

@Component({
  selector: 'app-patient-enrolled',
  templateUrl: './patient-enrolled.component.html',
  styleUrls: ['./patient-enrolled.component.scss'],
})
export class PatientEnrolledComponent implements OnInit {

  public data = null;
  public facility = null;

  constructor(
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    if (this.data.patient && this.data.patient.facility[0]) {
      this.store.Facility.read(this.data.patient.facility[0]).subscribe((res: any) => {
        this.facility = res;
      })
    }
  }
}
