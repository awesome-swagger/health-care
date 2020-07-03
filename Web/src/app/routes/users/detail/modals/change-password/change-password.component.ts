import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {AppConfig} from '../../../../../app.config';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss'],
})
export class ChangePasswordComponent implements OnInit {

  public data = null;

  public oldPassword;
  public newPassword1;
  public newPassword2;

  public tooltipCPM0Open;

  constructor(
    public modals: ModalService,
    public http: HttpClient,
  ) {

  }

  public ngOnInit() {
  }

  public get submitDisabled() {
    return !(this.oldPassword && this.newPassword1 && this.newPassword2);
  }

  public save() {
    this.http.request('POST', `${AppConfig.baseUrl}/rest-auth/password/change/`, {
      body: {
        old_password: this.oldPassword,
        new_password1: this.newPassword1,
        new_password2: this.newPassword2,
      },
      headers: new HttpHeaders().set('Accept', 'application/json'),
    }).subscribe((res) => {
      this.close();
    })
  }


  public close(data = null) {
    this.modals.close(data);
  }
}
