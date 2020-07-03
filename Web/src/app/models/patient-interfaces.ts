import { MomentInput } from 'moment';

import { IBillingType } from './billing_type';
import { ICarePlan } from './care-plan';
import { IHaveId } from './ihave-id';
import { ISimpleFacility } from './facility';
import { ISpecialty } from './specialty';
import { ITitle } from './title';
import { IUser } from './user';
import { IEmployee } from './employee';
import { IRole } from './role';

/*
 * TODO: Once the Patient.component is refactored move these to their own files
 */


export interface IPatientCarePlan extends IHaveId {
  billing_practitioner    ?: IBillingPractitioner;
  billing_type            ?: IBillingType;
  care_manager            ?: ICareTeamMember;
  created                 ?: MomentInput;
  is_billed               ?: boolean;
  modified                ?: MomentInput;
  overview                ?: IOverview;
  patient                 ?: ISimplePatientDetails;
  plan_template           ?: ICarePlan;
  team_members            ?: Array<any>;
}

export interface ISimplePatientDetails extends IHaveId {
  facility                ?: ISimpleFacility;
  facility_name           ?: string;
  first_name              ?: string;
  image_url               ?: string;
  last_name               ?: string;
}

export interface IBillingPractitioner extends IHaveId {
  qualified_practitioner  ?: boolean;
  specialty               ?: ISpecialty;
  status                  ?: string;
  title                   ?: ITitle;
  user                    ?: IUser;
}

export interface IOverview extends IHaveId {
  billing_type            ?: IBillingType;
  care_team               ?: Array<ICareTeamMember>;
  last_contact            ?: MomentInput;
  next_check_in           ?: MomentInput;
  patient                 ?: ISimplePatientDetails;
  plan_template           ?: ICarePlan;
  problem_areas_count     ?: number;
  risk_level              ?: number;
  time_spent_this_month   ?: MomentInput;
}

export interface ICareTeamMember {
  employee_profile        ?: IEmployee;
  is_manager              ?: boolean;
  next_checkin            ?: MomentInput;
  plan                    ?: string;
  role                    ?: IRole;
}
