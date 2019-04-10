import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService, StoreService, NavbarService, TimeTrackerService } from '../../../services';
import { PercentageGaugeComponent } from '../../../components/graphs/percentage-gauge/percentage-gauge.component'
import { ResultsGraphComponent } from '../../../components/graphs/results-graph/results-graph.component';

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
  ) { }

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
        });
        this.getPatient(params.patientId).then((patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        });
        this.getCarePlans(params.patientId).then((plans) => {
          this.carePlans = plans;
        });

        this.store.CarePlan.detailRoute('GET', null, 'patient_average', {}, {
          patient: params.patientId,
          plan: params.planId,
        }).subscribe(res => {
          this.patientAverage = res;
        })
      });
    });
  }

  public getPatient(patientId) {
    return new Promise((resolve, reject) => {
        let patientSub = this.store.PatientProfile.read(patientId).subscribe(
          patient => resolve(patient),
          err => reject(err),
          () => patientSub.unsubscribe()
        )
    });
  }12

  public getCarePlan(planId) {
    let promise = new Promise((resolve, reject) => {
      let carePlanSub = this.store.CarePlan.read(planId).subscribe(
        (carePlan) => resolve(carePlan),
        (err) => reject(err),
        () => {
          carePlanSub.unsubscribe();
        },
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
        )
    });
  }

  public ngOnDestroy() {
    this.timer.stopTimer();
  }
}
