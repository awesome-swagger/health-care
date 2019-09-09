import { Component, OnInit } from "@angular/core";
//import * as moment from 'moment';

import { ModalService } from "../../../modules/modals";

import { INewPatientDetails } from "../../../models/inew-patient-details";
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from "../../../models/ipatient-enrollment-modal-response";

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
  public startDate: string;

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public ngOnInit(): void {
    this.modalResponse.newPatientDetails = this.data;
  }

  public close(): void {
    this.modals.close(this.modalResponse);
  }
}
