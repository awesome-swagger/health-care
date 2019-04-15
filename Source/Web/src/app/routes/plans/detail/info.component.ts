import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  sum as _sum,
  sumBy as _sumBy,
  map as _map,
} from 'lodash';
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

  public formatTimeSince(time) {
    let momentTime = moment(time);
    let today = moment().startOf('day');
    if (momentTime.isSame(today, 'day')) {
      return 'Today';
    } else {
      return momentTime.fromNow();
    }
  }

  public routeToHistory(patient, plan) {
    this.router.navigate(['/patient', patient.id, 'history', plan.id]);
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
      closeDisabled: false,
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

  public formatTime(minutes) {
    if (!minutes) return '0:00';
    const h = `${Math.floor(minutes / 60)}`;
    const m = `${minutes % 60}`;
    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`
  }

  public timePillColor(plan) {
    if (!plan.patient.payer_reimbursement || !plan.billing_type) {
      return;
    }
    let timeCount = plan
    let allotted = plan.billing_type.billable_minutes;
    return this.utils.timePillColor(plan.time_count, allotted);
  }

  public totalTimeCount(plans) {
    if (!plans || plans.length < 1) {
      return;
    }
    let total = 0;
    // let billablePlans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    return _sum(_map(plans, (plan) => plan.time_count));
  }

  public averageTimeColor(plans) {
    if (!plans || plans.length < 1) {
      return null;
    }
    let billablePlans = plans.filter((plan) => plan.patient.payer_reimbursement && plan.billing_type);
    if (plans.length === 0) {
      return null;
    }
    let totalTime = _sum(_map(billablePlans, (p) => p.time_count));
    const totalAllotted = _sum(_map(billablePlans, (p) => p.billing_type.billable_minutes));
    if (totalAllotted < 1) {
      return null;
    }
    return this.utils.timePillColor(totalTime, totalAllotted);
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
    return Math.floor(_sumBy(activePlans, (plan) => plan.risk_level) / activePlans.length);
  }

  public routeToPatientOverview(patient, plan) {
    this.router.navigate(['/patient', patient, 'overview', plan]);
  }
}
