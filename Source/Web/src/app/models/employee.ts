import { MomentInput } from "moment";

import { IFacility } from "./facility";
import { IHaveId } from "./ihaveid";
import { IOrganization } from "./organization";
import { IRole } from "./role";
import { ISpecialty } from "./specialty";
import { ITitle } from "./title";
import { IUser } from "./user";

export interface IEmployee extends IHaveId {
  billing_view?: boolean;
  created?: MomentInput;
  facilities?: Array<IFacility>;
  facilities_managed?: Array<IFacility>;
  modified?: MomentInput;
  npi_code?: string;
  organizations?: Array<IOrganization>;
  organizations_managed?: Array<IOrganization>;
  qualified_practitioner?: boolean;
  roles?: Array<IRole>;
  specialty?: ISpecialty;
  status?: string;
  title?: ITitle;
  user?: IUser;
}

//export class Employee {
//  active_users: number;
//  addr_city: string | null;
//  addr_state: string | null;
//  addr_street: string | null;
//  addr_suite: string | null;
//  addr_zip: string | null;
//  created: string | Date;
//  id: string;
//  is_affiliate: boolean;
//  is_manager: boolean;
//  modified: string | Date;
//  name: string;
//  organization: Organization;
//  parent_company: null;
//}
