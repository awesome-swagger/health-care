import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { ToastService } from '../../../modules/toast';
import { AddCTMemberComponent } from '../../../components';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-patient-team',
  templateUrl: './team.component.html',
  styleUrls: ['./team.component.scss'],
})
export class PatientTeamComponent implements OnDestroy, OnInit {

  public patient = null;
  public planId = null;
  public careTeamMembers = [];
  public availableRoles = [];
  public careManager = null;
  public showCMPhone = false;

  private routeSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private toast: ToastService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.routeSub = this.route.params.subscribe((params) => {
      this.planId = params.planId;
      this.nav.patientDetailState(params.patientId, params.planId);
      let patientSub = this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
          // TODO: Do not grab care plans again here
          let carePlansSub = this.store.CarePlan.readListPaged({
            patient: this.patient.id,
          }).subscribe(
            (data) => {
              // Get the available roles for this care plan
              this.fetchAvailableRoles(params.planId).then((availableRoles: any) => {
                this.availableRoles = availableRoles;
              }, (err) => {
                this.toast.error('Error fetching available roles');
                console.log(err);
              });
              // Get the assigned team members for this care plan
              let teamMembersSub = this.store.CarePlan.detailRoute('get', params.planId, 'care_team_members').subscribe(
                (teamMembers: any) => {
                  this.careTeamMembers = teamMembers.filter((obj) => {
                    return !obj.is_manager;
                  });
                  this.careManager = teamMembers.filter((obj) => {
                    return obj.is_manager;
                  })[0];
                },
                (err) => {},
                () => {
                  teamMembersSub.unsubscribe();
                },
              );
            },
            (err) => {},
            () => {
              carePlansSub.unsubscribe();
            },
          );
        },
        (err) => {},
        () => {
          patientSub.unsubscribe();
        },
      );
    });
  }

  public ngOnDestroy() {
    if (this.routeSub) {
      this.routeSub.unsubscribe();
    }
  }

  public addCTMember(role) {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: true,
      data: {
        role: role,
        is_manager: false,
        is_bp: false,
      },
      width: '416px',
    }).subscribe(
      (selectedEmployee) => {
        if (selectedEmployee) {
          let createTeamMemberSub = this.store.CareTeamMember.create({
            employee_profile: selectedEmployee.id,
            role: role.id,
            plan: this.planId,
            is_manager: false,
          }).subscribe(
            (newTeamMember) => {
              this.careTeamMembers.push(newTeamMember);
              // Refetch the available roles
              this.fetchAvailableRoles(this.planId).then(
                (availableRoles: any) => {
                  this.availableRoles = availableRoles;
                },
                (err) => {
                this.toast.error('Error fetching available roles');
                console.log(err);
                }
              );
            },
            (err) => {
              this.toast.error('Error creating care team member.');
              console.log(err);
            },
            () => {
              createTeamMemberSub.unsubscribe();
            }
          )
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public addCareManager() {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: true,
      data: {
        role: null,
        is_manager: true,
        is_bp: false,
      },
      width: '416px',
    }).subscribe(
      (selectedEmployee) => {
        if (selectedEmployee) {
          this.store.CareTeamMember.create({
            employee_profile: selectedEmployee.id,
            role: null,
            plan: this.planId,
            is_manager: true,
          }).subscribe(
            (newCareManager) => {
              this.careManager = newCareManager;
            },
            () => {},
            () => {}
          )
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public removeCTMember(teamMember) {
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Remove Provider?',
       body: 'Are you sure you want to remove this provider from the care team?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (data && data.toLowerCase() === 'continue') {
          this.store.CareTeamMember.destroy(teamMember.id).subscribe(
            (res) => {
              this.careTeamMembers.splice(
                this.careTeamMembers.findIndex((obj) => obj.id === teamMember.id), 1);
              this.fetchAvailableRoles(this.planId).then(
                (availableRoles: any) => {
                  this.availableRoles = availableRoles;
                },
                (err) => {
                this.toast.error('Error fetching available roles');
                console.log(err);
                }
              );
            }
          );
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public changeBP() {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: true,
      width: '416px',
    }).subscribe(
      (data) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public changeCM(currentCm) {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: true,
      data: {
        role: null,
        is_manager: true,
        is_bp: false,
      },
      width: '416px',
    }).subscribe(
      (selectedEmployee) => {
        if (selectedEmployee) {
          this.store.CareTeamMember.create({
            employee_profile: selectedEmployee.id,
            role: null,
            plan: this.planId,
            is_manager: true,
          }).subscribe(
            (newCareManager) => {
              this.careManager = newCareManager;
              this.store.CareTeamMember.destroy(currentCm.id).subscribe();
            },
            () => {},
            () => {}
          )
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public fetchAvailableRoles(planId) {
    let promise = new Promise((resolve, reject) => {
      let availableRolesSub = this.store.CarePlan.detailRoute('get', planId, 'available_roles').subscribe(
        (availableRoles: any) => resolve(availableRoles),
        (err) => reject(err),
        () => {
          availableRolesSub.unsubscribe();
        }
      );
    });
    return promise;
  }
}
