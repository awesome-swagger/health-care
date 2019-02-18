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
  map as _map,
  uniqBy as _uniqBy
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
  public careTeam = [];
  public roleDetails = {};
  public selectedRole = [];
  public billingPractitioners = [];
  public selectedBillingPractitioner = [];

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
          this.employee = employee;
          console.log('employee', this.employee);

          this.store.BillingCoordinator.readListPaged().subscribe((res:any) => {
            res.forEach(bc => {
              if (bc.user.id !== this.employee.id) return;
              const facility = _find(this.employee.facilities, f => f.id = bc.facility.id);
              if (!facility.billingCoordinators) {
                facility.billingCoordinators = [];
              }
              facility.billingCoordinators.push(bc);
            })
          })
        },
        (err) => {
          this.router.navigate(['/error']);
        },
        () => {
          employeeSub.unsubscribe();
        },
      );

      let careTeamSub = this.store.CareTeamMember.readListPaged({employee_profile: res.id}).subscribe(
        careTeam => {
          this.roleDetails = groupByRole(careTeam)
          this.careTeam = careTeam;
          console.log('roleDetails', this.roleDetails);
        }
      )

      function groupByRole(careTeams) {
        const roles = {};
        careTeams.forEach(t => {
          if (!t.role) return;
          if (roles[t.role.id]) {
            roles[t.role.id].push(t);
          } else {
            roles[t.role.id] = [t];
          }
        })
        return roles;
      }
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
    );

    const employeesSub = this.store.EmployeeProfile.readListPaged().subscribe(res => {
      this.billingPractitioners = _filter(res, employee => employee.billing_view)
    })

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

  public confirmRemoveBC(bc) {
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove BC?',
       body: 'Are you sure you want to remove this billing coordinator?',
       cancelText,
       okText,
      },
      width: '384px',
    }).subscribe((res) => {
      if (res === okText) {
        this.store.BillingCoordinator.destroy(bc.id).subscribe((res:any) => {
          this.employee.facilities.forEach(facility => {
            if (facility.billingCoordinators) {
              facility.billingCoordinators = _filter(facility.billingCoordinators, b => b.id !== bc.id);
            }
          })
        })
      }
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

  public confirmAddRole(i) {
    const role = this.selectedRole[i];
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Add Role?',
        body: `Do you want to give ${employeeName} the role of ${role.name}?`,
        cancelText,
        okText,
      },
      width: '384px',
    }).subscribe(res => {
      if (res === okText) {
        const roles = _map(this.employee.roles, r => r.id);
        roles.push(role.id);
        this.store.EmployeeProfile.update(this.employee.id, {
          user: this.employee.user.id,
          roles
        }).subscribe(
          res => {
            this.employee = res;
          }
        )
      }
    })
  }

  public confirmAddBC(i) {
    const billingPractitioner = this.selectedBillingPractitioner[i];
    const name = `${billingPractitioner.user.first_name} ${billingPractitioner.user.last_name}`;
    const cancelText = 'Cancel';
    const okText = 'Continue';
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Add Billing Coordinator?',
        body: `Do you want to make ${name} a billing coordinator`,
        cancelText,
        okText,
      },
      width: '384px',
    }).subscribe(res => {
      if (res === okText) {
        this.store.BillingCoordinator.create({
          facility: this.employee.facilities[i].id,
          user: this.employee.id,
          coordinator: billingPractitioner.id,
        }).subscribe((res:any) => {
          const facility = this.employee.facilities[i];
          if (!facility.billingCoordinators) {
            facility.billingCoordinators = [];
          }
          facility.billingCoordinators.push(res);
        })
      }
    })

  }

  public confirmRemoveRole(role) {
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const cancelText = 'Cancel';
    const okText = 'Continue';
    const roles = _map(_filter(this.employee.roles, r => r.id !== role.id), r => r.id);
    this.modals.open(ConfirmModalComponent, {
      'closeDisabled': true,
      data: {
        title: 'Remove Role?',
        body: `Do you want to remove the role of ${role.name} from ${employeeName}?`,
        cancelText,
        okText,
      },
      width: '384px',
    }).subscribe(res => {
      if (res === okText) {
        this.store.EmployeeProfile.update(this.employee.id, {
          user: this.employee.user.id,
          roles
        }).subscribe(
          res => {
            this.employee = res;
          }
        )
      }
    })
  }

  confirmToggleBillingView(status:boolean) {
    const action = status ? ['give', 'to'] : ['remove', 'from'];
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const cancelText = "Cancel";
    const okText = "Continue";
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Billing View', 
        body: `Do you want to ${action[0]} billing view rights ${action[1]} ${employeeName}?`,
        cancelText,
        okText,
      },
      width: '384px'
    }).subscribe(res => {
      if (res === okText) {
        this.store.EmployeeProfile.update(this.employee.id, {
          user: this.employee.user.id,
          billing_view: status,
        }).subscribe(res => {
          this.employee.billing_view = status;
        })
      }
    })
  }

  confirmToggleQualifiedPractitioner(status:boolean) {
    const action = status ? ['give', 'to'] : ['remove', 'from'];
    const employeeName = `${this.employee.user.first_name} ${this.employee.user.last_name}`;
    const cancelText = "Cancel";
    const okText = "Continue";
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Billing View', 
        body: `Do you want to ${action[0]} the qualified practitioner role ${action[1]} ${employeeName}?`,
        cancelText,
        okText,
      },
      width: '384px'
    }).subscribe(res => {
      if (res === okText) {
        this.store.EmployeeProfile.update(this.employee.id, {
          user: this.employee.user.id,
          qualified_practitioner: status,
        }).subscribe(res => {
          this.employee.qualified_practitioner = status;
        })
      }
    })
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

  public isFacilityManager(facilityId) {
    return !!_find(this.employee.facilities_managed, f => f.id === facilityId);
  }

  public get isOrgAdmin() {
    if (this.employee && this.organization) {
      return !!_find(this.employee.organizations_managed, o => o.id === this.organization.id);
    }
    return false;
  }

  public roleStats(roleId, facilityId) {
    const stats = {
      patients: 0,
      managing: 0,
      careTeam: 0,
      billing: false,
    };

    if (this.roleDetails && this.roleDetails[roleId]) {
      const careTeamRoles = this.roleDetails[roleId];
      stats.patients = _uniqBy(careTeamRoles, r => r.plan.patient.id).length;
      stats.managing = _filter(careTeamRoles, r => r.is_manager).length;
      stats.careTeam = careTeamRoles.length;
    }
    return stats;
  }

  public get cmCount() {
    return this.careTeam.length;
  }

  public get ctCount() {
    return _filter(this.careTeam, c => c.is_manager).length;
  }

  public get billableCount() {
    return _filter(this.careTeam, c => c.is_billable).length;
  }

}
