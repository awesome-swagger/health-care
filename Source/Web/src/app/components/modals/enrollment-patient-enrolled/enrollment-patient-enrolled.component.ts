import { Component, OnInit } from '@angular/core';

import { ModalService } from '../../../modules/modals';

import { INewPatientDetails } from '../../../models/inew-patient-details';
import { IPatient } from '../../../models/patient';
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from '../../../models/ipatient-enrollment-modal-response';

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
  }

  public close(): void {
    this.modals.close(this.modalResponse);
  }
}
