import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';
import { AuthService, StoreService } from '../../../../../services';

@Component({
  selector: 'app-change-email',
  templateUrl: './change-email.component.html',
  styleUrls: ['./change-email.component.scss'],
})
export class ChangeEmailComponent implements OnInit {

  public data = null;

  public newEmail:string = '';
  public user = null;

  constructor(
    public modals: ModalService,
    private store: StoreService,
    private auth: AuthService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    this.auth.user$.subscribe(
      res => {
        this.user = res;
      }
    )
  }

  public submit() {
    if (this.newEmail && this.user) {
      this.store.EmployeeProfile.update(this.user.id, {
        email: this.newEmail,
      }).subscribe(
        res => {
          console.log(res);
        },
        err => {
          console.log('error', err);
        },
        () => {
          console.log('done');
        }
      )
    }
  }
}
