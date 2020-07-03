import { Component, OnInit } from '@angular/core';
import { ModalService, ModalsModule } from '../../../../../modules/modals';
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
    private modals: ModalService,
    private store: StoreService,
    private auth: AuthService,
  ) {

  }

  public ngOnInit() {
    this.auth.user$.subscribe(
      res => {
        this.user = res;
      }
    )
  }

  close() {
    this.modals.close(null);
  }

  public get submitDisabled() {
    return !this.newEmail;
  }

  public submit() {
    if (this.newEmail && this.user) {
      this.store.User.detailRoute('PATCH', this.user.user.id, 'change_email', {
        email: this.newEmail,
      }).subscribe(
        res => {
          this.modals.close(true);
        },
        err => {
        },
        () => {
        }
      )
    }
  }
}
