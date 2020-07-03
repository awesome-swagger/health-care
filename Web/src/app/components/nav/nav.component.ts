import * as moment from 'moment';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { filter as _filter, map as _map, sum as _sum } from 'lodash';
import { Router } from '@angular/router';
import { Subject } from 'rxjs/Subject';
import { Subscription } from 'rxjs/Subscription';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';

import { AuthService, NavbarService, StoreService } from '../../services';
import { ModalService } from '../../modules/modals';
import { PatientCreationModalService } from '../../services/patient-creation-modal.service';
import { PopoverOptions } from '../../modules/popover';
import { Utils } from '../../utils';

import { IApiResultsContainer } from '../../models/api-results-container';
import { IEmployee } from '../../models/employee';
import { INotification } from '../../models/notification';
import { IOrganization } from '../../models/organization';
import { IPatientsOverview } from '../../models/patient-overview';
import { ITask } from '../../models/task';
import { ITaskData } from '../../models/task-data';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnDestroy, OnInit {
  private readonly patientRoutes = /((in)?active|invited|potential)/;
  private authSub: Subscription = null;
  private orgSub: Subscription = null;
  private searchSub: Subscription = null;

  public activePatientsCount = 0;
  public analyticsOpen = false;
  public appListOpen = false;
  public appListOptions: PopoverOptions = { relativeBottom: '0', relativeLeft: '1.5rem', };
  public employee: IEmployee = null;
  public inactivePatientsCount = 0;
  public invitedPatientsCount = 0;
  public logoutDropOptions: PopoverOptions = { relativeRight: '16rem', };
  public logoutOpen = false;
  public moment = moment;
  public normalState = true;
  public notifications: Array<{ category: 'Assignments' | 'Flagged Patients' | 'Unread Messages', notifications: Array<INotification> }>;
  public notificationsCount: number = 0;
  public notificationsDropOpen = false;
  public notificationsDropOptions: PopoverOptions = { relativeRight: '30rem', };
  public organization: IOrganization = null;
  public organizations: Array<{ id: string, name: string }> = [];
  public patientDetailState = false;
  public patients: IPatientsOverview = {};
  public patientsDropOpen = false;
  public patientsDropOptions: PopoverOptions = { relativeBottom: '0', relativeLeft: '0', };
  public planDetailState = false;
  public potentialPatientsCount = 0;
  public searchOpen = false;
  public searchResults: Array<ISearchResult> = [];
  public searchString = '';
  public searchUpdated$: Subject<string> = new Subject<string>();
  public selectableOrganizations: Array<{ id: string, name: string }> = [];
  public taskDropOpen = false;
  public taskDropOptions: PopoverOptions = { relativeRight: '16rem', };
  public taskData: ITaskData = null;
  public taskCount: number;

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private patientCreationModalService: PatientCreationModalService,
    private router: Router,
    private store: StoreService,
    public nav: NavbarService,
  ) {
    // Nothing yet
  }

  public ngOnInit(): void {
    this.authSub = this.auth.user$.subscribe((employee: IEmployee) => {
      if (Utils.isNullOrWhitespace(((employee || {}).user || {}).id)) {
        return;
      }

      this.employee = employee;
      const userId = this.employee.user.id;
      Utils.convertObservableToPromise(this.store.User.detailRoute('GET', userId, 'tasks'))
        .then((taskData: ITaskData) => {
          const setCollectionData = (collection: Array<ITask>) => {
            if (Utils.isNullOrEmptyCollection(collection)) {
              return;
            }

            return collection.map(x => ({
              ...x,
              time: moment(x.due_datetime, ['YYYY-MM-DDTHH:mm:ss.SSSZZ']).format('h:mm a'),
              patientName: `${x.patient.first_name || ''} ${x.patient.last_name || ''}`.trim()
            }));
          };

          this.taskData = taskData || {};
          this.taskData.checkIns = setCollectionData(taskData.checkIns);
          this.taskData.tasks = setCollectionData(taskData.tasks);
          this.taskCount = (this.taskData.checkIns || []).length + (this.taskData.tasks || []).length;
        });

      Utils.convertObservableToPromise(this.store.User.detailRoute('GET', userId, 'notifications'))
        .then((response: IApiResultsContainer<Array<INotification>>) => {
          const notifications = response.results || [];
          const getCollection = (category: 'unread_message' | 'flagged_patient' | 'assignment') => {
            const collection = notifications.filter(x => x.category === category)
            if (Utils.isNullOrEmptyCollection(collection)) {
              return null;
            }

            return collection;
          };

          this.notificationsCount = notifications.length;
          this.notifications = [
            { category: 'Unread Messages', notifications: getCollection('unread_message') },
            { category: 'Flagged Patients', notifications: getCollection('flagged_patient') },
            { category: 'Assignments', notifications: getCollection('assignment') }
          ];
        });
    });

    this.orgSub = this.auth.organization$.subscribe((organization: IOrganization) => {
      if (Utils.isNullOrUndefined(organization)) {
        return;
      }

      this.organization = organization;
      this.refreshPatientOverview(this.organization.id);
      Utils.convertObservableToPromise(this.store.Organization.readListPaged())
        .then((res: Array<{ id: string, name: string }>) => {
          this.organizations = res;
          this.selectableOrganizations = this.organizations.filter((obj) => obj.id !== this.organization.id);
        });
    });

    this.searchSub = this
      .searchUpdated$
      .asObservable()
      .debounceTime(400)
      .distinctUntilChanged()
      .subscribe((searchStr) => {
        if (searchStr.length < 3) {
          this.searchResults = [];
          this.searchOpen = false;

          return;
        }

        Utils.convertObservableToPromise(this.store.PatientProfile.listRoute('get', 'search', {}, { q: searchStr }))
          .then((searchResults: IApiResultsContainer<Array<ISearchResult>>) => {
            this.searchResults = searchResults.results || [];
            this.searchOpen = this.searchResults.length > 0;
          });
      });


    document.addEventListener('refreshPatientOverview', () => this.refreshPatientOverview(this.organization.id));
  }

  public ngOnDestroy(): void {
    const unsub = (sub: Subscription) => (sub || { unsubscribe: () => null }).unsubscribe();

    unsub(this.authSub);
    unsub(this.orgSub);
    unsub(this.searchSub);
  }

  public isPatientsRoute(): boolean {
    return this.router.url.match(this.patientRoutes) !== null;
  }

  public logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  public switchOrganization(organization: IOrganization): void {
    this.auth.switchOrganization(organization.id);
    this.router.navigate(['/dashboard']);
  }

  public closeAllPopovers(): void {
    this.appListOpen = false;
    this.searchOpen = false;
    this.taskDropOpen = false;
    this.notificationsDropOpen = false;
    this.logoutOpen = false;
    this.patientsDropOpen = false;
  }

  public searchChange(value: string): void {
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

  public routeToPatientPage(route): void {
    this.router.navigate(['/patient', this.nav.patientDetailId, route, this.nav.patientPlanId]);
  }

  public refreshPatientOverview(organizationId: string): void {
    const data = { 'facility__organization__id': organizationId };
    Utils.convertObservableToPromise(this.store.PatientProfile.listRoute('GET', 'overview', {}, data))
      .then((patients: IPatientsOverview) => {
        this.patients = patients || {};
        this.activePatientsCount = this.patients.active || 0;
        this.inactivePatientsCount = this.patients.inactive || 0;
        this.potentialPatientsCount = this.patients.potential || 0;
        this.invitedPatientsCount = this.patients.invited || 0;
      });
  }

  public routeToAnalytics() {
    window.open('https://www.google.com', '_self');
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

interface ISearchResult {
  id: string;
  user: {
    first_name: string;
    image_url: string;
    last_name: string;
  };
}
