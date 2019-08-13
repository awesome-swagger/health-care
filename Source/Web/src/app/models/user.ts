import { Title } from './title';
import { Specialty } from './specialty';
import { Organization } from './organization';

export class User {
	firstName: string;
	lastName: string;
	title: Title;
	email: string;
	employedBy: Employee;
	facility: Employee[];
	specialty: Specialty;
	npi: string;
};

export class Employee {
	active_users: number;
	addr_city: string | null;
	addr_state: string | null;
	addr_street: string | null;
	addr_suite: string | null;
	addr_zip: string | null;
	created: string | Date;
	id: string;
	is_affiliate: boolean;
	is_manager: boolean;
	modified: string | Date;
	name: string;
	organization: Organization;
	parent_company: null;
}