import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { RecordResultsComponent, GoalComponent, AddCTTaskComponent } from '../../../components';
import { NavbarService, StoreService } from '../../../services';
import { GoalCommentsComponent } from './modals/goal-comments/goal-comments.component';

@Component({
  selector: 'app-patient-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss'],
})
export class PatientDetailsComponent implements OnDestroy, OnInit {

  public patient = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        },
        (err) => {},
        () => {},
      );
    });
  }

  public ngOnDestroy() { }

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
     closeDisabled: true,
     width: '512px',
    }).subscribe(() => {});
  }

  public addGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public updateGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public openGoalComments() {
    this.modals.open(GoalCommentsComponent, {
      closeDisabled: false,
      width: '512px',
    }).subscribe(() => {});
  }

  public addCTTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }
}
