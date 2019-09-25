import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';

import { ModalService } from '../../../modules/modals';

import { INewPatientDetails } from '../../../models/new-patient-details';
import { IPatient } from '../../../models/patient';
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from '../../../models/patient-enrollment-modal-response';
import { Utils } from '../../../utils';

@Component({
  selector: 'app-enrollment-patient-enrolled',
  templateUrl: './enrollment-patient-enrolled.component.html',
  styleUrls: ['./enrollment-patient-enrolled.component.scss'],
})
export class EnrollmentPatientEnrolledComponent implements OnInit {
  public carePlanName: string;
  public data: INewPatientDetails = null;
  public facilityName: string;
  public firstName: string;
  public lastName: string;
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Complete, step: PatientCreationStep.EnrollmentComplete };
  public serviceAreaName: string;
  public startDate: string;

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public ngOnInit() {
    this.modalResponse.patient = this.data.patient.patient as IPatient;
    this.carePlanName = this.data.carePlan.name;
    this.facilityName = this.data.facility.name;
    this.firstName = this.data.firstName;
    this.lastName = this.data.lastName;
    this.serviceAreaName = this.data.serviceArea.name;

    let date: moment.MomentInput = Utils.isNullOrUndefined(this.data.enrollmentConsentDetails.planStartDate)
      ? new Date()
      : this.data.enrollmentConsentDetails.planStartDate;

    let momentDate = moment(date);
    this.startDate = momentDate.format('M/D/YYYY');
  }

  public close(): void {
    this.modals.close(this.modalResponse);
  }
}
