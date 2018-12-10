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

  public showDate;
  public accordPD1Open;
  public accordPD2Open;
  public tooltipPD200Open;
  public accordPD3Open;
  public tooltipPD300Open;
  public accordPD4Open;
  public tooltipPD400Open;
  public tooltipPD401Open;
  public accordPD5Open;
  public tooltipPD500Open;
  public tooltipPD501Open;
  public tooltipPD502Open;
  public tooltipPD503Open;
  public tooltipPD504Open;
  public tooltipPD505Open;
  public tooltipPD506Open;
  public tooltipPD507Open;
  public tooltipPD508Open;
  public tooltipPD509Open;
  public tooltipPD510Open;
  public tooltipPD511Open;
  public tooltipPD512Open;
  public tooltipPD513Open;
  public accordPD6Open;
  public tooltipPD600Open;
  public tooltipPD601Open;
  public tooltipPD602Open;
  public tooltipPD603Open;
  public accordPD7Open;
  public tooltipPD700Open;
  public tooltipPD701Open;
  public tooltipPD702Open;
  public tooltipPD703Open;
  public accordPD8Open;
  public tooltipPD800Open;



  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.id);
      this.store.PatientProfile.read(params.id).subscribe(
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
