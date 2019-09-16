import { MomentInput } from "moment";

import { IBillingType } from "./ibilling_type";
import { IFacility } from "./facility";
import { IHaveId } from "./ihaveid";
import { IOrganization } from "./organization";
import { IPatient } from "./patient";
import { IRole } from "./role";
import { IServiceArea } from "./service-area";
import { IUser } from "./user";
import { ITitle } from "./title";
import { ISpecialty } from "./specialty";

/**
 * NOTE: This file exists only until the active patient page is re-factored then the actual types should be moved to separate files.
 * */

export interface IPillColorPlan {
  billing_type: {
    acronym: string,
    billable_minutes: number
  },
  created: string,
  patient: {
    payer_reimbursement: any
  },
  time_count: number
}

export interface IFacilityWithCarePlans extends IFacility {
  carePlans?: Array<IActivePatientCarePlans>;
  patients?: Array<IPatient>;
}

export interface IOtherCarePlans extends IHaveId {
  plan_template?: IPlanTemplate;
}

export interface IPlanTemplate extends IHaveId {
  created?: MomentInput;
  duration_weeks?: number;
  is_active?: boolean;
  modified?: MomentInput;
  name?: string;
  service_area?: IServiceArea;
}

export interface IActivePatient extends IHaveId {
  full_name?: string;
  image_url?: string;
  last_app_use?: MomentInput;
  payer_reimbursement?: boolean;
}

export interface IActivePatientCarePlans extends IHaveId {
  average_engagement?: number;
  average_outcome?: number;
  billing_type?: IBillingType;
  care_team_employee_ids?: Array<string>;
  created?: MomentInput;
  last_contact?: MomentInput;
  other_plans?: Array<IOtherCarePlans>;
  patient?: IActivePatient;
  plan_template?: IPlanTemplate;
  risk_level?: number;
  tasks_this_week?: number;
  time_count?: number;
}

export interface ICarePlanAverage {
  average_engagement?: number;
  average_outcome?: number;
  risk_level?: number;
  total_care_plans?: number;
  total_facilities?: number;
  total_patients?: number;
}

export interface IPatientProfile extends IHaveId {
  billing_view?: boolean;
  created?: MomentInput;
  facilities?: Array<IFacility>;
  facilities_managed?: Array<IFacility>;
  modified?: MomentInput;
  npi_code?: string;
  organizations?: Array<IOrganization>;
  organizations_managed?: Array<IOrganization>,
  qualified_practitioner?: boolean;
  roles?: Array<IRole>;
  specialty?: ISpecialty;
  status?: string
  title?: ITitle;
  user?: IUser;
}

//export interface ITitle extends IHaveId {
//  abbreviation?: string;
//  name?: string;
//}

//export interface ISpecialty extends IHaveId {
//  name?: string;
//  physician_specialty?: boolean;
//}
