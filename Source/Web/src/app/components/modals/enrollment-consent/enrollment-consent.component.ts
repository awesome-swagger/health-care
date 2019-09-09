import { Component, OnInit } from "@angular/core";
import { Moment } from "moment";

import { ModalService } from "../../../modules/modals";
import { Utils } from "../../../utils";

import { INewPatientDetails } from "../../../models/inew-patient-details";
import { IPatientEnrollmentModalResponse, PatientCreationAction, PatientCreationStep } from "../../../models/ipatient-enrollment-modal-response";

@Component({
  selector: 'app-enrollment-consent',
  templateUrl: './enrollment-consent.component.html',
  styleUrls: ['./enrollment-consent.component.scss'],
})
export class EnrollmentConsentComponent implements OnInit {
  public carePlan: string;
  public carePlanTypeAbr: string;
  public carePlanTypeName: string;
  public completeDailyTasks: boolean;
  public copayPotential: boolean;
  /** Input parameter from modal.data */
  public data: INewPatientDetails;
  public displayDate: string;
  public interactWithTeam: boolean;
  public isRpmPlan: boolean;
  public isValid: boolean = false;
  public modalResponse: IPatientEnrollmentModalResponse = { action: PatientCreationAction.Cancel, step: PatientCreationStep.PatientConsent };
  public name: string;
  public phone: string;
  public planStartDate: Moment;
  public seenInLastYear: boolean;
  public serviceArea: string;
  public showDate: boolean;
  public useMobilApp: boolean;
  public verbalConsent: boolean;

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public ngOnInit(): void {
    this.data.enrollmentConsentDetails = this.data.enrollmentConsentDetails || {};
    this.copayPotential = this.data.enrollmentConsentDetails.discussed_co_pay;
    this.planStartDate = this.data.enrollmentConsentDetails.planStartDate;
    this.seenInLastYear = this.data.enrollmentConsentDetails.seen_within_year;
    this.verbalConsent = this.data.enrollmentConsentDetails.verbal_consent;
    this.completeDailyTasks = this.data.enrollmentConsentDetails.will_complete_tasks;
    this.interactWithTeam = this.data.enrollmentConsentDetails.will_interact_with_team;
    this.useMobilApp = this.data.enrollmentConsentDetails.will_use_mobile_app;

    this.displayDate = 'Select Date';
    this.name = `${this.data.firstName} ${this.data.lastName}`;
    this.serviceArea = this.data.serviceArea.name;
    this.carePlan = this.data.carePlan.name;
    if (!Utils.isNullOrUndefined(this.data.planType)) {
      this.carePlanTypeAbr = this.data.planType.acronym;
      this.carePlanTypeName = this.data.planType.name;
    }

    const phone = this.data.phoneNumber;
    if (!Utils.isNullOrWhitespace(phone) && phone.trim() !== '-') {
      this.phone = ` - ${phone}`;
    }
  }

  public close(action?: PatientCreationAction): void {
    if (!Utils.isNullOrUndefined(action)) {
      this.modalResponse.newPatientDetails = this.data;
      this.modalResponse.action = action;
    }

    this.modals.close(this.modalResponse);
  }

  public dateChanged(selectedDate: Moment): void {
    this.planStartDate = selectedDate;
    this.displayDate = (this.isValid = Utils.isNullOrUndefined(selectedDate))
      ? 'Select Date'
      : selectedDate.format('MMM D, YYYY');
  }

  public enroll(): void {
    this.data.enrollmentConsentDetails.discussed_co_pay = this.copayPotential;
    this.data.enrollmentConsentDetails.planStartDate = this.planStartDate;
    this.data.enrollmentConsentDetails.seen_within_year = this.seenInLastYear;
    this.data.enrollmentConsentDetails.verbal_consent = this.verbalConsent;
    this.data.enrollmentConsentDetails.will_complete_tasks = this.completeDailyTasks;
    this.data.enrollmentConsentDetails.will_interact_with_team = this.interactWithTeam;
    this.data.enrollmentConsentDetails.will_use_mobile_app = this.useMobilApp;

    this.close(PatientCreationAction.Complete);
  }

  public later(): void {
    this.close(PatientCreationAction.Later);
  }
}
