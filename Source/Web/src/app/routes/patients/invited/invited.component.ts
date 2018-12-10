import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { ReminderEmailComponent } from './modals/reminder-email/reminder-email.component';

@Component({
  selector: 'app-invited',
  templateUrl: './invited.component.html',
  styleUrls: ['./invited.component.scss'],
})
export class InvitedPatientsComponent implements OnDestroy, OnInit {

  public toolIP1Open;
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;

  constructor(
    private modals: ModalService,
  ) { }

  public ngOnInit() { }

  public ngOnDestroy() { }

  public reminderEmail() {
    this.modals.open(ReminderEmailComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmRemovePatient() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove Patient?',
       body: 'Are you sure you want to revoke this patient’s invitation? This cannot be undone.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }
}
