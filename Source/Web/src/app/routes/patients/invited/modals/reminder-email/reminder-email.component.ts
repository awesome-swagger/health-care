import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';

@Component({
  selector: 'app-reminder-email',
  templateUrl: './reminder-email.component.html',
  styleUrls: ['./reminder-email.component.scss'],
})
export class ReminderEmailComponent implements OnInit {

  public data = null;

  public patient = null;
  public subjectInput = '';
  public messageInput = '';

  constructor(
    private modal: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.patient = this.data.patient;
    }
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public sendDisabled() {
    return (!this.patient || !this.subjectInput || !this.messageInput);
  }

  public clickSend() {
    if (!this.patient || !this.subjectInput || !this.messageInput) {
      return;
    }
    this.modal.close({
      patient: this.patient,
      subject: this.subjectInput,
      message: this.messageInput,
    })
  }
}
