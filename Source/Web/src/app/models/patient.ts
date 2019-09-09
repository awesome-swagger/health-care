import { MomentInput } from "moment";

import { IFacility } from "./facility";
import { IHaveId } from "./ihaveid";
import { IMessage } from "./message";
import { IUser } from "./user";

export interface IPatient extends IHaveId {
  addr_city?: string;
  addr_state?: string;
  addr_street?: string;
  addr_suite?: number;
  addr_zip?: string;
  cognitive_ability?: string;
  communication_email?: string;
  communication_preference?: string;
  created?: MomentInput;
  diagnosis?: Array<string>;
  emr_code?: number;
  ethnicity?: string;
  facility?: IFacility,
  height_feet?: number;
  height_inches?: number;
  insurance?: string;
  is_active?: boolean;
  is_archived?: boolean;
  is_invited?: boolean;
  is_using_mobile?: boolean;
  last_app_use?: MomentInput;
  message_for_day?: IMessage;
  modified?: MomentInput;
  mrn?: string | number;
  payer_reimbursement?: boolean;
  risk_level?: number;
  secondary_insurance?: string;
  source?: string;
  telemedicine?: string;
  user?: IUser;
}
