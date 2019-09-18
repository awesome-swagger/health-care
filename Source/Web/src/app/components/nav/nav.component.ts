import * as moment from 'moment';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { filter as _filter, map as _map, sum as _sum } from 'lodash';
import { Router } from '@angular/router';
import { Subject } from 'rxjs/Subject';
import { Subscription } from 'rxjs/Subscription';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';

import { AuthService, NavbarService, StoreService } from '../../services';
import { ConfirmModalComponent, ModalService } from '../../modules/modals';
import { PatientCreationModalService } from '../../services/patient-creation-modal.service';
import { PopoverOptions } from '../../modules/popover';

import { INotification } from '../../models/notification';
import { IPatientsOverview } from '../../models/patient-overview';
import { ITaskData } from '../../models/task-data';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnDestroy, OnInit {
  private readonly patientRoutes = /((in)?active|invited|potential)/;
  private authSub: Subscription = null;
  private organizationSub: Subscription = null;
  private routeParams = null;
  public activePatientsCount = 0;
  public analyticsOpen = false;
  public appListOpen = false;
  public appListOptions: PopoverOptions = { relativeBottom: '0', relativeLeft: '1.5rem', };
  public employee: { billing_view: {}, id: string, user: { id: string, image_url: string } } = null;
  public inactivePatientsCount = 0;
  public invitedPatientsCount = 0;
  public logoutDropOptions: PopoverOptions = { relativeRight: '16rem', };
  public logoutOpen = false;
  public moment = moment;
  public normalState = true;
  public notifications: Array<INotification> = [];
  public notificationsDropOpen = false;
  public notificationsDropOptions: PopoverOptions = { relativeRight: '30rem', };
  public organization: { id: string, is_manager: boolean } = null;
  public organizations: Array<{ id: string, name: string }> = [];
  public patientDetailState = false;
  public patients: IPatientsOverview = {};
  public patientsDropOpen = false;
  public patientsDropOptions: PopoverOptions = { relativeBottom: '0', relativeLeft: '0', };
  public planDetailState = false;
  public potentialPatientsCount = 0;
  public searchOpen = false;
  public searchResults = [];
  public searchString = '';
  public searchUpdated$: Subject<string> = new Subject<string>();
  public selectableOrganizations: Array<{ id: string, name: string }> = [];
  public taskDropOpen = false;
  public taskDropOptions: PopoverOptions = { relativeRight: '16rem', };
  public tasks = [];
  public tasksData: ITaskData = null;

  constructor(
    private router: Router,
    private auth: AuthService,
    public nav: NavbarService,
    private store: StoreService,
    private modals: ModalService,
    private patientCreationModalService: PatientCreationModalService
  ) {
    // Nothing yet
  }

  public ngOnInit() {
    this.authSub = this.auth.user$.subscribe(
      (res) => {
        if (!res || !res.user || !res.user.id) {
          return;
        }

        this.employee = res;
        this.getTasks(this.employee.user.id).then((tasks: any) => {
          this.tasks = tasks;
          this.tasksData = tasks;
        });
      },
      () => { },
      () => { }
    );

    this.organizationSub = this.auth.organization$.subscribe(
      (res) => {
        if (res === null) {
          return;
        }

        this.organization = res;
        this.getPatientsOverview(this.organization.id).then(e => this.refreshPatientOverview(e));

        this.store.Organization.readListPaged()
          .subscribe(
            (res: Array<{ id: string, name: string }>) => {
              this.organizations = res;
              this.selectableOrganizations = this.organizations.filter((obj) => obj.id !== this.organization.id);
            },
            () => { },
            () => { },
          );
      },
      () => { },
      () => { }
    );

    this.searchUpdated$
      .asObservable()
      .debounceTime(400)
      .distinctUntilChanged()
      .subscribe((searchStr) => {
        if (searchStr.length < 3) {
          this.searchResults = [];
          this.searchOpen = false;
          return;
        }

        const searchSub = this.store.PatientProfile.listRoute('get', 'search', {}, { q: searchStr }).subscribe(
          (searchResults: any) => {
            this.searchResults = searchResults.results;
            if (this.searchResults.length > 0) {
              this.searchOpen = true;
            }
          },
          () => { },
          () => searchSub.unsubscribe()
        );
      });

    this.getNotifications().then((notifications: { results: Array<INotification> }) => {
      this.notifications = notifications.results || [];
    });

    document.addEventListener('refreshPatientOverview', e => {
      this.getPatientsOverview(this.organization.id).then(e => this.refreshPatientOverview(e));
    });
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }

    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public isPatientsRoute(): boolean {
    return this.router.url.match(this.patientRoutes) !== null;
  }

  private refreshPatientOverview(patientOverview: IPatientsOverview) {
    this.patients = patientOverview || {};
    this.activePatientsCount = this.patients.active;
    this.inactivePatientsCount = this.patients.inactive;
    this.potentialPatientsCount = this.patients.potential;
    this.invitedPatientsCount = this.patients.invited;
  }

  public logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  public switchOrganization(organization) {
    this.auth.switchOrganization(organization.id);
    this.router.navigate(['/dashboard']);
  }

  public confirmUnarchive() {
    this.modals.open(ConfirmModalComponent, {
      backdrop: true,
      closeDisabled: true,
      width: '384px',
      height: 'auto',
      data: {
        'title': 'Unarchive Patient?',
        'body': 'This patient has been archived. Viewing this patient will unarchive them and change their status to inactive.',
        'okText': 'Continue',
        'cancelText': 'Cancel',
      }
    }).subscribe();
  }

  public closeAllPopovers() {
    this.appListOpen = false;
    this.searchOpen = false;
    this.taskDropOpen = false;
    this.notificationsDropOpen = false;
    this.logoutOpen = false;
    this.patientsDropOpen = false;
  }

  public searchChange(value: string) {
    this.searchUpdated$.next(value);
  }

  public routeToProfile() {
    this.router.navigate(['/user', this.employee.id]);
  }

  public routeToPatients() {
    this.router.navigate(['/patients/active']);
  }

  public routeToPatient(id: string) {
    this.searchString = '';
    this.router.navigate(['/patient', id]);
  }

  public routeToPatientPage(route) {
    this.router.navigate(['/patient', this.nav.patientDetailId, route, this.nav.patientPlanId]);
  }

  public getPatientsOverview(organizationId) {
    const promise = new Promise((resolve, reject) => {
      const data = {
        'facility__organization__id': organizationId,
      };
      const patientsSub = this.store.PatientProfile.listRoute('GET', 'overview', {}, data).subscribe(
        patients => resolve(patients),
        err => reject(err),
        () => patientsSub.unsubscribe()
      );
    });

    return promise;
  }

  private getNotifications() {
    return new Promise((resolve, reject) => {
      this.auth.user$.subscribe(response => {
        if (!response) {
          return;
        }

        const user = (Array.isArray(response.results) && response.results.length > 0)
          ? response.results[0]
          : response.user;

        if (!user || !user.id) {
          return;
        }

        this.store.User.detailRoute('GET', user.id, 'notifications').subscribe(notifications => resolve(notifications));
      });
    });
  }

  public get notificationData(): Array<{ category: string, notifications: Array<INotification> }> {
    if (this.notifications.length) {
      return [
        {
          category: 'Unread Messages',
          notifications: _filter(this.notifications, n => n.category === 'unread_message'),
        }, {
          category: 'Flagged Patients',
          notifications: _filter(this.notifications, n => n.category === 'flagged_patient'),
        }, {
          category: 'Assignments',
          notifications: _filter(this.notifications, n => n.category === 'assignment'),
        }
      ];
    }

    return null;
  }

  private getTasks(userId) {
    return new Promise((resolve, reject) => {
      const tasksSub = this.store.User.detailRoute('GET', userId, 'tasks').subscribe(
        tasks => resolve(tasks),
        err => reject(err),
        () => tasksSub.unsubscribe()
      );
    });
  }

  public routeToAnalytics() {
    window.open('https://www.google.com', '_self');
  }

  public get taskCount() {
    return this.tasksData.length;
  }

  public timeSince(d: moment.MomentInput): string {
    const date = moment(d);
    const daysSince = moment().diff(date, 'days');
    const hoursSince = moment().diff(date, 'hours');
    const minutesSince = moment().diff(date, 'minutes');

    if (!daysSince) {
      if (!hoursSince) {
        return `${minutesSince} minute${minutesSince !== 1 ? 's' : ''} ago`;
      }

      return `${hoursSince} hour${hoursSince !== 1 ? 's' : ''} ago`;
    }

    return `${daysSince} day${daysSince !== 1 ? 's' : ''} ago`;
  }

  public openEnrollPatient() {
    this.patientCreationModalService.openEnrollment_PotentialPatientDetails({ action: 'add' });
  }
}
