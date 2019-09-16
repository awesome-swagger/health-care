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
