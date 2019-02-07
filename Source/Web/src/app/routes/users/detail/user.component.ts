import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AuthService, StoreService } from '../../../services';
import { ReassignPatientsComponent } from '../../../components';
import { ChangeEmailComponent } from './modals/change-email/change-email.component';
import { ChangePasswordComponent } from './modals/change-password/change-password.component';
import { EditUserDetailsComponent } from './modals/edit-user-details/edit-user-details.component';
import {
  filter as _filter,
  find as _find,
  map as _map
} from 'lodash';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
})
export class UserComponent implements OnDestroy, OnInit {

  public employee: any = null;
  private paramsSub: Subscription = null;
  public organization: any = null;
  public roles = [];

  public tooltip1Open;
  public tooltip2Open;
  public isProvider;
  public tooltip3Open;
  public isBC;
  public tooltip4Open;
  public editName;
  public accord1Open;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private auth: AuthService,
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.paramsSub = this.route.params.subscribe((res) => {
      if (!res.id) {
        this.router.navigate(['/error']);
        return;
      }
      let employeeSub = this.store.EmployeeProfile.read(res.id).subscribe(
        (employee) => {
          console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
          console.log(employee);
          console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
          this.employee = employee;
        },
        (err) => {
          this.router.navigate(['/error']);
        },
        () => {
          employeeSub.unsubscribe();
        },
      );
    });

    const organizationSub = this.auth.organization$.subscribe(
      (res) => {
        if (res === null) {
          return;
        }
        this.organization = res;
      },
      (err) => {},
      () => { organizationSub.unsubscribe() }
    );

    const rolesSub = this.store.ProviderRole.readListPaged().subscribe(
      roles => {
        this.roles = roles;
      },
      err => {},
      () => rolesSub.unsubscribe()
    )

  }

  public ngOnDestroy() {
    if (this.paramsSub) {
      this.paramsSub.unsubscribe();
    }
  }

  public openReassignPatients() {
    this.modals.open(ReassignPatientsComponent, {
      closeDisabled: true,
      width: 'calc(100vw - 48px)',
      minWidth: '976px',
    }).subscribe(() => {});
  }

  public editUserDetails() {
    this.modals.open(EditUserDetailsComponent, {
      closeDisabled: true,
      width: '427px',
    }).subscribe(() => {});
  }

  public openChangeEmail() {
    this.modals.open(ChangeEmailComponent, {
      closeDisabled: true,
      width: '427px',
    }).subscribe(() => {});
  }

  public openChangePassword() {
    this.modals.open(ChangePasswordComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmRemoveRole() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove Role?',
       body: 'Are you sure you want to take this person out of this role? This will affect X patients.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public confirmRevokeAccess() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Revoke Access?',
       body: 'Are you sure you want revoke this person\'s access to this facility? This will affect X patients.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public confirmRemoveBC() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove BC?',
       body: 'Are you sure you want to remove this billing coordinator?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public confirmRemoveBP() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove BP?',
       body: 'Are you sure you want to remove this billing practitioner?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public confirmToggleAdmin(status:boolean, id:string = null) {
    const action = status ? 'add' : 'remove';
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const orgOrFacilityName = id ? _find(this.employee.facilities, f => f.id === id).name : this.organization.name;
    const cancelText = "Cancel";
    const okText = "Continue";
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Remove Administrator?', 
        body: `Do you want to ${action} ${employeeName} as an administrator at ${orgOrFacilityName}?`,
        cancelText,
        okText,
      },
      width: '384px'
    }).subscribe(res => {
      if (res === okText) {
        const facilities_managed = id
          ? toggleManaged(_map(this.employee.facilities_managed, f => f.id), id)
          : _map(this.employee.facilities_managed, f => f.id);
        const organizations_managed = !id
          ? toggleManaged(_map(this.employee.organizations_managed, o => o.id), this.organization.id)
          : _map(this.employee.organizations_managed, o => o.id);
        this.store.EmployeeProfile.update(this.employee.id, {
          user: this.employee.user.id,
          facilities_managed,
          organizations_managed,
        }).subscribe(
          res => {
            this.employee = res;
          }
        )
      }
    })

    function toggleManaged(managed:string[], id:string) {
      if (managed.indexOf(id) === -1) {
        managed.push(id);
        return managed;
      } else {
        return _filter(managed, m => m !== id);
      }
    }
  }

  public confirmToggleOrganization(status:boolean) {
    const action = status ? 'add' : 'remove';
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent)
  }

  public isFacilityManager(facilityId) {
    return !!_find(this.employee.facilities_managed, f => f.id === facilityId);
  }

  public get isOrgAdmin() {
    if (this.employee && this.organization) {
      return !!_find(this.employee.organizations_managed, o => o.id === this.organization.id);
    }
    return false;
  }
}
