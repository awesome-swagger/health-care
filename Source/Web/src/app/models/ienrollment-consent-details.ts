import { Moment } from "moment";

export interface IEnrollmentConsentDetails {
  discussed_co_pay?: boolean;
  planStartDate?: Moment;
  seen_within_year?: boolean;
  verbal_consent?: boolean;
  will_complete_tasks?: boolean;
  will_interact_with_team?: boolean;
  will_use_mobile_app?: boolean;
}
