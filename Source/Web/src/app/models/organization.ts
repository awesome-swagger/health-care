export class Organization {
	addr_city: string | null;
	addr_state: string | null;
	addr_street: string | null;
	addr_suite: string | null;
	addr_zip: string | null;
	available_users: number;
	created: string | Date;
	id: string;
	is_manager: boolean;
	modified: string | Date;
	name: string;
	renewal_date: string | Date;
}