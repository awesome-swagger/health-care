import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddUserComponent } from './modals/add-user.component';
import { AuthService, StoreService } from '../../../services';
import {
  find as _find,
} from 'lodash';

@Component({
  selector: 'app-invite',
  templateUrl: './invite.component.html',
  styleUrls: ['./invite.component.scss'],
})
export class InviteComponent implements OnDestroy, OnInit {

  public usersToInivite = [];
  public tooltipsOpen = [];
  public employees = [];

  constructor(
    private auth: AuthService,
    private store: StoreService,
    private modals: ModalService,
  ) { }

  public ngOnInit() {
    let organizationSub = this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.store.Organization.detailRoute('GET', org.id, 'employee_profiles').subscribe((employees:any) => {
        this.employees = employees.results;
      })
    })
  }

  public ngOnDestroy() { }

  public confirmDelete() {
    this.modals.open(ConfirmModalComponent, {
      closeDisabled: true,
      data: {
        title: 'Remove User?',
        body: 'Are you sure you want to remove this person from the list?',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public openAddUser() {
    this.modals.open(AddUserComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe((data) => {
      if (data) {
        data.id = this.usersToInivite.length;
        this.usersToInivite.push(data)
      }
    });
  }

  public openEditUser(user) {
    this.modals.open(AddUserComponent, {
      closeDisabled: true,
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

}
