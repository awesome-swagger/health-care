import { MomentInput } from 'moment';

export interface ICarePlanApiPostData {
  billing_type: string;
  billing_practitioner: string;
  patient: string;
  plan_start_date: MomentInput;
  plan_template: string;
}

export interface ICareTeamMemberPostData {
  employee_profile: string;
  is_manager: boolean;
  plan: string;
  role: string;
}

export interface ICreatePatientProfilePostData {
  facility: string;
  insurance: string;
  is_active: boolean;
  is_invited: boolean;
  payer_reimbursement: boolean;
  user: string;
}

export interface ICreateUserPostData {
  email: string;
  first_name: string;
  last_name: string;
  password1: string;
  password2: string;
}

export interface IPlanConsentPostData {
  discussed_co_pay: boolean;
  plan: string;
  seen_within_year: boolean;
  verbal_consent: boolean;
  will_complete_tasks: boolean;
  will_interact_with_team: boolean;
  will_use_mobile_app: boolean;
}

export interface IPotentialPatientPostData {
  care_plan: string;
  email: string;
  facility: Array<string>;
  first_name: string;
  last_name: string;
  phone: string;
  source: string;
}
