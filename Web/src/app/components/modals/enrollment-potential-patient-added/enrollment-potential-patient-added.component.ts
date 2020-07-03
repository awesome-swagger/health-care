import { Component, OnInit } from '@angular/core';

import { ModalService } from '../../../modules/modals';

import { INewPatientDetails } from '../../../models/new-patient-details';
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from '../../../models/patient-enrollment-modal-response';

@Component({
  selector: 'app-enrollment-potential-patient-added',
  templateUrl: './enrollment-potential-patient-added.component.html',
  styleUrls: ['./enrollment-potential-patient-added.component.scss'],
})
export class EnrollmentPotentialPatientAddedComponent implements OnInit {
  public carePlanName: string;
  public data: INewPatientDetails = null;
  public facilityName: string;
  public firstName: string;
  public lastName: string;
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Complete, step: PatientCreationStep.PotentialPatientAdded };
  public serviceAreaName: string;

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public ngOnInit(): void {
    this.modalResponse.newPatientDetails = this.data;
    this.carePlanName    = this.data.carePlan.name;
    this.facilityName    = this.data.facility.name;
    this.firstName       = this.data.firstName;
    this.lastName        = this.data.lastName;
    this.serviceAreaName = this.data.serviceArea.name;
  }

  public close(): void {
    this.modals.close(this.modalResponse);
  }
}
