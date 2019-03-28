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
  public carePlan = null;
  public careTeamMembers = [];
  public availableRoles = [];
  public careManager = null;
  public billingPractitioner = null;

  public phoneTooltipOpen = {};
  public emailTooltipOpen = {};

  public bpLoaded = false;
  public careTeamLoaded = false;

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
      this.bpLoaded = false;
      this.careTeamLoaded = false;
      this.getPatient(params.patientId).then((patient: any) => {
        this.patient = patient;
        this.nav.addRecentPatient(this.patient);
        this.getCarePlan(params.planId).then((carePlan: any) => {
          this.carePlan = carePlan;
          this.billingPractitioner = this.carePlan.billing_practitioner;
          this.bpLoaded = true;
          // Get the available roles for this care plan
          this.getAvailableRoles(params.planId).then((availableRoles: any) => {
            this.availableRoles = availableRoles;
          }, (err) => {
            this.toast.error('Error fetching available roles');
            console.log(err);
          });
          // Get the assigned team members for this care plan
          this.getCareTeam(params.planId).then((teamMembers: any) => {
            this.careTeamMembers = teamMembers.filter((obj) => {
              return !obj.is_manager && obj.role;
            });
            this.careManager = teamMembers.filter((obj) => {
              return obj.is_manager;
            })[0];
            this.careTeamLoaded = true;
          });
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.routeSub) {
      this.routeSub.unsubscribe();
    }
  }

  public getPatient(patientId) {
    let promise = new Promise((resolve, reject) => {
      let patientSub = this.store.PatientProfile.read(patientId).subscribe(
        (patient) => resolve(patient),
        (err) => reject(err),
        () => {
          patientSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getCarePlan(planId) {
    let promise = new Promise((resolve, reject) => {
      let planSub = this.store.CarePlan.read(planId).subscribe(
        (plan) => resolve(plan),
        (err) => reject(err),
        () => {
          planSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public getAvailableRoles(planId) {
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

  public getCareTeam(planId) {
    let promise = new Promise((resolve, reject) => {
      let teamMembersSub = this.store.CarePlan.detailRoute('get', planId, 'care_team_members').subscribe(
        (teamMembers: any) => resolve(teamMembers),
        (err) => reject(err),
        () => {
          teamMembersSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public addCTMember(role) {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: false,
      data: {
        role: role,
        is_manager: false,
        is_bp: false,
      },
      overflow: 'visible',
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
              this.getAvailableRoles(this.planId).then(
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
      closeDisabled: false,
      data: {
        role: null,
        is_manager: true,
        is_bp: false,
      },
      overflow: 'visible',
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
              this.getAvailableRoles(this.planId).then(
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
      closeDisabled: false,
      data: {
        role: null,
        is_manager: false,
        is_bp: true,
      },
      overflow: 'visible',
      width: '416px',
    }).subscribe(
      (newBp) => {
        if (!newBp) {
          return;
        }
        let updateSub = this.store.CarePlan.update(this.planId, {
          billing_practitioner: newBp.id,
        }, true).subscribe(
          (updatedPlan) => {
            this.billingPractitioner = updatedPlan.billing_practitioner;
          },
          (err) => {
            this.toast.error('Error updating billing practitioner');
          },
          () => {
            updateSub.unsubscribe();
          }
        );
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      },
    );
  }

  public changeCM(currentCm) {
    let modalSub = this.modals.open(AddCTMemberComponent, {
      closeDisabled: false,
      data: {
        role: null,
        is_manager: true,
        is_bp: false,
      },
      overflow: 'visible',
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
}
