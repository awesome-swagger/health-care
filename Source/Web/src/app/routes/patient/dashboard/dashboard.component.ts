import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService, StoreService, NavbarService, TimeTrackerService } from '../../../services';
import * as moment from 'moment';

@Component({
  selector: 'app-patient-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class PatientDashboardComponent implements OnDestroy, OnInit {

  public user = null;
  public patient = null;
  public carePlans = null;
  public patientAverage = null;
  public resultsOverTime = [];

  public weeksOnPlan = 0;
  public displayWeeks = 4;

  public billingInfo = {
    top: {
      total_time: 0,
      billable_time: 0,
      total_billed: 0,
    },
    bottom: {
      total_time: 0,
      billable_time: 0,
      total_billed: 0,
    },
  }

  public topBillingStart: moment.Moment = moment().startOf('M');
  public topBillingEnd: moment.Moment = moment();

  public bottomBillingStart: moment.Moment = moment().subtract('1', 'M').startOf('M');
  public bottomBillingEnd: moment.Moment = moment().subtract('1', 'M').endOf('M');


  public datepickerOptions = {
    relativeTop: '-368px',
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private auth: AuthService,
    private store: StoreService,
    private nav: NavbarService,
    private timer: TimeTrackerService,
  ) {
    // Nothing yet
  }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.auth.user$.subscribe((user) => {
        if (!user) {
          return;
        }

        this.user = user;
        this.getCarePlan(params.planId).then((plan: any) => {
          this.timer.startTimer(this.user, plan);

          console.log(plan);
          this.weeksOnPlan = moment(Date.parse(plan.created), ['YYYY-MM-DDTHH:mm:ss.SSSZZ']).diff('weeks');
        });

        this.getPatient(params.patientId).then((patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        });

        this.getCarePlans(params.patientId).then((plans) => this.carePlans = plans);

        const patientPlanData = {
          patient: params.patientId,
          plan: params.planId,
        };

        this.store.CarePlan
          .detailRoute('GET', null, 'patient_average', {}, patientPlanData)
          .subscribe(res => this.patientAverage = res);
      });

      this.store.CarePlan.detailRoute('GET', params.planId, 'results_over_time', {}, { weeks: 4 }).subscribe((res: any) => {
        const results = res;
        for (let i = 0; i < 4; i++) {
          if (!results[i]) {
            results[i] = {
              outcome: 0,
              engagement: 0,
            };
          }
        }

        this.resultsOverTime = results;
        this.displayWeeks = results.length;
      });

      this.onRangeChange('top');
      this.onRangeChange('bottom');
    });
  }

  public getPatient(patientId) {
    return new Promise((resolve, reject) => {
      let patientSub = this.store.PatientProfile.read(patientId).subscribe(
        patient => resolve(patient),
        err => reject(err),
        () => patientSub.unsubscribe()
      );
    });
  }

  public getCarePlan(planId) {
    let promise = new Promise((resolve, reject) => {
      let carePlanSub = this.store.CarePlan.read(planId).subscribe(
        (carePlan) => resolve(carePlan),
        (err) => reject(err),
        () => carePlanSub.unsubscribe(),
      );
    });
    return promise;
  }

  public getCarePlans(patientId) {
    return new Promise((resolve, reject) => {
      let carePlanSub = this.store.PatientProfile.detailRoute('get', patientId, 'care_plans').subscribe(
        plans => resolve(plans),
        err => reject(err),
        () => carePlanSub.unsubscribe()
      );
    });
  }

  public ngOnDestroy() {
    this.timer.stopTimer();
  }

  public get graphedResults() {
    return this.resultsOverTime.filter((r, i) => i < this.displayWeeks);
  }

  public onRangeChange(which) {
    let startDate: moment.Moment;
    let endDate: moment.Moment;
    if (which === 'top') {
      startDate = this.topBillingStart;
      endDate = this.topBillingEnd;
    } else if (which === 'bottom') {
      startDate = this.bottomBillingStart;
      endDate = this.bottomBillingEnd;
    }

    const range = {
      start_date: `${startDate.format('YYYY-M-D')}`,
      end_date: `${endDate.format('YYYY-M-D')}`,
    }

    this.getBillingInfo(range, which)
  }

  public getBillingInfo(range, which) {
    this.route.params.subscribe((params: any) => {
      this.store.CarePlan
        .detailRoute('GET', params.planId, 'billing_info', {}, range)
        .subscribe((res: any) => this.billingInfo[which] = res);
    });
  }

  public formatTime(minutes) {
    if (!minutes) {
      return '0:00';
    }

    const h = `${Math.floor(minutes / 60)}`;
    const m = `${minutes % 60}`;

    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`;
  }

  public formatMoney(amount) {
    let decimal;

    if (amount - Math.floor(amount) === 0) {
      decimal = '00';
    } else {
      decimal = `${amount - Math.floor(amount)}`.split('.')[1];
      if (decimal.length === 1) {
        decimal += '0';
      }
    }

    return `$${Math.floor(amount)}.${decimal}`;
  }

  public routeToBillingView() {
    this.router.navigate(['/billing'], {
      queryParams: {
        from_patient_dashboard: true,
        patient_id: this.patient.id,
      }
    });
  }
}
