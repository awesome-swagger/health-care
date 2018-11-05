import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/do';
import { AppConfig } from '../app.config';
import { HttpService } from './http.service';
import { LocalStorageService } from './storage.service';
import { StoreService } from './store.service';

interface Token {
  token: string;
  employee_profile?: string;
  patient_profile?: string;
}

@Injectable()
export class AuthService {

  private authTokenHeader = 'Authorization';
  private user: any = null;
  private userSubject$ = new BehaviorSubject<any>(null);
  public user$ = this.userSubject$.asObservable();
  private organizationSubject$ = new BehaviorSubject<any>(null);
  public organization$ = this.organizationSubject$.asObservable();
  private facilitiesSubject$ = new BehaviorSubject<any>(null);
  public facilities$ = this.facilitiesSubject$.asObservable();

  constructor(
    private storage: LocalStorageService,
    private http: HttpService,
    private store: StoreService,
  ) {
    if (this.getAuthToken()) {
      let userSub = this.getUser().subscribe(
        () => {},
        () => {},
        () => {
          userSub.unsubscribe();
        }
      );
    }
    if (this.getOrganizationId()) {
      let organizationSub = this.getOrganization().subscribe(
        () => {},
        () => {},
        () => {
          organizationSub.unsubscribe();
        }
      );
    }
  }

  public login(username: string, password: string): Observable<any> {
    const request = this.http.post(AppConfig.authTokenUrl, { username, password });
    return request.do((token: Token) => {
      this.setAuthToken(token);
      return this.getUser().subscribe();
    });
  }

  public isLoggedIn(): boolean {
    const localUser = this.storage.getObj('user');
    const localOrg = this.storage.getObj('organization');
    return !!(this.user || localUser) && !!localOrg;
  }

  public logout(): void {
    this.user = null;
    this.storage.removeItem('user');
    this.storage.removeItem('organization');
    this.userSubject$.next(null);
    this.organizationSubject$.next(null);
  }

  public getUser(): Observable<Object> {
    return this.store.EmployeeProfile.read(this.getAuthToken().employee_profile).do((user: any) => {
      this.user = user;
      this.userSubject$.next(this.user);
    });
  }

  public getOrganization(): Observable<Object> {
    return this.store.Organization.read(this.getOrganizationId()).do((organization: any) => {
      this.organizationSubject$.next(organization);
      let facilitiesSub = this.store.Facility.readListPaged({
        organization_id: organization.id,
      }).subscribe(
        (facilities) => {
          this.facilitiesSubject$.next(facilities);
        },
        (err) => {},
        () => {
          facilitiesSub.unsubscribe();
        }
      )
    });
  }

  public switchOrganization(id) {
    this.setOrganizationId(id);
    let organizationSub = this.getOrganization().subscribe(
      () => {},
      () => {},
      () => {
        organizationSub.unsubscribe();
      }
    );
  }

  public resetPassword(email: string): Observable<Object> {
    return this.http.post(`${AppConfig.resetPasswordUrl}`, {
      email: email,
    });
  }

  private getAuthToken(): Token {
    return this.storage.getObj('user');
  }

  private setAuthToken(token: Token): void {
    this.storage.setObj('user', token);
  }

  private getOrganizationId() {
    return this.storage.getObj('organization');
  }

  private setOrganizationId(id) {
    return this.storage.setObj('organization', id);
  }
}

@Injectable()
export class CanActivateViaAuthGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router
  ) { }

  public canActivate() {
    let worthy = this.auth.isLoggedIn(); // protect the realms of AuthGuard
    if (!worthy) {
      this.router.navigate(['/login']);
    }
    return worthy;
  }
}
