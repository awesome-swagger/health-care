import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { StoreService } from '../../../services';
import { ReassignPatientsComponent } from '../../../components';
import { ChangeEmailComponent } from './modals/change-email/change-email.component';
import { ChangePasswordComponent } from './modals/change-password/change-password.component';
import { EditUserDetailsComponent } from './modals/edit-user-details/edit-user-details.component';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
})
export class UserComponent implements OnDestroy, OnInit {

  public employee: any = null;
  private paramsSub: Subscription = null;

  public tooltip1Open;
  public isOrgAdmin;
  public tooltip2Open;
  public isProvider;
  public tooltip3Open;
  public isBC;
  public tooltip4Open;
  public editName;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
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
          console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
          console.log(this.employee);
          console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
        },
        (err) => {
          this.router.navigate(['/error']);
        },
        () => {
          employeeSub.unsubscribe();
        },
      );
    });
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
}
