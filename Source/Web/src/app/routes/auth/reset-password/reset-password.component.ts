import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService, NavbarService, LocalStorageService, StoreService } from '../../../services';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss'],
})
export class ResetPasswordComponent implements OnDestroy, OnInit {

  constructor(
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.nav.hide();
  }

  public ngOnDestroy() { }
}
