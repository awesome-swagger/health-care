import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { sumBy as _sumBy } from 'lodash';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPlanComponent } from '../modals/add-plan/add-plan.component';
import {
  AddPatientToPlanComponent,
  PlanDurationComponent
} from '../../../components';
import { DeletePlanComponent } from '../modals/delete-plan/delete-plan.component';
import {
  AuthService,
  NavbarService,
  StoreService,
  UtilsService,
} from '../../../services';

@Component({
  selector: 'app-plan-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss'],
})
export class PlanInfoComponent implements OnDestroy, OnInit {

  public planTemplateId = null;
  public planTemplate: any = null;
  public facilities = [];
  public accordionOpen = {};
  public otherPlansInfoOpen = {};
  public otherPlansOpen = {};

  public accord1Open;
  public tooltip1Open;
  public tooltip2Open;
  public accord2Open;

  private routeSub = null;
  private facilitiesSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private nav: NavbarService,
    private store: StoreService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.routeSub = this.route.params.subscribe((params) => {
      this.facilitiesSub = this.auth.facilities$.subscribe((facilities) => {
        if (!facilities) {
          return;
        }
        this.facilities = facilities.filter((obj) => {
          return !obj.is_affiliate;
        }).slice();
        this.getPlanTemplate(params.id).then((planTemplate: any) => {
          this.planTemplateId = planTemplate.id;
          this.planTemplate = planTemplate;
          this.nav.planDetailState(this.planTemplateId);
          this.facilities.forEach((facility) => {
            let plansSub = this.store.Facility.detailRoute('get', facility.id, 'care_plan_templates/' + this.planTemplateId + '/care_plans').subscribe(
              (plans: any) => {
                facility.plans = plans.results;
              },
              (err) => {},
              () => {
                plansSub.unsubscribe();
              }
            );
          });
        }).catch(() => {
          this.router.navigate(['/error']);
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.routeSub) {
      this.routeSub.unsubscribe();
    }
    if (this.facilitiesSub) {
      this.routeSub.unsubscribe();
    }
  }

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

  public openPlanDuration() {
    this.modals.open(PlanDurationComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public openReassignPatients(plan) {
    this.modals.open(DeletePlanComponent, {
      closeDisabled: true,
      data: {
        planTemplate: this.planTemplate,
        plan: plan
      },
      width: '900px',
    }).subscribe((result) => {
      if (!result) return;
      if (result.toLowerCase() === 'success') {
        this.facilities.forEach((facility) => {
          facility.plans = facility.plans.filter((obj) => plan.id !== obj.id);
        });
      }
    });
  }

  public addPlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: false,
      data: {
        duplicatePlan: null,
      },
      width: '480px',
    }).subscribe(() => {});
  }

  public addPatientToPlan(plan) {
    this.modals.open(AddPatientToPlanComponent, {
      closeDisabled: true,
      data: {
        action: 'add',
        patientKnown: false,
        patientInSystem: true,
        planKnown: true,
        planTemplate: this.planTemplate,
      },
      width: '576px',
    }).subscribe(() => {});
  }

  public zeroPad(num) {
    return num < 10 ? `0${num}` : `${num}`;
  }

  public totalTimeCount(plans) {
    let hours = 0;
    let minutes = 0;
    plans.forEach((obj) => {
      if (!obj.time_count) {
        return;
      }
      let timeCountSplit = obj.time_count.split(":");
      let splitHours = parseInt(timeCountSplit[0]);
      let splitMinutes = parseInt(timeCountSplit[1]);
      hours += splitHours;
      minutes += splitMinutes;
    });
    hours += Math.floor((minutes / 60));
    minutes = minutes % 60;
    return `${hours}:${this.zeroPad(minutes)}`;
  }

  public progressInWeeks(plan) {
    if (!plan || !plan.created) {
      return 0;
    }
    return moment().diff(moment(plan.created), 'weeks');
  }

  public totalFacilityRiskLevel(facility) {
    if (!facility.plans || facility.plans.length === 0) {
      return 0;
    }
    let activePlans = facility.plans.filter((obj) => obj.risk_level > 0);
    if (activePlans.length === 0) {
      return 0;
    }
    return _sumBy(activePlans, (plan) => plan.risk_level) / activePlans.length;
  }

  public routeToPatientOverview(patient, plan) {
    this.router.navigate(['/patient', patient, 'overview', plan]);
  }
}
