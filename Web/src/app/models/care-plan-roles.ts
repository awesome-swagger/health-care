import { IRole } from './role';

export interface ICarePlanRoles {
  display: string;
  open: boolean;
  roleIds: Array<string>;
  roles: { [key: string]: IRole };
  selectedIds: { [key: string]: boolean };
}
