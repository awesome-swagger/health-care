import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService, NavbarService, LocalStorageService, StoreService } from '../../../services';

@Component({
  selector: 'app-create-account',
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.scss'],
})
export class CreateAccountComponent implements OnDestroy, OnInit {

  constructor(
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.nav.hide();
  }

  public ngOnDestroy() { }
}
