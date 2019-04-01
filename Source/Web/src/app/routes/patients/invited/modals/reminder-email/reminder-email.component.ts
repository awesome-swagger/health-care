import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';
import { AuthService } from '../../../../../services';

@Component({
  selector: 'app-reminder-email',
  templateUrl: './reminder-email.component.html',
  styleUrls: ['./reminder-email.component.scss'],
})
export class ReminderEmailComponent implements OnInit {

  public data = null;

  public patient = null;
  public subjectInput = 'CareAdopt Email Reminder';
  public messageInput = '';

  constructor(
    private modal: ModalService,
    private auth: AuthService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.patient = this.data.patient;
      this.auth.user$.subscribe(user => {
        if (!user) return;
        this.messageInput = `Hi ${this.patient.full_name},
        
This is a reminder about your custom care plan from ${this.data.facility.name} click the link below to create your account.
        
www.careadopt.com/app_download
        
Thanks,
${user.user.first_name} ${user.user.last_name}`
      })
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
