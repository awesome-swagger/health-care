import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService, NavbarService, LocalStorageService, StoreService } from '../../../services';

@Component({
  selector: 'app-verify-email',
  templateUrl: './verify-email.component.html',
  styleUrls: ['./verify-email.component.scss'],
})
export class VerifyEmailComponent implements OnDestroy, OnInit {

  constructor(
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.nav.hide();
  }

  public ngOnDestroy() { }
}
