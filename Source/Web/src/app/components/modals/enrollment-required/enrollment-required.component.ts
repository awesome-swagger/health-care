import { Component } from '@angular/core';

import { ModalService } from '../../../modules/modals';

import { INewPatientDetails } from '../../../models/new-patient-details';
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from '../../../models/patient-enrollment-modal-response';

@Component({
  selector: 'app-enrollment-required',
  templateUrl: './enrollment-required.component.html',
  styleUrls: ['./enrollment-required.component.scss'],
})
export class EnrollmentRequiredComponent {
  public data: INewPatientDetails = null;
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Later, step: PatientCreationStep.EnrollmentRequired };

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public later(): void {
    this.modals.close(this.modalResponse);
  }

  public next(): void {
    this.modalResponse.action = PatientCreationAction.Next;
    this.modalResponse.newPatientDetails = this.data;
    this.modals.close(this.modalResponse);
  }
}
