import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddUserComponent } from './modals/add-user.component';

@Component({
  selector: 'app-invite',
  templateUrl: './invite.component.html',
  styleUrls: ['./invite.component.scss'],
})
export class InviteComponent implements OnDestroy, OnInit {

  public usersToInivite = [];
  public tooltipsOpen = [];

  constructor(
    private modals: ModalService,
  ) { }

  public ngOnInit() { }

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
    }).subscribe(() => {});
  }

  public openEditUser() {
    this.modals.open(AddUserComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

}
