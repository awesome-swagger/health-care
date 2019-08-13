import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddUserComponent } from './modals/add-user.component';
import { AuthService, StoreService } from '../../../services';
import {
	find as _find,
} from 'lodash';
import { Router } from '@angular/router';

import { User } from '../../../models/user';

class IndexedUser extends User {
	id: string | number;
}

@Component({
	selector: 'app-invite',
	templateUrl: './invite.component.html',
	styleUrls: ['./invite.component.scss'],
})
export class InviteComponent implements OnDestroy, OnInit {

	public usersToInivite: IndexedUser[] = [];
	public tooltipsOpen = [];
	public employees = [];
	public emailBody = 'Join us on CareAdopt! CareAdopt empowers patients to adopt care after discharge and in between visits improving care coordination and engagement, decreasing costs, and providing better outcomes. Click the link below to create your profile.'

	constructor(
		private auth: AuthService,
		private store: StoreService,
		private modals: ModalService,
		private router: Router,
	) { }

	public ngOnInit() {
		let organizationSub = this.auth.organization$.subscribe(org => {
			if (!org) return;
			this.store.Organization.detailRoute('GET', org.id, 'employee_profiles').subscribe((employees: any) => {
				this.employees = employees.results;
			})
		})
	}

	public ngOnDestroy() { }

	public confirmDelete(id) {
		this.modals.open(ConfirmModalComponent, {
			data: {
				title: 'Remove User?',
				body: 'Are you sure you want to remove this person from the list?',
				cancelText: 'Cancel',
				okText: 'Continue',
			},
			width: '384px',
		}).subscribe((res) => {
			if (res === 'Continue') {
				this.usersToInivite = this.usersToInivite.filter(u => u.id !== id);
			}
		});
	}

	public openAddUser() {
		this.modals.open(AddUserComponent, {
			width: '512px',
		}).subscribe((data: IndexedUser) => {
			if (data) {
				data.id = this.usersToInivite.length;
				this.usersToInivite.push(data)
			}
		});
	}

	public openEditUser(user) {
		this.modals.open(AddUserComponent, {
			width: '512px',
			data: {
				edit: true,
				user: user,
			}
		}).subscribe((data) => {
			if (data) {
				user = Object.assign(user, data);
			}
		});
	}

	public get activeUsersCount() {
		if (this.employees && this.employees.length) {
			return this.employees.filter(e => e.status === 'active').length;
		}
		return 0;
	}

	public isAdmin(user: IndexedUser) {
		if (user.facility && user.facility.length > 0 && !user.facility.hasOwnProperty('parent_company')) {
			return true;
		} else {
			return false;
		}
	}

	public get sendDisabled() {
		return this.usersToInivite.length === 0;
	}

	public sendInvites() {
		const cancelText = 'Cancel';
		const okText = 'Continue';
		const title = 'Send Invites?';
		const body = `Do you wish to send this invite to ${this.usersToInivite.length} employee${this.usersToInivite.length > 1 ? 's' : ''}?`
		this.modals.open(ConfirmModalComponent, {
			width: '384px',
			data: { cancelText, okText, title, body },
		}).subscribe(res => {
			if (res === okText) {
				this.usersToInivite.forEach(user => {
					this.store.AddUser.createAlt({
						first_name: user.firstName,
						last_name: user.lastName,
						email: user.email,
						password1: 'password',
						password2: 'password',
					}).subscribe(res => {
						this.store.EmployeeProfile.detailRoute('POST', null, 'invite', {
							employees: [res.pk],
							email_content: this.emailBody
						}, {}).subscribe(
							res => {
								this.router.navigate(['/users']);
							},
							err => {
								this.router.navigate(['/users']);
							}
						)
					})
				})
			}
		})
	}
}
