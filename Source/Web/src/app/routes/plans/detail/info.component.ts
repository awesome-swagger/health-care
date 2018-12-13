import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPlanComponent } from '../modals/add-plan/add-plan.component';
import {
  AddPatientToPlanComponent,
  ReassignPatientsComponent,
  PlanDurationComponent
} from '../../../components';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-plan-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss'],
})
export class PlanInfoComponent implements OnDestroy, OnInit {

  public planTemplateId = null;
  public planTemplate: any = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private nav: NavbarService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.store.CarePlanTemplate.read(params.id).subscribe(
        (planTemplate) => {
          this.planTemplateId = planTemplate.id;
          this.planTemplate = planTemplate;
          this.nav.planDetailState(this.planTemplateId);
        },
        (err) => {
          this.router.navigate(['/error']);
        }
      );
    });
  }

  public ngOnDestroy() { }

  public openPlanDuration() {
    this.modals.open(PlanDurationComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public openReassignPatients() {
    this.modals.open(ReassignPatientsComponent, {
      closeDisabled: true,
      width: 'calc(100vw - 48px)',
      minWidth: '976px',
    }).subscribe(() => {});
  }

  public addPlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: true,
      width: '480px',
    }).subscribe(() => {});
  }

  public addPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      width: '576px',
    }).subscribe(() => {});
  }
}
