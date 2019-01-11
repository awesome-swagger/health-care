import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddCTMemberComponent } from '../../../components';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-patient-team',
  templateUrl: './team.component.html',
  styleUrls: ['./team.component.scss'],
})
export class PatientTeamComponent implements OnDestroy, OnInit {

  public patient = null;
  public careTeamMembers = [];

  public tooltipPCT0Open;
  public tooltipPCT1Open;
  public tooltipPCT2Open;
  public tooltipPCT3Open;
  public tooltipPCT4Open;
  public tooltipPCT5Open;
  public tooltipPCT6Open;
  public tooltipPCT7Open;
  public tooltipPCT8Open;
  public tooltipPCT9Open;

  private routeSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.routeSub = this.route.params.subscribe((params) => {
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
              let teamMembersSub = this.store.CarePlan.detailRoute('get', data[0].id, 'care_team_members').subscribe(
                (data: any) => {
                  this.careTeamMembers = data;
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

  public addCTMember() {
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

  public removeCTMember() {
    let modalSub = this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove Provider?',
       body: 'Are you sure you want to remove this provider from the care team?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(
      (data) => {},
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

  public changeCM() {
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
}
