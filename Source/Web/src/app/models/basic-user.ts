import { IHaveId } from './ihaveid';

export interface IBasicUser extends IHaveId {
  email?: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  source?: string;
}
