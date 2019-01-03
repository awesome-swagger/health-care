import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { groupBy as _groupBy } from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPlanComponent } from '../modals/add-plan/add-plan.component';
import {
  AddPatientToPlanComponent,
  ReassignPatientsComponent,
  PlanDurationComponent
} from '../../../components';
import { AuthService, NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-plan-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss'],
})
export class PlanInfoComponent implements OnDestroy, OnInit {

  public planTemplateId = null;
  public planTemplate: any = null;
  public facilities = [];
  public patients = [];
  public patientsGrouped = [];
  public accordionOpen = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private nav: NavbarService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.auth.facilities$.subscribe((facilities) => {
        if (!facilities) {
          return;
        }
        this.facilities = facilities;
        this.getPlanTemplate(params.id).then((planTemplate: any) => {
          this.planTemplateId = planTemplate.id;
          this.planTemplate = planTemplate;
          this.nav.planDetailState(this.planTemplateId);
          this.getPatients(this.planTemplateId).then((patients: any) => {
            this.patients = patients.results;
            this.patientsGrouped = _groupBy(this.patients, (obj) => {
              return obj.facility.id;
            });
          });
        }).catch(() => {
          this.router.navigate(['/error']);
        });
      });
    });
  }

  public ngOnDestroy() { }

  public getPlanTemplate(id) {
    let promise = new Promise((resolve, reject) => {
      let readSub = this.store.CarePlanTemplate.read(id).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          readSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getPatients(planId) {
    let promise = new Promise((resolve, reject) => {
      let detailSub = this.store.CarePlanTemplate.detailRoute('get', planId, 'patients').subscribe(
        (patients) => resolve(patients),
        (err) => reject(err),
        () => {
          detailSub.unsubscribe();
        }
      );
    });
    return promise;
  }

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
