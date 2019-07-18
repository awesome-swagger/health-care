import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from '../../../modules/toast';
import { AuthService, NavbarService, LocalStorageService, StoreService } from '../../../services';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnDestroy, OnInit {

  public username = '';
  public password = '';
  public error = '';

  public resetState = false;
  public selectOrgState = false;

  public user = null;
  public organizations = null;
  public selectedOrganization = null;

  constructor(
    private auth: AuthService,
    private router: Router,
    private toast: ToastService,
    private nav: NavbarService,
    private storage: LocalStorageService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.nav.hide();
    // This is triggered after the user logins in
    let userSub = this.auth.user$.subscribe((user) => {
		if(user === null)
			return;

      if (user.results) {
		  this.toast.error('Invalid username or password. Please try again.');
        return;
      }
      this.user = user;
      let orgSub = this.store.Organization.readListPaged().subscribe(
        (organizations) => {
          if (organizations.length === 1) {
            this.selectedOrganization = organizations[0];
            this.selectOrganization();
          }
          this.selectOrgState = true;
          this.organizations = organizations;
        },
        (err) => { console.log(err) },
        () => {
          orgSub.unsubscribe();
        }
      );
    });
  }

  public ngOnDestroy() {

  }

  public login() {
    let authSub = this.auth.login(this.username, this.password)
      .subscribe(
        (res) => { },
        (err) => {
			if(err.status === 401)
				this.toast.error('Invalid username or password. Please try again.');
			else
				this.toast.error('An error occurred.');
        },
        () => {
          this.username = '';
          this.password = '';
          authSub.unsubscribe();
        }
      );
  }

  public selectOrganization() {
    this.auth.setOrganizationId(this.selectedOrganization.id);
    this.router.navigate(['/']);
  }

  public resetPassword() {
    let resetSub = this.auth.resetPassword(this.username)
      .subscribe(
        (res) => {
          this.router.navigate(['/']);
        },
        (err) => {
          this.toast.error('An error occurred.');
        },
        () => {
          resetSub.unsubscribe();
        }
      );
  }

  public switchUser() {
    this.selectOrgState = false;
    this.auth.logout();
  }
}
