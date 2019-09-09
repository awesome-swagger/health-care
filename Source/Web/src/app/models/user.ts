import { MomentInput } from 'moment';

import { IBasicUser } from './basic-user';

export interface IUser extends IBasicUser {
  birthdate?: MomentInput;
  date_joined?: MomentInput;
  gender?: string;
  image?: string;
  is_active?: boolean;
  last_login?: MomentInput;
  preferred_name?: string;
  time_zone?: string;
}

//export class User {
//	firstName: string;
//	lastName: string;
//	title: Title;
//	email: string;
//	employedBy: Employee;
//	facility: Employee[];
//	specialty: Specialty;
//	npi: string;
//};
